from hardware import rtc
import re

def cmd_help():
    return COMMANDS.keys()

def test():
    return 'Hello World!'

def cmd_time(value = None):
    time = rtc.datetime()
    if value == None :
        return f"{time[4]}:{time[5]}:{time[6]}"
    elif re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$", value):
        value = value.split(":")
        time = list(time)
        time[4] = int(value[0])
        time[5] = int(value[1])
        time[6] = int(value[2])
        time = tuple(time)
        rtc.datetime(time)
        return f'New time is {time[4]}:{time[5]}:{time[6]}'
    else:
        return f'{value}'
        
COMMANDS = {'help':cmd_help,
            'test':test,
            'time':cmd_time}
