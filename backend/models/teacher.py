from . import db

class Teacher(db.Model):
    __tablename__ = 'teachers'
    
    teacher_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, unique=True)
    employee_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    subject = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=True)
    is_class_teacher = db.Column(db.Boolean, default=False)  # True if class teacher
    assigned_class = db.Column(db.String(20), nullable=True)  # e.g., "8" (for class teachers)
    assigned_section = db.Column(db.String(10), nullable=True)  # e.g., "A"
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('teacher_profile', uselist=False), overlaps="teacher,user_account")
    marked_attendance = db.relationship('Attendance', foreign_keys='Attendance.marked_by', backref='marker')
    
    def to_dict(self):
        return {
            'teacher_id': self.teacher_id,
            'user_id': self.user_id,
            'employee_id': self.employee_id,
            'subject': self.subject,
            'department': self.department,
            'is_class_teacher': self.is_class_teacher,
            'assigned_class': self.assigned_class,
            'assigned_section': self.assigned_section
        }
