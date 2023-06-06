class Railway:
    _position = 0

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
