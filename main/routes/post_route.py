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
from .service_route import service


auth = Blueprint('post_route', __name__)
bcrypt = Bcrypt()
login_manager = LoginManager()

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))


@auth.route('/post', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        author_id = current_user.id

        # Create a list to store the unique image filenames
        image_filenames = []

        # Handle multiple image uploads
        for image_file in form.image_filenames.data:
            # Generate a unique filename for each image
            unique_filename = str(uuid.uuid4()) + secure_filename(image_file.filename)
            image_upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], unique_filename)

            
            # Save the uploaded image with the unique filename
            image_file.save(image_upload_path)

            # Append the unique filename to the list
            image_filenames.append(unique_filename)
            
        if form.video_filename.data:
            # Similar logic for generating a unique filename for the video
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
            image_filenames=image_filenames,  # Store the list of unique image filenames
            video_filename=video_unique_filename if form.video_filename.data else None
        )
        listing.set_image_filenames(image_filenames)
       
        db.session.add(listing)
        db.session.commit()

        flash('Posted successfully', 'success')
        return redirect(url_for('service_route.service'))
    return render_template('post.html', form=form)


@auth.context_processor
def inject_user_name():
    user_name = current_user.fullName if current_user.is_authenticated else None
    capitalized_user_name = capitalize_first_letter(user_name)
    return dict(current_user_name=capitalized_user_name)