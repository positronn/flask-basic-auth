# restauth/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

db = SQLAlchemy()
auth = HTTPBasicAuth()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'the-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    db.init_app(app)
    
    # blueprint for api routes
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
