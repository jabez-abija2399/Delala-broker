from flask import Flask,redirect,url_for
 
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'a8476bd73b1e5123741e21f3642dec0e'
    from main.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
