from flask import Blueprint, render_template, request, flash, redirect, url_for
from .form import RegistrationForm




auth= Blueprint('auth', __name__)
@auth.route('/')
def home():
    return render_template('home.html')


# @route.route('/login', methods=['GET', 'POST'])
# def login():
#     return render_template('login.html', title='Login', form=form)


@auth.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)

# @route.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('auth.register'))



