# Easy Database Reset Instructions (No Shell Required!)

## Problem
Render's free tier doesn't have shell access or separate database service, so we can't reset the database the traditional way.

## Solution
I've created a special admin endpoint and a simple HTML tool to reset the database remotely!

---

## Step-by-Step Instructions

### Step 1: Wait for Deployment (2-3 minutes)
The new code with the reset endpoint is deploying to Render right now. Wait for:
1. Go to https://dashboard.render.com
2. Click on your backend service
3. Wait for "Deploy succeeded" message

### Step 2: Open the Reset Tool
1. Open this file in your browser: `reset-database.html`
2. Or double-click it from your file explorer

### Step 3: Reset the Database
1. The form should already have:
   - Backend URL: `https://student-performance-backend-rsga.onrender.com`
   - Secret Key: `RESET_DB_2026_SECURE`
2. Click the **"Reset Database Now"** button
3. Confirm the warning dialog
4. Wait 30-60 seconds for the reset to complete

### Step 4: Verify Success
You should see a success message with:
- ✅ Database reset and reseeded successfully
- Total users: 54
- New credentials listed

### Step 5: Test Teacher Dashboard
1. Go to: https://student-performance-system-kohl.vercel.app/login
2. Login with: `rajesh.kumar@school.com` / `Teacher@123`
3. You should see:
   - Total Students: **9** (not 75!)
   - Class 6 - Section A
   - 9 students in the table
   - No CORS errors

---

## Alternative Method (Using Browser Console)

If the HTML tool doesn't work, you can use your browser console:

1. Go to: https://student-performance-backend-rsga.onrender.com
2. Open browser DevTools (F12)
3. Go to Console tab
4. Paste this code:

```javascript
fetch('https://student-performance-backend-rsga.onrender.com/api/admin/reset-database', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-Reset-Secret': 'RESET_DB_2026_SECURE'
    }
})
.then(res => res.json())
.then(data => console.log('Success:', data))
.catch(err => console.error('Error:', err));
```

5. Press Enter
6. Wait for response in console

---

## Alternative Method (Using Postman/Thunder Client)

If you have Postman or Thunder Client:

1. Create a new POST request
2. URL: `https://student-performance-backend-rsga.onrender.com/api/admin/reset-database`
3. Headers:
   - `Content-Type`: `application/json`
   - `X-Reset-Secret`: `RESET_DB_2026_SECURE`
4. Send the request
5. Wait for response

---

## Alternative Method (Using curl)

If you have curl installed:

```bash
curl -X POST https://student-performance-backend-rsga.onrender.com/api/admin/reset-database \
  -H "Content-Type: application/json" \
  -H "X-Reset-Secret: RESET_DB_2026_SECURE"
```

---

## What Happens During Reset

1. **Drops all tables** - Deletes all existing data
2. **Creates fresh tables** - Recreates database structure
3. **Seeds new data**:
   - 1 Admin
   - 3 Teachers (with class assignments)
   - 25 Students (3 classes, 1 section each)
   - 25 Parents
   - ~5,500 records (attendance, marks, etc.)

---

## After Reset - New Credentials

### Admin
- Email: `admin@school.edu`
- Password: `Admin@123`

### Teachers (3 total)
1. **Dr. Rajesh Kumar** (Class 6A - 9 students)
   - Email: `rajesh.kumar@school.com`
   - Password: `Teacher@123`

2. **Prof. Priya Sharma** (Class 7A - 8 students)
   - Email: `priya.sharma@school.com`
   - Password: `Teacher@123`

3. **Mr. Rohit Verma** (Class 8A - 8 students)
   - Email: `rohit.verma@school.com`
   - Password: `Teacher@123`

### Students (25 total)
- Emails: `student1@school.com` to `student25@school.com`
- Password: `Student@123`

### Parents (25 total)
- Emails: `parent1@email.com` to `parent25@email.com`
- Password: `Parent@123`

---

## Troubleshooting

### Error: "Unauthorized"
- Check that secret key is exactly: `RESET_DB_2026_SECURE`
- Case-sensitive!

### Error: "Failed to fetch" or "Network Error"
- Backend might still be deploying
- Wait 2-3 minutes and try again
- Check Render dashboard for deployment status

### Error: "Failed to reset database"
- Check Render logs for Python errors
- Backend might be out of memory
- Try again in a few minutes

### Reset Succeeds but Teacher Dashboard Still Shows 75 Students
- Clear browser cache (Ctrl+Shift+Delete)
- Hard refresh (Ctrl+Shift+R)
- Try in incognito/private window

---

## Expected Results After Reset

✅ **Memory Usage**: ~100-150MB (down from ~250-300MB)
✅ **Teacher Dashboard**: Shows 8-9 students (not 75)
✅ **No CORS Errors**: All API calls succeed
✅ **All Dashboards Work**: Admin, Student, Parent, Teacher

---

## If Reset Fails Multiple Times

Consider migrating to a different platform:
- **Railway.app** - More generous free tier
- **Fly.io** - Good performance
- **Koyeb** - Simple deployment

I can help you migrate if needed!

---

**Last Updated**: March 18, 2026
**Status**: Ready to use after deployment completes
