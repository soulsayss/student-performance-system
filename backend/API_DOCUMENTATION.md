# Student Academic Performance System - API Documentation

## Base URL
```
http://localhost:5000
```

## Authentication
All protected endpoints require JWT token in Authorization header:
```
Authorization: Bearer <access_token>
```

---

## Authentication Endpoints

### 1. Register User
**POST** `/api/auth/register`

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "Test1234",
  "role": "student",
  
  // For students:
  "roll_number": "2024001",
  "class": "10",
  "section": "A",
  "gender": "male",
  "dob": "2008-05-15",
  
  // For teachers:
  "employee_id": "EMP001",
  "subject": "Mathematics",
  "department": "Science"
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "message": "User registered successfully",
  "user": { ... }
}
```

---

### 2. Login
**POST** `/api/auth/login`

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "Test1234"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Login successful",
  "access_token": "eyJhbGci...",
  "refresh_token": "eyJhbGci...",
  "user": {
    "user_id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "student",
    "student_info": { ... }
  }
}
```

---

### 3. Get Profile
**GET** `/api/auth/profile`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "user": { ... }
}
```

---

### 4. Logout
**POST** `/api/auth/logout`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

---

### 5. Refresh Token
**POST** `/api/auth/refresh`

**Headers:** `Authorization: Bearer <refresh_token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "access_token": "eyJhbGci..."
}
```

---

## Student Endpoints

### 1. Dashboard
**GET** `/api/student/dashboard`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "dashboard": {
    "attendance_percentage": 81.67,
    "average_marks": 80.03,
    "total_points": 325,
    "unread_alerts": 2,
    "pending_assignments": 2,
    "prediction": {
      "predicted_grade": "A",
      "risk_level": "low",
      "confidence_score": 0.87
    },
    "student_info": { ... }
  }
}
```

---

### 2. Attendance Records
**GET** `/api/student/attendance`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "attendance": {
    "records": [...],
    "statistics": {
      "total_days": 60,
      "present": 49,
      "absent": 6,
      "late": 5,
      "attendance_percentage": 81.67
    },
    "chart_data": [
      {
        "month": "2025-12",
        "present": 25,
        "absent": 3,
        "late": 2
      }
    ]
  }
}
```

---

### 3. Marks/Grades
**GET** `/api/student/marks`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "marks": {
    "by_subject": {
      "Mathematics": [...],
      "Physics": [...]
    },
    "subject_averages": {
      "Mathematics": 77.01,
      "Physics": 82.49
    },
    "overall_average": 80.03,
    "chart_data": [...],
    "total_exams": 15
  }
}
```

---

### 4. Predictions
**GET** `/api/student/predictions`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "predictions": {
    "latest": {
      "predicted_grade": "A",
      "risk_level": "low",
      "confidence_score": 0.87,
      "factors": {
        "attendance": "good",
        "marks_trend": "improving"
      }
    },
    "history": [...],
    "total_predictions": 1
  }
}
```

---

### 5. Recommendations
**GET** `/api/student/recommendations`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "recommendations": {
    "all": [...],
    "completed": [...],
    "pending": [...],
    "total": 2,
    "completion_rate": 0.0
  }
}
```

---

### 6. Achievements
**GET** `/api/student/achievements`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "achievements": {
    "all": [
      {
        "badge_name": "Top Scorer",
        "points": 150,
        "description": "Scored above 90%"
      }
    ],
    "total_points": 325,
    "total_badges": 3,
    "badge_counts": { ... }
  }
}
```

---

### 7. Alerts
**GET** `/api/student/alerts`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "alerts": {
    "all": [...],
    "unread": [...],
    "read": [...],
    "by_severity": {
      "critical": [...],
      "warning": [...],
      "info": [...]
    },
    "counts": {
      "total": 3,
      "unread": 2,
      "critical": 1
    }
  }
}
```

---

### 8. Career Suggestions
**GET** `/api/student/career-suggestions`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "career_suggestions": {
    "all": [...],
    "top_matches": [
      {
        "career_path": "Software Engineer",
        "match_percentage": 92.5,
        "description": "Build software applications",
        "required_skills": ["Programming", "Math"]
      }
    ],
    "total": 3
  }
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "message": "Validation error message"
}
```

### 401 Unauthorized
```json
{
  "success": false,
  "message": "Invalid or expired token"
}
```

### 403 Forbidden
```json
{
  "success": false,
  "message": "Access denied. Required roles: student"
}
```

### 404 Not Found
```json
{
  "success": false,
  "message": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "message": "Internal server error",
  "error": "Error details"
}
```

---

## Data Models

### User Roles
- `student`
- `teacher`
- `parent`
- `admin`

### Attendance Status
- `present`
- `absent`
- `late`

### Exam Types
- `midterm`
- `final`
- `quiz`
- `assignment`

### Risk Levels
- `low`
- `medium`
- `high`

### Alert Severity
- `info`
- `warning`
- `critical`

### Resource Types
- `video`
- `article`
- `pdf`
- `quiz`

### Difficulty Levels
- `beginner`
- `intermediate`
- `advanced`

---

## Rate Limiting
Currently no rate limiting implemented (add in production)

## CORS
Enabled for all origins (configure for production)

## Security Notes
- Passwords hashed with Werkzeug
- JWT tokens expire after 24 hours
- Refresh tokens expire after 30 days
- Input validation on all endpoints
- SQL injection protection via SQLAlchemy ORM


---

## Teacher Endpoints

### 1. Dashboard
**GET** `/api/teacher/dashboard`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "dashboard": {
    "total_students": 1,
    "at_risk_students": 0,
    "present_today": 1,
    "class_average": 80.03,
    "teacher_info": {
      "name": "Jane Smith",
      "subject": "Mathematics",
      "department": "Science",
      "employee_id": "EMP001"
    }
  }
}
```

