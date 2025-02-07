class Relay():
    pin = None
    state = False
    
    def __init__(self , relayPin):
        self.pin = relayPin
        self.pin.off()
        
    def write(self, value = False):
        self.pin.value(value)
        self.state = value
    
    def read(self):
        return self.state
    
    def change(self):
        self.pin.value(not self.state)
        self.state = not self.state
    