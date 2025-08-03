# StemsCreator PWA - Progressive Web App

A mobile-friendly web application for AI-powered audio stem separation.

## Features

🎵 **Professional AI Separation** - Uses Demucs AI model for high-quality results  
📱 **Mobile Optimized** - Works perfectly on iOS and Android  
💾 **PWA Support** - Install like a native app  
🎧 **5 Stems Output** - Vocals, Drums, Bass, Other, Instrumental  
☁️ **Cloud Processing** - Heavy AI processing on server  

## Setup Instructions

### 1. Install Dependencies
```bash
cd web_app
pip install -r requirements.txt
```

### 2. Run the Server
```bash
python app.py
```

### 3. Access the App
- **Local**: http://localhost:5000
- **Mobile**: Use your computer's IP address (e.g., http://192.168.1.100:5000)

## Mobile Installation

### iOS (Safari):
1. Open the web app in Safari
2. Tap the Share button
3. Select "Add to Home Screen"
4. The app will install like a native app

### Android (Chrome):
1. Open the web app in Chrome
2. Tap the menu (3 dots)
3. Select "Add to Home Screen" or "Install App"
4. The app will install like a native app

## How It Works

1. **Upload Audio** - Drag & drop or select audio files
2. **AI Processing** - Server runs Demucs AI separation
3. **Download Stems** - Get individual stems or ZIP package

## File Support

- MP3, WAV, FLAC, M4A, AAC, OGG
- Up to 10 minutes recommended for mobile
- Stereo and mono files supported

## Deployment Options

### Local Network:
- Run on your computer, access from mobile devices on same WiFi

### Cloud Deployment:
- Deploy to Heroku, Google Cloud, AWS, or DigitalOcean
- Requires server with enough RAM for Demucs processing

### Docker:
```bash
# Build container
docker build -t stemscreator .

# Run container
docker run -p 5000:5000 stemscreator
```

## API Endpoints

- `POST /api/upload` - Upload audio file
- `GET /api/status/<job_id>` - Check processing status
- `GET /api/download/<job_id>` - Download all stems (ZIP)
- `GET /api/download/<job_id>/<filename>` - Download individual stem

## Performance Notes

- Processing time: 1-3 minutes per song depending on server
- Memory usage: ~2GB RAM per concurrent job
- Mobile browsers handle playback and download well
- PWA works offline for UI, but needs internet for processing
