import os

# TODO add fill list with updated topics for INview
topics = {
    "train_aa": "TrainAA",
    "speed_a": "SpeedA",
    "doors_a": "DoorsA",

    "train_ba": "TrainBA",
    "speed_b": "SpeedB",
    "doors_b": "DoorsB",

    "train_ca": "TrainCA",
    "speed_c": "SpeedC",
    "doors_c": "DoorsC",

    "passing_ab": "PassingAB",
    "passing_ac": "PassingAC",
    "passing_bc": "PassingBC",

    "emergency": "EmergencyStopMetro",
    "emergency_view": "EmergencyMetroView",
    "start": "MetroStartButton"
}

broker = os.getenv('BROKER')
port = int(os.getenv('PORT'))
client_id = os.getenv('CLIENT_ID')
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
