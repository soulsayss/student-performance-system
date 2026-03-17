# ⚡ Quick Fix - 5 Minutes to Working System

## The Problem
Frontend can't connect to backend because it doesn't know the backend URL.

## The Solution
Tell Vercel where the backend is.

## Do This Now

### 1. Open Vercel
https://vercel.com/dashboard

### 2. Click Your Project
`student-performance-system`

### 3. Settings → Environment Variables

### 4. Add Variable
```
Name:  VITE_API_URL
Value: https://student-performance-backend-rsga.onrender.com
```

### 5. Save & Redeploy
- Click "Save"
- Go to "Deployments"
- Click "..." on latest deployment
- Click "Redeploy"
- Wait for "Ready" status

### 6. Test
https://student-performance-system-kohl.vercel.app

Login:
- Email: `admin@school.edu`
- Password: `Admin@123`

## Done! 🎉

