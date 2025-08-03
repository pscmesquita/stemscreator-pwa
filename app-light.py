#!/usr/bin/env python3
"""
Ultra-Light Web API for StemsCreator - Flask backend for PWA
Uses basic FFT separation instead of AI for minimal size
"""

from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import os
import uuid
import numpy as np
import soundfile as sf
from pathlib import Path
import zipfile
import threading
import time
from werkzeug.utils import secure_filename
from scipy import signal

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

def basic_stem_separation(audio_data, sr):
    """
    Basic stem separation using frequency domain techniques
    Much lighter than AI but still effective
    """
    if len(audio_data.shape) == 1:
        # Convert mono to stereo
        audio_data = np.column_stack([audio_data, audio_data])
    
    # Ensure we have stereo
    if audio_data.shape[1] == 1:
        audio_data = np.column_stack([audio_data.flatten(), audio_data.flatten()])
    
    left = audio_data[:, 0]
    right = audio_data[:, 1]
    
    # Center channel extraction (vocals)
    center = (left + right) / 2
    vocals = center * 0.8  # Reduce slightly
    
    # Side channels (instruments)
    side = (left - right) / 2
    
    # Create instrumental by removing center
    instrumental = audio_data - np.column_stack([center * 0.6, center * 0.6])
    
    # Frequency-based separation
    f, t, Zxx = signal.stft(audio_data.T, sr, nperseg=2048)
    
    # Bass: Low frequencies (20-250 Hz)
    bass_mask = (f >= 20) & (f <= 250)
    bass_stft = np.zeros_like(Zxx)
    bass_stft[bass_mask] = Zxx[bass_mask]
    _, bass = signal.istft(bass_stft, sr)
    bass = bass.T
    
    # Drums: Mid frequencies with emphasis on transients (80-8000 Hz)
    drums_mask = (f >= 80) & (f <= 8000)
    drums_stft = np.zeros_like(Zxx)
    drums_stft[drums_mask] = Zxx[drums_mask] * 1.2  # Emphasize
    _, drums = signal.istft(drums_stft, sr)
    drums = drums.T
    
    # Other: Everything else
    other = audio_data - vocals.reshape(-1, 1) - bass - drums
    
    return {
        'vocals': vocals.reshape(-1, 1) if vocals.ndim == 1 else vocals,
        'drums': drums,
        'bass': bass,
        'other': other,
        'instrumental': instrumental
    }

def process_audio_async(job_id, input_file, output_folder):
    """Process audio in background thread with basic separation"""
    try:
        processing_status[job_id] = {'status': 'processing', 'progress': 10}
        
        # Load audio file
        audio_data, sr = sf.read(input_file)
        processing_status[job_id]['progress'] = 30
        
        # Perform basic stem separation
        stems = basic_stem_separation(audio_data, sr)
        processing_status[job_id]['progress'] = 70
        
        # Save stems
        final_files = []
        for stem_name, stem_data in stems.items():
            output_path = output_folder / f"{stem_name}.wav"
            
            # Ensure proper shape for saving
            if stem_data.ndim == 1:
                stem_data = stem_data.reshape(-1, 1)
            elif stem_data.shape[1] > 2:
                stem_data = stem_data[:, :2]  # Keep only first 2 channels
            
            sf.write(output_path, stem_data, sr)
            final_files.append(output_path.name)
        
        processing_status[job_id] = {
            'status': 'completed',
            'progress': 100,
            'files': final_files
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
