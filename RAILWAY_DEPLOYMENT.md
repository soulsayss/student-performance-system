# 🚂 Railway Deployment Guide

## Why Railway?
- **8GB RAM** (vs Render's 512MB) - Perfect for our 60 students!
- **PostgreSQL database** included
- **$5 free credit per month**
- Better performance and reliability

---

## Step-by-Step Deployment

### 1. Create Railway Account
1. Go to https://railway.app/
2. Sign up with GitHub (recommended)
3. Verify your email

### 2. Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository: `soulsayss/student-performance-system`
4. Railway will detect it's a Python app

### 3. Add PostgreSQL Database
1. In your project, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically create the database
4. The `DATABASE_URL` environment variable is auto-configured

### 4. Configure Backend Service
1. Click on your backend service
2. Go to "Settings" tab
3. Set the following:

**Root Directory:**
```
backend
```

**Start Command:**
```
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

**Environment Variables:**
- `SECRET_KEY` = `your-secret-key-here-change-this`
- `JWT_SECRET_KEY` = `your-jwt-secret-key-here-change-this`
- `PYTHON_VERSION` = `3.11`
- `FORCE_RESEED` = `true` (for first deployment only, then remove)

**Note:** `DATABASE_URL` is automatically set by Railway when you add PostgreSQL

### 5. Deploy
1. Click "Deploy" or push to GitHub (auto-deploys)
2. Wait 3-5 minutes for build and deployment
3. Check logs for "Database tables created successfully!"
4. Your backend URL will be: `https://[your-project].railway.app`

### 6. Update Frontend (Vercel)
1. Go to your Vercel project settings
2. Update environment variable:
   - `VITE_API_URL` = `https://[your-railway-url].railway.app`
3. Redeploy frontend

### 7. Test
1. Visit your Vercel frontend URL
2. Login with admin: `admin@school.edu` / `Admin@123`
3. Test all 4 dashboards (admin, teacher, parent, student)

---

## Troubleshooting

### Database Not Seeding?
- Check logs for errors
- Set `FORCE_RESEED=true` environment variable
- Redeploy

### 500 Errors?
- Check Railway logs (click on service → "Logs" tab)
- Verify `DATABASE_URL` is set correctly
- Check PostgreSQL service is running

### CORS Errors?
- Verify Railway URL is added to CORS in `app.py`
- Check Vercel environment variable has correct Railway URL

---

## Cost Estimate (Free Tier)
- **$5 free credit per month**
- Backend + PostgreSQL = ~$3-4/month
- **You get ~1-2 months free!**

After free credit runs out, you can:
1. Add a credit card for $5/month
2. Use a new account (not recommended)
3. Switch to paid plan ($5/month)

---

## Railway vs Render Comparison

| Feature | Railway Free | Render Free |
|---------|-------------|-------------|
| RAM | 8GB | 512MB ❌ |
| Database | PostgreSQL ✅ | SQLite only |
| Free Credit | $5/month | None |
| Performance | Excellent | Poor for our app |
| Auto-deploy | Yes | Yes |

**Winner: Railway** 🏆

---

## Next Steps After Deployment

1. Remove `FORCE_RESEED=true` environment variable (to prevent data loss)
2. Test all features thoroughly
3. Share your live demo URL!
4. Monitor Railway usage dashboard

---

## Support

If you face any issues:
1. Check Railway logs first
2. Check this guide
3. Railway Discord: https://discord.gg/railway
