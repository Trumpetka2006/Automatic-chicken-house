import time

class SIM800L():
    uart = None
    konwnnumbers = ["+420607560209"]
    
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
        return response
    
    def read_SMS(self, index = 1):
        response = self._send_command('AT+CMGL="REC UNREAD"')
        lenght = len(response)
        #print(response)
        if response[lenght - 2] == 'OK':
            try:
                return (response[2],response[1].split('"')[3])
            except IndexError:
                return None
        else:
            return None
    
    def send_SMS(self, message, number):
        self.uart.write(f'AT+CMGS="{number}"')
        self.uart.write(message + chr(26))
        return self.uart.read().decode("utf-8")
    
    def delete_memory(self):
        response = self._send_command('AT+CMGD=1,1')
        lenght = len(response)
        return response[lenght-2]
    
    def get_time(self):
        response = self._send_command('AT+CCLK?')
        lenght = len(response)
        if response[lenght - 2] == 'OK':
            tim = response[1].split('"')[1]
            YEAR = int('20'+tim[:2])
            MONTH = int(tim[3:5])
            DAY = int(tim[6:8])
            HOUR = int(tim[9:11])
            MIN = int(tim[12:14])
            SEC = int(tim[15:17])
            return (YEAR,MONTH,DAY,HOUR,MIN,SEC)
        else:
            return  None
    
    def send_raw_command(self, command, delay=1):
        self.uart.write(command + '\r\n')
        time.sleep(delay)
        response = self.uart.read()
        return response.decode('utf-8')
        
    def registred(self):
        print((self._send_command("AT+CREG?")[1],0))
        if self._send_command("AT+CREG?")[1] == '+CREG: 0,1\r\n':
            return True
        else:
            return False 