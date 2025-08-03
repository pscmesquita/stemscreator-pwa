# Custom Domain Setup Guide

## 🌐 Setting Up Your Custom Domain for StemsCreator

### Prerequisites:
- Your app deployed on Railway/Render
- A domain name you own (e.g., GoDaddy, Namecheap, Cloudflare)

### Step 1: Railway Domain Configuration

1. **Login to Railway.app**
2. **Go to your StemsCreator project**
3. **Click "Settings" tab**
4. **Click "Domains" section**
5. **Click "Add Domain"**
6. **Enter your domain:**
   - For subdomain: `stemscreator.yourdomain.com`
   - For root domain: `yourdomain.com`

### Step 2: DNS Configuration

#### For Subdomain (Recommended):
```
Record Type: CNAME
Name: stemscreator
Target: your-app-name.up.railway.app
TTL: 300 (or default)
```

#### For Root Domain:
```
Record Type: A
Name: @ (or leave blank)
Target: [Railway will provide IP]
TTL: 300
```

### Step 3: SSL Certificate

- Railway automatically provides **FREE SSL certificates**
- Your site will be available as `https://stemscreator.yourdomain.com`
- Certificate updates automatically

### Step 4: PWA Manifest Update

Update your `static/manifest.json`:

```json
{
    "name": "StemsCreator",
    "short_name": "StemsCreator", 
    "start_url": "https://stemscreator.yourdomain.com/",
    "scope": "https://stemscreator.yourdomain.com/",
    ...
}
```

### Popular Domain Providers:

#### **Namecheap:**
1. Login to Namecheap
2. Go to "Domain List" → "Manage"
3. Click "Advanced DNS"
4. Add CNAME record

#### **GoDaddy:**
1. Login to GoDaddy
2. Go to "My Products" → "DNS"
3. Add CNAME record

#### **Cloudflare:**
1. Login to Cloudflare
2. Select your domain
3. Go to "DNS" tab
4. Add CNAME record
5. **Set proxy status to "DNS only" (gray cloud)**

#### **Google Domains:**
1. Login to Google Domains
2. Select your domain
3. Go to "DNS" tab
4. Add CNAME record

### Step 5: Verification

1. **Wait 5-60 minutes** for DNS propagation
2. **Visit your custom domain**
3. **Test PWA installation** from mobile
4. **Verify SSL certificate** (should show green lock)

### Troubleshooting:

#### **"Site not found" error:**
- Check DNS configuration
- Wait longer for propagation (up to 24 hours)
- Verify Railway domain settings

#### **SSL certificate issues:**
- Railway handles this automatically
- May take 10-15 minutes after DNS is working

#### **PWA not installing:**
- Clear browser cache
- Update manifest.json with new domain
- Redeploy app

### Cost:
- **Domain**: $10-15/year (your domain provider)
- **SSL Certificate**: FREE (included with Railway)
- **Hosting**: FREE on Railway (or $5/month for Pro)

### Example URLs:
- `https://stemscreator.yoursite.com`
- `https://ai-stems.yoursite.com` 
- `https://musictools.yoursite.com`
- `https://yoursite.com` (root domain)

### Benefits of Custom Domain:
- **Professional appearance**
- **Better for marketing**
- **Custom branding**
- **Easier to remember**
- **SEO benefits**
- **Custom email possible** (contact@yoursite.com)
