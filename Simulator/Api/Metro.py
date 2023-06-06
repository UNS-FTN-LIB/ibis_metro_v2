from flask import Blueprint, jsonify, request
from Simulator import Simulator

metro = Blueprint('metro', __name__)

simulator = Simulator()

@metro.route('/train-a', methods=['GET'])
def get_a_train_data():
    metro_status = {
        "position" : simulator.train_a.train_position,
        "train_direction" : simulator.train_a.train_direction,
        "speed" : simulator.train_a.train_speed,
        "doors" : simulator.train_a.train_door,
        "railway_ab_position" : simulator.railway_ab.position,
        "railway_ac_position" : simulator.railway_ac.position
    }
    return jsonify(metro_status)


@metro.route('/train-b', methods=['GET'])
def get_b_train_data():
    metro_status = {
        "position" : simulator.train_b.train_position,
        "train_direction" : simulator.train_b.train_direction,
        "speed" : simulator.train_b.train_speed,
        "doors" : simulator.train_b.train_door,
        "railway_ab_position" : simulator.railway_bc.position,
        "railway_ac_position" : simulator.railway_ab.position
    }
    return jsonify(metro_status)


@metro.route('/train-c', methods=['GET'])
def get_c_train_data():
    metro_status = {
        "position" : simulator.train_c.train_position,
        "train_direction" : simulator.train_c.train_direction,
        "speed" : simulator.train_c.train_speed,
        "doors" : simulator.train_c.train_door,
        "railway_ab_position" : simulator.railway_ac.position,
        "railway_ac_position" : simulator.railway_bc.position
    }
    return jsonify(metro_status)
