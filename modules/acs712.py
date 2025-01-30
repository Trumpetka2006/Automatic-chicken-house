class ACS712():
    pin = None
    zeroVoltage = 1.25
    
    def __init__(self, adcPin):
        self.pin = adcPin
    
    def set_zero_voltage(self):
        self.zeroVoltage = self.read_V()
        
    def _measure(self):
        return self.pin.read_u16() * 3 / 65535
    
    def read_V(self, numReads = 100):
        measurements = 0
        
        for i in range(numReads):
            measurements += self._measure()
            #print(f"{i}->{self._measure()}")
            
        return measurements / numReads
    
    def read_mA(self):
        voltage = self.read_V() - self.zeroVoltage

        return abs(voltage * 185)
        