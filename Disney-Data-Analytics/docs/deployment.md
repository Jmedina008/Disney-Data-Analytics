# 🚀 Deployment Guide

## Overview

This guide covers deploying the Disney Data Analytics portfolio for live demonstration. Multiple deployment options are provided to suit different needs and technical requirements.

## Quick Demo Options

### 1. GitHub Pages (Recommended for Portfolio)

#### Setup Steps:
```bash
# 1. Push to GitHub
git add .
git commit -m "Disney Analytics Portfolio - Production Ready"
git push origin main

# 2. Enable GitHub Pages
# Go to repository Settings → Pages
# Source: Deploy from branch 'main' 
# Folder: / (root) or /docs
```

#### Configuration:
- **URL**: `https://yourusername.github.io/Disney-Data-Analytics`
- **Cost**: Free
- **Features**: Static site hosting, custom domains
- **Limitations**: Static content only (no backend APIs)

### 2. Netlify (Full-Stack Option)

#### Automated Deployment:
```bash
# 1. Connect GitHub repository to Netlify
# 2. Build settings:
#    Base directory: web/
#    Build command: npm run build
#    Publish directory: web/build
```

#### Features:
- **Functions**: Serverless backend support
- **Forms**: Contact form handling
- **Analytics**: Built-in visitor tracking
- **CDN**: Global content delivery

### 3. Vercel (Modern Deployment)

#### Quick Deploy:
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy from project root
cd Disney-Data-Analytics
vercel --prod
```

#### Benefits:
- **Edge Functions**: Global serverless computing
- **Analytics**: Real-time performance metrics
- **Previews**: Automatic deployment previews
- **Domains**: Free .vercel.app subdomain

## Production Setup

### Environment Configuration

#### Create Production Environment File:
```bash
# .env.production
REACT_APP_API_BASE_URL=https://your-api.herokuapp.com
REACT_APP_GA_TRACKING_ID=UA-XXXXXXXXX-X
REACT_APP_ENVIRONMENT=production
NODE_ENV=production
```

#### Build Optimization:
```json
// package.json
{
  "scripts": {
    "build": "react-scripts build",
    "build:analyze": "npm run build && npx bundle-analyzer build/static/js/*.js",
    "serve": "serve -s build -l 3000"
  }
}
```

### Backend API Deployment (Optional)

#### Heroku Deployment:
```bash
# 1. Create Heroku app
heroku create disney-analytics-api

# 2. Set environment variables
heroku config:set TMDB_API_KEY=your_key_here
heroku config:set DATABASE_URL=your_db_url

# 3. Deploy
git push heroku main
```

#### Railway Deployment (Alternative):
```yaml
# railway.toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "python -m uvicorn api.main:app --host 0.0.0.0 --port $PORT"
```

## Performance Optimization

### Frontend Optimization

#### Code Splitting:
```javascript
// Lazy load components
const MovieAnalytics = lazy(() => import('./components/MovieAnalytics'));
const ThemeParkDashboard = lazy(() => import('./components/ThemeParkDashboard'));

// Usage with Suspense
<Suspense fallback={<Loading />}>
  <MovieAnalytics />
</Suspense>
```

#### Bundle Analysis:
```bash
# Analyze bundle size
npm run build:analyze

# Optimize large dependencies
npm install --save-dev webpack-bundle-analyzer
```

### Data Optimization

#### CDN Setup for Data:
```javascript
// Use CDN for large datasets
const DATA_CDN_BASE = 'https://cdn.your-domain.com/data/';

const fetchMovieData = async () => {
  const response = await fetch(`${DATA_CDN_BASE}disney_movies.json`);
  return response.json();
};
```

#### Caching Strategy:
```javascript
// Service Worker for offline support
// sw.js
const CACHE_NAME = 'disney-analytics-v1';
const urlsToCache = [
  '/',
  '/static/js/bundle.js',
  '/static/css/main.css',
  '/data/disney_movies.json'
];
```

## Analytics & Monitoring

### Google Analytics Setup:
```javascript
// gtag configuration
gtag('config', 'GA_TRACKING_ID', {
  page_title: 'Disney Analytics Portfolio',
  page_location: window.location.href,
  custom_map: {
    'custom_parameter': 'dimension1'
  }
});
```

### Error Monitoring:
```bash
# Install Sentry
npm install @sentry/react

