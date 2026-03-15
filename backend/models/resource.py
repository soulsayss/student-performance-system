from . import db
from datetime import datetime

class Resource(db.Model):
    __tablename__ = 'resources'
    
    resource_id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    link = db.Column(db.String(500), nullable=False)
    resource_type = db.Column(db.String(50), nullable=False)  # video, article, pdf, quiz
    difficulty = db.Column(db.String(20), nullable=False)  # beginner, intermediate, advanced
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    recommendations = db.relationship('Recommendation', backref='resource', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'resource_id': self.resource_id,
            'subject': self.subject,
            'title': self.title,
            'description': self.description,
            'link': self.link,
            'resource_type': self.resource_type,
            'difficulty': self.difficulty,
            'created_at': self.created_at.isoformat()
        }
