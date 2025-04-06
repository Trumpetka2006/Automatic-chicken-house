from hardware import *
from controls import *
from commands import *
from rtc_events import *
from utime import sleep
from time import sleep_ms, ticks_ms
from machine import WDT
import json

start_time = ticks_ms()

command_queue = [] #("time","+420723748913")

rtc.datetime((2017, 8, 23, 0, 23, 59, 48, 0))



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
    sim.known_numbers = ["+420607560209", "+420602716250"]
    sim.init()
stdout("info","HelloWorld!")
sleep(1)
curr.set_zero_voltage()
"""
while not sim.registred():
    print("waiting")
    sleep(1)
"""
door.numA = 0
door.request(0)


#print(sim.registred())
if console:
    console.write('\033[2J\033[H')
    console.write('Starting...\r\n')

stdout("info",f"Started in {ticks_ms()-start_time} ms")
if debugMode.value():
    wdt = None#WDT(timeout=5000)
else:
    stdout("warning","Debug mode is active")
    stdout("debug", str(cmd_help))
    
loop = 0

print(sim.read_all_sms())

while True:
    loop += 1
    LED.on()
    
    RTC_check(rtc.datetime(), time_actions)

    if console:
        cmd = read_console(console)
    if cmd != None:
        console.write(str(process(cmd))+"\r\n> ")
        
    if command_queue != []:
        stdout("debug", command_queue)
        phone_command = command_queue.pop()
        stdout("debug",f"Sending {phone_command[1]} to {phone_command[0]}")
        sim.send_SMS(str(process(phone_command[1])).replace("\t"," "), phone_command[0])
    
    #if door.action():
        #monitor_motor(3000, curr, door)
        
    if loop > 50:
        loop = 0
        if bmp280_i2c:
            door.a = bmp280_i2c.measurements['t']
            #stdout("debug",str(door.a))
        if sim:
            if sim.has_msg():
                stdout("INFO","new message!")
                for msg in sim.pop_sms_commands():
                    stdout("debug",msg)
                    if msg[0] in sim.known_numbers:
                        
                        command_queue.append(msg)
                    else : stdout("warning", f"{msg[0]} is unknown number!")
        
    if wdt:
        wdt.feed()
    
    LED.off()
    sleep_ms(10)

    
