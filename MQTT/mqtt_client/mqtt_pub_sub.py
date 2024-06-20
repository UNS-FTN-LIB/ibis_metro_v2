from time import sleep
from paho.mqtt import client as mqtt_client
import requests
import mqtt_client.mqtt_config as config
import mqtt_client.states as states
import ssl


endpoint = 'http://simulator:5000'
pull_metro_data_url = endpoint + '/metro/'
pull_trainA_data_url = endpoint + '/metro/train-a'
pull_trainB_data_url = endpoint + '/metro/train-b'
pull_trainC_data_url = endpoint + '/metro/train-c'
position_url = endpoint + '/railway/position/'
metro_start_url = endpoint + '/metro/start'
emergency_url = endpoint + '/emergency/'

def connect_mqtt(client_id):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # Set the username to "oauth2" and password to the access token
    client.username_pw_set(config.username, config.password)
    client.on_connect = on_connect
    # Configure TLS settings without verifying the server's certificate
    client.tls_set(cert_reqs=ssl.CERT_NONE)
    # Ensure that is working with self-signed cert
    client.tls_insecure_set(True)
    client.connect(config.broker, config.port)
    return client


def _publish(client, topic, message):
    status_message = client.publish(topic, message)
    if status_message == 0:
        print(f"Failed to send message to topic {topic}")
    else:
        print(f"Successfully sent message {message}")


def create_connection(client_id):
    client = connect_mqtt(client_id)
    client.loop_start()
    return client

def set_initial_passings():
    client = connect_mqtt('initial_values')
    client.loop_start()
    _publish(client, config.topics['passing_ab'], 0)
    _publish(client, config.topics['passing_ac'], 0)
    _publish(client, config.topics['passing_bc'], 0)
    _publish(client, config.topics['start'], 0)
    _publish(client, config.topics['emergency_view'], 0)
    client.loop_stop()

def reset_start_button():
    client = connect_mqtt('start_button_reset')
    client.loop_start()
    _publish(client, config.topics['start'], 0)
    client.loop_stop()

def reset_emergency_button():
    client = connect_mqtt('emergency_button_reset')
    client.loop_start()
    _publish(client, config.topics['emergency_view'], 0)
    client.loop_stop()


def _subscribe(client, topic):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        # notify simulator
        while True:
            if msg.topic[0:7] == 'Passing':
                passing = msg.topic[7:].lower().strip()
                response = requests.put(position_url + passing, json={'position': msg.payload.decode()})
                states.metro_state['passing_' + passing] = msg.payload.decode()
            elif msg.topic == 'EmergencyStopMetro':
                #response = requests.put(emergency_url, json={'emergency': 1})
                response = requests.post(metro_start_url, json={'button': 1})
                reset_start_button()
            elif msg.topic == 'MetroStartButton' and client._client_id == b'MetroStartButton':
                response = requests.post(metro_start_url, json={'button': msg.payload.decode()})
                reset_emergency_button()
            else:
                break

            if response.status_code == 200:
                break

    client.subscribe(topic)
    client.on_message = on_message


def get_message(topic):
    client = connect_mqtt(topic)
    _subscribe(client, topic)
    client.loop_start()


def pull_metro_data(client):

    while True:
        sleep(2)
        response = requests.get(pull_metro_data_url)

        if response.status_code == 200:
            data_json = response.json()
            print(data_json)

            if states.metro_state['passing_ab'] != data_json['railway_ab_position']:
                states.metro_state['passing_ab'] = data_json['railway_ab_position']
                _publish(client, config.topics['passing_ab'], states.metro_state['passing_ab'])

            if states.metro_state['passing_ac'] != data_json['railway_ac_position']:
                states.metro_state['passing_ac'] = data_json['railway_ac_position']
                _publish(client, config.topics['passing_ac'], states.metro_state['passing_ac'])

            if states.metro_state['passing_bc'] != data_json['railway_bc_position']:
                states.metro_state['passing_bc'] = data_json['railway_bc_position']
                _publish(client, config.topics['passing_bc'], states.metro_state['passing_bc'])


def pull_trainA_data(client):

    while True:
        sleep(2)
        response = requests.get(pull_trainA_data_url)

        if response.status_code == 200:
            data_json = response.json()
            print(data_json)

            if states.train_A['direction'] != data_json['train_direction']:
                states.train_A['direction'] = data_json['train_direction']

            if states.train_A['position'] != data_json['position']:
                states.train_A['position'] = data_json['position']
                if states.train_A['direction'] == 'A':
                    _publish(client, config.topics['train_aa'], states.train_A['position'])
                else:
                    _publish(client, config.topics['train_ab'], states.train_A['position'])

            if states.train_A['speed'] != data_json['speed']:
                states.train_A['speed'] = data_json['speed']
                _publish(client, config.topics['speed_a'], states.train_A['speed'])

            if states.train_A['doors'] != data_json['doors']:
                states.train_A['doors'] = data_json['doors']
                _publish(client, config.topics['doors_a'], states.train_A['doors'])

def pull_trainB_data(client):

    while True:
        sleep(2)
        response = requests.get(pull_trainB_data_url)
        
        if response.status_code == 200:
            data_json = response.json()
            print(data_json)

            if states.train_B['direction'] != data_json['train_direction']:
                states.train_B['direction'] = data_json['train_direction']

            if states.train_B['position'] != data_json['position']:
                states.train_B['position'] = data_json['position']
                if states.train_B['direction'] == 'A':
                    _publish(client, config.topics['train_ba'], states.train_B['position'])
                else:
                    _publish(client, config.topics['train_bb'], states.train_B['position'])
            
            if states.train_B['speed'] != data_json['speed']:
                states.train_B['speed'] = data_json['speed']
                _publish(client, config.topics['speed_b'], states.train_B['speed'])

            if states.train_B['doors'] != data_json['doors']:
                states.train_B['doors'] = data_json['doors']
                _publish(client, config.topics['doors_b'], states.train_B['doors'])

def pull_trainC_data(client):

    while True:
        sleep(2)
        response = requests.get(pull_trainC_data_url)
        
        if response.status_code == 200:
            data_json = response.json()
            print(data_json)

            if states.train_C['direction'] != data_json['train_direction']:
                states.train_C['direction'] = data_json['train_direction']

            if states.train_C['position'] != data_json['position']:
                states.train_C['position'] = data_json['position']
                if states.train_C['direction'] == 'A':
                    _publish(client, config.topics['train_ca'], states.train_C['position'])
                else:
                    _publish(client, config.topics['train_cb'], states.train_C['position'])
            
            if states.train_C['speed'] != data_json['speed']:
                states.train_C['speed'] = data_json['speed']
                _publish(client, config.topics['speed_c'], states.train_C['speed'])

            if states.train_C['doors'] != data_json['doors']:
                states.train_C['doors'] = data_json['doors']
                _publish(client, config.topics['doors_c'], states.train_C['doors'])
