# Comprehensive 500-Student Database Seed

## Overview

This seed script creates a production-ready, full-scale school management system with:

- **1,016 Total Users**
- **100,000+ Records**
- **10 Sections** (Classes 6A, 6B, 7A, 7B, 8A, 8B, 9A, 9B, 10A, 10B)
- **50 Students per section** (28 boys + 22 girls)

## Database Structure

### Users (1,016 total)

1. **1 Admin**
   - Email: `admin@school.edu`
   - Password: `Admin@123`

2. **15 Teachers** (covering all 11 subjects)
   - Science: 2 teachers
   - Mathematics: 2 teachers
   - History: 1 teacher
   - Social Science: 2 teachers
   - Geography: 1 teacher
   - Hindi: 1 teacher
   - English: 2 teachers
   - Sports: 1 teacher (Male, age 31-35)
   - Music: 1 teacher
   - Additional Language: 1 teacher
   - Arts/Drawing: 1 teacher
   - Email format: `[firstname].[lastname]@school.com`
   - Password: `Teacher@123`

3. **500 Students** (10 sections × 50 students)
   - Each section: 28 boys + 22 girls
   - Email format: `[firstname].[lastname][number]@gmail.com`
   - Password: `Student@123`
   - Performance distribution:
     * High performers: 150 (30%)
     * Average performers: 250 (50%)
     * At-risk students: 100 (20%)

4. **500 Parents** (1:1 relationship with students)
   - Email format: `parent.[lastname][number]@gmail.com`
   - Password: `Parent@123`

### Records (100,000+ total)

| Record Type | Count | Description |
|------------|-------|-------------|
| Attendance | ~65,000 | 500 students × 130 school days |
| Marks | 33,000 | 500 students × 6 exams × 11 subjects |
| Assignments | ~3,750 | 500 students × 7-8 assignments |
| Alerts | ~1,050 | Based on performance category |
| Achievements | ~1,125 | High performers get 3-6 each |
| Predictions | 500 | 1 per student (ML predictions) |
| Career Suggestions | ~2,000 | 500 students × 3-5 suggestions |
| Recommendations | ~1,700 | Personalized learning resources |
| Resources | 66 | 11 subjects × 6 resources |

## Usage

### Local Testing

```bash
cd backend
python utils/seed_database_500.py
```

This will:
1. Drop all existing tables
2. Create fresh database schema
3. Populate with 1,016 users and 100,000+ records
4. Takes approximately 3-5 minutes

### Railway Deployment

1. **Push to GitHub:**
```bash
git add .
git commit -m "Add comprehensive 500-student database seed"
git push origin main
```

2. **Force Reseed on Railway:**
   - Go to Railway Dashboard
   - Select your backend service
   - Variables → Add:
     ```
     FORCE_RESEED=true
     ```
   - Wait for redeployment (3-5 minutes)
   - **IMPORTANT:** Remove `FORCE_RESEED` variable after successful seed

3. **Verify Deployment:**
   - Visit: `https://your-railway-url.railway.app/api/auth/debug/quick-test-logins`
   - Should return credentials for all 4 user types

## Performance Distribution

### High Performers (150 students - 30%)
- Attendance: 95-100%
- Average Marks: 85-100%
- Risk Level: Low
- Predicted Grade: A+, A
- Achievements: 3-6 per student
- Alerts: 0-2 (informational)

### Average Performers (250 students - 50%)
- Attendance: 75-90%
- Average Marks: 65-85%
- Risk Level: Low/Medium
- Predicted Grade: B+, B, C+
- Achievements: 1-3 per student
- Alerts: 1-3 (warnings)

### At-Risk Students (100 students - 20%)
- Attendance: 30-65%
- Average Marks: 35-65%
- Risk Level: Medium/High
- Predicted Grade: C, D, F
- Achievements: 0
- Alerts: 4-7 (critical/warnings)

## Class Structure

Each section has exactly 50 students:

| Class | Section | Students | Boys | Girls |
|-------|---------|----------|------|-------|
| 6 | A | 50 | 28 | 22 |
| 6 | B | 50 | 28 | 22 |
| 7 | A | 50 | 28 | 22 |
| 7 | B | 50 | 28 | 22 |
| 8 | A | 50 | 28 | 22 |
| 8 | B | 50 | 28 | 22 |
| 9 | A | 50 | 28 | 22 |
| 9 | B | 50 | 28 | 22 |
| 10 | A | 50 | 28 | 22 |
| 10 | B | 50 | 28 | 22 |
| **Total** | | **500** | **280** | **220** |

## Subjects (11 total)

1. Science
2. Mathematics
3. History
4. Social Science
5. Geography
6. Hindi
7. English
8. Sports
9. Music
10. Additional Language
11. Arts/Drawing

## Exam Types (6 per subject)

1. Unit Test 1 (30 marks)
2. Unit Test 2 (30 marks)
3. Midterm (50 marks)
4. Unit Test 3 (30 marks)
5. Unit Test 4 (30 marks)
6. Final Exam (100 marks)

## Expected Database Size

- **SQLite:** ~150-200 MB
- **PostgreSQL:** ~100-150 MB (better compression)
- **Memory Usage:** ~500 MB during seeding
- **Seeding Time:** 3-5 minutes

## Troubleshooting

### Seed Takes Too Long
- The script uses batch commits (every 1000 records)
- Progress indicators show dots (.) during processing
- If it takes more than 10 minutes, check database connection

### Out of Memory
- Railway provides 8GB RAM (should be sufficient)
- If issues persist, reduce `STUDENTS_PER_SECTION` from 50 to 25

### Database Already Populated
- Set `FORCE_RESEED=true` environment variable
- Or manually run: `python utils/seed_database_500.py`

## Comparison with Original Seed

| Metric | Original | New (500 Students) |
|--------|----------|-------------------|
| Total Users | 132 | 1,016 |
| Students | 60 | 500 |
| Parents | 60 | 500 |
| Teachers | 11 | 15 |
| Classes | 3 | 10 |
| Attendance Records | ~7,800 | ~65,000 |
| Marks Records | ~3,960 | 33,000 |
| Total Records | ~13,000 | ~107,000 |
| Database Size | ~20 MB | ~150 MB |

## Notes

- All passwords are simple for testing purposes
- Parent-child relationships use matching last names
- Performance categories are randomly distributed
- Attendance follows realistic patterns (weekdays only)
- Marks include natural variation within performance bands
- Career suggestions match student strengths
- ML predictions align with performance categories

---

**Last Updated:** March 21, 2026
**Status:** Production Ready ✅
