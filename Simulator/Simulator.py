import time
import threading
import yaml
import os

NUM_STATIONS = 15
TIME_INTERVAL = 10

SPEED_INTERVAL = 30
POSITION_INTERVAL = 1

class Simulator:
    _instance = None
    _train_speed = 0
    _train_door = 0
    _train_position = 0
    _railway_position = 0
    _emergency = 0
    _train_direction = 'A'

    _door_open_time = 0
    _direction_change_time = 0
    _train_position_change_time = 0


    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    @property
    def train_speed(self):
        return self._train_speed

    @property
    def train_direction(self):
        return self._train_direction

    @property
    def train_door(self):
        return self._train_door

    @train_door.setter
    def train_door(self, value):
        self._train_door = value

    @property
    def train_position(self):
        return self._train_position

    @property
    def railway_position(self):
        return self._railway_position

    @railway_position.setter
    def railway_position(self, value):
        self._railway_position = value

    @property
    def emergency(self):
        return self._emergency

    @emergency.setter
    def emergency(self, value):
        self._emergency = value


    def load_config_data(self):
        current_dir = os.getcwd()
        absolute_path = 'Simulator/config.yaml'
        relative_path = os.path.join(current_dir, absolute_path)

        with open(relative_path, 'r') as file:
            config_data = yaml.safe_load(file)

        self._door_open_time = config_data['door_open_time']
        self._direction_change_time = config_data['direction_change_time']
        self._train_position_change_time = config_data['train_position_change_time']


    def simulate_train(self):
        for direction in ("A", "B"):
            self._train_direction = direction
            for station in range(1, NUM_STATIONS + 1):
                for time_interval in range(1, TIME_INTERVAL + 1):
                    time.sleep(self._train_position_change_time)

                    if time_interval < 6:
                        self._train_speed = self._train_speed + SPEED_INTERVAL
                    else:
                        self._train_speed = self._train_speed - SPEED_INTERVAL

                    self._train_position = self._train_position + POSITION_INTERVAL

                self._train_door = 1
                time.sleep(self._door_open_time)
                self._train_door = 0
            self._train_position = 0
            time.sleep(self._direction_change_time)


    def run_metro(self):
        while(self._emergency == 0):
            self.simulate_train()


    def start_thread(self):
        self.load_config_data()
        thread = threading.Thread(target=self.run_metro)
        thread.start()
