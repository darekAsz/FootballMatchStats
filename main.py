from app import app, db
from app.models import init_db

db.create_all()
init_db()
