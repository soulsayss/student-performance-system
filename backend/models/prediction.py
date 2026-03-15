from . import db
from datetime import datetime

class Prediction(db.Model):
    __tablename__ = 'predictions'
    
    prediction_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False, index=True)
    predicted_grade = db.Column(db.String(5), nullable=False)  # A+, A, B+, etc.
    risk_level = db.Column(db.String(20), nullable=False)  # low, medium, high
    confidence_score = db.Column(db.Float, nullable=False)
    factors = db.Column(db.JSON, nullable=True)  # Store contributing factors
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'prediction_id': self.prediction_id,
            'student_id': self.student_id,
            'predicted_grade': self.predicted_grade,
            'risk_level': self.risk_level,
            'confidence_score': self.confidence_score,
            'factors': self.factors,
            'created_at': self.created_at.isoformat()
        }
