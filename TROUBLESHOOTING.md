# 🔧 Troubleshooting Guide - Teacher Dashboard CORS Issues

## 📋 Problem Summary

**Issue**: Teacher dashboard login fails with CORS errors and breaks all other dashboards until browser cache is cleared.

**Symptoms**:
- ✅ Parent dashboard works after cache clear
- ✅ Student/Admin dashboards work after parent loads
- ❌ Teacher dashboard always fails with CORS errors
- ❌ When teacher login fails, all subsequent logins fail
- ❌ Requires hard cache delete to reset

**Pattern Identified**:
1. Teacher dashboard makes 3 API calls on load:
   - `/api/teacher/dashboard` - ✅ Works (shows data)
   - `/api/teacher/students` - ❌ Fails with CORS
   - `/api/teacher/at-risk-students` - ❌ Fails with CORS

2. These failures corrupt backend state or CORS headers
3. All subsequent API calls fail until cache is cleared

---

## 🎯 Step-by-Step Local Testing Guide

### Step 1: Setup Local Environment

#### 1.1 Backend Setup
```bash
# Navigate to backend directory
cd student-academic-system/backend

# Create virtual environment (if not exists)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create local .env file
# Copy from .env.example and set:
DATABASE_URL=sqlite:///instance/student_academic.db
SECRET_KEY=your-local-secret-key
JWT_SECRET_KEY=your-local-jwt-secret
```

#### 1.2 Initialize Local Database
```bash
# Run database initialization
python init_db.py

# Seed the database
python utils/seed_database.py
```

#### 1.3 Start Backend Server
```bash
# Start Flask development server
python app.py

# Backend should start on http://localhost:5000
# You should see:
# * Running on http://127.0.0.1:5000
```

#### 1.4 Frontend Setup (New Terminal)
```bash
# Navigate to frontend directory
cd student-academic-system/frontend

# Install dependencies (if not done)
npm install

# Create .env file
# Copy from .env.example and set:
VITE_API_URL=http://localhost:5000

# Start frontend development server
npm run dev

# Frontend should start on http://localhost:5173
```

---

### Step 2: Test Each Dashboard Individually

#### 2.1 Test Parent Dashboard (Baseline - Known Working)
```bash
# Open browser: http://localhost:5173/login
# Login with: parent1@email.com / Parent@123
# Expected: Dashboard loads successfully
# Check browser console for any errors
```

**✅ Success Criteria**:
- No CORS errors in console
- Dashboard shows attendance, marks, risk level
- All data loads properly

#### 2.2 Test Student Dashboard
```bash
# Logout from parent
# Login with: student1@school.com / Student@123
# Expected: Dashboard loads successfully
```

**✅ Success Criteria**:
- No CORS errors
- Shows marks, attendance, predictions
- All charts render

#### 2.3 Test Admin Dashboard
```bash
# Logout from student
# Login with: admin@school.edu / Admin@123
# Expected: Dashboard loads successfully
```

**✅ Success Criteria**:
- No CORS errors
- Shows total users, students, resources
- Admin controls visible

#### 2.4 Test Teacher Dashboard (Problem Area)
```bash
# Logout from admin
# Login with: rajesh.kumar@school.com / Teacher@123
# Expected: May fail with CORS errors
```

**🔍 What to Check**:
1. Open browser DevTools (F12)
2. Go to Network tab
3. Watch for these requests:
   - `/api/auth/login` - Should succeed (200)
   - `/api/teacher/dashboard` - Check status
   - `/api/teacher/students` - Check status
   - `/api/teacher/at-risk-students` - Check status

4. Check Console tab for errors
5. Check backend terminal for error logs

---

### Step 3: Debug Teacher Endpoints

#### 3.1 Test Endpoints Directly with curl/Postman

**First, get a valid JWT token**:
```bash
# Login to get token
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"rajesh.kumar@school.com","password":"Teacher@123"}'

# Copy the "access_token" from response
```

