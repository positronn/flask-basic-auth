from flask import g
from flask import make_response

from . import api
from .. import auth

@api.route('/api/resource')
@auth.login_required
def get_resource():
    return make_response(
        {'data': f'Hello, {g.user.username}'}
    )
