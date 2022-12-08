class Observer:
    def __init__(self):
        self._state = 0
        self._new_state = 0

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def new_state(self):
        return self._new_state

    @new_state.setter
    def new_state(self, value):
        self._new_state = value