---

### 2. Get Students List
**GET** `/api/teacher/students`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "students": [
    {
      "student_id": 1,
      "name": "John Doe",
      "roll_number": "2024001",
      "class": "10",
      "section": "A",
      "email": "john@example.com",
      "attendance_percentage": 81.67,
      "average_marks": 80.03,
      "risk_level": "low"
    }
  ],
  "total": 1
}
```

---

### 3. Mark Attendance
**POST** `/api/teacher/attendance`

**Headers:** `Authorization: Bearer <token>`

#### Single Record:
**Request Body:**
```json
{
  "student_id": 1,
  "date": "2026-01-31",
  "status": "present"
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "message": "Attendance marked successfully"
}
```

#### CSV Upload:
**Form Data:** `file: attendance.csv`

**CSV Format:**
```csv
student_id,date,status
1,2026-02-01,present
1,2026-02-02,absent
```

**Response:** `201 Created`
```json
{
  "success": true,
  "message": "Attendance marked for 2 records",
  "records_added": 2,
  "errors": null
}
```

---

### 4. Add Marks
**POST** `/api/teacher/marks`

**Headers:** `Authorization: Bearer <token>`

#### Single Record:
**Request Body:**
```json
{
  "student_id": 1,
  "subject": "Mathematics",
  "exam_type": "quiz",
  "score": 95,
  "max_score": 100,
  "exam_date": "2026-01-30"
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "message": "Marks added successfully",
  "marks": { ... }
}
```

#### CSV Upload:
**Form Data:** `file: marks.csv`

**CSV Format:**
```csv
student_id,subject,exam_type,score,max_score,exam_date
1,Physics,midterm,88,100,2026-01-25
1,Chemistry,quiz,92,100,2026-01-26
```

**Response:** `201 Created`
```json
{
  "success": true,
  "message": "Marks added for 2 records",
  "records_added": 2,
  "errors": null
}
```

---

### 5. Class Analytics
**GET** `/api/teacher/analytics`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "analytics": {
    "subject_performance": [
      {
        "subject": "Mathematics",
        "average": 81.51,
        "total_exams": 4
      }
    ],
    "attendance_trend": [
      {
        "month": "2025-12",
        "present": 25,
        "absent": 3,
        "late": 2,
        "attendance_rate": 83.33
      }
    ],
    "grade_distribution": {
      "A": 2,
      "B": 8,
      "C": 2,
      "D": 4,
      "F": 0
    },
    "risk_distribution": {
      "low": 1,
      "medium": 0,
      "high": 0,
      "unknown": 0
    },
    "total_students": 1
  }
}
```

---

### 6. At-Risk Students
**GET** `/api/teacher/at-risk-students`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "at_risk_students": [
    {
      "student_id": 1,
      "name": "John Doe",
      "roll_number": "2024001",
      "class": "10",
      "section": "A",
      "attendance_percentage": 65.5,
      "average_marks": 45.2,
      "risk_level": "high",
      "risk_factors": [
        "Low attendance: 65.5%",
        "Low marks: 45.2%",
        "Risk level: high"
      ]
    }
  ],
  "total": 1
}
```

---

### 7. Send Alert
**POST** `/api/teacher/send-alert`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "student_id": 1,
  "message": "Great performance in Mathematics quiz!",
  "severity": "info"
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "message": "Alert sent successfully",
  "alert": {
    "alert_id": 4,
    "student_id": 1,
    "message": "Great performance in Mathematics quiz!",
    "severity": "info",
    "is_read": false,
    "created_at": "2026-01-30T14:27:43.262389"
  }
}
```

---

## CSV Upload Guidelines

### Attendance CSV Requirements:
- **Required columns:** student_id, date, status
- **Date format:** YYYY-MM-DD
- **Status values:** present, absent, late
- **Encoding:** UTF-8

### Marks CSV Requirements:
- **Required columns:** student_id, subject, exam_type, score
- **Optional columns:** max_score (default: 100), exam_date
- **Date format:** YYYY-MM-DD
- **Score:** Numeric values
- **Encoding:** UTF-8

