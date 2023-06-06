class Train:
    _train_speed = 0
    _train_door = 0
    _train_position = 0
    _train_direction = 'A'

    @property
    def train_speed(self):
        return self._train_speed

    @train_speed.setter
    def train_speed(self, value):
        self._train_speed = value

    @property
    def train_direction(self):
        return self._train_direction

    @train_direction.setter
    def train_direction(self, value):
        self._train_direction = value

    @property
    def train_door(self):
        return self._train_door

    @train_door.setter
    def train_door(self, value):
        self._train_door = value

    @property
    def train_position(self):
        return self._train_position

    @train_position.setter
    def train_position(self, value):
        self._train_position = value
