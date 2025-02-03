import time

class SIM800L():
    uart = None
    def __init__(self,sim_uart):
        self.uart = sim_uart
        print("Sim800 init!")
        
    def init(self):
        strikes = 0
        while strikes < 10:
            if self._send_command('AT+CMGF=1')[1] != 'OK':
                strikes += 1
                continue
            print("OK")
            break
        
    def _send_command(self, command, delay=1):
        self.uart.write(command + '\r\n')
        time.sleep(delay)
        response = self.uart.read()
        response = response.decode("utf-8").replace("\r", "").split("\n")
        lenght = len(response)
        return (response[1], response[lenght - 2])
    
    def send_raw_command(self, command, delay=1):
        self.uart.write(command + '\r\n')
        time.sleep(delay)
        response = self.uart.read()
        return response.decode('utf-8')
        
    def registred(self):
        if self._send_command("AT+CREG?")[1] == '+CREG: 0,1\r':
            return True
        else:
            return False 