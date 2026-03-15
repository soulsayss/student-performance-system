from app import create_app
from models import User

app = create_app()

with app.app_context():
    teachers = User.query.filter_by(role='teacher').all()
    print("Teachers in database:")
    for t in teachers[:3]:
        print(f"  {t.name}: {t.email}")
