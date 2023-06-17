from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@localhost/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from routes.user_routes import user_routes
from routes.organization_routes import organization_routes
from routes.call_counter_routes import call_counter_routes
from utils.scheduler import scheduler

app.register_blueprint(user_routes)
app.register_blueprint(organization_routes)
app.register_blueprint(call_counter_routes)