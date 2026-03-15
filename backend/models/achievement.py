from . import db
from datetime import datetime

class Achievement(db.Model):
    __tablename__ = 'achievements'
    
    achievement_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False, index=True)
    badge_name = db.Column(db.String(100), nullable=False)
    points = db.Column(db.Integer, default=0)
    description = db.Column(db.Text, nullable=True)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'achievement_id': self.achievement_id,
            'student_id': self.student_id,
            'badge_name': self.badge_name,
            'points': self.points,
            'description': self.description,
            'earned_at': self.earned_at.isoformat()
        }
