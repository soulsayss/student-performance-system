# 🔄 Update Vercel Environment Variable

## Current Issue

The environment variable `VITE_API_URL` is set to the OLD backend URL:
```
https://student-performance-backend.onrender.com
```

But the backend is now at the NEW URL:
```
https://student-performance-backend-rsga.onrender.com
```

## How to Fix (2 minutes)

### Step 1: Go to Vercel Settings
1. Open: https://vercel.com/dashboard
2. Click your project: `student-performance-system`
3. Click **Settings** tab
4. Click **Environment Variables** in left sidebar

### Step 2: Edit the Variable
1. Find `VITE_API_URL` in the list
2. Click the **three dots (...)** on the right
3. Click **Edit**

### Step 3: Update the Value
Change from:
```
https://student-performance-backend.onrender.com
```

To:
```
https://student-performance-backend-rsga.onrender.com
```

### Step 4: Save
Click **Save**

### Step 5: Redeploy Frontend
1. Go to **Deployments** tab
2. Click the **three dots (...)** on the latest deployment
3. Click **Redeploy**
4. Wait for status to change to **Ready** (1-2 minutes)

## Verify It Works

After redeployment:
1. Go to: https://student-performance-system-kohl.vercel.app
2. Open browser console (F12)
3. Should see NO errors
4. Try login:
   - Email: `admin@school.edu`
   - Password: `Admin@123`

## Why This Matters

- Frontend needs to know where backend is
- Old URL doesn't exist anymore
- New URL is where Render deployed the backend
- Without this, login will fail with network error

---

**This is the final step to make everything work!**

