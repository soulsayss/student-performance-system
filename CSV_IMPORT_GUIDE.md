# CSV Data Import Guide

## Overview

The Student Academic System supports bulk data import via CSV files with flexible formatting and comprehensive error handling. Import students, teachers, parents, marks, and attendance records with ease.

## Recent Updates (Latest Session)

✅ **Enhanced CSV Import System**
- Added UTF-8 BOM handling for all import types
- Flexible header normalization (spaces, special characters)
- Multiple date format support (DD-MM-YYYY, YYYY-MM-DD, MM/DD/YYYY, etc.)
- Intelligent exam type mapping (Unit Test 1/2/3 → quiz, Mid Term → midterm, Final Exam → final)
- Improved error messages with row numbers
- Duplicate detection and graceful skipping

✅ **Successfully Tested With:**
- 150 student records
- 15 teacher records  
- 150 parent records
- Large marks datasets with various exam types
- International date formats

## Features

✅ Import multiple data types (students, teachers, parents, marks, attendance)
✅ CSV template download for each data type
✅ Flexible header matching (case-insensitive, space-tolerant)
✅ Multiple date format support
✅ Comprehensive validation with detailed error reporting
✅ Option to clear existing data before import
✅ Duplicate detection and skipping
✅ Batch processing with transaction support
✅ UTF-8 BOM handling
✅ User-friendly admin interface

## Supported Data Types

### 1. Students
Import student records with user accounts.

**CSV Format (Flexible Headers):**
```csv
Name,Email,Password,Roll Number,Class,Section,Gender,Date of Birth,Performance Level
John Doe,john@example.com,password123,S001,10,A,Male,13-08-2013,Good
Jane Smith,jane@example.com,password123,S002,10,A,Female,15-08-2013,Excellent
```

**Accepted Header Variations:**
- "Date of Birth" / "date_of_birth" / "dob" / "DOB"
- "Roll Number" / "roll_number" / "Roll No"
- "Performance Level" / "performance_level" (optional)

**Date Formats Supported:**
- DD-MM-YYYY (13-08-2013) - Indian/European format
- YYYY-MM-DD (2013-08-13) - ISO format
- MM/DD/YYYY (08/13/2013) - US format
- DD/MM/YYYY (13/08/2013)
- DD.MM.YYYY (13.08.2013)

**Validations:**
- Unique email addresses
- Unique roll numbers
- Valid email format
- Required: name, email, password, roll_number, class, section

### 2. Teachers
Import teacher records with user accounts.

**CSV Format (Flexible Headers):**
```csv
Name,Email,Password,Employee,Subject,Class Assigned,Phone,Experience (Years)
Dr. Smith,smith@school.com,teacher123,T001,Mathematics,Science,1234567890,5
Prof. Johnson,johnson@school.com,teacher123,T002,Physics,Science,0987654321,10
```

**Accepted Header Variations:**
- "Employee" / "employee_id" / "Employee ID"
- "Class Assigned" / "department" / "Department"
- "Experience (Years)" / "experience" (optional)
- "Phone" / "phone" (optional)

**Validations:**
- Unique email addresses
- Unique employee IDs
- Valid email format
- Required: name, email, password, employee_id, subject

### 3. Parents
Import parent records linked to existing students.

**CSV Format (Flexible Headers):**
```csv
Name,Email,Password,Phone,Student Roll Number,Relation,Occupation
Parent One,parent1@email.com,parent123,1234567890,S001,Father,Engineer
Parent Two,parent2@email.com,parent123,0987654321,S002,Mother,Doctor
```

**Accepted Header Variations:**
- "Student Roll Number" / "student_roll_number" / "Student Roll No"
- "Occupation" (optional field)

**Validations:**
- Unique email addresses
- Student must exist (by roll number)
- Valid email format
- Required: name, email, password, student_roll_number

### 4. Marks
Import exam marks for existing students.

**CSV Format (Flexible Headers):**
```csv
roll_number,subject,exam_type,score,max_score,exam_date
6A001,Mathematics,Unit Test 1,86.4,100,15-01-2024
6A001,Mathematics,Unit Test 2,91,100,22-01-2024
6A001,Mathematics,Mid Term,89.4,100,05-02-2024
6A001,Mathematics,Final Exam,92.9,100,15-03-2024
```

**Exam Type Mapping (Flexible):**
- **Quiz:** "Unit Test 1", "Unit Test 2", "Unit Test 3", "quiz", "test", "class test"
- **Midterm:** "Mid Term", "midterm", "mid-term", "semester", "half yearly"
- **Final:** "Final Exam", "final", "annual", "yearly"
- **Assignment:** "assignment", "homework", "project", "practical"

**Date Formats Supported:**
- DD-MM-YYYY, YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY, DD.MM.YYYY, YYYY/MM/DD

**Validations:**
- Student must exist (by roll number)
- Valid exam_type (automatically mapped)
- Score must be between 0 and max_score
- All fields required

### 5. Attendance
Import attendance records for existing students.

**CSV Format:**
```csv
roll_number,date,status
S001,2024-01-15,present
S001,2024-01-16,present
S002,2024-01-15,absent
```

**Validations:**
- Student must exist (by roll number)
- Valid status: present, absent, late
- Multiple date formats supported
- No duplicate entries (same student + date)
- All fields required

## How to Use

### Via Admin Dashboard (UI)

1. **Login as Admin**
   - Navigate to the admin dashboard
   - Click "Import CSV Data" button (green button in header)

2. **Select Data Type**
   - Choose the type of data you want to import
   - Options: Students, Teachers, Parents, Marks, Attendance