**Test each teacher endpoint**:
```bash
# Replace YOUR_TOKEN with actual token

# Test dashboard endpoint
curl -X GET http://localhost:5000/api/teacher/dashboard \
  -H "Authorization: Bearer YOUR_TOKEN"

# Test students endpoint
curl -X GET http://localhost:5000/api/teacher/students \
  -H "Authorization: Bearer YOUR_TOKEN"

# Test at-risk students endpoint
curl -X GET http://localhost:5000/api/teacher/at-risk-students \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**🔍 What to Look For**:
- Status codes (200 = success, 500 = server error, 401 = auth error)
- Error messages in response
- Backend terminal logs showing errors

#### 3.2 Check Backend Logs

When testing teacher dashboard, watch the backend terminal for:
- Python exceptions/tracebacks
- Database query errors
- SQLAlchemy warnings
- Any error messages

**Common Issues to Look For**:
```
❌ AttributeError: 'NoneType' object has no attribute 'X'
❌ KeyError: 'X'
❌ SQLAlchemy relationship errors
❌ Database query timeouts
❌ Memory errors
```

---

### Step 4: Specific Checks for Teacher Routes

#### 4.1 Verify Teacher User Exists
```bash
# In Python shell
python

>>> from app import create_app
>>> from models import User, Teacher
>>> app = create_app()
>>> with app.app_context():
...     teacher_user = User.query.filter_by(email='rajesh.kumar@school.com').first()
...     print(f"User found: {teacher_user}")
...     print(f"Has teacher_profile: {teacher_user.teacher_profile if teacher_user else 'N/A'}")
...     if teacher_user and teacher_user.teacher_profile:
...         print(f"Teacher ID: {teacher_user.teacher_profile.teacher_id}")
...         print(f"Subject: {teacher_user.teacher_profile.subject}")
```

**✅ Expected Output**:
```
User found: <User 'Dr. Rajesh Kumar'>
Has teacher_profile: <Teacher object>
Teacher ID: 1
Subject: Science
```

#### 4.2 Test Database Queries
```python
# Still in Python shell
>>> from models import Student
>>> with app.app_context():
...     students = Student.query.all()
...     print(f"Total students: {len(students)}")
...     if students:
...         s = students[0]
...         print(f"Sample student: {s.user.name}")
...         print(f"Has marks: {len(s.marks)}")
...         print(f"Has attendance: {len(s.attendance_records)}")
```

**✅ Expected Output**:
```
Total students: 75
Sample student: [Student Name]
Has marks: 66
Has attendance: 129
```

---

### Step 5: Fix Common Issues

#### Issue 1: Teacher Profile Not Found

**Symptom**: `teacher_profile` is None

**Fix**: Check User model relationships
```python
# In backend/models/user.py
# Ensure this line exists:
teacher_profile = db.relationship('Teacher', backref='user', uselist=False)
```

#### Issue 2: Relationship Attribute Errors

**Symptom**: `AttributeError: 'Student' object has no attribute 'marks_records'`

**Fix**: Use correct relationship name
```python
# In backend/routes/teacher.py
# WRONG:
student.marks_records

# CORRECT:
student.marks
```

#### Issue 3: Eager Loading Missing

**Symptom**: N+1 query problem, slow performance

**Fix**: Add eager loading
```python
# In backend/routes/teacher.py
from sqlalchemy.orm import joinedload

