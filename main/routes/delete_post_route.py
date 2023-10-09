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



auth = Blueprint('delete_post_route', __name__)
bcrypt = Bcrypt()
login_manager = LoginManager()
# auth.config["UPLOAD_FOLDER"] = "uploads"  # Specify the folder where you want to save uploaded files
# auth.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif", "mp4", "avi", "pdf", "doc", "docx"}  # Specify allowed file extensions


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))

@auth.route('/post/<int:listing_id>/delete', methods=['POST'])
@login_required
def delete_post(listing_id):
    # Retrieve the listing and its associated image filenames
    listing = Listing.query.get_or_404(listing_id)
    image_filenames = listing.image_filenames

    # Check if the user has permission to delete the post
    if current_user != listing.author:
        abort(403)

    # Delete the image files from the "uploads" folder
    for image_filename in image_filenames:
        if image_filename:
            image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], image_filename)
            if os.path.exists(image_path):
                try:
                    os.remove(image_path)
                except OSError as e:
                    # Handle the error gracefully (e.g., log it)
                    print(f"Error deleting file: {e}")
                

    # Delete the post from the database
    db.session.delete(listing)
    db.session.commit()

    flash('Post deleted successfully', 'success')
    return redirect(url_for('service_route.service'))

@auth.context_processor
def inject_user_name():
    user_name = current_user.fullName if current_user.is_authenticated else None
    capitalized_user_name = capitalize_first_letter(user_name)
    return dict(current_user_name=capitalized_user_name)