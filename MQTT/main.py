from multiprocessing import Process
from flask import Flask
from Api.Mqtt_api import mqtt_api
import mqtt_client.mqtt_pub_sub as mqtt_pub_sub

app = Flask(__name__)

app.register_blueprint(mqtt_api, url_prefix='/mqtt_api')

def metro_state_update_process():
    client = mqtt_pub_sub.create_connection('metro')
    mqtt_pub_sub.pull_metro_data(client)

def trainA_state_update_process():
    client = mqtt_pub_sub.create_connection('trainA')
    mqtt_pub_sub.pull_trainA_data(client)

def trainB_state_update_process():
    client = mqtt_pub_sub.create_connection('trainB')
    mqtt_pub_sub.pull_trainB_data(client)

def trainC_state_update_process():
    client = mqtt_pub_sub.create_connection('trainC')
    mqtt_pub_sub.pull_trainC_data(client)

def start_processes():
    mqtt_pub_sub.set_initial_passings()
    metro_update_proces = Process(target=metro_state_update_process, args=())
    metro_update_proces.start()

    trainA_update_proces = Process(target=trainA_state_update_process, args=())
    trainA_update_proces.start()

    trainB_update_proces = Process(target=trainB_state_update_process, args=())
    trainB_update_proces.start()

    trainC_update_proces = Process(target=trainC_state_update_process, args=())
    trainC_update_proces.start()

    passing_ab = Process(target=mqtt_pub_sub.get_message(mqtt_pub_sub.config.topics['passing_ab']), args=())
    passing_ab.start()

    passing_ac = Process(target=mqtt_pub_sub.get_message(mqtt_pub_sub.config.topics['passing_ac']), args=())
    passing_ac.start()

    passing_bc = Process(target=mqtt_pub_sub.get_message(mqtt_pub_sub.config.topics['passing_bc']), args=())
    passing_bc.start()

    start_simulation = Process(target=mqtt_pub_sub.get_message(mqtt_pub_sub.config.topics['start']), args=())
    start_simulation.start()

    emergency_process = Process(target=mqtt_pub_sub.get_message(mqtt_pub_sub.config.topics['emergency']), args=())
    emergency_process.start()


if __name__ == '__main__':
    start_processes()
    app.run(host='0.0.0.0', port=5001)
