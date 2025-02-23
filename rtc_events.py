from hardware import *


def RTC_check(time,actions,lastaction):
    datetime = f"{time[4]}:{time[5]}"
    trigger_times = actions.keys()
    if datetime in trigger_times and lastaction != datetime:
        lastaction = datetime
        actions[datetime]()
        

def get_time(rtc):
    raw=rtc.datetime()
    return (raw[4],raw[5],raw[6])

def open_door():
    door.request(0)
    
def close_door():
    door.request(1)
    
def light_on():
    light.write(1)
    
def light_off():
    light.write(0)