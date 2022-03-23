from . import (
    app, request, mongo, jsonify
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json
from bson import json_util
import jwt


@app.route('/register', methods=["POST"])
def register():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        if data and data.get('email') and data.get('password'):
            check = mongo.db.user.find_one({'email': data['email']})
            if check:
                return jsonify({'message': 'User already exists!'}), 409
            else:
                hashed_password = generate_password_hash(data.get('password'), method='sha256')
                user = mongo.db.user.insert_one({
                    'first_name': data.get('first_name'),
                    'last_name': data.get('last_name'),
                    'email': data.get('email'),
                    'password': hashed_password
                })

                return jsonify({'message': 'User created!'}), 201
        else:
            return jsonify({'message': 'Email and password are required!'}), 400
    else:
        return jsonify({'message': 'Invalid content type!'}), 400


@app.route('/login', methods=["POST"])
def login():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        if data and data.get('email') and data.get('password'):
            user = mongo.db.user.find_one({'email': data['email']})
            if not user:
                return jsonify({'message': 'User does not exist!'}), 404
            if check_password_hash(user['password'], data['password']):
                user = json.loads(json_util.dumps(user))
                token = jwt.encode({
                    'public_id': user['_id'],
                    'iat': datetime.utcnow(),
                    'exp': datetime.utcnow() + timedelta(hours=3)
                }, app.config['SECRET_KEY'])
                return jsonify({'message': 'User logged in!', 'token': token}), 200
            else:
                return jsonify({'message': 'Incorrect Password'})
        else:
            return jsonify({'message': 'Email and password are required!'}), 400
    else:
        return jsonify({'message': 'Invalid content type!'}), 400
