from . import db
from datetime import datetime

class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    attendance_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False)  # present, absent, late
    marked_by = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'attendance_id': self.attendance_id,
            'student_id': self.student_id,
            'date': self.date.isoformat(),
            'status': self.status,
            'marked_by': self.marked_by,
            'created_at': self.created_at.isoformat()
        }
