from hardware import *
from controls import *
from commands import *
from rtc_events import *
from utime import sleep
from time import sleep_ms, ticks_ms
from machine import WDT
import json

start_time = ticks_ms()

command_queue = [["+420602716209","time"]]

rtc.datetime((2017, 8, 23, 0, 23, 59, 48, 0))
print(rtc.datetime())



# "hour:minutes":"action/argument"

time_actions = {
    "0:0":light_off,
    "0:1":light_on,
    "23:59":light_on
                }
with open("timetable.json", "w") as file:
    json.dump(time_actions, file)
    file.close()

    


door.stop()

if init_sim800l:
    sim.konwnnumbers = ["+420607560209"]
    sim.init()

sleep(1)
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
if console:
    console.write('\033[2J\033[H')
    console.write('Starting...\r\n')

stdout("info",f"Started in {ticks_ms()-start_time} ms")
if debugMode.value():
    wdt = WDT(timeout=5000)
else:
    stdout("warning","Debug mode is active")
    stdout("debug", str(cmd_help))

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
    if console:
        cmd = read_console(console)
    if cmd != None:
        console.write(str(process(cmd))+"\r\n> ")
        
    if command_queue:
        phone_command = command_queue.pop()
        stdout("debug",f"Sending {str(process(phone_command[1]))} to {phone_command[0]}")
    
    #if door.action():
        #monitor_motor(3000, curr, door)
    if wdt:
        wdt.feed()
    
    LED.off()
    sleep_ms(100)

    
