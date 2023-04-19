# restauth/api/__init__.py
from flask import Blueprint

api = Blueprint('api', __name__)

from . import auth
from . import users
from . import resource
