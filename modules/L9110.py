class MotorDriver:
    # OPEN = 0
    # CLOSE = 1
    # UNKNOW = -1

    pinA = None
    pinB = None

    numA = 0
    numB = 0

    direction = 0

    _request = -1
    _state = -1

    def __init__(self, InA, InB):
        self.pinA = InA
        self.pinB = InB

        self.pinA.off()
        self.pinB.off()

        self.action_calls = {0: self._open, 1: self._close}

    def state(self):
        return self._state

    def lock_error(self):
        self._state = -1
        self.stop()

    def request(self, req):
        if req in [0, 1]:
            self._request = req

    def _turn(self, dirr=0):
        self.pinA.value(dirr)
        self.pinB.value(not dirr)

    def _open(self):
        if self.numA > self.numB:
            self._turn(self.direction)
            return True
        else:
            return False

    def _close(self):
        self._turn(not self.direction)
        return True

    def stop(self):
        self.pinA.off()
        self.pinB.off()

    def complete(self):
        self.stop()
        self._state = self._request

    def action(self):
        if self._request != self._state:
            return self.action_calls[self._request]()
        else:
            return False