3. **Download Template**
   - Click "Download Template" to get the correct CSV format
   - Open in Excel/Google Sheets and fill in your data

4. **Upload CSV File**
   - Click "Choose CSV file" and select your prepared file
   - Review the selected file name

5. **Configure Options**
   - ⚠️ Optional: Check "Clear existing data" to delete all current records
   - WARNING: This action is permanent!

6. **Import**
   - Click "Import Data" button
   - Wait for processing (may take a few seconds for large files)

7. **Review Results**
   - Check imported count
   - Review any errors or skipped records
   - Fix issues and re-import if needed

### Via API (cURL)

**Import Students:**
```bash
curl -X POST http://localhost:5000/api/admin/import-data \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -F "file=@students.csv" \
  -F "file_type=students" \
  -F "clear_existing=false"
```

**Download Template:**
```bash
curl -X GET http://localhost:5000/api/admin/csv-template/students \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -o students_template.csv
```

## Best Practices

### 1. Preparation
- ✅ Always download and use the provided templates
- ✅ Prepare data in Excel/Google Sheets
- ✅ Validate data before export to CSV
- ✅ Check for duplicates
- ✅ Use consistent formatting

### 2. Import Order
Import data in this order to avoid reference errors:

1. **First:** Students and Teachers (independent)
2. **Second:** Parents (requires students)
3. **Third:** Marks and Attendance (requires students)

### 3. Testing
- ✅ Test with small batches first (5-10 records)
- ✅ Review results before importing large datasets
- ✅ Keep backup of your CSV files

### 4. Security
- ✅ Use strong passwords in CSV files
- ✅ Change passwords after import
- ✅ Don't share CSV files with sensitive data
- ✅ Delete CSV files after successful import

### 5. Error Handling
- ✅ Review all errors and skipped records
- ✅ Fix issues in your CSV file
- ✅ Re-import only the failed records
- ✅ Keep track of import logs

## Common Errors and Solutions

### Error: "Invalid CSV headers"
**Solution:** Download the template and ensure your CSV has exact same headers (case-sensitive)

### Error: "Email already exists"
**Solution:** Check for duplicate emails in your CSV or existing database

### Error: "Student with roll number X not found"
**Solution:** Import students first before importing parents/marks/attendance

### Error: "Invalid email format"
**Solution:** Ensure all emails follow format: user@domain.com

### Error: "Invalid date format"
**Solution:** Use YYYY-MM-DD format (e.g., 2024-01-15)

### Error: "Score must be between 0 and max_score"
**Solution:** Ensure score values are valid numbers within range

### Error: "Invalid exam type"
**Solution:** Use only: quiz, midterm, final, or assignment

### Error: "Invalid status"
**Solution:** Use only: present, absent, or late

## File Format Requirements

### CSV File Requirements
- ✅ UTF-8 encoding
- ✅ Comma-separated values
- ✅ First row must be headers
- ✅ No empty rows
- ✅ No special characters in headers
- ✅ Consistent column count

### Excel to CSV Conversion
1. Open your Excel file
2. Click "File" → "Save As"
3. Choose "CSV (Comma delimited) (*.csv)"
4. Click "Save"
5. Confirm "Yes" to keep CSV format

### Google Sheets to CSV
1. Open your Google Sheet
2. Click "File" → "Download" → "Comma Separated Values (.csv)"
3. File will download automatically

## API Endpoints

### Import Data
```
POST /api/admin/import-data
Authorization: Bearer <admin_token>
Content-Type: multipart/form-data

Form Data:
- file: CSV file
- file_type: students|teachers|parents|marks|attendance
- clear_existing: true|false (optional)
```

### Download Template
```
GET /api/admin/csv-template/:type
Authorization: Bearer <admin_token>

Parameters:
- type: students|teachers|parents|marks|attendance
```

## Response Format

### Success Response
```json
{
  "success": true,
  "message": "Import completed. 10 records imported.",
  "imported_count": 10,
  "errors": [],
  "skipped": []
}
```

### Partial Success Response
```json
{
  "success": true,
  "message": "Import completed. 8 records imported.",
  "imported_count": 8,
  "errors": [
    "Row 3: Invalid email format: invalid-email"
  ],
  "skipped": [
    "Row 5: Email already exists: john@example.com"
  ]
}
```

### Error Response
```json
{
  "success": false,
  "message": "Import completed. 0 records imported.",
  "imported_count": 0,
  "errors": [
    "Invalid CSV headers. Expected: name,email,password,roll_number,class,section"
  ],
  "skipped": []
}
```

## Troubleshooting

### Import is slow
- Large files (>1000 records) may take time
- Be patient and don't refresh the page
- Consider splitting into smaller batches

### Some records are skipped
- Check the "Skipped" section in results
- Usually due to duplicates
- Fix and re-import only those records

### All records failed
- Check CSV format matches template exactly
- Verify headers are correct (case-sensitive)
- Ensure file is saved as CSV, not Excel

### Database errors
- Contact system administrator
- Check database connection
- Verify sufficient storage space

## Support

For additional help:
- Check API_DOCUMENTATION.md for detailed API specs
- Review error messages carefully
- Test with template files first
- Contact system administrator for database issues

## Security Notes

⚠️ **Important Security Considerations:**

1. Only administrators can import data
2. All imports are logged
3. Passwords are hashed before storage
4. Validate all data before import
5. Use strong passwords in CSV files
6. Change default passwords after import
7. Keep CSV files secure
8. Delete CSV files after import
9. Regular database backups recommended
10. Monitor import logs for suspicious activity

## Version History

- **v1.0** - Initial CSV import functionality
  - Support for 5 data types
  - Template download
  - Validation and error reporting
  - Admin UI integration
