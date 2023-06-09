from flask import Blueprint, jsonify, request
from Simulator import Simulator

railway = Blueprint('railway', __name__)

simulator = Simulator()

@railway.route('/position/ab', methods=['GET'])
def get_position_ab():
    return jsonify(simulator.railway_ab.position)


@railway.route('/position/ab', methods=['PUT'])
def update_position_ab():
    print(request)
    new_position_value = request.json.get('position')
    simulator.railway_ab.position = new_position_value
    return jsonify(simulator.railway_ab.position)


@railway.route('/position/ac', methods=['GET'])
def get_position_ac():
    return jsonify(simulator.railway_ac.position)


@railway.route('/position/ac', methods=['PUT'])
def update_position_ac():
    new_position_value = request.json.get('position')
    simulator.railway_ac.position = new_position_value
    return jsonify(simulator.railway_ac.position)


@railway.route('/position/bc', methods=['GET'])
def get_position_bc():
    return jsonify(simulator.railway_bc.position)


@railway.route('/position/bc', methods=['PUT'])
def update_position_bc():
    new_position_value = request.json.get('position')
    simulator.railway_bc.position = new_position_value
    return jsonify(simulator.railway_bc.position)
