from . import db
from datetime import datetime

class Assignment(db.Model):
    __tablename__ = 'assignments'
    
    assignment_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False, index=True)
    subject = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, submitted, graded
    submission_date = db.Column(db.DateTime, nullable=True)
    grade = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'assignment_id': self.assignment_id,
            'student_id': self.student_id,
            'subject': self.subject,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.isoformat(),
            'status': self.status,
            'submission_date': self.submission_date.isoformat() if self.submission_date else None,
            'grade': self.grade,
            'created_at': self.created_at.isoformat()
        }
