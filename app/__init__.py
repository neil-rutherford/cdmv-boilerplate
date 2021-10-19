from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
moment = Moment()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    moment.init_app(app)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp)

    from app.content import bp as content_bp
    app.register_blueprint(content_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

from app import models