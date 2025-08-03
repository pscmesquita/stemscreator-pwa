# 🎵 StemsCreator PWA

A Progressive Web App for AI-powered audio stem separation. Upload any song and get professional-quality stems (vocals, drums, bass, other, instrumental).

## 🚀 Features

- **AI-Powered Separation**: Uses Demucs (Facebook's AI model) for professional results
- **5 Stem Output**: Vocals, Drums, Bass, Other, Instrumental
- **Progressive Web App**: Install on mobile devices like a native app
- **Drag & Drop Upload**: Easy file upload interface
- **Real-time Progress**: Track processing status
- **ZIP Download**: Download all stems at once
- **Mobile Optimized**: Responsive design for all devices

## 🎧 Supported Formats

- MP3, WAV, FLAC, M4A, AAC, OGG

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **AI Model**: Demucs (Facebook Research)
- **Frontend**: HTML5, CSS3, JavaScript
- **PWA**: Service Worker, Web App Manifest
- **Audio Processing**: SoundFile, NumPy

## 📱 Installation

The app can be installed on mobile devices:

1. **iOS**: Open in Safari → Share → Add to Home Screen
2. **Android**: Open in Chrome → Menu → Add to Home Screen

## 🔧 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Access at http://localhost:5000
```

## 📁 Project Structure

```
├── app.py              # Main Flask application
├── templates/          # HTML templates
│   └── index.html     # PWA interface
├── static/            # Static assets
│   ├── css/          # Stylesheets
│   ├── js/           # JavaScript
│   ├── icons/        # PWA icons
│   ├── manifest.json # PWA manifest
│   └── sw.js         # Service worker
├── requirements.txt   # Python dependencies
└── Dockerfile        # Docker configuration
```

## 🎵 Usage

1. **Upload Audio**: Drag and drop or click to select an audio file
2. **Processing**: AI separation takes 1-3 minutes depending on song length
3. **Download**: Get individual stems or download all as ZIP

## ⚡ Performance

- **Processing Time**: 1-3 minutes per song
- **Quality**: Professional-grade separation
- **File Size**: Stems are uncompressed WAV files for best quality

## 🔒 Privacy

- Files are processed locally on the server
- No data is stored permanently
- Uploads and results are automatically cleaned up
