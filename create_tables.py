from app import app, db
from models import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
