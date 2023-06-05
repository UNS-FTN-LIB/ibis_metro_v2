from flask import Blueprint, jsonify, request

railway = Blueprint('railway', __name__)

railway_position_data = {
    'position': 215
}


@railway.route('/position', methods=['GET'])
def get_position():
    return jsonify(railway_position_data)


@railway.route('/position', methods=['PUT'])
def update_position():
    new_position_value = request.json.get('door')
    railway_position_data['door'] = new_position_value
    return jsonify(railway_position_data)
