from flask import Blueprint, jsonify, request

mqtt_api = Blueprint('train', __name__)

train_speed_data = {
    'speed': 215
}

train_door_data = {
    'door': 0
}

train_position_data = {
    'position': 123
}


@mqtt_api.route('/speed', methods=['GET'])
def get_speed():
    return jsonify(train_speed_data)


@mqtt_api.route('/door', methods=['GET'])
def get_door():
    return jsonify(train_door_data)


@mqtt_api.route('/door', methods=['PUT'])
def update_door():
    new_door_value = request.json.get('door')
    train_door_data['door'] = new_door_value
    return jsonify(train_door_data)


@mqtt_api.route('/position', methods=['GET'])
def get_position():
    return jsonify(train_position_data)
