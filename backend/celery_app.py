import os
from celery import Celery
from celery.schedules import crontab

def create_app():
    from flask import Flask
    from models import db
    from extensions import mail

    app = Flask(__name__)

    database_url = os.getenv("DATABASE_URL")

    if database_url:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'nehutipvt@gmail.com'
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
    app.config['MAIL_DEFAULT_SENDER'] = 'nehutipvt@gmail.com'

    db.init_app(app)
    mail.init_app(app)

    return app


flask_app = create_app()

celery = Celery(
    'tasks',
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL")
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