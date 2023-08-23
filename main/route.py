from flask import Blueprint, render_template, request, flash, redirect, url_for
from .form import RegistrationForm



auth = Blueprint('auth', __name__)

@auth.route('/')
@login_required
def home():
    return render_template('home.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', title='Login', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html', title='Register', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



