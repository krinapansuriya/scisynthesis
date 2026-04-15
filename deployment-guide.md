# Complete Deployment Guide: SciSynthesis to scisynthesis.in

## Overview
Your SciSynthesis project is a full-stack application with a React frontend and FastAPI backend. Here's the complete deployment strategy.

---

## Step 1: Prepare Your Repository

### 1.1 Add Production Environment Files

Create `.env` files for production (keep them out of git):

**backend/.env.production**
```
GOOGLE_API_KEY=your_actual_gemini_api_key
VECTOR_DB_TYPE=faiss
ENVIRONMENT=production
LOG_LEVEL=info
CORS_ORIGINS=https://scisynthesis.in,https://www.scisynthesis.in
```

**frontend/.env.production**
```
VITE_API_URL=https://api.scisynthesis.in
VITE_ENV=production
```

### 1.2 Update GitHub Repository

Push all code to GitHub with proper structure:
```bash
git add .
git commit -m "Add production configuration"
git push origin main
```

---

## Step 2: Deploy Backend (FastAPI)

### Option A: Render.com (RECOMMENDED - Easy + Free Tier)

1. **Create Account**: Go to [render.com](https://render.com) and sign up
2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repo (krinapansuriya/scisynthesis)
   - Select "backend" folder as root directory
   - Runtime: Python
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables** (in Render Dashboard):
   ```
   GOOGLE_API_KEY = your_gemini_api_key
   VECTOR_DB_TYPE = faiss
   ENVIRONMENT = production
   CORS_ORIGINS = https://scisynthesis.in,https://www.scisynthesis.in
   ```

4. **Custom Domain**:
   - Go to Service Settings
   - Add Custom Domain: `api.scisynthesis.in`
   - Render will provide DNS records to add

**Expected Backend URL**: `https://api.scisynthesis.in`

### Option B: Railway.app

1. Create account at [railway.app](https://railway.app)
2. New Project → GitHub repo
3. Select backend folder
4. Add environment variables
5. Deploy → Get public URL
6. Configure custom domain in project settings

### Option C: Heroku (Requires Credit Card)

```bash
# Install Heroku CLI
heroku login
heroku create scisynthesis-api
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set GOOGLE_API_KEY=your_key
git push heroku main
```

---

## Step 3: Deploy Frontend (React + Vite)

### Option A: Vercel (RECOMMENDED - Best for React)

1. **Create Account**: Go to [vercel.com](https://vercel.com) and sign up with GitHub
2. **Import Project**:
   - Click "New Project"
   - Select your GitHub repo
   - Framework: Vite
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

3. **Environment Variables**:
   ```
   VITE_API_URL = https://api.scisynthesis.in
   ```

4. **Add Custom Domain**:
   - Settings → Domains
   - Add domain: `scisynthesis.in`
   - Vercel provides nameservers/DNS records
   - Can also add `www.scisynthesis.in` as alias

**Expected Frontend URL**: `https://scisynthesis.in`

### Option B: Netlify

1. Go to [netlify.com](https://netlify.com)
2. "New site from Git" → Select repo
3. Build settings:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `dist`

4. Add custom domain in site settings

### Option C: GitHub Pages (Free but limited)

```bash
# In frontend/vite.config.ts
export default {
  base: '/',
  // ... rest of config
}
```

---

## Step 4: Configure Custom Domain

### 4.1 Purchase Domain (if not already done)

**Recommended registrars for .in domain:**
- **Namecheap**: ~₹99/year
- **GoDaddy India**: ~₹199/year
- **BlueHost**: ~₹249/year
- **HostGator India**: ~₹149/year

### 4.2 DNS Configuration

After deploying to Vercel + Render, you'll get DNS records:

**In your domain registrar dashboard:**

1. **For Frontend (Vercel)**:
   ```
   Type: A
   Name: @
   Value: 76.76.19.89  (Vercel's IP)
   
   OR use CNAME:
   Type: CNAME
   Name: @
   Value: cname.vercel-dns.com
   ```

2. **For Backend API Subdomain**:
   ```
   Type: CNAME
   Name: api
   Value: render.onrender.com  (or your Render service URL)
   ```

3. **For WWW Subdomain**:
   ```
   Type: CNAME
   Name: www
   Value: cname.vercel-dns.com
   ```

4. **Optional - Mail (if needed)**:
   ```
   Type: MX
   Priority: 10
   Value: mail.scisynthesis.in
   ```

⏱️ **Wait 24-48 hours** for DNS propagation

---

## Step 5: Update Application Configuration

### 5.1 Update Frontend API URL

**frontend/src/config/api.ts** (or similar):
```typescript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
export const apiClient = axios.create({
  baseURL: API_URL,
  withCredentials: true,
});
```

### 5.2 Update Backend CORS

**backend/app/main.py**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://scisynthesis.in",
        "https://www.scisynthesis.in",
        "http://localhost:3000",  # local dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 5.3 Update Database Connections (if using external DB)

For production, use managed database services:
- **PostgreSQL**: Railway, Render, or Supabase
- **MongoDB**: MongoDB Atlas (free tier available)
- **Update connection strings** in `.env.production`

---

## Step 6: SSL/HTTPS Setup

✅ **Both Vercel and Render provide FREE SSL certificates automatically**
- Certificates auto-renew
- HTTPS enabled by default
- No additional action needed

---

## Step 7: Environment-Specific Build Process

### Create Deploy Script

**backend/requirements.txt** should include:
```
fastapi==0.104.1
uvicorn==0.24.0
python-dotenv==1.0.0
google-generativeai==0.4.0
sentence-transformers==2.2.2
faiss-cpu==1.7.4
# ... other dependencies
```

**frontend/package.json**:
```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint src"
  }
}
```

---

## Step 8: Monitoring & Maintenance

### 8.1 Set Up Logging

**Render Dashboard**:
- View real-time logs
- Set up error alerts
- Monitor resource usage

**Vercel Dashboard**:
- View build logs
- Monitor performance metrics
- Set up error notifications

### 8.2 Set Up Monitoring

**Recommended tools** (free tier available):
- **Sentry** - Error tracking
- **Uptime Robot** - Uptime monitoring
- **Vercel Analytics** - Built-in performance monitoring

### 8.3 CI/CD Pipeline (Optional but Recommended)

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          cd backend
          pip install -r requirements.txt
          pytest

  deploy-backend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Render
        run: |
          curl -X POST https://api.render.com/deploy/srv-${{ secrets.RENDER_BACKEND_ID }}?key=${{ secrets.RENDER_API_KEY }}

  deploy-frontend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Vercel
        run: |
          cd frontend
          npm ci
          npm run build
        env:
          VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
          VITE_API_URL: https://api.scisynthesis.in
```

---

## Step 9: Testing Deployment

### 9.1 Test Backend API

```bash
# Check if API is running
curl https://api.scisynthesis.in/health

# Or use Postman/Insomnia to test endpoints
GET https://api.scisynthesis.in/docs
```

### 9.2 Test Frontend

```bash
# Check if frontend loads
curl https://scisynthesis.in

# Check console for API connection issues
# Verify in Network tab of DevTools
```

### 9.3 Full Integration Test

1. Open `https://scisynthesis.in` in browser
2. Try logging in
3. Upload a document
4. Submit a query
5. Verify API responses in Network tab

---

## Quick Checklist

- [ ] Backend requirements.txt complete
- [ ] Frontend package.json up to date
- [ ] Environment variables configured
- [ ] GitHub repo is public and accessible
- [ ] Render account created and backend deployed
- [ ] Vercel account created and frontend deployed
- [ ] Domain purchased (scisynthesis.in)
- [ ] DNS records added to registrar
- [ ] CORS configured on backend
- [ ] API URL set in frontend .env
- [ ] SSL certificates active (auto-generated)
- [ ] Both frontend & backend responding to requests
- [ ] Full end-to-end test completed
- [ ] Monitoring alerts set up (optional)

---

## Troubleshooting

### Frontend can't reach Backend API
**Problem**: CORS error in console
**Solution**: 
- Check CORS_ORIGINS in backend .env matches frontend URL
- Verify api.scisynthesis.in DNS resolution
- Check backend logs for errors

### Domain not resolving
**Problem**: ERR_NAME_NOT_RESOLVED
**Solution**:
- Wait 24-48 hours for DNS propagation
- Clear browser cache and DNS cache
- Test with `nslookup scisynthesis.in` or `dig scisynthesis.in`

### 502 Bad Gateway
**Problem**: Backend timeout or not responding
**Solution**:
- Check Render/Railway logs
- Verify API key and environment variables
- Restart service

### High latency
**Problem**: Slow response times
**Solution**:
- Use Vercel's Edge Functions for frontend
- Optimize backend response times
- Enable caching headers

---

## Cost Estimation

**Free Tier Options (Monthly Cost)**:
- Vercel: $0 (generous free tier)
- Render: $0 (free tier with limitations)
- Railway: $5 (includes $5 credit)
- Total: ~$0-5/month (after free credits)

**Paid Domain**: ~₹99-249/year for .in domain

---

## Next Steps

1. **Start with Backend Deployment** (Render)
   - Quickest to set up
   - Can test independently

2. **Deploy Frontend** (Vercel)
   - Connect to backend
   - Test full integration

3. **Configure DNS**
   - Point domain to services
   - Wait for propagation

4. **Monitor & Maintain**
   - Set up error tracking
   - Monitor performance
   - Plan for scaling

---

## Additional Resources

- [Render Docs](https://render.com/docs)
- [Vercel Docs](https://vercel.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Vite Production Guide](https://vitejs.dev/guide/build.html)
- [CORS Best Practices](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)

---

**Need Help?**
- Render Support: support@render.com
- Vercel Support: support@vercel.com
- Check logs in respective dashboards
- Test endpoints with Postman/curl

