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

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "______" 

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'nehutipvt@gmail.com'
app.config['MAIL_PASSWORD'] = '____'
app.config['MAIL_DEFAULT_SENDER'] = 'nehutipvt@gmail.com'

# Check if Redis is running, fallback to simple cache if not
try:
    r = redis.Redis(host='localhost', port=6379, socket_connect_timeout=1)
    r.ping()
    app.config['CACHE_TYPE'] = 'redis'
    app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
    print("Redis connected successfully. Caching is using Redis.")
except redis.RedisError as e:
    print(f"WARNING: Redis is not running ({e}). Caching will use 'simple' in-memory cache.")
    app.config['CACHE_TYPE'] = 'simple'

db.init_app(app)
jwt.init_app(app)
mail.init_app(app)
cache.init_app(app)
CORS(app)

app.register_blueprint(student_b)
app.register_blueprint(company_b)
app.register_blueprint(auth_b)
app.register_blueprint(drive_b)
app.register_blueprint(admin_b)
app.register_blueprint(app_b)

def create_admin():
    if_admin = User.query.filter_by(role='admin').first()
    if not if_admin:
        hashed_pass=generate_password_hash('admin123')
        admin_user = User (
            name = 'Admin',
            email = 'admin@admin.com',
            password = hashed_pass,
            role = 'admin',
            is_active = True
        )
        db.session.add(admin_user)                
        db.session.commit()
        print("admin created successfully")
    else:
        return "admin existing already"

@app.route('/')
def home():
    return "Placement Portal Running"
  
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_admin()
    app.run(debug=True)    
