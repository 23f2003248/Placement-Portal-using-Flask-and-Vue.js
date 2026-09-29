import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from models import db, User
from werkzeug.security import generate_password_hash
import redis
from routes.student_route import student_b
from routes.company_route import company_b
from routes.drive_route import drive_b
from routes.authorise import auth_b
from routes.application_route import app_b
from routes.admin_route import admin_b
from flask_jwt_extended import JWTManager
from celery_app import celery
from extensions import mail, cache
from flask_cors import CORS

app = Flask(__name__)
jwt = JWTManager()

database_url = os.getenv("DATABASE_URL")

if database_url:
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'nehutipvt@gmail.com'
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = 'nehutipvt@gmail.com'

redis_url = os.getenv("REDIS_URL")

if redis_url:
    app.config['CACHE_TYPE'] = 'redis'
    app.config['CACHE_REDIS_URL'] = redis_url
    print("Redis configured successfully.")
else:
    app.config['CACHE_TYPE'] = 'simple'
    print("WARNING: REDIS_URL not found. Using simple in-memory cache.")

db.init_app(app)
jwt.init_app(app)
mail.init_app(app)
cache.init_app(app)

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
CORS(app, origins=[frontend_url])

app.register_blueprint(student_b)
app.register_blueprint(company_b)
app.register_blueprint(auth_b)
app.register_blueprint(drive_b)
app.register_blueprint(admin_b)
app.register_blueprint(app_b)


def create_admin():
    if_admin = User.query.filter_by(role='admin').first()

    if not if_admin:
        hashed_pass = generate_password_hash(os.getenv("ADMIN_PASSWORD"))

        admin_user = User(
            name='Admin',
            email='admin@admin.com',
            password=hashed_pass,
            role='admin',
            is_active=True
        )

        db.session.add(admin_user)
        db.session.commit()
        print("admin created successfully")
    else:
        return "admin existing already"


@app.route('/')
def home():
    return "Placement Portal Running"


with app.app_context():
    db.create_all()
    create_admin()


if __name__ == "__main__":
    app.run(debug=True)