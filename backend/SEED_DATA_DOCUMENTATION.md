# Database Seeding Documentation

## Overview
Comprehensive database seeding script that generates realistic, interconnected sample data for the Student Academic Performance System.

---

## Usage

### Run the Seed Script
```bash
cd student-academic-system/backend
python utils/seed_database.py
```

**⚠️ Warning:** This script will **DROP ALL EXISTING DATA** and create fresh tables with new sample data.

---

## Generated Data Summary

### 📊 Total Records Created

| Category | Count | Details |
|----------|-------|---------|
| **Users** | 131 | 1 Admin, 10 Teachers, 20 Parents, 100 Students |
| **Attendance** | ~13,000 | 6 months of daily records |
| **Marks** | 3,600 | 6 exams × 6 subjects × 100 students |
| **Assignments** | ~775 | 5-10 per student |
| **Resources** | 51 | Learning materials across all subjects |
| **Alerts** | ~179 | Notifications for students |
| **Achievements** | ~178 | Badges for top performers |
| **Predictions** | 100 | ML predictions for all students |
| **Recommendations** | ~339 | Personalized learning resources |
| **Career Suggestions** | ~390 | 3-5 per student |

**Total Records:** ~18,700+

---

## Student Distribution

### Performance Categories
- **High Performers:** 30 students (30%)
  - Attendance: 95-100%
  - Marks: 85-100%
  - Predicted Grades: A+, A
  - Risk Level: Low

- **Average Performers:** 50 students (50%)
  - Attendance: 75-85%
  - Marks: 65-85%
  - Predicted Grades: B+, B, C+
  - Risk Level: Low

- **At-Risk Students:** 20 students (20%)
  - Attendance: 30-60%
  - Marks: 35-65%
  - Predicted Grades: C, D, F
  - Risk Level: Medium/High

### Demographics
- **Classes:** 9, 10, 11, 12
- **Sections:** A, B, C, D
- **Age Range:** 14-18 years
- **Gender:** Mixed (Male/Female)
- **Parent Assignment:** 90% have assigned parents

---

## Teachers

### 10 Teachers Created

| Name | Subject | Department | Employee ID |
|------|---------|------------|-------------|
| Dr. Rajesh Kumar | Mathematics | Science | TCH001 |
| Prof. Priya Sharma | Physics | Science | TCH002 |
| Dr. Amit Patel | Chemistry | Science | TCH003 |
| Ms. Sneha Gupta | Biology | Science | TCH004 |
| Mr. Vikram Singh | English | Languages | TCH005 |
| Mrs. Kavita Reddy | Hindi | Languages | TCH006 |
| Mr. Arjun Nair | Computer Science | Technology | TCH007 |
| Dr. Meera Iyer | History | Social Studies | TCH008 |
| Prof. Suresh Joshi | Geography | Social Studies | TCH009 |
| Ms. Anjali Mehta | Economics | Commerce | TCH010 |

---

## Attendance Data

### 6 Months of Records
- **Period:** Last 180 days
- **School Days:** Monday to Friday only
- **Total Records:** ~13,000 (130 days × 100 students)

### Status Distribution by Category
- **High Performers:** 95% present, 3% absent, 2% late
- **Average Performers:** 85% present, 10% absent, 5% late
- **At-Risk Students:** 60% present, 30% absent, 10% late

---

## Exam Records

### 6 Exam Types
1. **Unit Test 1** (30 marks) - 150 days ago
2. **Unit Test 2** (30 marks) - 120 days ago
3. **Midterm** (50 marks) - 90 days ago
4. **Unit Test 3** (30 marks) - 60 days ago
5. **Unit Test 4** (30 marks) - 30 days ago
6. **Final Exam** (100 marks) - 10 days ago

### Subjects
- Mathematics
- Physics
- Chemistry
- Biology
- English
- Hindi

**Total:** 6 exams × 6 subjects × 100 students = 3,600 marks records

---

## Assignments

