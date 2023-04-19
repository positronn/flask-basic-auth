import time
import jwt
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask import current_app

from .. import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(123))

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_auth_token(self, expires_in=600):
        return jwt.encode(
            {
                'id': self.id, 
                'exp': time.time() + expires_in
            },
            current_app.config['SECRET_KEY'], algorithm='HS256'
        )
    
    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'],
                              algorithms=['HS256'])
        except:
            return 
        return User.query.get(data['id'])
