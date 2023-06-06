import os
import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from earthy.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager = LoginManager(app)
    login_manager.login_view = 'users.login'
    login_manager.login_message_category = 'info'

    from earthy import models
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    
    from earthy.users.routes import users
    from earthy.posts.routes import posts
    from earthy.main.routes import main
    from earthy.errors.handlers import errors
    from earthy.tracker.routes import tracker
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(tracker)

    
    from earthy.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

   
    return app


def create_database(app):
    if not os.path.exists("website/database.db"):
        db.create_all(app=app)
        print("Created database!")