### Assignment Types
- Chapter Summary Essay
- Lab Report
- Research Project
- Problem Set
- Case Study Analysis
- Group Presentation

### Status Distribution
- **High Performers:** 70% graded, 30% submitted
- **Average Performers:** 50% graded, 40% submitted, 10% pending
- **At-Risk Students:** 30% graded, 20% submitted, 50% pending

### Grading
- **High Performers:** 85-100%
- **Average Performers:** 70-85%
- **At-Risk Students:** 50-70%

---

## Learning Resources

### 51 Resources Created

**By Subject:**
- Mathematics: 5 core + 6 additional
- Physics: 5 core + 6 additional
- Chemistry: 5 core + 6 additional
- Biology: 6 resources
- English: 6 resources
- Hindi: 6 resources
- Computer Science: 6 resources
- History: 6 resources
- Geography: 6 resources

**By Type:**
- Videos
- Articles
- PDFs
- Quizzes

**By Difficulty:**
- Beginner
- Intermediate
- Advanced

---

## Alerts

### Alert Distribution

**At-Risk Students (3-6 alerts each):**
- 60% Critical alerts
- 40% Warning alerts

**Average Students (1-3 alerts, 50% chance):**
- 60% Warning alerts
- 40% Info alerts

**High Performers (1-2 alerts, 70% chance):**
- 100% Info alerts (positive feedback)

### Alert Types

**Critical:**
- Attendance below 60%
- Multiple overdue assignments
- Risk of failing
- Poor exam performance

**Warning:**
- Attendance below 75%
- Assignment due tomorrow
- Marks need improvement
- Pending assignments

**Info:**
- Great exam performance
- Excellent attendance
- New achievement earned
- New resources available

---

## Achievements

### 10 Badge Types

| Badge | Points | Description |
|-------|--------|-------------|
| Perfect Attendance | 100 | No absences for a month |
| Top Scorer | 150 | Scored above 95% |
| Consistent Performer | 120 | Maintained 85%+ for 3 months |
| Quick Learner | 75 | Completed 5 modules |
| Assignment Master | 80 | All assignments on time |
| Quiz Champion | 90 | 100% in 3 quizzes |
| Subject Expert | 110 | 90%+ in all exams |
| Improvement Star | 85 | Improved by 20%+ |
| Participation Pro | 70 | Active participation |
| Study Streak | 95 | 30-day study routine |

### Distribution
- **High Performers:** 3-6 achievements each
- **Average Performers:** 1-3 achievements (60% chance)
- **At-Risk Students:** No achievements

---

## ML Predictions

### Prediction Data
- **Total:** 100 predictions (one per student)
- **Confidence Scores:**
  - High Performers: 85-95%
  - Average Performers: 70-85%
  - At-Risk Students: 60-75%

### Predicted Grades
- **High:** A+, A
- **Average:** B+, B, C+
- **At-Risk:** C, D, F

### Risk Levels
- **Low:** High and average performers
- **Medium/High:** At-risk students

---

## Recommendations

### Distribution
- **At-Risk Students:** 5-8 recommendations each
- **Average Students:** 2-4 recommendations each
- **High Performers:** 1-3 recommendations each

### Completion Status
- High performers have some completed recommendations
- Others have mostly pending recommendations

---

## Career Suggestions

### 10 Career Paths

1. Software Engineer
2. Data Scientist
3. Doctor
4. Mechanical Engineer
5. Teacher
6. Business Analyst
7. Architect
8. Lawyer
9. Chartered Accountant
10. Civil Engineer

### Match Percentages
- **High Performers:** 80-95%
- **Average Performers:** 65-80%
- **At-Risk Students:** 50-65%

Each student gets 3-5 career suggestions ranked by match percentage.

---

## Login Credentials

### Test Accounts

| Role | Email | Password |
|------|-------|----------|
| **Admin** | admin@school.com | Admin@123 |
| **Teacher** | rajesh.kumar@school.com | Teacher@123 |
| **Parent** | parent1@email.com | Parent@123 |
| **Student** | student1@school.com | Student@123 |