# Configuration
Sentry.init({
  dsn: "YOUR_SENTRY_DSN",
  environment: process.env.NODE_ENV,
  beforeSend(event) {
    // Filter sensitive data
    return event;
  }
});
```

## Security Considerations

### API Key Protection:
```javascript
// Never expose API keys in frontend
// Use environment variables and proxy endpoints
const API_PROXY = process.env.REACT_APP_API_PROXY;

// Secure headers
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  next();
});
```

### Content Security Policy:
```html
<!-- Add to HTML head -->
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self' 'unsafe-inline' https://www.google-analytics.com;
               style-src 'self' 'unsafe-inline';
               img-src 'self' data: https:;">
```

## Custom Domain Setup

### DNS Configuration:
```bash
# For custom domain (optional)
# 1. Add CNAME record: www.your-domain.com → your-username.github.io
# 2. Add A records for apex domain:
#    185.199.108.153
#    185.199.109.153
#    185.199.110.153
#    185.199.111.153
```

### SSL Certificate:
- GitHub Pages: Automatic HTTPS
- Netlify: Free SSL certificates
- Custom: Let's Encrypt or Cloudflare

## Deployment Checklist

### Pre-Deployment:
- [ ] ✅ All data generated and working locally
- [ ] ✅ Tests passing (`npm test` / `pytest`)
- [ ] ✅ Build successful (`npm run build`)
- [ ] ✅ Environment variables configured
- [ ] ✅ Analytics tracking added
- [ ] ✅ SEO meta tags included

### Post-Deployment:
- [ ] ✅ Site accessible at deployment URL
- [ ] ✅ All visualizations loading correctly
- [ ] ✅ Interactive features working
- [ ] ✅ Mobile responsiveness verified
- [ ] ✅ Performance scores acceptable (>90)
- [ ] ✅ Analytics tracking functional

## Maintenance & Updates

### Automated Updates:
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '16'
      - run: npm install
      - run: npm run build
      - name: Deploy to Netlify
        uses: netlify/actions/cli@master
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
        with:
          args: deploy --prod --dir=build
```

### Data Updates:
```bash
# Automated data refresh (if using APIs)
# Setup cron job or GitHub Actions to run:
python scripts/update_data.py
git add data/
git commit -m "Automated data update"
git push
```

## Demo URLs

### Live Portfolio Examples:
- **Portfolio Demo**: `https://yourusername.github.io/Disney-Data-Analytics`
- **Interactive Dashboard**: `https://disney-analytics.netlify.app`
- **API Documentation**: `https://disney-api.herokuapp.com/docs`

### QR Code for Mobile Demo:
```
Generate QR code linking to deployed portfolio
for easy mobile demonstration during interviews
```

## Troubleshooting

### Common Issues:

#### Build Failures:
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

#### Routing Issues (SPA):
```javascript
// Add to build output
// _redirects file for Netlify:
/* /index.html 200

// Or for Apache (.htaccess):
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.html [L]
```

#### Performance Issues:
```bash
# Optimize images
npm install imagemin imagemin-mozjpeg imagemin-pngquant
# Minify JSON data
npm install jsonminify
# Enable gzip compression
```

---

## 🎯 Launch Strategy

1. **GitHub Pages** - For basic portfolio demonstration
2. **Netlify/Vercel** - For full-featured deployment
3. **Custom Domain** - For professional presentation
4. **Analytics** - To track engagement and performance
5. **CI/CD** - For seamless updates and maintenance

*Ready to showcase Disney data magic to the world! ✨*