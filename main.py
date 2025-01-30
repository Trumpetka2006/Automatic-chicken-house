from hardware import *
from controls import *
from rtc_events import *
from utime import sleep
from time import sleep_ms
from machine import RTC

#[func, arg]
command = []

#hw_init()
rtc = RTC()
rtc.datetime((2017, 8, 23, 0, 23, 59, 48, 0))
print(rtc.datetime())

# "hour:minutes":"action/argument"

time_actions = {
    "0:0":open_door,
    "0:1":close_door,
                }

lastactiontime = ""

def turn():
    LED.value(not LED.value())
    
def switch_relay():
    if relay_state:
        relA.on()
        relB.off()
    else:
        relA.off()
        relB.on()
        
relayA.write(0)
relayB.write(1)
door.stop()

sleep(2)
curr.set_zero_voltage()

door.numA = 0
door.request(0)

if door.action():
        monitor_motor(3000, curr, door)
        
door.request(0)

if door.action():
        monitor_motor(3000, curr, door)

print("check")
print(sim._send_command("AT+CPMS?"))
sim._send_command('AT+CMGL="REC READ"')
"""
door.request(1)
door.numA = 5
if door.action():
    monitor_motor(17000, curr, door)
"""

print(sim.registred())

while False:
    LED.on()

    print(uart0.read())
    uart0.write("AT\r\n")
    
    RTC_check(rtc.datetime(), time_actions, lastactiontime)
    
    if command != []:
        print(command)
        command = []
        busy.set()
    
    if door.action():
        monitor_motor(3000, curr, door)
    
    LED.off()
    sleep_ms(1000)
    print(get_time(rtc))
    
