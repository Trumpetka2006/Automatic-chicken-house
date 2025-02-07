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
    "0:0":light_off,
    "0:1":close_door,
    "23:59":light_on
                }

lastactiontime = ""

def turn():
    LED.value(not LED.value())
    
        
door.stop()

sleep(2)
curr.set_zero_voltage()

sim.init()

door.numA = 0
door.request(0)

if door.action():
        monitor_motor(3000, curr, door)
        
door.request(0)

if door.action():
        monitor_motor(3000, curr, door)

print(sim.delete_memory())

print(sim.get_time())

print(sim._send_command('AT+CMGL="REC UNREAD"'))
print(sim.read_SMS())
print("check")
#print(sim.send_raw_command('AT+CPMS?'))
#print(sim.send_raw_command('AT+CMGL="REC UNREAD"'))
print(sim._send_command('AT+CMGL="REC READ"'))
"""
door.request(1)
door.numA = 5
if door.action():
    monitor_motor(17000, curr, door)
"""

print(sim.registred())

while True:
    LED.on()
    
    RTC_check(rtc.datetime(), time_actions, lastactiontime)
    
    print(sim.read_SMS())
    
    if command != []:
        print(command)
        command = []
        busy.set()
    
    #if door.action():
        #monitor_motor(3000, curr, door)
    
    LED.off()
    #sleep_ms(1000)
    print(get_time(rtc))
    
