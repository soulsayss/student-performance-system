# 🚀 Render Deployment Guide

Complete step-by-step guide to deploy your backend on Render (FREE tier).

## What is Render?

Render is a cloud platform that hosts your backend for free. It's perfect for beginners!

## Prerequisites

- GitHub account with your code pushed
- Render account (create at https://render.com)

## Step-by-Step Deployment

### 1. Create Render Account

1. Go to https://render.com
2. Click "Sign up"
3. Choose "Sign up with GitHub"
4. Authorize Render to access your GitHub

### 2. Create a New Web Service

1. Click "New +" button (top right)
2. Select "Web Service"
3. Click "Connect a repository"
4. Find and select `student-performance-system`
5. Click "Connect"

### 3. Configure the Service

Fill in these settings:

**Name:** `student-performance-backend`

**Environment:** `Python 3`

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
gunicorn app:create_app()
```

**Root Directory:** `backend` (IMPORTANT!)

### 4. Add Environment Variables

Click "Advanced" and add these variables:

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |
| `SECRET_KEY` | Generate a random string (or leave blank for auto-generation) |
| `JWT_SECRET_KEY` | Generate a random string (or leave blank for auto-generation) |
| `PRODUCTION_FRONTEND_URL` | Leave blank for now (add after frontend deployment) |

**How to generate random strings:**
- Use: https://www.random.org/strings/
- Or just use any random text like: `my-secret-key-12345`

### 5. Deploy

1. Click "Create Web Service"
2. Wait for deployment (2-5 minutes)
3. You'll see a URL like: `https://student-performance-backend.onrender.com`

### 6. Create Admin User

After deployment completes:

1. Go to your Render dashboard
2. Click on your service
3. Click "Shell" tab
4. Run this command:
   ```bash
   python create_admin_render.py
   ```
5. You'll see:
   ```
   ✓ Admin user created successfully!
   
   📋 Admin Credentials:
      Email: admin@school.com
      Password: admin123
   ```

### 7. Test Your Backend

Open this URL in your browser:
```
https://your-service-name.onrender.com/health
```

You should see:
```json
{"status": "healthy"}
```

## 🔗 Connect Frontend to Backend

After deploying frontend on Vercel:

1. Go back to Render dashboard
2. Click your service
3. Click "Environment"
4. Add new variable:
   - Key: `PRODUCTION_FRONTEND_URL`
   - Value: `https://your-frontend.vercel.app`
5. Click "Save"
6. Service will auto-redeploy

## 📊 Database

Your backend uses PostgreSQL on Render (automatically provided).

- Database is created automatically
- Data persists between deployments
- Free tier has 1GB storage

## 🆘 Troubleshooting

### "Build failed"
- Check that `requirements.txt` is in the `backend/` folder
- Make sure all dependencies are listed

### "Service won't start"
- Check logs in Render dashboard
- Make sure `gunicorn` is in requirements.txt
- Verify `render.yaml` is correct

### "Admin user creation failed"
- Make sure database is initialized
- Check that `create_admin_render.py` is in backend folder
- Try running it again

### "CORS errors in frontend"
- Make sure frontend URL is added to `PRODUCTION_FRONTEND_URL`
- Wait 5 minutes for changes to take effect

## 📝 Important Notes

1. **Free tier limitations:**
   - Service spins down after 15 minutes of inactivity
   - First request after spin-down takes 30 seconds
   - 1GB storage limit

2. **Security:**
   - Change admin password after first login
   - Use strong SECRET_KEY in production
   - Never commit secrets to GitHub

3. **Database:**
   - PostgreSQL is provided automatically
   - Backups are automatic
   - Data persists between deployments

## 🎯 Next Steps

1. ✅ Deploy backend on Render
2. Deploy frontend on Vercel
3. Connect them together
4. Test all features
5. Share your live demo!

## 📞 Need Help?

- Render Docs: https://render.com/docs
- Check Render dashboard logs for errors
- Common issues are usually in the logs

---

**Your backend is now live! 🎉**

Share your API URL: `https://your-service-name.onrender.com`
