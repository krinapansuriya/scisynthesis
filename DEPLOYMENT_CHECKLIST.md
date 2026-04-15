# 🚀 SciSynthesis Deployment Checklist for scisynthesis.in

**Target Domain**: scisynthesis.in  
**Backend API**: api.scisynthesis.in  
**Frontend**: scisynthesis.in (with www.scisynthesis.in)

---

## ✅ Pre-Deployment Checklist

- [x] Backend requirements.txt complete (all dependencies listed)
- [x] Frontend package.json up to date
- [x] Production environment files created:
  - [x] `backend/.env.production` (with placeholder for GOOGLE_API_KEY)
  - [x] `frontend/.env.production` (with VITE_API_URL)
- [x] Frontend API configuration updated for production
- [x] Vite build configuration optimized
- [ ] GitHub repository is public and accessible
- [ ] All local changes committed

---

## 📋 Step 1: Prepare GitHub Repository

Before deploying, ensure your code is pushed to GitHub:

```bash
# From project root
git add .
git commit -m "Configure production deployment for scisynthesis.in"
git push origin main
```

**Verify**:
- Visit https://github.com/YOUR_USERNAME/scisynthesis
- Ensure `backend/` and `frontend/` folders are visible
- Check that `.env.production` files are NOT committed (add to .gitignore if needed)

---

## 🔧 Step 2: Deploy Backend to Render.com

### 2.1 Create Render Account & Connect GitHub

