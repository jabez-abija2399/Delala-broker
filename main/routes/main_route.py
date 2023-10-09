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



auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()
login_manager = LoginManager()
# auth.config["UPLOAD_FOLDER"] = "uploads"  # Specify the folder where you want to save uploaded files
# auth.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif", "mp4", "avi", "pdf", "doc", "docx"}  # Specify allowed file extensions


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))

@auth.route('/')
def home():
    form = SearchFormss()
    return render_template('home.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(phoneNumber=form.phoneNumber.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('auth.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


def email_already_exists(email):
    # Query your database to check if the email already exists
    existing_user = User.query.filter_by(email=email).first()
    return existing_user is not None
def phone_already_exists(phoneNumber):
    # Query your database to check if the email or phone number already exists
    existing_user = User.query.filter_by(phoneNumber=phoneNumber).first()
    return existing_user is not None

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.home'))
    form = RegistrationForm()
    error_message = None 

    if form.validate_on_submit():
        if email_already_exists(form.email.data):
            error_message = "Email address already exists. Please choose another."
            flash(error_message, 'danger')  # Use flash to display the message
        elif phone_already_exists(form.phoneNumber.data):
            error_message = "Phone number already exists. Please choose another."
            flash(error_message, 'danger')

        else:  
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(fullName=form.FullName.data,
                        email=form.email.data, phoneNumber=form.phoneNumber.data,
                        password=hashed_password)
            db.session.add(user)
            db.session.commit()
                
            return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)

        
@auth.route('/Catagories')
def catagories():
    return render_template('categories.html')

@auth.route('/contact')
def contact():

    return render_template('contact.html')


@auth.route('/about')
def about():
    return render_template('about.html')


# @auth.route('/get_data', methods=['GET'])
# def get_data():
#     # Query the database to get the data
#     data = Listing.query.all()

#     # Create a list to store the formatted data
#     formatted_data = []

#     # Iterate through the data and format it
#     for listing in data:
#         formatted_item = {
#             'id': listing.id,
#             'city': listing.city,
#             'catagories': listing.catagories,
#             'sub_City': listing.sub_City,
#             'price': listing.price,
#             'image_filename': listing.image_filename,
#             'description': listing.description,
#             'contact_information': listing.contact_information,
#             # 'kebele': listing.kebele,
#             'video_filename': listing.video_filename,
            
#         }
#         formatted_data.append(formatted_item)
        
        
#     print(formatted_data)    
#     # Convert the formatted data to JSON using jsonify
#     return jsonify(formatted_data)


@auth.context_processor
def inject_user_name():
    user_name = current_user.fullName if current_user.is_authenticated else None
    capitalized_user_name = capitalize_first_letter(user_name)
    return dict(current_user_name=capitalized_user_name)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.home'))
    