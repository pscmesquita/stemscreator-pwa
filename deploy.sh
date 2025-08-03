# Quick deployment script for Railway
# This creates all necessary files for deployment

echo "🚀 Preparing StemsCreator for deployment..."

# Create .gitignore
cat > .gitignore << EOF
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv
uploads/
results/
*.wav
*.mp3
*.flac
*.zip
.env
.DS_Store
Thumbs.db
EOF

echo "✅ Created .gitignore"

# Create railway.json for configuration
cat > railway.json << EOF
{
  "\$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
EOF

echo "✅ Created railway.json"

echo "🎯 Ready for deployment!"
echo ""
echo "Next steps:"
echo "1. Create GitHub repository"
echo "2. Push code: git add . && git commit -m 'Deploy StemsCreator' && git push"
echo "3. Go to https://railway.app and deploy from GitHub"
echo "4. Your app will be live at: https://yourapp.railway.app"
