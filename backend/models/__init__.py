from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .student import Student
from .teacher import Teacher
from .attendance import Attendance
from .marks import Marks
from .assignment import Assignment
from .prediction import Prediction
from .resource import Resource
from .alert import Alert
from .achievement import Achievement
from .recommendation import Recommendation
from .career import CareerSuggestion
