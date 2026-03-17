# 🔐 Vercel Environment Variable Setup - CRITICAL STEP

## ⚠️ THIS STEP IS REQUIRED FOR LOGIN TO WORK

The frontend needs to know the backend URL. Without this environment variable, the frontend will try to connect to `localhost:5000` and fail.

## Step-by-Step Instructions

### 1. Go to Vercel Dashboard
- URL: https://vercel.com/dashboard
- Log in with your GitHub account

### 2. Select Your Project
- Click on: `student-performance-system`

### 3. Go to Settings
- Click the **Settings** tab at the top
- (NOT "Deployment Settings" - just "Settings")

### 4. Find Environment Variables
- In the left sidebar, click **Environment Variables**
- You should see a section to add new variables

### 5. Add the Backend URL Variable

Click **Add New** and fill in:

| Field | Value |
|-------|-------|
| **Name** | `VITE_API_URL` |
| **Value** | `https://student-performance-backend-rsga.onrender.com` |
| **Environments** | ✓ Production ✓ Preview ✓ Development |

Then click **Save**

### 6. Redeploy the Frontend

After saving the environment variable:

1. Go to **Deployments** tab
2. Find the latest deployment (should be at the top)
3. Click the **three dots (...)** on the right
4. Click **Redeploy**
5. Wait for it to complete (status changes to "Ready")

This takes about 1-2 minutes.

## Verification

After redeployment:

1. Go to: https://student-performance-system-kohl.vercel.app
2. Open browser console (F12 → Console tab)
3. You should see **NO errors**
4. Try logging in:
   - Email: `admin@school.edu`
   - Password: `Admin@123`

## What This Does

- Tells the frontend where the backend API is located
- Without this, frontend can't communicate with backend
- This is why you were seeing "Network error" messages

## If You Don't See Environment Variables Section

Try this:
1. Go to: https://vercel.com/dashboard
2. Click your project name
3. Click **Settings** (top menu)
4. Scroll down to find **Environment Variables**

## Troubleshooting

**Q: I set the variable but login still fails?**
A: Make sure you clicked "Redeploy" after setting the variable. The frontend needs to be rebuilt with the new variable.

**Q: How do I know if the variable is set?**
A: Go to Settings → Environment Variables. You should see `VITE_API_URL` listed there.

**Q: The deployment is still showing "Building"?**
A: Wait 2-3 minutes. Vercel deployments take time.

---

**This is the final critical step to make everything work!**

