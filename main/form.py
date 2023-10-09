from flask_login import LoginManager, UserMixin
from flask_wtf import FlaskForm
from wtforms import (BooleanField, DecimalField, FileField, PasswordField,
                     RadioField, SelectField, StringField, SubmitField,
                     TextAreaField,MultipleFileField)
from wtforms.fields import SelectMultipleField
from wtforms.validators import (DataRequired, Email, EqualTo, Length, Optional,
                                ValidationError)

from .models import User


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

# List of all areas in Addis Ababa
areas_list = [
    "Addis Ketema",
    "Addis Sefer",
    "Adiss",
    "Agusta",
    "Akaki-Kaliti",
    "Amanuel Area",
    "American Gibi",
    "Arat Kilo",
    "Ayat",
    "Ayertena",
    "Bantyiketu",
    "Beg Tera",
    "Beherawi",
    "Bekelo Bet",
    "Berberee Berenda",
    "Besrat Gebriel",
    "Bole",
    "Bole Ayat",
    "Bole Mikael",
    "Bulgariya Mazoriya",
    "Cabana",
    "Ched Tera",
    "Coca",
    "Darmar",
    "District 3",
    "Doro Tera",
    "Gebre Kristos Bete Kristiyan",
    "Geja Seffer",
    "Gerji",
    "Ghiliffalegn Stream",
    "Giorgis",
    "Goma Kuteba",
    "Gotera",
    "Great Acachi",
    "Gulele Bota",
    "Haile Garment",
    "Hana",
    "Harbu Shet’",
    "Irtu Bota",
    "Jemo",
    "Jos Hanssen",
    "Kara",
    "Kara Alo",
    "Kazanchis",
    "Kera",
    "Ketena Hulet",
    "Kirkos",
    "Kolfe Keranio",
    "Kolfe Keranyo",
    "Korech Tera",
    "Kotebe",
    "Kurtume Stream",
    "Lafto",
    "Lancha",
    "Lebu",
    "Lebu Mebrathayil",
    "Legahar",
    "Lideta",
    "Lideta Gebri’El Bete Kristiyan",
    "Mechare Meda",
    "Megenagna",
    "Mekanisa",
    "Mekanisa Abo",
    "Menahereya Kazanchis",
    "Menisa",
    "Meshuwalekiya",
    "Meskel Flower",
    "Mesob Tera",
    "Mexico",
    "Microlink Project",
    "Minalesh Tera",
    "Mobil",
    "Molla Maru",
    "Nefas Silk-Lafto",
    "Olympia",
    "Piassa (piazza)",
    "Repi",
    "Riche",
    "Rwanda",
    "Sarbet",
    "Saris",
    "Saris Abo Area",
    "Sebategna",
    "Sengatera",
    "Shekela Tera",
    "Shema Tera",
    "Somale Tera",
    "Soste Kuter Mazoria (Total)",
    "Sunshine Real state",
    "Tekelehaymanot",
    "Tor Hiylloch",
    "Urael",
    "Vatican",
    "Wello Sefer",
    "Yedejazmach Alula Irsha",
    "Yeka",
    "Yeka Bole Bota",
    "Zenebework"
]

# list of tuples for choices
area_choices = [('', '')] + [(area, area) for area in areas_list]



class UploadForm(FlaskForm):
    city = SelectField('City',choices=area_choices, validators=[DataRequired()])
    contact_information = StringField('Contact Information', validators=[DataRequired()])
    # catagories = StringField('catagories', validators=[DataRequired()])
    catagories = SelectField('Categories', choices=[('', ''), ('HouseRent', 'House Rent'), ('CarRent', 'Car Rent'),('CarSell', 'Car Sell'),('HomeSell', 'Home Sell'),('Land Sell', 'Land Sell'),('other', 'Others')])
    sub_City = SelectField('Sub_City',choices=area_choices, validators=[DataRequired()])
    # kebele = StringField('Kebele', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    # max_price = StringField('max_rice', validators=[DataRequired()])
    image_filenames = MultipleFileField('Upload Image')
    video_filename = FileField('Upload Video')
    # document_filename = FileField('Upload Document')
    submit = SubmitField('Post')

class SearchForm(FlaskForm):
    catagories = SelectField('Catagories', choices=[('', ''),('HouseRent', 'House Rent'), ('CarRent', 'Car Rent'),('CarSell', 'Car Sell'),('HouseSell', 'House Sell'),('Land Sell', 'Land Sell'),('other', 'Others')])
    min_price = DecimalField('Minimum Price',validators=[Optional()])
    max_price = DecimalField('Maximum Price', validators=[Optional()])
    city = SelectField('City',choices=area_choices)
    sub_City = SelectField('Sub_City',choices=area_choices)
    submit = SubmitField('Search')

class SearchForms(FlaskForm):
    categories = SelectField('Categories', choices=[('', ''),('HouseRent', 'House Rent'), ('CarRent', 'Car Rent'),('CarSell', 'Car Sell')])
    min_price = DecimalField('Minimum Price', places=2)
    max_price = DecimalField('Maximum Price', places=2)
    city = SelectField('City',choices=area_choices)
    submit = SubmitField('Search')
class SearchFormss(FlaskForm):
    categories = SelectField('Categories', choices=[('', ''),('HouseRent', 'House Rent'),('HouseSell', 'House Sell'), ('CarRent', 'Car Rent'),('CarSell', 'Car Sell'),('Land Sell', 'Land Sell'),('other', 'Others')])
    min_price = DecimalField('Minimum Price', places=2)
    max_price = DecimalField('Maximum Price', places=2)
    city = SelectField('City',choices=area_choices)
    sub_City = SelectField('City',choices=area_choices)
    submit = SubmitField('Search')



class DeleteForm(FlaskForm):
    pass