1. Go to [render.com](https://render.com) and sign up
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select your repo (e.g., `krinapansuriya/scisynthesis`)
5. Click **"Continue"**

### 2.2 Configure Web Service

Fill in these settings:

- **Service Name**: `scisynthesis-api`
- **Root Directory**: `backend` ✅ (Important!)
- **Environment**: `Python`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Instance Type**: Free tier (or paid if needed)

### 2.3 Add Environment Variables

In the Render dashboard, add these environment variables:

```
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY_HERE
VECTOR_DB_TYPE=faiss
ENVIRONMENT=production
LOG_LEVEL=info
ALLOWED_ORIGINS=https://scisynthesis.in,https://www.scisynthesis.in,http://localhost:3000
```

⚠️ **Important**: Replace `YOUR_GEMINI_API_KEY_HERE` with your actual Google Gemini API key

### 2.4 Deploy

- Click **"Create Web Service"**
- Wait for deployment (3-5 minutes)
- You'll get a public URL like: `https://scisynthesis-api.onrender.com`
- ✅ **Note this URL** - you'll need it for DNS setup

### 2.5 Add Custom Domain (api.scisynthesis.in)

1. Go to Service Settings
2. Scroll to **"Custom Domain"**
3. Enter: `api.scisynthesis.in`
4. Render will show you DNS records to add (we'll do this later)

---

## 🎨 Step 3: Deploy Frontend to Vercel

### 3.1 Create Vercel Account & Connect GitHub

1. Go to [vercel.com](https://vercel.com) and sign up with GitHub
2. Click **"New Project"**
3. Import your GitHub repo
4. Vercel should auto-detect it's a Vite project

### 3.2 Configure Project Settings

- **Framework Preset**: Vite ✅
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm ci`

### 3.3 Add Environment Variables

Add to Vercel dashboard:

```
VITE_API_URL=https://api.scisynthesis.in/api/v1
VITE_ENV=production
```

### 3.4 Deploy

- Click **"Deploy"**
- Wait for build to complete (2-3 minutes)
- You'll get a Vercel URL like: `https://scisynthesis.vercel.app`
- ✅ **This confirms frontend builds correctly**

### 3.5 Add Custom Domain (scisynthesis.in)

1. Go to Project Settings
2. Click **"Domains"**
3. Add domain: `scisynthesis.in`
4. Follow Vercel's instructions for DNS setup
5. Also add: `www.scisynthesis.in` as alias

---

## 🌐 Step 4: Configure DNS at Domain Registrar

After both services are deployed, log into your domain registrar (Namecheap, GoDaddy, etc.) and add these DNS records:

### For Frontend (Vercel):

**Option A: Using Vercel's CNAME** (Recommended)

| Type  | Name | Value                           |
|-------|------|----------------------------------|
| CNAME | @    | cname.vercel-dns.com            |
| CNAME | www  | cname.vercel-dns.com            |

**Option B: Using A Record** (Alternative)

| Type  | Name | Value       |
|-------|------|-------------|
| A     | @    | 76.76.19.89 |
| CNAME | www  | scisynthesis.in |

### For Backend API (Render):

Get your Render service URL first:
1. Go to your Render service dashboard
2. Copy the public URL (something like `https://scisynthesis-api-xxxxx.onrender.com`)
3. Extract just the domain part without https://

| Type  | Name | Value                      |
|-------|------|----------------------------|
| CNAME | api  | scisynthesis-api.onrender.com |

⏱️ **Wait 24-48 hours for DNS propagation**

**Test DNS Resolution**:
```bash
# In terminal/cmd
nslookup scisynthesis.in
nslookup api.scisynthesis.in

# Should show the IP addresses pointing to Vercel and Render
```

---

## 🧪 Step 5: Testing Deployment

Once DNS propagates, test the deployment:

### 5.1 Test Backend API

```bash
# Check if API is responding
curl https://api.scisynthesis.in/docs

# Should return Swagger UI for API documentation
```

### 5.2 Test Frontend

1. Open https://scisynthesis.in in your browser
2. Application should load
3. Open **DevTools** → **Network** tab
4. Try logging in or any action that calls the API
5. Verify API calls go to `https://api.scisynthesis.in/api/v1/...`

### 5.3 Full Integration Test

1. ✅ Frontend loads from scisynthesis.in
2. ✅ Can access the app without errors
3. ✅ Login/authentication works
4. ✅ API requests succeed (check Network tab)
5. ✅ No CORS errors in console
6. ✅ Try main features (upload document, submit query, etc.)

---

## 🔒 SSL/HTTPS Setup

✅ **Already Done!**
- Vercel provides FREE SSL certificate automatically
- Render provides FREE SSL certificate automatically
- HTTPS enabled by default
- Certificates auto-renew

---

## 📊 Monitoring & Maintenance

### View Logs

**Render Logs**:
1. Go to your service on Render
2. Click **"Logs"** tab
3. View real-time logs

**Vercel Logs**:
1. Go to your project
2. Click **"Deployments"**
3. Select latest deployment → **"Logs"**

### Set Up Error Alerts (Optional)

- **Sentry**: Error tracking for both frontend and backend
- **Uptime Robot**: Monitor if sites are up
- **Vercel Analytics**: Built-in performance metrics

---

## ⚠️ Troubleshooting

### Issue: Frontend can't reach backend (CORS error)

**Solution**:
1. Check `ALLOWED_ORIGINS` in Render environment variables
2. Verify it includes: `https://scisynthesis.in,https://www.scisynthesis.in`
3. Restart Render service
4. Clear browser cache and try again

### Issue: Domain not resolving (ERR_NAME_NOT_RESOLVED)

**Solution**:
1. Wait 24-48 hours for full DNS propagation
2. Test with: `nslookup scisynthesis.in`
3. Clear local DNS cache:
   - **Windows**: `ipconfig /flushdns`
   - **Mac**: `sudo dscacheutil -flushcache`

### Issue: 502 Bad Gateway from Render

**Solution**:
1. Check Render logs for errors
2. Verify GOOGLE_API_KEY is correct
3. Check if dependencies installed correctly
4. Restart service from Render dashboard

### Issue: Build fails on Vercel

**Solution**:
1. Check Vercel build logs
2. Ensure `npm run build` works locally
3. Verify all dependencies in package.json
4. Check TypeScript errors: `npm run lint`

---

## 🎯 Quick Reference URLs

| Service      | URL                                    | Dashboard              |
|--------------|----------------------------------------|------------------------|
| Frontend     | https://scisynthesis.in                | vercel.com             |
| Frontend (www) | https://www.scisynthesis.in          | vercel.com             |
| Backend API  | https://api.scisynthesis.in/docs       | render.com             |
| API Health   | https://api.scisynthesis.in/health     | -                      |

---

## 📈 Cost Summary

| Service           | Cost           | Notes                 |
|-------------------|----------------|-----------------------|
| Vercel Frontend   | Free           | Generous free tier    |
| Render Backend    | Free/Paid      | Free tier with sleep  |
| Domain (.in)      | ~₹99-249/year  | One-time purchase     |
| **Total**         | ~₹0-249/year   | Mostly free!          |

---

## ✨ Next Steps After Deployment

1. **Monitor**: Check logs daily for errors
2. **Backup**: Set up regular database backups if using external DB
3. **Updates**: Keep dependencies updated
4. **Performance**: Monitor Vercel Analytics and Render metrics
5. **Scaling**: Upgrade plan if needed as traffic grows

---

## 📞 Support

- **Render Support**: support@render.com
- **Vercel Support**: support@vercel.com
- **Docs**: See deployment-guide.md for detailed docs

---

**Good luck with your deployment! 🚀**
