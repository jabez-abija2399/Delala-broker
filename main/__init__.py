from flask import Flask,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .models import db,User
import os
from werkzeug.utils import secure_filename


login_manager = LoginManager()
@login_manager.user_loader

def load_user(user_id):
    return User.query.get(int(user_id))
 
# def create_app():
#     app = Flask(__name__)
#     app.config['SECRET_KEY'] = 'a8476bd73b1e5123741e21f3642dec0e'
#     from main.auth import auth as auth_blueprint
#     app.register_blueprint(auth_blueprint)

#     return app

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'a8476bd73b1e5123741e21f3642dec0e'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///delalas.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["UPLOAD_FOLDER"] = "uploads"  # Specify the folder where you want to save uploaded files
    app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif", "mp4", "avi", "pdf", "doc", "docx"}  # Specify allowed file extensions

    db.init_app(app)
    login_manager.init_app(app)

    from main.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app