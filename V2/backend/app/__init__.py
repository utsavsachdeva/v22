import os
import logging
from flask_mail import Mail
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from celery import Celery

# Local imports
from app.routes import api
from app.config import Config  # Import your Config class directly

# Initialize extensions (excluding login_manager for now)
db = SQLAlchemy()
migrate = Migrate()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL) 
cors = CORS()
mail = Mail()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """
    Application factory function to create a Flask application instance.
    """

    app = Flask(__name__)

    # Configuration (Use the Config class directly)
    app.config.from_object(Config)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    celery.conf.update(app.config)
    cors.init_app(app)
    mail.init_app(app)

    # Blueprints
    app.register_blueprint(api, url_prefix='/api')

    # Error Handling
    register_error_handlers(app)

    # Initialize login_manager after the app is created
    def init_login_manager(app):
        from flask_login import LoginManager
        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(app) 


    init_login_manager(app)

    # Initialize Celery 
    init_celery(app, celery)

    logger.info('Flask app created successfully!')

    return app

# Celery Task Base Class
class ContextTask(celery.Task):
    """
    Custom Celery task base class to provide Flask app context.
    """

    def __call__(self, *args, **kwargs):
        with create_app().app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask

# Error Handlers
def register_error_handlers(app):
    """
    Registers error handlers for the Flask application.
    """

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error'}), 500

# Initialize Celery (optional)
def init_celery(app, celery):
    """
    Initializes Celery with the Flask application.
    """

    # You can add any further Celery configuration here if needed
    pass 
