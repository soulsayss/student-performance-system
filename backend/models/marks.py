from . import db
from datetime import datetime

class Marks(db.Model):
    __tablename__ = 'marks'
    
    mark_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False, index=True)
    subject = db.Column(db.String(100), nullable=False)
    exam_type = db.Column(db.String(50), nullable=False)  # midterm, final, quiz, assignment
    score = db.Column(db.Float, nullable=False)
    max_score = db.Column(db.Float, nullable=False)
    exam_date = db.Column(db.Date, nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'mark_id': self.mark_id,
            'student_id': self.student_id,
            'subject': self.subject,
            'exam_type': self.exam_type,
            'score': self.score,
            'max_score': self.max_score,
            'percentage': round((self.score / self.max_score) * 100, 2) if self.max_score > 0 else 0,
            'exam_date': self.exam_date.isoformat() if self.exam_date else None,
            'created_at': self.created_at.isoformat()
        }
