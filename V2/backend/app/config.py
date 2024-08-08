import os
from celery.schedules import crontab

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Configuration settings for the Flask application.
    """

    # Flask settings
    SECRET_KEY = 'your_secret_key_here'  # Replace with a strong, random key for production
    DEBUG = True  # Enable debug mode for development (set to False in production)

    # Database settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False 

    # Celery settings
    CELERY_BROKER_URL = 'redis://localhost:6379/0'  
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0' 

    # Email settings 
    MAIL_SERVER = 'smtp.gmail.com'  
    MAIL_PORT = 587  
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'your_email@gmail.com'  # Replace with your actual email address
    MAIL_PASSWORD = 'your_email_password'   # Replace with your actual email password 

    # Celery Beat settings
    CELERY_BEAT_SCHEDULE = {
        'send-daily-reminders': {
            'task': 'app.tasks.send_daily_reminders',
            'schedule': crontab(hour=18, minute=0),  # Every day at 6:00 PM 
        },
        'generate-monthly-reports': {
            'task': 'app.tasks.generate_monthly_reports',
            'schedule': crontab(day_of_month=1, hour=0, minute=0),  # 1st day of every month at midnight
        }
    }
