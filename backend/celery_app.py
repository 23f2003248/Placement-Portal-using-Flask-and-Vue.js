from celery import Celery

def create_app():
    from flask import Flask
    from models import db
    from extensions import mail
    from werkzeug.security import generate_password_hash

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'nehutipvt@gmail.com'
    app.config['MAIL_PASSWORD'] = 'ayji waak rgug hbsx'
    app.config['MAIL_DEFAULT_SENDER'] = 'nehutipvt@gmail.com'

    db.init_app(app)
    mail.init_app(app)
    return app

flask_app = create_app()

from celery.schedules import crontab

celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

celery.conf.imports = ('tasks',)

celery.conf.beat_schedule = {
    'daily-reminder-at-midnight': {
        'task': 'tasks.daily_reminder',
        'schedule': crontab(hour=0, minute=0),
    },
    'monthly-activity-report-first-day': {
        'task': 'tasks.monthly_report',
        'schedule': crontab(day_of_month=1, hour=0, minute=0),
    },
}