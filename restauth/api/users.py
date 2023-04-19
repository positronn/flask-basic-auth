from flask import request
from flask import url_for
from flask import abort
from flask import jsonify

from . import api
from .. import db
from ..model import User


@api.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)
    if User.query.filter_by(username=username).first() is not None:
        abort(409)
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (
        jsonify({'username': user.username}),
        201,
        {'location': url_for('api.get_user', id=user.id, _external=True)}
    )


@api.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(404)
    return jsonify(
        {'username': user.username},
    )
