from flask import Blueprint, request, jsonify

from app import models

api = Blueprint('api', __name__)


@api.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'This is great'})
