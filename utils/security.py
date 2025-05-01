from functools import wraps
import jwt
import datetime
import pytz
import bcrypt
from flask import request, jsonify


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            
            auth_header = request.headers['Authorization']
            token = auth_header.split(" ")[1] # Bearer 
            
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, 'ggeasy', algorithms=["HS256"])
            current_user = data['sub']
            
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expired!'}), 401
        
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        
        return f(*args, **kwargs)
    
    return decorated


class SecurityUserController:
    
    @staticmethod
    def hash_password(password:str):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt) 
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password_plain:str, password_hash:str):
        return bcrypt.checkpw(
            password_plain.encode('utf-8'),
            password_hash.encode('utf-8')
        )
    
    @staticmethod
    def generar_token_authorizer(user_id:str, secret_key:str = 'ggeasy', expiracion:int=30):
        utc_now = datetime.datetime.now(pytz.utc)
        
        payload = {
            'sub': user_id,
            'iat': utc_now, 
            'exp': utc_now + datetime.timedelta(minutes=expiracion)
        }

        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return token
