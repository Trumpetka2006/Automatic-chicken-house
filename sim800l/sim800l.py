import time

class SIM800L():
    uart = None
    konwnnumbers = ["+420607560209"]
    
    def __init__(self,sim_uart):
        self.uart = sim_uart
        
    def init(self):
        strikes = 0
        self._send_command("AT+CNMI=0,0,0,0,0")
        self._send_command("AT+GSMBUSY=1")
        while strikes < 10:
            if self._send_command('AT+CMGF=1')[1] != 'OK':
                strikes += 1
                continue
            break
        
    def _send_command(self, command, delay=1):
        self.uart.write(command + '\r\n')
        time.sleep(delay)
        if self.uart.any():
            response = self.uart.read()
            response = response.decode("utf-8").replace("\r", "").split("\n")
        else: response = [None, "ERROR"]
        return response

    def _beta_send_command(self,command):
        self.uart.read()
        self.uart.write(command + '\r\n')
        time.sleep_ms(50)
        response = ""
        while self.uart.any():
            response += self.uart.read().decode("utf-8")
            time.sleep_ms(50)
        return response
    
    def has_msg(self):
        try:
            response = self._beta_send_command("AT+CPMS?").replace('\r','').split('\n')
            return int(response[1].split(',')[1]) > 0
        except IndexError:
            return False 
    
    def pop_sms_commands(self):
        sms_list = self.read_all_sms().split("\n")
        sms_list.pop()
        output = []
        for i in range(len(sms_list)):
            if sms_list[i][:5] == "+CMGL":
                metadata = sms_list[i].split(',')
                output.append([metadata[2].replace('"', ''), sms_list[i+1].replace('\r', '')])
                self._send_command(f"AT+CMGD={int(metadata[0].split()[1])},0")
        return output
    
    def read_SMS(self, index = 1):
        response = self._send_command('AT+CMGL="REC UNREAD"') #REC UNREAD
        lenght = len(response)
        if response[lenght - 2] == 'OK':
            try:
                return (response[2],response[1].split('"')[3])
            except IndexError:
                return None
        else:
            return None

    def read_all_sms(self):
        response = self._beta_send_command('AT+CMGL="ALL"')
        return response

    
    def send_SMS(self, message, number):
        self._send_command(f'AT+CMGS="{number}"')
        self.uart.write(message + chr(26))
        time.sleep(3)
        return self.uart.read()
    
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