**Note:** All teachers, parents, and students follow the same password pattern:
- Teachers: `Teacher@123`
- Parents: `Parent@123`
- Students: `Student@123`

---

## Data Relationships

### Interconnected Data
- ✅ Students linked to parents (90%)
- ✅ Attendance marked by teachers
- ✅ Marks for all students across subjects
- ✅ Assignments with realistic completion status
- ✅ Alerts based on performance
- ✅ Achievements for top performers
- ✅ Predictions based on category
- ✅ Recommendations linked to resources
- ✅ Career suggestions with required skills

---

## Realistic Features

### Time-Based Data
- Attendance: Last 6 months (weekdays only)
- Exams: Spread over 5 months
- Assignments: Past and future due dates
- Achievements: Earned over time

### Performance Correlation
- High attendance → Better marks
- Better marks → More achievements
- Poor performance → More alerts
- Category-based predictions

### Randomization
- Names from Indian name pool
- Random class/section assignment
- Varied performance within categories
- Natural distribution of data

---

## Script Features

### Safety
- ⚠️ Drops all existing tables
- ✅ Creates fresh schema
- ✅ Transaction-based (all or nothing)
- ✅ Error handling

### Performance
- Bulk inserts where possible
- Efficient data generation
- ~5-10 seconds execution time

### Extensibility
- Easy to modify counts
- Configurable categories
- Adjustable distributions
- Modular functions

---

## Verification

### After Seeding

```bash
# Check user counts
SELECT role, COUNT(*) FROM users GROUP BY role;

# Check student distribution
SELECT COUNT(*) FROM students;

# Check attendance records
SELECT COUNT(*) FROM attendance;

# Check marks records
SELECT COUNT(*) FROM marks;

# Check total records
SELECT 
  (SELECT COUNT(*) FROM users) as users,
  (SELECT COUNT(*) FROM attendance) as attendance,
  (SELECT COUNT(*) FROM marks) as marks,
  (SELECT COUNT(*) FROM assignments) as assignments;
```

---

## Use Cases

### Perfect For:
- ✅ Development and testing
- ✅ Demo presentations
- ✅ API testing
- ✅ Frontend development
- ✅ Performance testing
- ✅ ML model training
- ✅ Feature demonstrations

### Not Suitable For:
- ❌ Production use
- ❌ Real student data
- ❌ Data migration

---

## Customization

### Modify Counts
Edit these variables in the script:
```python
# In create_students()
high_performers = 30  # Change to desired count
average_performers = 50
at_risk = 20

# In create_teachers()
teacher_data = [...]  # Add/remove teachers

# In create_parents()
range(1, 21)  # Change to desired count
```

### Modify Time Periods
```python
# In create_attendance()
start_date = end_date - timedelta(days=180)  # Change days

# In create_marks()
exam_types = [
    ('Exam Name', max_score, days_ago),
    # Add/modify exams
]
```

---

## Troubleshooting

### Common Issues

**Issue:** Script fails with foreign key error
**Solution:** Ensure all parent records are committed before creating child records

**Issue:** Duplicate email errors
**Solution:** Drop all tables and run script fresh

**Issue:** Slow execution
**Solution:** Reduce number of students or attendance days

---

## Future Enhancements

- [ ] Command-line arguments for counts
- [ ] Selective seeding (only specific tables)
- [ ] Import from CSV
- [ ] Preserve existing admin user
- [ ] Progress bar for long operations
- [ ] Configurable date ranges
- [ ] Multiple school support

---

## Summary

The seed script creates a **complete, realistic dataset** with:
- ✅ 131 users across 4 roles
- ✅ 18,700+ total records
- ✅ 6 months of historical data
- ✅ Realistic performance distribution
- ✅ Interconnected relationships
- ✅ Ready for immediate use

**Perfect for development, testing, and demonstrations!**
