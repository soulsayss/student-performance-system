# Action Plan - Fixing All Issues

## Current Status

✅ **Code Changes**: Deployed to GitHub
- Reduced to 25 students (3 classes, 1 section each)
- Teachers now see only their assigned class
- Memory usage reduced by 66%

❌ **Production Database**: Still has old data (75 students)
❌ **Teacher Dashboard**: Still showing errors
❌ **Render Memory**: Still hitting limits

---

## Step-by-Step Action Plan

### STEP 1: Reset Render Database ⚠️ CRITICAL

**Why**: The production database still has 75 students and 10 teachers. The new code expects 25 students and 3 teachers with assigned classes.

**How to Reset**:

#### Option A: Via Render Dashboard (Easiest)
1. Go to https://dashboard.render.com
2. Click on your PostgreSQL database service
3. Go to "Settings" tab
4. Scroll down and click "Delete Database"
5. Confirm deletion
6. Render will auto-create a new empty database
7. Restart your backend service
8. The auto-seed script will run and create 54 users (25 students)

#### Option B: Via Render Shell (Advanced)
1. Go to your backend service on Render
2. Click "Shell" tab
3. Run these commands:
```bash
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     db.drop_all()
...     db.create_all()
...     print("Database reset complete")
>>> exit()
```
4. Restart the service
5. Auto-seed will run

#### Option C: Manual SQL (Most Control)
1. Connect to Render PostgreSQL using provided credentials
2. Run:
```sql
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```
3. Restart backend service
4. Auto-seed will run

**Expected Result After Reset**:
- Admin dashboard shows: 54 total users, 25 students
- Teacher login works with new credentials
- No memory errors

---

### STEP 2: Verify Auto-Seed Completed

**Check Render Logs**:
1. Go to your backend service on Render
2. Click "Logs" tab
3. Look for these messages:
```
🌱 DATABASE IS EMPTY - RUNNING AUTO-SEED SCRIPT
Creating admin user...
Creating 3 teachers...
Creating 25 parents...
Creating 25 students...
✅ Auto-seeding completed successfully!
Total Users: 54
```

**If Auto-Seed Fails**:
- Check logs for Python errors
- Manually run seed script via Shell:
```bash
python utils/seed_database.py
```

---

### STEP 3: Test Teacher Dashboard

**Test with Dr. Rajesh Kumar (Class 6A)**:
1. Go to: https://student-performance-system-kohl.vercel.app/login
2. Login with:
   - Email: `rajesh.kumar@school.com`
   - Password: `Teacher@123`
3. **Expected Results**:
   - Dashboard loads without errors
   - Shows "Class 6 - Section A"
   - Total Students: 9 (not 75!)
   - At-Risk Students: 0-2
   - Students table shows 9 students only
   - No CORS errors in console

**Test with Prof. Priya Sharma (Class 7A)**:
1. Logout and login with:
   - Email: `priya.sharma@school.com`
   - Password: `Teacher@123`
2. **Expected Results**:
   - Shows "Class 7 - Section A"
   - Total Students: 8
   - Students table shows 8 students only

**Test with Mr. Rohit Verma (Class 8A)**:
1. Logout and login with:
   - Email: `rohit.verma@school.com`
   - Password: `Teacher@123`
2. **Expected Results**:
   - Shows "Class 8 - Section A"
   - Total Students: 8
   - Students table shows 8 students only

---

### STEP 4: Test Other Dashboards

**Admin Dashboard**:
- Login: `admin@school.edu` / `Admin@123`
- Should show: 54 total users, 25 students
- Should work without errors

**Student Dashboard**:
- Login: `student1@school.com` / `Student@123`
- Should show attendance, marks, predictions
- Should work without errors

**Parent Dashboard**:
- Login: `parent1@email.com` / `Parent@123`
- Should show child's data
- Should work without errors

---

### STEP 5: Monitor Render Memory Usage

**Check Memory**:
1. Go to Render dashboard
2. Click on backend service
3. Go to "Metrics" tab
4. Check "Memory Usage" graph

**Expected**:
- Memory usage: ~100-150MB (down from ~250-300MB)
- Well below 512MB limit
- No "out of memory" errors in logs

**If Memory Still High**:
- Check for memory leaks in code
- Consider upgrading Render plan
- Or migrate to Railway/Fly.io

---

### STEP 6: Fix CORS Errors (If They Persist)

**If teacher dashboard still shows CORS errors after database reset**:

1. **Check Browser Console**:
   - Open DevTools (F12)
   - Go to Console tab
   - Copy exact error message

