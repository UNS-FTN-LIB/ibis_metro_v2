from flask import Blueprint, jsonify, request
from Simulator.Simulator import Simulator

train = Blueprint('train', __name__)

simulator = Simulator()


@train.route('/speed', methods=['GET'])
def get_speed():
    return jsonify(simulator.train_speed)


@train.route('/door', methods=['GET'])
def get_door():
    return jsonify(simulator.train_door)


@train.route('/door', methods=['PUT'])
def update_door():
    new_door_value = request.json.get('door')
    simulator.train_door(new_door_value)
    return jsonify(simulator.train_door)


@train.route('/position', methods=['GET'])
def get_position():
    return jsonify(simulator.train_position)