students = Student.query.options(
    joinedload(Student.user),
    joinedload(Student.marks),
    joinedload(Student.attendance_records)
).all()
```

#### Issue 4: CORS Headers Not Set

**Symptom**: CORS errors in browser

**Fix**: Verify CORS configuration in app.py
```python
# In backend/app.py
CORS(app, 
     resources={
         r"/*": {  # Apply to ALL routes
             "origins": [
                 "http://localhost:3000",
                 "http://localhost:5173",
                 "https://student-performance-system-kohl.vercel.app"
             ],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "supports_credentials": True
         }
     }
)
```

---

### Step 6: Test Fixes Locally

After making any fixes:

1. **Restart Backend**:
```bash
# Stop backend (Ctrl+C)
# Start again
python app.py
```

2. **Clear Browser Cache**:
   - Open DevTools (F12)
   - Right-click refresh button
   - Select "Empty Cache and Hard Reload"

3. **Test Teacher Login Again**:
   - Login with: rajesh.kumar@school.com / Teacher@123
   - Check console for errors
   - Verify all 3 API calls succeed

4. **Test Other Dashboards**:
   - Ensure teacher dashboard fix didn't break others
   - Test parent, student, admin in sequence

---

### Step 7: Verify Fix Works

**✅ Success Criteria**:
- [ ] Teacher dashboard loads without CORS errors
- [ ] All 3 API calls succeed (dashboard, students, at-risk)
- [ ] Dashboard shows: 75 students, attendance, at-risk count, class average
- [ ] Other dashboards still work after teacher login
- [ ] No errors in browser console
- [ ] No errors in backend terminal

---

### Step 8: Deploy to Production

Only after local testing succeeds:

```bash
# Commit changes
git add .
git commit -m "Fix teacher dashboard CORS and API issues"

# Push to GitHub
git push origin main

# Render will auto-deploy backend
# Vercel will auto-deploy frontend

# Wait 2-3 minutes for deployment
# Test on production URLs
```

---

## 🐛 Common Error Messages and Solutions

### Error 1: "Access-Control-Allow-Origin header is present"
**Cause**: CORS not configured properly
**Solution**: Check Step 5, Issue 4

### Error 2: "Teacher profile not found"
**Cause**: User doesn't have teacher_profile relationship
**Solution**: Check Step 5, Issue 1

### Error 3: "AttributeError: 'Student' object has no attribute 'X'"
**Cause**: Wrong relationship name used
**Solution**: Check Step 5, Issue 2

### Error 4: "Network Error" / "ERR_FAILED"
**Cause**: Backend crashed or not responding
**Solution**: Check backend terminal for Python errors

### Error 5: Slow loading / Timeout
**Cause**: N+1 query problem
**Solution**: Check Step 5, Issue 3

---

## 📝 Debugging Checklist

Before asking for help, verify:

- [ ] Backend is running on http://localhost:5000
- [ ] Frontend is running on http://localhost:5173
- [ ] Database is seeded with 75 students, 10 teachers
- [ ] Teacher user exists: rajesh.kumar@school.com
- [ ] Teacher has teacher_profile relationship
- [ ] CORS is configured for localhost:5173
- [ ] Browser cache is cleared
- [ ] DevTools Network tab shows actual error codes
- [ ] Backend terminal shows error logs
- [ ] Tested with curl/Postman to isolate frontend vs backend

---

## 🔍 Advanced Debugging

### Enable Flask Debug Mode
```python
# In backend/app.py
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### Add Logging to Teacher Routes
```python
# In backend/routes/teacher.py
import logging
logging.basicConfig(level=logging.DEBUG)

@teacher_bp.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    logging.debug("=== GET /students called ===")
    try:
        user = get_current_teacher()
        logging.debug(f"User: {user}")
        logging.debug(f"Teacher profile: {user.teacher_profile if user else None}")
        # ... rest of code
```

### Check Database State
```bash
# Open SQLite database
sqlite3 backend/instance/student_academic.db

# Check teachers
SELECT u.email, u.name, t.teacher_id, t.subject 
FROM users u 
LEFT JOIN teachers t ON u.user_id = t.user_id 
WHERE u.role = 'teacher';

# Check students count
SELECT COUNT(*) FROM students;

# Exit
.exit
```

---

## 📞 Next Steps

1. Follow this guide step by step
2. Document any errors you encounter
3. Note which step fails
4. Share backend terminal output
5. Share browser console errors
6. We'll fix the specific issue together

---

**Last Updated**: March 18, 2026
**Status**: Ready for local testing
