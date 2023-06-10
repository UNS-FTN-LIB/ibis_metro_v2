from flask import Blueprint, jsonify, request
from Simulator import Simulator

metro = Blueprint('metro', __name__)

simulator = Simulator()

@metro.route('/', methods=['GET'])
def get_metro_data():
    metro_status = {
        "railway_ab_position" : simulator.railway_ab.position,
        "railway_ac_position" : simulator.railway_ac.position,
        "railway_bc_position" : simulator.railway_bc.position
    }
    return jsonify(metro_status)

@metro.route('/train-a', methods=['GET'])
def get_a_train_data():
    metro_status = {
        "position" : simulator.train_a.train_position,
        "train_direction" : simulator.train_a.train_direction,
        "speed" : simulator.train_a.train_speed,
        "doors" : simulator.train_a.train_door
    }
    return jsonify(metro_status)


@metro.route('/train-b', methods=['GET'])
def get_b_train_data():
    metro_status = {
        "position" : simulator.train_b.train_position,
        "train_direction" : simulator.train_b.train_direction,
        "speed" : simulator.train_b.train_speed,
        "doors" : simulator.train_b.train_door
    }
    return jsonify(metro_status)


@metro.route('/train-c', methods=['GET'])
def get_c_train_data():
    metro_status = {
        "position" : simulator.train_c.train_position,
        "train_direction" : simulator.train_c.train_direction,
        "speed" : simulator.train_c.train_speed,
        "doors" : simulator.train_c.train_door
    }
    return jsonify(metro_status)


@metro.route('/start', methods=['POST'])
def start_metro():
    data = request.json.get('button')
    if data == '0':
        data = False
    elif data == '1':
        data = True

    simulator.start_thread(data)

    if data:
        return jsonify("Metro is stopped", 200)
    elif not data:
        return jsonify("Metro is started", 200)
