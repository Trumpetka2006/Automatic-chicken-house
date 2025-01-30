class MotorDriver:
    pinA = None
    pinB = None
    
    def __init__(self, InA, InB):
        self.pinA = InA
        self.pinB = InB
        
        self.pinA.off()
        self.pinB.off()
        
    def _turn(self, dirr = 0):
        self.pinA.value(dirr)
        self.pinB.value(not dirr)