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


auth = Blueprint('service_route', __name__)
bcrypt = Bcrypt()
login_manager = LoginManager()

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))



@auth.route('/Services', methods=['GET'])
def service():
    # Fetch data from the database
    all_listings = Listing.query.all()
    form = SearchFormss()
    results =[]
    # Create a list to store the data you want to display
    listings_data = []
 
    for listing in all_listings:
        listing_info = {
            'id': listing.id,
            'city': listing.city,
            'catagories': listing.catagories,
            'sub_City': listing.sub_City,
            'price': listing.price,
            'image_filename': listing.image_filenames,
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


    return render_template('display_post.html', listings=listings_data, form=form, results=results)

@auth.context_processor
def inject_user_name():
    user_name = current_user.fullName if current_user.is_authenticated else None
    capitalized_user_name = capitalize_first_letter(user_name)
    return dict(current_user_name=capitalized_user_name)

