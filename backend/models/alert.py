from . import db
from datetime import datetime

class Alert(db.Model):
    __tablename__ = 'alerts'
    
    alert_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False, index=True)
    message = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), nullable=False)  # info, warning, critical
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'alert_id': self.alert_id,
            'student_id': self.student_id,
            'message': self.message,
            'severity': self.severity,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat()
        }
