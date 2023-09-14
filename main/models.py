from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from datetime import datetime

db = SQLAlchemy()
login_manager = LoginManager()  # Instantiate the LoginManager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(255), nullable=False)
    phoneNumber = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.Enum('Male', 'Female', name='gender_enum'))
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp(), nullable=False)


    def __repr__(self):
        return f"<User(id={self.id}, fullName='{self.fullName}', username='{self.username}', " \
               f"phoneNumber='{self.phoneNumber}', gender='{self.gender}')>"


class Listing(db.Model):
    __tablename__ = 'listings'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(255), nullable=False)
    sub_City = db.Column(db.Text, nullable=False)
    contact_information = db.Column(db.String(255), nullable=True)
    # kebele = db.Column(db.String(50), nullable=False)
    catagories = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.String(50), nullable=False)
    # max_price = db.Column(db.String(50), nullable=False) 
    image_filename = db.Column(db.String(255), nullable=True)
    video_filename = db.Column(db.String(255))
    # document_filename = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    
    def __repr__(self):
        return f"<Listing(id={self.id}, city='{self.city}')>"
