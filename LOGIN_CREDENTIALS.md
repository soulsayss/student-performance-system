# � Login Credentials - Railway Production Database

**Last Updated:** March 22, 2026  
**Database:** PostgreSQL on Railway  
**Total Users:** 1,016 (1 admin + 15 teachers + 500 students + 500 parents)

---

## � Email Format

- **Admin:** `admin@school.edu`
- **Teachers:** `firstname.lastname@school.com`
- **Students:** `firstname.lastname{number}@gmail.com`
- **Parents:** `parent.lastname{number}@gmail.com`

## 🔐 Password Pattern

All passwords follow the same pattern: `[Role]@123`

- Admin: `Admin@123`
- Teachers: `Teacher@123`
- Students: `Student@123`
- Parents: `Parent@123`

---

## 👨‍💼 Admin Account

| Name | Email | Password | Role |
|------|-------|----------|------|
| System Administrator | admin@school.edu | Admin@123 | Admin |

---

## 👨‍🏫 Teachers (15 Total)

### Science Teachers (2)
| Name | Email | Password | Subject |
|------|-------|----------|---------|
| Dr. Rajesh Kumar | rajesh.kumar@school.com | Teacher@123 | Science |
| Dr. Priya Malhotra | priya.malhotra@school.com | Teacher@123 | Science |

### Mathematics Teachers (2)
| Name | Email | Password | Subject |
|------|-------|----------|---------|
| Prof. Amit Sharma | amit.sharma@school.com | Teacher@123 | Mathematics |
| Mrs. Sneha Kapoor | sneha.kapoor@school.com | Teacher@123 | Mathematics |

### Other Subject Teachers
| Name | Email | Password | Subject |
|------|-------|----------|---------|
| Mr. Vikram Patel | vikram.patel@school.com | Teacher@123 | History |
| Ms. Anjali Reddy | anjali.reddy@school.com | Teacher@123 | Social Science |
| Dr. Nikhil Desai | nikhil.desai@school.com | Teacher@123 | Social Science |
| Mr. Suresh Iyer | suresh.iyer@school.com | Teacher@123 | Geography |
| Mrs. Kavita Singh | kavita.singh@school.com | Teacher@123 | Hindi |
| Mr. Arjun Nair | arjun.nair@school.com | Teacher@123 | English |
| Mrs. Deepa Rao | deepa.rao@school.com | Teacher@123 | English |
| Mr. Rohit Verma | rohit.verma@school.com | Teacher@123 | Sports |
| Ms. Pooja Mehta | pooja.mehta@school.com | Teacher@123 | Music |
| Dr. Meera Gupta | meera.gupta@school.com | Teacher@123 | Additional Language |
| Prof. Karan Joshi | karan.joshi@school.com | Teacher@123 | Arts/Drawing |

---

## 👨‍🎓 Students (500 Total)

### Sample Students by Class

#### Class 6A (50 students)
| Student Name | Student Email | Parent Name | Parent Email | Password |
|--------------|---------------|-------------|--------------|----------|
| Pranav Kumar | pranav.kumar1@gmail.com | Shobha Kumar | parent.kumar1@gmail.com | Student@123 / Parent@123 |
| Vivaan Kapoor | vivaan.kapoor2@gmail.com | Shobha Kapoor | parent.kapoor2@gmail.com | Student@123 / Parent@123 |
| Aryan Agarwal | aryan.agarwal3@gmail.com | Kavita Agarwal | parent.agarwal3@gmail.com | Student@123 / Parent@123 |
| Shaurya Bansal | shaurya.bansal4@gmail.com | Geeta Bansal | parent.bansal4@gmail.com | Student@123 / Parent@123 |
| Advik Gupta | advik.gupta5@gmail.com | Anjali Gupta | parent.gupta5@gmail.com | Student@123 / Parent@123 |

#### Class 6B (50 students)
| Student Name | Student Email | Parent Name | Parent Email | Password |
|--------------|---------------|-------------|--------------|----------|
| Pranav Bansal | pranav.bansal51@gmail.com | Ramesh Bansal | parent.bansal51@gmail.com | Student@123 / Parent@123 |
| Virat Patel | virat.patel52@gmail.com | Ravi Patel | parent.patel52@gmail.com | Student@123 / Parent@123 |
| Atharv Agarwal | atharv.agarwal53@gmail.com | Meera Agarwal | parent.agarwal53@gmail.com | Student@123 / Parent@123 |

