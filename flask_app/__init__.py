from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
username = 'purna1'
pwd = 'GtGeyiMpTUj6ktAN'
app.config['MONGO_URI'] = f'mongodb+srv://{username}:{pwd}@cluster0.ztuby.mongodb.net/sloovi?retryWrites=true&w=majority'
app.config['SECRET_KEY'] = "sfvgsvlfsbfshjbuy"
mongo = PyMongo(app)


from .auth_routes import app
from .teplate_routes import app