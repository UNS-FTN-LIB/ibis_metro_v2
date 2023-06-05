from flask import Blueprint, jsonify, request

emergency = Blueprint('emergency', __name__)

emergency_data = {
    'emergency': 0
}


@emergency.route('/', methods=['GET'])
def get_position():
    return jsonify(emergency_data)


@emergency.route('/', methods=['PUT'])
def update_position():
    new_emergency_value = request.json.get('emergency')
    emergency_data['emergency'] = new_emergency_value
    return jsonify(emergency_data)
