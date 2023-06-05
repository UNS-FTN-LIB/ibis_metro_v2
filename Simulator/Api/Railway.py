from flask import Blueprint, jsonify, request
from Simulator import Simulator

railway = Blueprint('railway', __name__)

simulator = Simulator()

@railway.route('/position', methods=['GET'])
def get_position():
    return jsonify(simulator.railway_position)


@railway.route('/position', methods=['PUT'])
def update_position():
    new_position_value = request.json.get('door')
    simulator.railway_position(new_position_value)
    return jsonify(simulator.railway_position)
