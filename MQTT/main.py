from multiprocessing import Process
from flask import Flask
from Api.Mqtt_api import mqtt_api
import mqtt_client.mqtt_pub_sub as mqtt_pub_sub

app = Flask(__name__)

app.register_blueprint(mqtt_api, url_prefix='/mqtt_api')

def start_loop():
    client = mqtt_pub_sub.create_connection()
    mqtt_pub_sub.pull_data(client)

if __name__ == '__main__':
    update_proces = Process(target=start_loop, args=())
    update_proces.start()
    app.run(debug=True, port=5001)
