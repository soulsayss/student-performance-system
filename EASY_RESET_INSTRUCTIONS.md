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
- Total users: 132 (1 admin + 11 teachers + 60 students + 60 parents)
- New credentials listed

### Step 5: Test Teacher Dashboard
1. Go to your frontend URL
2. Login with: `rajesh.kumar@school.com` / `Teacher@123`
3. You should see:
   - Total Students: **20** (Class 8A only)
   - Badge: "Class Teacher: 8A"
   - 20 students in the table
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
   - 11 Teachers (3 class teachers + 8 subject teachers)
   - 60 Students (3 classes: 8A, 9A, 10A - 20 students each)
   - 60 Parents (1 per student)
   - ~12,000+ records (attendance, marks, assignments, etc.)

---

## After Reset - New Credentials

### Admin
- Email: `admin@school.edu`
- Password: `Admin@123`

### Class Teachers (3 total - see only their 20 assigned students)
1. **Dr. Rajesh Kumar** (Class 8A - Science)
   - Email: `rajesh.kumar@school.com`
   - Password: `Teacher@123`

2. **Prof. Priya Sharma** (Class 9A - Mathematics)
   - Email: `priya.sharma@school.com`
   - Password: `Teacher@123`

3. **Mr. Rohit Verma** (Class 10A - Sports)
   - Email: `rohit.verma@school.com`
   - Password: `Teacher@123`

### Subject Teachers (8 total - see all 60 students)
- `amit.patel@school.com` (History)
- `sneha.gupta@school.com` (Social Science)
- `vikram.singh@school.com` (Geography)
- `kavita.reddy@school.com` (Hindi)
- `arjun.nair@school.com` (English)
- `anjali.mehta@school.com` (Music)
- `meera.iyer@school.com` (Additional Language)
- `zara.khan@school.com` (Arts/Drawing)
- All passwords: `Teacher@123`

### Students & Parents (60 pairs)
- Format: `firstname.lastname@gmail.com`
- Parent and student share the same last name
- See `LOGIN_CREDENTIALS.md` for complete list
- All passwords: `Student@123` / `Parent@123`

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

### Reset Succeeds but Teacher Dashboard Shows Wrong Student Count
- Clear browser cache (Ctrl+Shift+Delete)
- Hard refresh (Ctrl+Shift+R)
- Try in incognito/private window
- Class teachers should see 20 students
- Subject teachers should see 60 students

---

## Expected Results After Reset

✅ **Total Users**: 132 (1 admin + 11 teachers + 60 students + 60 parents)
✅ **Class Teachers**: See 20 students (their assigned class only)
✅ **Subject Teachers**: See 60 students (all classes)
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
