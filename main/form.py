from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,SelectField,RadioField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo,Optional,ValidationError
from wtforms.fields import SelectMultipleField



class RegistrationForm(FlaskForm):
    FullName = StringField('Full Name:', validators=[DataRequired(), Length(min=4, max=100)])
    # username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email:', validators=[Optional(), Email()])
    phoneNumber = StringField('Phone Number:', validators=[DataRequired(), Length(min=10, max=10)])
    gender = RadioField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], validators=[DataRequired()])
    password = PasswordField('password:', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password:', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

