from flask import jsonify, request
from bson import ObjectId
from functools import wraps
from . import app, mongo
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].strip().split("Bearer ")[1]
            # print(auth_value)
            # token = auth_value[6:]
            if not token:
                return jsonify({'message': 'Token is missing!'}), 401
        else:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # print(token)
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = mongo.db.user.find_one({'_id': ObjectId(data['public_id']['$oid'])})
            print(current_user)
            # request.json['user'] = current_user
        except Exception as e:
            print(e)
            return jsonify({'message': 'Token is invalid!'}), 401
        
        return f(current_user, *args, **kwargs)

    return decorated

