from . import app, request, mongo, jsonify
from .utils import token_required
from bson import ObjectId, json_util
import json

@app.route('/template/<string:template_id>', methods=["GET"])
@token_required
def get_template(user, template_id):
    if request.headers['Content-Type'] == 'application/json':
        try:
            template = mongo.db.templates.find_one({'_id': ObjectId(template_id), 'user_id': user['_id']})
            if template:
                template = json.loads(json_util.dumps(template))
                return jsonify({'template': template}), 200
            else:
                return jsonify({'message': 'Template not found!'}), 404
        except Exception as e:
            return jsonify({'message': 'Template not found!'}), 404 
    else:
        return jsonify({'message': 'Invalid content type!'}), 400


@app.route('/template/<string:template_id>', methods=["PUT"])
@token_required
def update_template(user, template_id):
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        try:
            template = mongo.db.templates.find_one_and_update(
                filter= {'_id': ObjectId(template_id), 'user_id': user['_id']},
                update= {'$set': data},
            )
            return jsonify({'message': 'Template updated!'}), 200
        except Exception as e:
            return jsonify({'message': 'Template not found!'}), 404 
    else:
        return jsonify({'message': 'Invalid content type!'}), 400


@app.route('/template/<string:template_id>', methods=["DELETE"])
@token_required
def delete_template(user, template_id):
    if request.headers['Content-Type'] == 'application/json':
        try:
            template = mongo.db.templates.find_one_and_delete(
                filter= {'_id': ObjectId(template_id), 'user_id': user['_id']}
            )
            return jsonify({'message': 'Template deleted!'}), 200
        except Exception as e:
            return jsonify({'message': 'Template not found!'}), 404 
    else:
        return jsonify({'message': 'Invalid content type!'}), 400


@app.route('/template', methods=["POST"])
@token_required
def insert_template(user):
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        if data and data.get('template_name') and data.get('subject') and data.get('body'):
            template = mongo.db.templates.insert_one({
                'template_name': data.get('template_name'),
                'subject': data.get('subject'),
                'body': data.get('body'),
                'user_id': user['_id']
            })
            return jsonify({'message': 'Template created!', 'template': str(template.inserted_id)}), 201
        else:
            return jsonify({'message': 'Name, description and template are required!'}), 400
    else:
        return jsonify({'message': 'Invalid content type!'}), 400


@app.route('/template', methods=["GET"])
@token_required
def get_templates(user):
    if request.headers['Content-Type'] == 'application/json':
        templates = mongo.db.templates.find({'user_id': user['_id']})
        templates =  json.loads(json_util.dumps(list(templates)))
        return jsonify({'templates': list(templates)}), 200
    else:
        return jsonify({'message': 'Invalid content type!'}), 400

