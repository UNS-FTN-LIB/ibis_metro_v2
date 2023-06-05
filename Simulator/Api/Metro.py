from flask import Blueprint, jsonify, request
from Simulator import Simulator

metro = Blueprint('metro', __name__)

simulator = Simulator()

@metro.route('/', methods=['GET'])
def get_position():
    metro_status = {
        "position" : simulator.train_position,
        "train_direction" : simulator.train_direction,
        "speed" : simulator.train_speed,
        "doors" : simulator.train_door,
        "railway_position" : simulator.railway_position
    }
    return jsonify(metro_status)
