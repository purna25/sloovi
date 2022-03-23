from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_CONNECTION_STRING')
app.config['SECRET_KEY'] = os.getenv('APP_SECRET')
mongo = PyMongo(app)


from .auth_routes import app
from .teplate_routes import app