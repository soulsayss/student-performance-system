from . import db
from datetime import datetime

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    
    recommendation_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False, index=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.resource_id'), nullable=False)
    reason = db.Column(db.Text, nullable=True)
    is_completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'recommendation_id': self.recommendation_id,
            'student_id': self.student_id,
            'resource_id': self.resource_id,
            'reason': self.reason,
            'is_completed': self.is_completed,
            'created_at': self.created_at.isoformat()
        }
