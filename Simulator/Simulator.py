import time
import threading

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


    def simulate_train_forward(self):
        for station in range(1, NUM_STATIONS + 1):
            for time_interval in range(1, TIME_INTERVAL + 1):
                time.sleep(time_interval)

                if time_interval < 6:
                    self._train_speed = self._train_speed + SPEED_INTERVAL
                else:
                    self._train_speed = self._train_speed - SPEED_INTERVAL

                self._train_position = self._train_position + POSITION_INTERVAL

            self._train_door = 1
            time.sleep(5)
            self._train_door = 0


    def simulate_train_backward(self):
        self._train_direction = "B"
        self._train_position = 150

        for station in range(1, NUM_STATIONS + 1):
            for time_interval in range(1, TIME_INTERVAL + 1):
                time.sleep(time_interval)

                if time_interval < 6:
                    self._train_speed = self._train_speed + SPEED_INTERVAL
                else:
                    self._train_speed = self._train_speed - SPEED_INTERVAL

                self._train_position = self._train_position - POSITION_INTERVAL

            self._train_door = 1
            time.sleep(5)
            self._train_door = 0


    def run_metro(self):
        while(self._emergency is 0):
            self.simulate_train_forward()
            time.sleep(20)
            self.simulate_train_backward()
            time.sleep(20)


    def start_thread(self):
        thread = threading.Thread(target=self.run_metro)
        thread.start()
