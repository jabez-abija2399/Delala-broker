from flask import Flask,redirect,url_for
 
def create_app():
    app = Flask(__name__)
    from main.route import route as route_blueprint
    app.register_blueprint(route_blueprint)

    return app
