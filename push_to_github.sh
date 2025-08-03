#!/bin/bash
# GitHub Push Script - Run this after creating your GitHub repository
# Replace YOUR_USERNAME with your actual GitHub username

echo "🚀 Setting up GitHub remote..."

# Replace YOUR_USERNAME with your actual GitHub username
read -p "Enter your GitHub username: " USERNAME

echo "Adding GitHub remote for user: $USERNAME"
git remote add origin https://github.com/$USERNAME/stemscreator-pwa.git

echo "📤 Pushing to GitHub..."
git branch -M main
git push -u origin main

echo "✅ Successfully pushed to GitHub!"
echo "🌐 Your repository: https://github.com/$USERNAME/stemscreator-pwa"
echo ""
echo "🚀 Next step: Deploy on Railway.app"
echo "1. Go to https://railway.app"
echo "2. Sign up with GitHub"
echo "3. Click 'Deploy from GitHub repo'"
echo "4. Select your stemscreator-pwa repository"
echo "5. Railway will automatically deploy your app!"
