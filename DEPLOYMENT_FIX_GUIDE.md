# 🔧 Deployment Fix Guide

## Issues Found and Fixed

### 1. ❌ CORS Configuration Error
**Problem:** Backend had `'https://*.vercel.app'` which is NOT valid for CORS
- CORS doesn't support wildcard subdomains
- This was causing "Ensure CORS response header values are valid" error

**Fix:** Removed wildcard, kept only specific Vercel URL:
```python
cors_origins = [
    'http://localhost:3000',
    'http://localhost:5000',
    'https://student-performance-system-kohl.vercel.app',
]
```

### 2. ❌ Vercel Environment Variable Not Set
**Problem:** Frontend environment variable `VITE_API_URL` wasn't being used during build

**Fix:** Created `frontend/vercel.json` to explicitly configure environment variables

### 3. ❌ Backend URL Mismatch
**Problem:** Frontend was trying to reach old backend URL

**Fix:** Updated `.env.example` with correct Render backend URL

## What's Been Done

✅ Fixed CORS configuration in `backend/app.py`
✅ Created `frontend/vercel.json` for proper environment variable handling
✅ Updated `frontend/.env.example` with correct backend URL
✅ Pushed all changes to GitHub

## Next Steps

### Step 1: Set Environment Variable in Vercel (CRITICAL!)

1. Go to: https://vercel.com/dashboard
2. Click your project: `student-performance-system`
3. Go to **Settings** → **Environment Variables**
4. Add this variable:
   - **Name:** `VITE_API_URL`
   - **Value:** `https://student-performance-backend-rsga.onrender.com`
   - **Environments:** Select all (Production, Preview, Development)
5. Click **Save**

### Step 2: Trigger Vercel Redeploy

After setting the environment variable:
1. Go to **Deployments** tab
2. Click the three dots on the latest deployment
3. Click **Redeploy**
4. Wait for deployment to complete (shows "Ready")

### Step 3: Wait for Render Redeploy

Render will automatically redeploy with the CORS fix (2-3 minutes)

### Step 4: Test the Connection

1. Open: https://student-performance-system-kohl.vercel.app
2. Open browser console (F12)
3. You should see **NO CORS errors**
4. Try logging in with:
   - Email: `admin@school.edu`
   - Password: `Admin@123`

## Verification Checklist

- [ ] Backend health check works: https://student-performance-backend-rsga.onrender.com/health
- [ ] Frontend loads without console errors
- [ ] CORS error is gone from console
- [ ] Login request goes to correct backend URL
- [ ] Login succeeds and redirects to dashboard

## If Still Not Working

### Check 1: Verify Environment Variable in Vercel
```
Settings → Environment Variables → VITE_API_URL should be set
```

### Check 2: Check Vercel Deployment
```
Deployments → Latest deployment should show "Ready"
```

### Check 3: Check Render Backend
```
https://student-performance-backend-rsga.onrender.com/health
Should return: {"status": "healthy"}
```

### Check 4: Browser Console
```
F12 → Console tab
Should show NO errors about CORS or network
```

## Important URLs

| Component | URL |
|-----------|-----|
| Frontend | https://student-performance-system-kohl.vercel.app |
| Backend | https://student-performance-backend-rsga.onrender.com |
| Backend Health | https://student-performance-backend-rsga.onrender.com/health |
| GitHub | https://github.com/soulsayss/student-performance-system |

## Admin Credentials

```
Email: admin@school.edu
Password: Admin@123
```

⚠️ Change password after first login!

---

**The main issue was the invalid CORS wildcard. This should now be fixed!**