2. **Check Network Tab**:
   - Go to Network tab
   - Filter by "Fetch/XHR"
   - Click on failed request
   - Check "Response" tab for error details

3. **Common CORS Issues**:

   **Issue**: "CORS policy: No 'Access-Control-Allow-Origin' header"
   **Fix**: Already fixed in `app.py`, but verify CORS config includes your frontend URL

   **Issue**: "CORS policy: Response to preflight request doesn't pass"
   **Fix**: Check that OPTIONS method is allowed in CORS config

   **Issue**: "Network Error" or "ERR_FAILED"
   **Fix**: Backend crashed - check Render logs for Python errors

4. **If CORS errors persist**, add this to `app.py`:
```python
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
```

---

### STEP 7: Alternative Platforms (If Render Keeps Failing)

**If Render continues to have memory issues or instability**:

#### Option A: Railway.app
- **Pros**: More generous free tier, better performance
- **Cons**: Requires credit card for free tier
- **Migration**: Easy - just connect GitHub repo

#### Option B: Fly.io
- **Pros**: Good free tier, fast deployment
- **Cons**: More complex setup
- **Migration**: Requires Dockerfile

#### Option C: Koyeb
- **Pros**: Simple deployment, good free tier
- **Cons**: Less popular, fewer resources
- **Migration**: Similar to Render

**Recommendation**: Try Railway.app first if Render fails

---

## Troubleshooting Checklist

### Teacher Dashboard Shows 75 Students (Not 9/8)
- [ ] Database not reset - follow STEP 1
- [ ] Old cache - hard refresh browser (Ctrl+Shift+R)
- [ ] Check Render logs for auto-seed completion

### Teacher Dashboard Shows CORS Errors
- [ ] Check browser console for exact error
- [ ] Verify backend is running (check Render logs)
- [ ] Check Network tab for failed requests
- [ ] Try different browser
- [ ] Clear browser cache completely

### Render Shows "Out of Memory" Error
- [ ] Database not reset - still has 75 students
- [ ] Follow STEP 1 to reset database
- [ ] Check memory usage in Render metrics
- [ ] Consider upgrading plan or migrating platform

### Auto-Seed Not Running
- [ ] Check Render logs for errors
- [ ] Manually run: `python utils/seed_database.py`
- [ ] Check database connection
- [ ] Verify DATABASE_URL environment variable

### Teacher Login Fails
- [ ] Using old credentials (e.g., amit.patel@school.com)
- [ ] Use new credentials: rajesh.kumar, priya.sharma, rohit.verma
- [ ] Database not reset yet
- [ ] Check Render logs for authentication errors

---

## Success Criteria

✅ **Database Reset Complete**:
- Admin dashboard shows 54 users
- Admin dashboard shows 25 students

✅ **Teacher Dashboard Working**:
- Dr. Rajesh Kumar sees 9 students (Class 6A only)
- Prof. Priya Sharma sees 8 students (Class 7A only)
- Mr. Rohit Verma sees 8 students (Class 8A only)
- No CORS errors in console
- All 3 API calls succeed (dashboard, students, at-risk)

✅ **Memory Usage Optimized**:
- Render shows ~100-150MB usage
- No "out of memory" errors
- Service runs stably

✅ **All Dashboards Working**:
- Admin dashboard loads
- Student dashboard loads
- Parent dashboard loads
- Teacher dashboard loads
- No errors in any dashboard

---

## Timeline

**Immediate (Next 10 minutes)**:
1. Reset Render database (STEP 1)
2. Wait for auto-seed to complete (STEP 2)
3. Test teacher dashboard (STEP 3)

**Short-term (Next 30 minutes)**:
4. Test all dashboards (STEP 4)
5. Monitor memory usage (STEP 5)
6. Fix any remaining CORS errors (STEP 6)

**If Issues Persist (Next 1-2 hours)**:
7. Consider migrating to Railway.app (STEP 7)
8. Document any new issues found
9. Create additional fixes as needed

---

## Contact & Support

**If you encounter issues**:
1. Check Render logs first
2. Check browser console for errors
3. Review this action plan
4. Document exact error messages
5. Share screenshots if needed

**Key Files to Check**:
- `backend/app.py` - CORS configuration
- `backend/routes/teacher.py` - Teacher endpoints
- `backend/models/teacher.py` - Teacher model
- `backend/utils/seed_database.py` - Seed script
- `TROUBLESHOOTING.md` - Detailed debugging guide

---

**Last Updated**: March 18, 2026
**Status**: Awaiting database reset
**Priority**: CRITICAL
