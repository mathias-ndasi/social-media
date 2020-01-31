from flask import jsonify, Blueprint, request

post_api = Blueprint('post_api', __name__, url_prefix='/post')