#### Class 7A (50 students)
| Student Name | Student Email | Parent Name | Parent Email | Password |
|--------------|---------------|-------------|--------------|----------|
| Aarav Mehta | aarav.mehta151@gmail.com | Pooja Mehta | parent.mehta151@gmail.com | Student@123 / Parent@123 |
| Rohan Kapoor | rohan.kapoor152@gmail.com | Meera Kapoor | parent.kapoor152@gmail.com | Student@123 / Parent@123 |

#### Class 7B (50 students)
| Student Name | Student Email | Parent Name | Parent Email | Password |
|--------------|---------------|-------------|--------------|----------|
| Aarav Sharma | aarav.sharma201@gmail.com | Rajesh Sharma | parent.sharma201@gmail.com | Student@123 / Parent@123 |

#### Class 8A (50 students)
| Student Name | Student Email | Parent Name | Parent Email | Password |
|--------------|---------------|-------------|--------------|----------|
| Arjun Patel | arjun.patel251@gmail.com | Vinod Patel | parent.patel251@gmail.com | Student@123 / Parent@123 |

#### Class 8B (50 students)
| Student Name | Student Email | Parent Name | Parent Email | Password |
|--------------|---------------|-------------|--------------|----------|
| Rohan Sharma | rohan.sharma301@gmail.com | Amit Sharma | parent.sharma301@gmail.com | Student@123 / Parent@123 |

#### Class 9A (50 students)
| Student Name | Student Email | Parent Name | Parent Email | Password |
|--------------|---------------|-------------|--------------|----------|
| Vivaan Kumar | vivaan.kumar351@gmail.com | Prakash Kumar | parent.kumar351@gmail.com | Student@123 / Parent@123 |

#### Class 9B (50 students)
| Student Name | Student Email | Parent Name | Parent Email | Password |
|--------------|---------------|-------------|--------------|----------|
| Aarav Gupta | aarav.gupta401@gmail.com | Suresh Gupta | parent.gupta401@gmail.com | Student@123 / Parent@123 |

#### Class 10A (50 students)
| Student Name | Student Email | Parent Name | Parent Email | Password |
|--------------|---------------|-------------|--------------|----------|
| Dhruv Mehta | dhruv.mehta451@gmail.com | Ramesh Mehta | parent.mehta451@gmail.com | Student@123 / Parent@123 |

#### Class 10B (50 students)
| Student Name | Student Email | Parent Name | Parent Email | Password |
|--------------|---------------|-------------|--------------|----------|
| Arnav Singh | arnav.singh501@gmail.com | Vikram Singh | parent.singh501@gmail.com | Student@123 / Parent@123 |

---

## 📊 Database Statistics

- **Total Users:** 1,016
  - 1 Admin
  - 15 Teachers
  - 500 Students (10 sections × 50 each)
  - 500 Parents (1:1 with students)

- **Total Records:** 107,920
  - 64,500 Attendance records
  - 33,000 Marks records
  - 4,234 Assignments
  - 947 Alerts
  - 981 Achievements
  - 500 ML Predictions
  - 2,000 Career Suggestions
  - 1,692 Recommendations
  - 66 Learning Resources

- **Class Structure:** 10 sections
  - Classes: 6, 7, 8, 9, 10
  - Sections: A, B
  - Students per section: 50 (28 boys, 22 girls)

---

## 🧪 Quick Test Credentials

Use these for quick testing on Vercel:

```
Admin:
Email: admin@school.edu
Password: Admin@123

Teacher:
Email: rajesh.kumar@school.com
Password: Teacher@123

Student:
Email: pranav.kumar1@gmail.com
Password: Student@123

Parent:
Email: parent.kumar1@gmail.com
Password: Parent@123
```

---

## 🔗 Debug Endpoints

Get fresh credentials from Railway:

- **Quick Test Logins:** `https://student-performance-system-production.up.railway.app/api/auth/debug/quick-test-logins`
- **Export All Users:** `https://student-performance-system-production.up.railway.app/api/auth/debug/export-all-users`

---

## 📝 Notes

- All student emails include a number suffix for uniqueness (e.g., `pranav.kumar1@gmail.com`)
- All parent emails use `parent.` prefix (e.g., `parent.kumar1@gmail.com`)
- Parent and student share the same last name to indicate relationship
- The number suffix matches between parent and child (e.g., kumar1 for both)
- All passwords are simple for testing purposes only

---

**Production URL:** https://student-performance-system-production.up.railway.app  
**Frontend URL:** https://your-vercel-url.vercel.app
