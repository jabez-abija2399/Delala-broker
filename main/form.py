from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,SelectField,RadioField,BooleanField,TextAreaField,FileField,DecimalField
from wtforms.validators import DataRequired,Length,Email,EqualTo,Optional,ValidationError
from .models import User
from wtforms.fields import SelectMultipleField
from flask_login import LoginManager, UserMixin



class RegistrationForm(FlaskForm,UserMixin):
    FullName = StringField('Full Name:', validators=[DataRequired(), Length(min=4, max=100)],render_kw={"placeholder": "YourFullName"})
    # username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email:', validators=[Optional(), Email()],render_kw={"placeholder": "youremail@gmail.com"})
    phoneNumber = StringField('Phone Number:', validators=[DataRequired(), Length(min=10, max=10)],render_kw={"placeholder": "YourPhoneNumber"})
    gender = RadioField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    password = PasswordField('password:', validators=[DataRequired()],render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password:', validators=[DataRequired(), EqualTo('password')],render_kw={"placeholder": "ReTypePassword"})
    submit = SubmitField('Sign Up')
    def validate_username(self, phoneNumber):
        user =User.query.filter_by(phoneNumber=phoneNumber.data).first()
        if user:
            raise ValidationError('that phone number is taken. please choose diffrent one')
        
    def validate_username(self, email):
        user =User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('that email is taken. please choose diffrent one')
class LoginForm(FlaskForm):
    phoneNumber = StringField('phone Number', validators=[DataRequired()],render_kw={"placeholder": "YourPhoneNumber"})
    password = PasswordField('Password', validators=[DataRequired()],render_kw={"placeholder": "Password"})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UploadForm(FlaskForm):
    city = StringField('City', validators=[DataRequired()])
    contact_information = StringField('Contact Information', validators=[DataRequired()])
    # catagories = StringField('catagories', validators=[DataRequired()])
    catagories = SelectField('Categories', choices=[('', ''), ('HouseRent', 'House Rent'), ('CarRent', 'Car Rent'),('CarSell', 'Car Sell'),('HomeSell', 'Home Sell'),('Land Sell', 'Land Sell'),('other', 'Others')])
    sub_City = TextAreaField('subcity', validators=[DataRequired()])
    # kebele = StringField('Kebele', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    # max_price = StringField('max_rice', validators=[DataRequired()])
    image_filename = FileField('Upload Image')
    video_filename = FileField('Upload Video')
    # document_filename = FileField('Upload Document')


class SearchForm(FlaskForm):
    catagories = SelectField('Catagories', choices=[('', ''),('HouseRent', 'House Rent'), ('CarRent', 'Car Rent'),('CarSell', 'Car Sell'),('HouseSell', 'House Sell'),('other', 'Others')])
    min_price = DecimalField('Minimum Price')
    max_price = DecimalField('Maximum Price')
    city = SelectField('City')
    sub_City = SelectField('Sub City')
    submit = SubmitField('Search')