### CSV Upload Tips:
- Use proper CSV format with headers
- Validate data before upload
- Check error messages for failed rows
- Maximum file size: 16MB
- Successful rows are processed even if some fail


---

## CSV Data Import Endpoints

### Import Data from CSV
```
POST /api/admin/import-data
Authorization: Bearer <admin_token>
Content-Type: multipart/form-data
```

**Form Data:**
- `file`: CSV file (required)
- `file_type`: One of: `students`, `teachers`, `parents`, `marks`, `attendance` (required)
- `clear_existing`: `true` or `false` (optional, default: false) - WARNING: This will delete all existing data of that type

**CSV Formats:**

**Students CSV:**
```csv
name,email,password,roll_number,class,section
John Doe,john@example.com,password123,S001,10,A
Jane Smith,jane@example.com,password123,S002,10,A
```

**Teachers CSV:**
```csv
name,email,password,employee_id,subject,department
Dr. Smith,smith@school.com,teacher123,T001,Mathematics,Science
Prof. Johnson,johnson@school.com,teacher123,T002,Physics,Science
```

**Parents CSV:**
```csv
name,email,password,phone,student_roll_number,relation
Parent One,parent1@email.com,parent123,1234567890,S001,Father
Parent Two,parent2@email.com,parent123,0987654321,S002,Mother
```

**Marks CSV:**
```csv
roll_number,subject,exam_type,score,max_score,exam_date
S001,Mathematics,midterm,85,100,2024-01-15
S001,Physics,midterm,78,100,2024-01-16
```

**Attendance CSV:**
```csv
roll_number,date,status
S001,2024-01-15,present
S001,2024-01-16,present
S002,2024-01-15,absent
```

**Validation Rules:**
- All emails must be unique and valid format
- Roll numbers must be unique for students
- Employee IDs must be unique for teachers
- Student roll numbers in parents/marks/attendance CSV must exist
- Exam types: `quiz`, `midterm`, `final`, `assignment`
- Attendance status: `present`, `absent`, `late`
- Dates must be in YYYY-MM-DD format
- Scores must be between 0 and max_score

**Response:**
```json
{
  "success": true,
  "message": "Import completed. 10 records imported.",
  "imported_count": 10,
  "errors": [
    "Row 5: Invalid email format: invalid-email",
    "Row 8: Student with roll number S999 not found"
  ],
  "skipped": [
    "Row 3: Email already exists: john@example.com",
    "Row 7: Roll number already exists: S001"
  ]
}
```

**Error Response:**
```json
{
  "success": false,
  "message": "Import completed. 5 records imported.",
  "imported_count": 5,
  "errors": [
    "Invalid CSV headers. Expected: name,email,password,roll_number,class,section",
    "Row 2: Missing required fields"
  ],
  "skipped": []
}
```

### Download CSV Template
```
GET /api/admin/csv-template/:type
Authorization: Bearer <admin_token>
```

**Parameters:**
- `type`: One of: `students`, `teachers`, `parents`, `marks`, `attendance`

**Example:**
```
GET /api/admin/csv-template/students
```

**Response:**
Returns a downloadable CSV file with correct headers and sample data.

**Example Response (students template):**
```csv
name,email,password,roll_number,class,section
John Doe,john@example.com,password123,S001,10,A
Jane Smith,jane@example.com,password123,S002,10,A
```

---

## CSV Import Usage Examples

### Using cURL

**Import Students:**
```bash
curl -X POST http://localhost:5000/api/admin/import-data \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -F "file=@students.csv" \
  -F "file_type=students" \
  -F "clear_existing=false"
```

**Import Marks:**
```bash
curl -X POST http://localhost:5000/api/admin/import-data \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -F "file=@marks.csv" \
  -F "file_type=marks"
```

**Download Template:**
```bash
curl -X GET http://localhost:5000/api/admin/csv-template/students \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -o students_template.csv
```

### Using JavaScript (Frontend)

```javascript
// Import data
const importData = async (file, fileType, clearExisting = false) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('file_type', fileType);
  formData.append('clear_existing', clearExisting);
  
  const response = await fetch('/api/admin/import-data', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    },
    body: formData
  });
  
  return await response.json();
};

// Download template
const downloadTemplate = async (type) => {
  const response = await fetch(`/api/admin/csv-template/${type}`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${type}_template.csv`;
  a.click();
};
```

---

## CSV Import Best Practices

1. **Always download and use the provided templates** to ensure correct format
2. **Test with small batches first** before importing large datasets
3. **Backup your database** before using `clear_existing=true`
4. **Review errors and skipped records** in the response to fix issues
5. **Import in correct order:**
   - First: Students and Teachers
   - Second: Parents (requires students to exist)
   - Third: Marks and Attendance (requires students to exist)
6. **Use strong passwords** in CSV files and change them after import
7. **Validate data** in spreadsheet software before importing
8. **Check for duplicates** to avoid skipped records
9. **Use consistent date format** (YYYY-MM-DD)
10. **Ensure roll numbers match** when importing related data

---
