# 🎵 StemsCreator PWA - AI Audio Separation

A professional Progressive Web App for AI-powered audio stem separation. Split any song into vocals, drums, bass, and other instruments using advanced AI models.

![StemsCreator](https://img.shields.io/badge/StemsCreator-PWA-blue)
![AI](https://img.shields.io/badge/AI-Demucs-green)
![Mobile](https://img.shields.io/badge/Mobile-Ready-orange)

## ✨ Features

🎵 **Professional AI Separation** - Uses Facebook's Demucs AI model  
📱 **Mobile Optimized** - Works perfectly on iOS and Android  
💾 **PWA Support** - Install like a native app  
🎧 **5 Stems Output** - Vocals, Drums, Bass, Other, Instrumental  
☁️ **Cloud Processing** - Heavy AI processing on server  
🚀 **Fast & Reliable** - Professional quality results  

## 🔥 Live Demo

**Deploy your own instance:**
- Railway: [![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/yourusername/stemscreator-pwa)
- Render: [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## 📱 Mobile Installation

### iOS (Safari):
1. Open the web app in Safari
2. Tap the Share button
3. Select "Add to Home Screen"
4. The app installs like a native app

### Android (Chrome):
1. Open the web app in Chrome
2. Tap the menu (3 dots)
3. Select "Add to Home Screen" or "Install App"
4. The app installs like a native app

## 🚀 Quick Deploy

### Option 1: Railway.app (FREE)
1. Fork this repository
2. Go to [Railway.app](https://railway.app)
3. Connect your GitHub account
4. Deploy from GitHub repository
5. Your app will be live at `https://yourapp.railway.app`

### Option 2: Render.com (FREE)
1. Fork this repository
2. Go to [Render.com](https://render.com)
3. Create new "Web Service"
4. Connect your GitHub repository
5. Deploy automatically

## 💻 Local Development

### Prerequisites
- Python 3.11+
- Git

### Setup
```bash
git clone https://github.com/yourusername/stemscreator-pwa.git
cd stemscreator-pwa
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000` in your browser.

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **AI Model**: Demucs (Facebook Research)
- **Frontend**: Vanilla JavaScript (PWA)
- **Deployment**: Docker
- **Hosting**: Railway/Render/Fly.io

## 📁 File Support

- **Formats**: MP3, WAV, FLAC, M4A, AAC, OGG
- **Max Size**: 50MB (configurable)
- **Processing**: 1-3 minutes per song
- **Output**: 5 high-quality WAV stems

## 🎯 API Endpoints

- `POST /api/upload` - Upload audio file
- `GET /api/status/<job_id>` - Check processing status
- `GET /api/download/<job_id>` - Download all stems (ZIP)
- `GET /api/download/<job_id>/<filename>` - Download individual stem

## 💰 Deployment Costs

### FREE Options:
- **Railway**: $0 (512MB RAM, $5 monthly credit)
- **Render**: $0 (sleeps after 15min inactivity)
- **Fly.io**: $0 (256MB RAM)

### Paid Upgrades:
- **Railway Pro**: $5/month (1GB RAM, always-on)
- **Render Paid**: $7/month (512MB RAM, always-on)

## 📈 Performance

### Free Tier:
- ~10-20 users per day
- 1-2 concurrent jobs
- 5MB file limit

### Paid Tier ($5/month):
- ~100 users per day
- 3-5 concurrent jobs
- 50MB file limit

## 🔧 Environment Variables

- `PORT` - Server port (default: 5000)
- `MAX_FILE_SIZE` - Maximum upload size in MB
- `PROCESSING_TIMEOUT` - Max processing time in seconds

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - feel free to use for personal and commercial projects.

## 🙏 Acknowledgments

- [Demucs](https://github.com/facebookresearch/demucs) - Facebook Research
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Railway](https://railway.app) - Deployment platform

## 📞 Support

- 🐛 [Report Issues](https://github.com/yourusername/stemscreator-pwa/issues)
- 💬 [Discussions](https://github.com/yourusername/stemscreator-pwa/discussions)
- 📧 Email: your-email@example.com

---

**Made with ❤️ for musicians and audio engineers**
# stemscreator-pwa
# stemscreator-pwa
