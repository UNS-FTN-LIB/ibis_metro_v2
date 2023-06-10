import time
import threading
import yaml
import os

from Model.Train import Train
from Model.Railway import Railway

NUM_A_STATIONS = 15
NUM_B_STATIONS = 9
NUM_C_STATIONS = 11

A_TRAIN_AB_CHANGE_A_DIRECTION = 75
A_TRAIN_AB_CHANGE_B_DIRECTION = 85
B_TRAIN_AB_CHANGE_A_DIRECTION = 15
B_TRAIN_AB_CHANGE_B_DIRECTION = 25
A_TRAIN_AC_CHANGE_A_DIRECTION = 95
A_TRAIN_AC_CHANGE_B_DIRECTION = 105
C_TRAIN_AC_CHANGE_A_DIRECTION = 35
C_TRAIN_AC_CHANGE_B_DIRECTION = 45
B_TRAIN_BC_CHANGE_A_DIRECTION = 35
B_TRAIN_BC_CHANGE_B_DIRECTION = 45
C_TRAIN_BC_CHANGE_A_DIRECTION = 45
C_TRAIN_BC_CHANGE_B_DIRECTION = 55

TIME_INTERVAL = 10

SPEED_INTERVAL = 30
POSITION_INTERVAL = 1

STOPED = False
POSITIONS_LEFT = 0
STOPED_POSITION = 0

class Simulator:
    _instance = None
    _emergency = 0

    _train_a = Train()
    _train_b = Train()
    _train_c = Train()

    _railway_ab = Railway()
    _railway_ac = Railway()
    _railway_bc = Railway()

    _door_open_time = 0
    _direction_change_time = 0
    _train_position_change_time = 0
    _train_start_time = 0

    is_started = False


    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    @property
    def train_a(self):
        return self._train_a

    @property
    def train_b(self):
        return self._train_b

    @property
    def train_c(self):
        return self._train_c

    @property
    def railway_ab(self):
        return self._railway_ab

    @railway_ab.setter
    def railway_ab(self, value):
        self._railway_ab = value

    @property
    def railway_ac(self):
        return self._railway_ac

    @railway_ac.setter
    def railway_ac_position(self, value):
        self._railway_ac = value

    @property
    def railway_bc(self):
        return self._railway_bc

    @railway_bc.setter
    def railway_bc(self, value):
        self._railway_bc = value

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
        self._train_start_time = config_data['train_start_time']


    def simulate_train(self, train:Train, number_of_stations, train_type):
        for direction in ("A", "B"):
            self._train_direction = direction
            for station in range(1, number_of_stations + 1):
                STOPED = False
                POSITIONS_LEFT = 0
                STOPED_POSITION = 0
                train.train_speed = 0
                for time_interval in range(1, TIME_INTERVAL + 1):

                    if self.event.is_set() == False:
                        train.train_speed = 0
                        self.event.wait()
                        STOPED = True
                        STOPED_POSITION = time_interval - 1
                        POSITIONS_LEFT = 10 - STOPED_POSITION
                        
                    time.sleep(self._train_position_change_time)

                    if STOPED == False:
                        if time_interval < 6:
                            train.train_speed = train.train_speed + SPEED_INTERVAL
                        else:
                            train.train_speed = train.train_speed - SPEED_INTERVAL
                    else:
                        if POSITIONS_LEFT % 2 == 1:
                            if time_interval < round(POSITIONS_LEFT / 2) + STOPED_POSITION:
                                train.train_speed = train.train_speed + SPEED_INTERVAL
                            elif time_interval == round(POSITIONS_LEFT / 2) + STOPED_POSITION:
                                train.train_speed = train.train_speed
                            else:
                                train.train_speed = train.train_speed - SPEED_INTERVAL
                        else:
                            if time_interval <= round(POSITIONS_LEFT / 2) + STOPED_POSITION:
                                train.train_speed = train.train_speed + SPEED_INTERVAL
                            else:
                                train.train_speed = train.train_speed - SPEED_INTERVAL

                    if direction == "A":
                        train.train_position = train.train_position + POSITION_INTERVAL
                    elif direction == "B":
                        train.train_position = train.train_position - POSITION_INTERVAL

                    self.update_railway_position(direction, train_type, train)

                train.train_door = 1
                time.sleep(self._door_open_time)
                train.train_door = 0

            #train.train_position = 0
            time.sleep(self._direction_change_time)


    def update_railway_position(self, train_direction, train_type, train : Train):
        if train_direction == 'A':
            if train_type == 'A':
                if train.train_position == A_TRAIN_AB_CHANGE_A_DIRECTION:
                    self.railway_ab.position = 0
                elif train.train_position == A_TRAIN_AC_CHANGE_A_DIRECTION:
                    self.railway_ac.position = 0
            elif train_type == 'B':
                if train.train_position == B_TRAIN_AB_CHANGE_A_DIRECTION:
                    self.railway_ab.position = 1
                elif train.train_position == B_TRAIN_BC_CHANGE_A_DIRECTION:
                    self.railway_bc.position = 0
            elif train_type == 'C':
                if train.train_position == C_TRAIN_AC_CHANGE_A_DIRECTION:
                    self.railway_ac.position = 1
                elif train.train_position == C_TRAIN_BC_CHANGE_A_DIRECTION:
                    self.railway_bc.position = 1
        elif train_direction == 'B':
            if train_type == 'A':
                if train.train_position == A_TRAIN_AB_CHANGE_B_DIRECTION:
                    self.railway_ab.position = 0
                elif train.train_position == A_TRAIN_AC_CHANGE_B_DIRECTION:
                    self.railway_ac.position = 0
            elif train_type == 'B':
                if train.train_position == B_TRAIN_AB_CHANGE_B_DIRECTION:
                    self.railway_ab.position = 1
                elif train.train_position == B_TRAIN_BC_CHANGE_B_DIRECTION:
                    self.railway_bc.position = 0
            elif train_type == 'C':
                if train.train_position == C_TRAIN_AC_CHANGE_B_DIRECTION:
                    self.railway_ac.position = 1
                elif train.train_position == C_TRAIN_BC_CHANGE_B_DIRECTION:
                    self.railway_bc.position = 1


    def run_metro(self, train, stations, train_type):
        while(self._emergency == 0):
            self.simulate_train(train, stations, train_type)


    def start_thread(self, button_status):
        if not button_status and self.is_started:
            self.event.clear()
        elif button_status and self.is_started:
            self.event.set()
        elif not self.is_started:
            self.is_started = True

            self.event = threading.Event()
            self.event.set()

            self.load_config_data()
            thread_a = threading.Thread(target=self.run_metro, args=(self._train_a, NUM_A_STATIONS, 'A'))
            thread_b = threading.Thread(target=self.run_metro, args=(self._train_b, NUM_B_STATIONS, 'B'))
            thread_c = threading.Thread(target=self.run_metro, args=(self._train_c, NUM_C_STATIONS, 'C'))

            thread_a.start()
            thread_b.start()
            thread_c.start()
