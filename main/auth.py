from flask import Blueprint, render_template, request, flash, redirect, url_for,abort, jsonify
from flask_login import login_user, current_user, login_required, logout_user,LoginManager
from .models import db, User,Listing
from .form import RegistrationForm, LoginForm,UploadForm,SearchForm,DeleteForm,SearchFormss
from flask_bcrypt import Bcrypt
import os
from werkzeug.utils import secure_filename
from flask import current_app
from main import create_app
import uuid


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


@auth.route('/post', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        author_id = current_user.id

        # Generate a unique filename (e.g., using a UUID)
        unique_filename = str(uuid.uuid4()) + secure_filename(form.image_filename.data.filename)
        image_upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], unique_filename)

        # Save the uploaded file with the unique filename
        form.image_filename.data.save(image_upload_path)

        if form.video_filename.data:
            # Similar logic for generating a unique filename for videos
            video_unique_filename = str(uuid.uuid4()) + secure_filename(form.video_filename.data.filename)
            video_upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], video_unique_filename)
            form.video_filename.data.save(video_upload_path)

        listing = Listing(
            author_id=author_id,
            catagories=form.catagories.data,
            city=form.city.data,
            contact_information=form.contact_information.data,
            sub_City=form.sub_City.data,
            description=form.description.data,
            price=form.price.data,
            image_filename=unique_filename,  # Store the unique filename in the database
            video_filename=video_unique_filename if form.video_filename.data else None  # Store the unique video filename
        )
        db.session.add(listing)
        db.session.commit()

        flash('Posted successfully', 'success')
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
    form = SearchFormss()
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


    if form.validate_on_submit():
        categories = form.categories.data
        min_price = form.min_price.data
        max_price = form.max_price.data
        city = form.city.data
        sub_City= form.sub_City.data
        print("correct")
        # Implement your search logic based on the parameters
        for item in listings_data:
            # Check if the item matches the selected category
            if categories and item['catagories'] != categories:
                continue

            item_price = float(item['price'])
            # Check if the item's price is within the selected price range
            # is not None
            if min_price and item_price <= float(min_price):
                continue
            if max_price  and item_price >= float(max_price):
                continue


            # Check if the item's sub_City matches the selected city
            if sub_City and item['sub_City'] != sub_City:
                continue

            # Check if the item's city matches the selected city
            if city and item['city'] != city:
                continue
            print(item)
            # If all criteria match, add the item to the results
            results.append(item)
            # return redirect(url_for('auth.home'))


    return render_template('service.html', listings=listings_data, form=form, results=results)



@auth.route('/get_data', methods=['GET'])
def get_data():
    # Query the database to get the data
    data = Listing.query.all()

    # Create a list to store the formatted data
    formatted_data = []

    # Iterate through the data and format it
    for listing in data:
        formatted_item = {
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
        formatted_data.append(formatted_item)
    print(formatted_data)
    # Convert the formatted data to JSON using jsonify
    return jsonify(formatted_data)


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

@auth.route('/post/<int:listing_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(listing_id):
    # Retrieve the listing
    listing = Listing.query.get_or_404(listing_id)

    # Check if the current user has permission to update the post
    if current_user != listing.author:
        abort(403)  # Return a 403 Forbidden error if the user doesn't have permission

    # Create the form for updating the post
    form = UploadForm()

    if form.validate_on_submit():
        # Update the fields of the existing listing object
        listing.catagories = form.catagories.data
        listing.city = form.city.data
        listing.contact_information = form.contact_information.data
        listing.sub_City = form.sub_City.data
        listing.description = form.description.data
        listing.price = form.price.data

        # Process file uploads
        if form.image_filename.data:
            # Generate a unique filename for the new image
            new_image_filename = str(uuid.uuid4()) + secure_filename(form.image_filename.data.filename)
            new_image_upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], new_image_filename)
            os.makedirs(os.path.dirname(new_image_upload_path), exist_ok=True)
            form.image_filename.data.save(new_image_upload_path)

            # Remove the old image if it exists
            if listing.image_filename:
                old_image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], listing.image_filename)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

            # Update the listing's image filename with the new unique filename
            listing.image_filename = new_image_filename

        if form.video_filename.data:
            # Similar logic for generating a unique filename for videos
            new_video_filename = str(uuid.uuid4()) + secure_filename(form.video_filename.data.filename)
            new_video_upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], new_video_filename)
            os.makedirs(os.path.dirname(new_video_upload_path), exist_ok=True)
            form.video_filename.data.save(new_video_upload_path)

            # Remove the old video if it exists
            if listing.video_filename:
                old_video_path = os.path.join(current_app.config["UPLOAD_FOLDER"], listing.video_filename)
                if os.path.exists(old_video_path):
                    os.remove(old_video_path)

            # Update the listing's video filename with the new unique filename
            listing.video_filename = new_video_filename

        # Commit the changes to the database
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('auth.view_listing', listing_id=listing.id))

    elif request.method == 'GET':
        # Populate the form with the current values of the listing
        form.catagories.data = listing.catagories
        form.city.data = listing.city
        form.contact_information.data = listing.contact_information
        form.sub_City.data = listing.sub_City
        form.description.data = listing.description
        form.price.data = listing.price
        form.image_filename.data = listing.image_filename

    return render_template('post.html', form=form, listing=listing)



@auth.route('/post/<int:listing_id>/delete', methods=['POST'])
@login_required
def delete_post(listing_id):
    # Retrieve the listing and its associated image filename
    listing = Listing.query.get_or_404(listing_id)
    image_filename = listing.image_filename

    # Check if the user has permission to delete the post
    if current_user != listing.author:
        abort(403)

    # Delete the image file from the "uploads" folder
    if image_filename:
        image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)

    # Delete the post from the database
    db.session.delete(listing)
    db.session.commit()

    flash('Post deleted successfully', 'success')
    return redirect(url_for('auth.service'))






@auth.route('/searches', methods=['GET', 'POST'])
def searchss():
    form = SearchFormss()
    results = []  # Initialize an empty list to store search results
        # Query the database to get the data
    data = Listing.query.all()

    # Create a list to store the formatted data
    formatted_data = []

    # Iterate through the data and format it
    for listing in data:
        formatted_item = {
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
        formatted_data.append(formatted_item)
    if form.validate_on_submit():
        categories = form.categories.data
        min_price = form.min_price.data
        max_price = form.max_price.data
        city = form.city.data
        sub_City = form.sub_City.data
        print("correct")
        # Implement your search logic based on the parameters
        for item in formatted_data:
            # Check if the item matches the selected category
            if categories and item['catagories'] != categories:
                continue

            item_price = float(item['price'])
            # Check if the item's price is within the selected price range
            if min_price and item_price <= float(min_price):
                continue
            if max_price and item_price >= float(max_price):
                continue

            # Check if the item's city matches the selected city
            if city and item['city'] != city:
                continue

            # Check if the item's sub_City matches the selected city
            if sub_City and item['sub_City'] != sub_City:
                continue
            print(item)
            # If all criteria match, add the item to the results
            results.append(item)
        #   return redirect(url_for('auth.home'))

    return render_template('search_resultss.html', form=form, results=results)












@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
