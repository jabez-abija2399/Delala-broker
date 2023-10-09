from flask import Blueprint, render_template, request, flash, redirect, url_for,abort, jsonify
from flask_login import login_user, current_user, login_required, logout_user,LoginManager
from ..models import db, User,Listing
from ..form import RegistrationForm, LoginForm,UploadForm,SearchForm,DeleteForm,SearchFormss
from flask_bcrypt import Bcrypt
import os
from werkzeug.utils import secure_filename
from flask import current_app
from main import create_app
import uuid
from ..utils import capitalize_first_letter



auth = Blueprint('catagory_display_post_route', __name__)
bcrypt = Bcrypt()
login_manager = LoginManager()
# auth.config["UPLOAD_FOLDER"] = "uploads"  # Specify the folder where you want to save uploaded files
# auth.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif", "mp4", "avi", "pdf", "doc", "docx"}  # Specify allowed file extensions


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))

@auth.route('/category/<string:category_name>')
def category(category_name):
    # Query the database to get listings that match the specified category
    listings = Listing.query.filter_by(catagories=category_name).all()
    print(listings)
    return render_template('category.html', category_name=category_name, listings=listings)

@auth.context_processor
def inject_user_name():
    user_name = current_user.fullName if current_user.is_authenticated else None
    capitalized_user_name = capitalize_first_letter(user_name)
    return dict(current_user_name=capitalized_user_name)