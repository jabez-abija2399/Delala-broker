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



auth = Blueprint('update_post_route', __name__)
bcrypt = Bcrypt()
login_manager = LoginManager()
# auth.config["UPLOAD_FOLDER"] = "uploads"  # Specify the folder where you want to save uploaded files
# auth.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif", "mp4", "avi", "pdf", "doc", "docx"}  # Specify allowed file extensions


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))


@auth.route('/post/<int:listing_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(listing_id):
    # Retrieve the listing
    listing = Listing.query.get_or_404(listing_id)

    # Check if the current user has permission to update the post
    if current_user != listing.author:
        abort(403)  # Return a 403 Forbidden error if the user doesn't have permission

    # Create the form for updating the post, including the ability to upload multiple images
    form = UploadForm()

    if form.validate_on_submit():
        # Update the fields of the existing listing object
        listing.catagories = form.catagories.data
        listing.city = form.city.data
        listing.contact_information = form.contact_information.data
        listing.sub_City = form.sub_City.data
        listing.description = form.description.data
        listing.price = form.price.data
        # listing.image_filenames = form.image_filenames.data

        # Process file uploads
        if form.image_filenames.data:
            # Remove the old images if they exist
            if listing.image_filenames:
                for old_image_filename in listing.image_filenames:
                    old_image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], old_image_filename)
                    # if os.path.exists(old_image_path):
                    #     os.remove(old_image_path)
                    if os.path.exists(old_image_path):
                        try:
                            os.remove(old_image_path)
                        except OSError as e:
                            # Handle the error gracefully (e.g., log it)
                            print(f"Error deleting file: {e}")


            # Generate unique filenames for the new images and save them
            new_image_filenames = []
            for image_file in form.image_filenames.data:
                new_image_filename = str(uuid.uuid4()) + secure_filename(image_file.filename)
                new_image_upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], new_image_filename)
                os.makedirs(os.path.dirname(new_image_upload_path), exist_ok=True)
                image_file.save(new_image_upload_path)
                new_image_filenames.append(new_image_filename)

            # Update the listing's image filenames with the new unique filenames
            listing.set_image_filenames(new_image_filenames)

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
        return redirect(url_for('details_post_route.view_listing', listing_id=listing.id))

    elif request.method == 'GET':
        # Populate the form with the current values of the listing
        form.catagories.data = listing.catagories
        form.city.data = listing.city
        form.contact_information.data = listing.contact_information
        form.sub_City.data = listing.sub_City
        form.description.data = listing.description
        form.price.data = listing.price

    return render_template('post.html', form=form, listing=listing)

@auth.context_processor
def inject_user_name():
    user_name = current_user.fullName if current_user.is_authenticated else None
    capitalized_user_name = capitalize_first_letter(user_name)
    return dict(current_user_name=capitalized_user_name)