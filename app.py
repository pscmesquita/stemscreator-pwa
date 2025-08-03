#!/usr/bin/env python3
"""
Web API for StemsCreator - Flask backend for PWA
Handles audio upload and processing using Demucs AI
"""

from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import os
import uuid
import subprocess
from pathlib import Path
import tempfile
import zipfile
import threading
import time
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Enable CORS for PWA

# Configuration
UPLOAD_FOLDER = Path('uploads')
RESULTS_FOLDER = Path('results')
UPLOAD_FOLDER.mkdir(exist_ok=True)
RESULTS_FOLDER.mkdir(exist_ok=True)

# Store processing status
processing_status = {}

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac', 'm4a', 'aac', 'ogg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_audio_async(job_id, input_file, output_folder):
    """Process audio in background thread"""
    try:
        processing_status[job_id] = {'status': 'processing', 'progress': 10}
        
        # Run Demucs separation
        cmd = [
            "python", "-m", "demucs.separate",
            "--out", str(output_folder),
            str(input_file)
        ]
        
        processing_status[job_id]['progress'] = 25
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            processing_status[job_id]['progress'] = 75
            
            # Find and organize output files
            stem_files = []
            for pattern in ["**/*.wav", "**/*.flac"]:
                stem_files.extend(output_folder.glob(pattern))
            
            # Move files to main folder
            final_files = []
            for f in stem_files:
                if f.parent != output_folder:
                    new_path = output_folder / f.name
                    if new_path.exists():
                        new_path.unlink()  # Remove if exists
                    f.rename(new_path)
                    final_files.append(new_path)
                else:
                    final_files.append(f)
            
            # Create instrumental track (like our AI version)
            vocals_file = None
            for f in final_files:
                if 'vocals.wav' in str(f):
                    vocals_file = f
                    break
            
            if vocals_file and vocals_file.exists():
                processing_status[job_id]['progress'] = 90
                
                try:
                    import soundfile as sf
                    import numpy as np
                    
                    # Load original and vocals
                    original_data, sr = sf.read(input_file)
                    vocals_data, _ = sf.read(vocals_file)
                    
                    # Ensure same dimensions and length
                    if original_data.ndim != vocals_data.ndim:
                        if original_data.ndim == 1 and vocals_data.ndim == 2:
                            original_data = np.column_stack([original_data, original_data])
                        elif original_data.ndim == 2 and vocals_data.ndim == 1:
                            vocals_data = np.column_stack([vocals_data, vocals_data])
                    
                    min_length = min(len(original_data), len(vocals_data))
                    original_data = original_data[:min_length]
                    vocals_data = vocals_data[:min_length]
                    
                    # Create instrumental
                    instrumental = original_data - vocals_data * 0.8
                    
                    # Save instrumental
                    instrumental_path = output_folder / "instrumental.wav"
                    sf.write(instrumental_path, instrumental, sr)
                    final_files.append(instrumental_path)
                except Exception as e:
                    print(f"Error creating instrumental: {e}")
            
            # Get final file list
            final_file_names = []
            for f in output_folder.glob("*.wav"):
                final_file_names.append(f.name)
            
            processing_status[job_id] = {
                'status': 'completed',
                'progress': 100,
                'files': final_file_names
            }
            
        else:
            processing_status[job_id] = {
                'status': 'error',
                'error': result.stderr or 'Processing failed'
            }
            
    except Exception as e:
        processing_status[job_id] = {
            'status': 'error',
            'error': str(e)
        }

@app.route('/')
def index():
    """Serve the PWA main page"""
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle audio file upload and start processing"""
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    file = request.files['audio']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        input_path = UPLOAD_FOLDER / f"{job_id}_{filename}"
        file.save(input_path)
        
        # Create output folder
        output_folder = RESULTS_FOLDER / job_id
        output_folder.mkdir(exist_ok=True)
        
        # Start processing in background
        thread = threading.Thread(
            target=process_audio_async,
            args=(job_id, input_path, output_folder)
        )
        thread.start()
        
        return jsonify({
            'job_id': job_id,
            'status': 'started',
            'message': 'Processing started'
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/status/<job_id>')
def get_status(job_id):
    """Get processing status"""
    if job_id in processing_status:
        return jsonify(processing_status[job_id])
    else:
        # Check if results exist but status was lost
        output_folder = RESULTS_FOLDER / job_id
        if output_folder.exists():
            files = [f.name for f in output_folder.glob("*.wav")]
            if files:
                # Mark as completed
                processing_status[job_id] = {
                    'status': 'completed',
                    'progress': 100,
                    'files': files
                }
                return jsonify(processing_status[job_id])
        
        return jsonify({'error': 'Job not found'}), 404

@app.route('/api/download/<job_id>')
def download_results(job_id):
    """Download results as ZIP file"""
    output_folder = RESULTS_FOLDER / job_id
    if not output_folder.exists():
        return jsonify({'error': 'Job not found'}), 404
    
    # Check if there are any WAV files
    wav_files = list(output_folder.glob('*.wav'))
    if not wav_files:
        return jsonify({'error': 'No stems found'}), 404
    
    # Create ZIP file with all stems
    zip_path = output_folder / 'stems.zip'
    
    try:
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file_path in wav_files:
                zipf.write(file_path, file_path.name)
        
        return send_file(zip_path, as_attachment=True, download_name='stems.zip')
    except Exception as e:
        return jsonify({'error': f'Failed to create ZIP: {str(e)}'}), 500

@app.route('/api/download/<job_id>/<filename>')
def download_individual_stem(job_id, filename):
    """Download individual stem file"""
    if job_id not in processing_status:
        return jsonify({'error': 'Job not found'}), 404
    
    file_path = RESULTS_FOLDER / job_id / filename
    if not file_path.exists():
        return jsonify({'error': 'File not found'}), 404
    
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    # Get port from environment variable for deployment
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
