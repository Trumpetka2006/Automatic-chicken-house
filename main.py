from hardware import *
from controls import *
from commands import *
from rtc_events import *
from utime import sleep
from time import sleep_ms


buff = ""

rtc.datetime((2017, 8, 23, 0, 23, 59, 48, 0))
print(rtc.datetime())

# "hour:minutes":"action/argument"

time_actions = {
    "0:0":light_off,
    "0:1":light_on,
    "23:59":light_on
                }

def read_console(uart):
    global buff
    command = ""
    read = uart.read()
    if read == None:
        return
    else:
        read = read.decode("ascii")
    if read in "\r":
        buff += read
        uart.write(bytes(read,"ascii"))
        command = buff
        buff = ""
        uart.write('\r\n')
        if command == "":
            return None
        return command
    else :
        buff += read
        uart.write(bytes(read,"ascii"))
        return None
    
def process(cmd):
    cmd = cmd.split()
    lenght = len(cmd)
    print([cmd, lenght])
    try:
        if lenght == 0:
            return ""
        elif lenght == 1:
            return COMMANDS[cmd[0]]()
        elif lenght == 2:
            return COMMANDS[cmd[0]](cmd[1])
        elif lenght == 3:
            return COMMANDS[cmd[0]](cmd[1], cmd[2])
        else :
            raise TypeError
    except KeyError:
        return 'Invalid Command'
    except IndexError:
        return ""
    #except TypeError:
        #return "Too many arguments"

door.stop()

if init_sim800l:
    sim.konwnnumbers = ["+420607560209"]
    sim.init()

sleep(2)
curr.set_zero_voltage()
"""
while not sim.registred():
    print("waiting")
    sleep(1)
"""
door.numA = 0
door.request(0)
"""
if door.action():
        monitor_motor(3000, curr, door)
        
door.request(0)

if door.action():
        monitor_motor(3000, curr, door)


"""
#print(sim.get_time())

#print(sim._send_command('AT+CMGL="REC UNREAD"'))
#print(sim.read_SMS())
#print("check")
#print(sim.send_raw_command('AT+CPMS?'))
#print(sim.send_raw_command('AT+CMGL="REC UNREAD"'))
#print(sim._send_command('AT+CMGL="REC READ"'))
"""
door.request(1)
door.numA = 5
if door.action():
    monitor_motor(17000, curr, door)
"""

#print(sim.registred())
if init_console:
    console.write('\033[2J\033[H')
    console.write('Starting...\r\nEggOS>')

while True:
    LED.on()
    
    RTC_check(rtc.datetime(), time_actions)
    
    #print(sim.read_SMS())
    """
    if command != []:
        print(command)
        command = []
        busy.set()
    """ 
    cmd = read_console(console)
    if cmd != None:
        console.write(str(process(cmd))+"\r\n>")
    
    #if door.action():
        #monitor_motor(3000, curr, door)
    
    LED.off()
    sleep_ms(100)

    
