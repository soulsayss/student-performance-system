# Deploy 500-Student Database to Railway

## Quick Deployment Steps

### Step 1: Railway Will Auto-Deploy (2-3 minutes)

Railway automatically detects the GitHub push and will start deploying. You can monitor progress at:
```
https://railway.app/dashboard
```

### Step 2: Force Reseed the Database

Once deployment completes, you need to trigger the new seed script:

1. Go to Railway Dashboard
2. Click on your backend service
3. Go to **Variables** tab
4. Click **+ New Variable**
5. Add:
   ```
   Variable: FORCE_RESEED
   Value: true
   ```
6. Click **Add**
7. Railway will automatically redeploy (wait 3-5 minutes)

### Step 3: Monitor Seeding Progress

1. Go to **Deployments** tab
2. Click on the latest deployment
3. Click **View Logs**
4. You should see:
   ```
   COMPREHENSIVE SCHOOL DATABASE POPULATION
   1,016 USERS & 100,000+ RECORDS
   ============================================================
   PHASE 1: CREATING 1,016 USERS
   Creating admin user...
   ✅ Admin created: admin@school.edu / Admin@123
   Creating 15 teachers...
   ✅ Created 15 teachers
   Creating 500 students and 500 parents...
   ...
   ```

### Step 4: Verify Completion

Wait for these success messages in logs:
```
✅ Created 500 students and 500 parents
✅ Created 65,000 attendance records
✅ Created 33,000 marks records
✅ Created 3,750 assignments
✅ Created 66 learning resources
✅ Created 1,050 alerts
✅ Created 1,125 achievements
✅ Created 500 ML predictions
✅ Created 2,000 career suggestions
✅ Created 1,700 recommendations

DATABASE POPULATION COMPLETE!
✅ Database successfully populated with 1,016 users and 107,000+ records!
```

### Step 5: Remove FORCE_RESEED Variable

**CRITICAL:** After successful seeding, remove the variable to prevent data loss on future deployments:

1. Go back to **Variables** tab
2. Find `FORCE_RESEED`
3. Click the **X** to delete it
4. Confirm deletion

### Step 6: Test the Deployment

Visit your debug endpoint to get test credentials:
```
https://your-railway-url.railway.app/api/auth/debug/quick-test-logins
```

Expected response:
```json
{
  "admin": {
    "email": "admin@school.edu",
    "password": "Admin@123"
  },
  "teacher": {
    "email": "rajesh.kumar@school.com",
    "password": "Teacher@123"
  },
  "student": {
    "email": "[some-student]@gmail.com",
    "password": "Student@123"
  },
  "parent": {
    "email": "parent.[lastname]1@gmail.com",
    "password": "Parent@123"
  }
}
```

### Step 7: Update Vercel Frontend (if needed)

If you changed the Railway URL, update Vercel:

1. Go to Vercel Dashboard
2. Select your frontend project
3. Go to **Settings** → **Environment Variables**
4. Update `VITE_API_URL` to your Railway URL
5. Redeploy frontend

### Step 8: Test on Vercel

1. Visit your Vercel URL
2. Login with credentials from debug endpoint
3. Test all 4 user types:
   - Admin Dashboard
   - Teacher Dashboard
   - Student Dashboard
   - Parent Dashboard

---

## What Changed?

### Database Scale

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Total Users | 132 | 1,016 | +770% |
| Students | 60 | 500 | +733% |
| Classes | 3 | 10 | +233% |
| Attendance Records | ~7,800 | ~65,000 | +733% |
| Marks Records | ~3,960 | 33,000 | +733% |
| Total Records | ~13,000 | ~107,000 | +723% |
| Database Size | ~20 MB | ~150 MB | +650% |

### New Features

1. **10 Sections** instead of 3 (6A, 6B, 7A, 7B, 8A, 8B, 9A, 9B, 10A, 10B)
2. **50 Students per section** (28 boys + 22 girls)
3. **15 Teachers** covering all subjects
4. **Realistic performance distribution**:
   - 150 high performers (30%)
   - 250 average performers (50%)
   - 100 at-risk students (20%)
5. **Optimized seeding** with batch commits

---

## Troubleshooting

### Seeding Takes Too Long (>10 minutes)

Check Railway logs for errors. The script should complete in 3-5 minutes.

### Out of Memory Error

Railway provides 8GB RAM which should be sufficient. If issues persist:
1. Check for memory leaks in logs
2. Consider upgrading Railway plan
3. Or reduce students to 250 (modify `STUDENTS_PER_SECTION` to 25)

### Database Already Populated Error

If you see:
```
✓ Database already populated with 132 users. Skipping seed.
```

Make sure `FORCE_RESEED=true` is set in Railway variables.

### Deployment Fails

1. Check Railway logs for Python errors
2. Verify all dependencies in `requirements.txt`
3. Ensure PostgreSQL database is connected
4. Check `DATABASE_URL` environment variable

### Frontend Can't Connect

1. Verify Railway backend URL is correct
2. Check CORS settings in `backend/app.py`
3. Ensure Vercel has correct `VITE_API_URL`
4. Test backend directly: `https://your-url.railway.app/api/health`

---

## Expected Timeline

| Step | Duration | Status Check |
|------|----------|--------------|
| GitHub Push | Instant | ✅ Pushed |
| Railway Auto-Deploy | 2-3 min | Check Deployments tab |
| Add FORCE_RESEED | Instant | Check Variables tab |
| Railway Redeploy | 2-3 min | Check Deployments tab |
| Database Seeding | 3-5 min | Check Logs |
| Remove FORCE_RESEED | Instant | Check Variables tab |
| Test Endpoints | 1 min | Visit debug endpoint |
| **Total Time** | **8-12 min** | |

---

## Post-Deployment Checklist

- [ ] Railway deployment succeeded
- [ ] FORCE_RESEED variable added
- [ ] Seeding completed (check logs)
- [ ] FORCE_RESEED variable removed
- [ ] Debug endpoint returns credentials
- [ ] Admin login works on Vercel
- [ ] Teacher login works on Vercel
- [ ] Student login works on Vercel
- [ ] Parent login works on Vercel
- [ ] All dashboards load correctly
- [ ] Data displays properly (500 students visible)

---

## Next Steps

After successful deployment:

1. **Update LOGIN_CREDENTIALS.md** with actual Railway credentials from debug endpoint
2. **Test all features** on Vercel with real data
3. **Monitor performance** with 500 students
4. **Share credentials** with team/testers
5. **Document any issues** for future reference

---

**Deployment Date:** March 21, 2026
**Status:** Ready to Deploy ✅
**Estimated Time:** 8-12 minutes
