import time

class SIM800L():
    uart = None
    def __init__(self,sim_uart):
        self.uart = sim_uart
        print("Sim800 init!")
        
    def _send_command(self, command, delay=1):
        self.uart.write(command + '\r\n')
        time.sleep(delay)
        response = self.uart.read()
        print(response.decode("utf-8").replace("\r", "").split("\n"))
        return response.decode("utf-8").replace("\r", "").split("\n")
        
    def registred(self):
        if self._send_command("AT+CREG?")[1] == '+CREG: 0,1\r':
            return True
        else:
            return False 