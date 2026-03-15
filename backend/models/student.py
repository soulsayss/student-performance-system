from . import db
from datetime import datetime

class Student(db.Model):
    __tablename__ = 'students'
    
    student_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, unique=True, index=True)
    roll_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    class_name = db.Column(db.String(20), nullable=False)
    section = db.Column(db.String(10), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    dob = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('student_profile', uselist=False), overlaps="student,user_account")
    parent = db.relationship('User', foreign_keys=[parent_id], backref='children', overlaps="student_profile,user")
    attendance_records = db.relationship('Attendance', backref='student', cascade='all, delete-orphan')
    marks = db.relationship('Marks', backref='student', cascade='all, delete-orphan')
    assignments = db.relationship('Assignment', backref='student', cascade='all, delete-orphan')
    predictions = db.relationship('Prediction', backref='student', cascade='all, delete-orphan')
    alerts = db.relationship('Alert', backref='student', cascade='all, delete-orphan')
    achievements = db.relationship('Achievement', backref='student', cascade='all, delete-orphan')
    recommendations = db.relationship('Recommendation', backref='student', cascade='all, delete-orphan')
    career_suggestions = db.relationship('CareerSuggestion', backref='student', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'student_id': self.student_id,
            'user_id': self.user_id,
            'roll_number': self.roll_number,
            'class': self.class_name,
            'section': self.section,
            'parent_id': self.parent_id,
            'dob': self.dob.isoformat() if self.dob else None,
            'gender': self.gender
        }
