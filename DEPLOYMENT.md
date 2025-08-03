# Deployment Guide for StemsCreator PWA

## Option 1: Railway.app (RECOMMENDED - FREE)

### Step 1: Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub account
3. Connect your GitHub account

### Step 2: Push Code to GitHub
```bash
# In your web_app folder
git init
git add .
git commit -m "Initial StemsCreator PWA"

# Create repository on GitHub, then:
git remote add origin https://github.com/yourusername/stemscreator-pwa.git
git push -u origin main
```

### Step 3: Deploy on Railway
1. Go to Railway dashboard
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will auto-detect Python and deploy!

### Step 4: Configure Environment
- Railway automatically detects the Dockerfile
- Your app will be available at: https://yourapp.railway.app

---

## Option 2: Render.com (FREE Alternative)

### Steps:
1. Go to https://render.com
2. Connect GitHub
3. Create "Web Service"
4. Choose your repository
5. Set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`

---

## Option 3: Fly.io (FREE with Docker)

### Steps:
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login and deploy
flyctl auth login
flyctl apps create stemscreator-pwa
flyctl deploy
```

---

## Expected Costs:

### FREE Options:
- **Railway**: $0 (512MB RAM, $5 monthly credit)
- **Render**: $0 (sleeps after 15min inactivity)
- **Fly.io**: $0 (256MB RAM)

### Paid Upgrades:
- **Railway Pro**: $5/month (1GB RAM, always-on)
- **Render Paid**: $7/month (512MB RAM, always-on)
- **DigitalOcean**: $5/month (512MB RAM)

---

## Performance Tips:

### For FREE tiers:
- Limit file size to 5MB
- Processing timeout after 5 minutes
- App may sleep when not used

### For PAID tiers:
- Support larger files (up to 50MB)
- Faster processing
- Always available

---

## Mobile Access:

Once deployed, your app will be available at:
- `https://yourapp.railway.app`
- `https://yourapp.render.com`
- `https://yourapp.fly.dev`

Users can:
- Open in mobile browser
- "Add to Home Screen" for app-like experience
- Works on iOS and Android
- Offline UI (online processing)

---

## Domain Setup (Optional):

### Free Custom Domain:
1. Use Freenom (.tk, .ml domains)
2. Point DNS to your Railway/Render URL
3. Enable HTTPS in platform settings

### Paid Domain:
1. Buy domain from Namecheap (~$10/year)
2. Configure DNS in Railway/Render
3. Automatic HTTPS

---

## Scaling:

### Free Tier Limits:
- ~10-20 users per day
- 1-2 concurrent jobs
- 5MB file limit

### Paid Tier ($5/month):
- ~100 users per day
- 3-5 concurrent jobs
- 50MB file limit

### Higher Scale ($20+/month):
- Unlimited users
- 10+ concurrent jobs
- 100MB+ files
