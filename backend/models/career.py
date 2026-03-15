from . import db
from datetime import datetime

class CareerSuggestion(db.Model):
    __tablename__ = 'career_suggestions'
    
    suggestion_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False, index=True)
    career_path = db.Column(db.String(200), nullable=False)
    match_percentage = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    required_skills = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'suggestion_id': self.suggestion_id,
            'student_id': self.student_id,
            'career_path': self.career_path,
            'match_percentage': self.match_percentage,
            'description': self.description,
            'required_skills': self.required_skills,
            'created_at': self.created_at.isoformat()
        }
