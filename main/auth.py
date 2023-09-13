from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user,LoginManager
from .models import db, User,Listing
from .form import RegistrationForm, LoginForm,UploadForm
from flask_bcrypt import Bcrypt
import os
from werkzeug.utils import secure_filename
from flask import current_app
from main import create_app


auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()
login_manager = LoginManager()
# auth.config["UPLOAD_FOLDER"] = "uploads"  # Specify the folder where you want to save uploaded files
# auth.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif", "mp4", "avi", "pdf", "doc", "docx"}  # Specify allowed file extensions


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))

@auth.route('/')
@login_required
def home():
    return render_template('home.html')


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


@auth.route('/post', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        # Process the form data and file uploads
        image_filename = None
        video_filename = None
        document_filename = None

        if form.image_filename.data:
            image_filename = secure_filename(form.image_filename.data.filename)
            image_upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], image_filename)
            os.makedirs(os.path.dirname(image_upload_path), exist_ok=True)
            form.image_filename.data.save(image_upload_path)

        if form.video_filename.data:
            video_filename = secure_filename(form.video_filename.data.filename)
            video_upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], video_filename)
            os.makedirs(os.path.dirname(video_upload_path), exist_ok=True)
            form.video_filename.data.save(video_upload_path)
        listing = Listing(
            catagories=form.catagories.data,
            city=form.city.data, 
            contact_information=form.contact_information.data, 
            sub_City=form.sub_City.data, 
            # kebele=form.kebele.data, 
            description=form.description.data, 
            price=form.price.data, 
            image_filename=image_filename, 
            video_filename=video_filename
        )
        db.session.add(listing)
        db.session.commit()

        return redirect(url_for('auth.service'))
    return render_template('post.html', form=form)

# @auth.route('/Services')
# @login_required
# def service():
#     return render_template('service.html')
        
@auth.route('/Catagories')
@login_required
def catagories():
    return render_template('catagories.html')

@auth.route('/contact')
@login_required
def contact():
    return render_template('contact.html')


@auth.route('/about')
@login_required
def about():
    return render_template('about.html')



@auth.route('/Services', methods=['GET'])
@login_required
def service():
    # Fetch data from the database
    all_listings = Listing.query.all()

    # Create a list to store the data you want to display
    listings_data = []

    for listing in all_listings:
        listing_info = {
            'id': listing.id,
            'city': listing.city,
            'catagories': listing.catagories,
            'sub_City': listing.sub_City,
            'price': listing.price,
            'image_filename': listing.image_filename,
            'description': listing.description,
            'contact_information': listing.contact_information,
            # 'kebele': listing.kebele,
            'video_filename': listing.video_filename,
            

        }
        listings_data.append(listing_info)

    return render_template('service.html', listings=listings_data)


@auth.route('/post/<int:listing_id>', methods=['GET'])
@login_required
def view_listing(listing_id):
    # Fetch the specific listing from the database using the listing_id
    listing = Listing.query.get(listing_id)

    if not listing:
        # Handle the case where the listing with the given ID doesn't exist
        flash('Listing not found', 'danger')
        return redirect(url_for('auth.service'))

    return render_template('details.html', listing=listing)





@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
