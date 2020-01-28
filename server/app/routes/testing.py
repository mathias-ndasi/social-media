from flask import Blueprint, request, jsonify



@api.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'This is great'})
