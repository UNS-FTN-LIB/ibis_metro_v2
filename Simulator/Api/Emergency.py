from flask import Blueprint, jsonify, request
from Simulator import Simulator

emergency = Blueprint('emergency', __name__)

simulator = Simulator()

@emergency.route('/', methods=['GET'])
def get_position():
    return jsonify(simulator.emergency)


@emergency.route('/', methods=['PUT'])
def update_position():
    new_emergency_value = request.json.get('emergency')
    simulator.emergency = new_emergency_value
    return jsonify(simulator.emergency)
