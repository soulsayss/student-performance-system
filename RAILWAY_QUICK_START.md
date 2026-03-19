# 🚀 Railway Quick Start (5 Minutes)

## What You Need to Do

### 1️⃣ Go to Railway (2 min)
```
https://railway.app/
```
- Sign up with GitHub
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose: `soulsayss/student-performance-system`

### 2️⃣ Add PostgreSQL (1 min)
- Click "New" → "Database" → "PostgreSQL"
- Done! (DATABASE_URL auto-configured)

### 3️⃣ Configure Backend (2 min)
Click on backend service → Settings:

**Root Directory:**
```
backend
```

**Environment Variables (Add these):**
```
SECRET_KEY=my-super-secret-key-2026
JWT_SECRET_KEY=my-jwt-secret-key-2026
PYTHON_VERSION=3.11
FORCE_RESEED=true
```

**Start Command:**
```
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

### 4️⃣ Deploy & Get URL
- Click "Deploy" (or it auto-deploys)
- Wait 3-5 minutes
- Copy your Railway URL: `https://[something].railway.app`

### 5️⃣ Update Vercel Frontend
- Go to Vercel project settings
- Environment Variables
- Update `VITE_API_URL` = `https://[your-railway-url].railway.app`
- Redeploy frontend

### 6️⃣ Test!
- Visit your Vercel URL
- Login: `admin@school.edu` / `Admin@123`
- Test teacher dashboard (should work now with 8GB RAM!)

---

## Why This Will Work

✅ **8GB RAM** (vs Render's 512MB)  
✅ **PostgreSQL** (better than SQLite)  
✅ **$5 free credit** (1-2 months free)  
✅ **All 60 students** will work perfectly  
✅ **No more 500 errors!**

---

## After First Successful Test

**IMPORTANT:** Remove `FORCE_RESEED=true` from environment variables to prevent data loss on future deployments!

---

## Your Railway URL Will Be
```
https://student-performance-backend-production-XXXX.up.railway.app
```

Copy this and update in Vercel!
