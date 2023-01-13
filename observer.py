import subprocess


class Observer:
    def __init__(self):
        self._state = 0
        self._new_state = 0
        self._is_first = 1
        self.time_internet_start = "nooo way pogarmist durenb"

    @property
    def is_first(self):
        return self._is_first

    @is_first.setter
    def is_first(self, value):
        self._is_first = value


    @property
    def state(self):
        res = subprocess.call(['ping', '-c', '1', "8.8.8.8"], stdout=subprocess.DEVNULL)
        if res == 0:
            return True
        else:
            return False

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def new_state(self):
        return self._new_state

    @new_state.setter
    def new_state(self, value):
        self._new_state = value
