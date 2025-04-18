from hardware import (
    rtc,
    sim,
    light,
    heater,
    door,
    curr,
    bmp280_i2c,
    init_sim800l,
    init_bmp280,
)
from controls import monitor_motor
import re
import time

on_off = {"o": True, "f": False}
true_false = {1: "ON", 0: "OFF"}
open_close = {"o": 0, "c": 1}
door_state = {0: "OPEN", 1: "CLOSE", -1: "UNKNOWN"}

def process(cmd):
    cmd = cmd.lower()
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
    except TypeError:
        return "Too many arguments"


def cmd_help(cmd = None,info=False):
    if info:
        return "Show this dialog"
    cmds = COMMANDS.keys()
    if cmd and cmd in cmds:
        return f"Command help:\r\n\t{cmd}\t- {COMMANDS[cmd](info=True)}\r\n"
    ansfer = "Available commands:\r\n"
    for cmd in cmds:
        ansfer = ansfer + f"\t{str(cmd)}\t- {COMMANDS[cmd](info=True)}\r\n"
    ansfer = ansfer + "For more info visit: https://github.com/Trumpetka2006/Automatic-chicken-house/blob/main/README.md"
    return ansfer

def cmd_sms_read(info=False):
    if info:
        return "Print incoming SMS"
    return sim.read_SMS()

def cmd_sms_send(info=False):
    if info:
        return "Sends test string to all admins"
    return sim.send_SMS("Hello World!", "+420602716250")


def test(info=False):
    if info:
        return "Print a test string"
    
    return sim.pop_sms_commands()


def cmd_time(value=None,info=False):
    if info:
        return "Get/set system time [HH:MM:SS]"
    time = rtc.datetime()
    if value == None:
        return f"{time[4]}:{time[5]}:{time[6]}"
    elif re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$", value):
        value = value.split(":")
        time = list(time)
        time[4] = int(value[0])
        time[5] = int(value[1])
        time[6] = int(value[2])
        time = tuple(time)
        rtc.datetime(time)
        return f"New time is {time[4]}:{time[5]}:{time[6]}"
    else:
        return f"{value}"


def cmd_date(value=None,info=False):
    if info:
        return "Get/set system date [YYYY-MM-DD]"
    date = rtc.datetime()
    if value == None:
        return f"{date[0]}-{date[1]}-{date[2]}"
    elif re.match(r"^\d\d\d\d-\d\d-\d\d$", value):
        value = value.split("-")
        date = list(date)
        date[0] = int(value[0])
        date[1] = int(value[1])
        date[2] = int(value[2])
        date = tuple(date)
        rtc.datetime(date)
        return f"New date is {date[0]}-{date[1]}-{date[2]}"
    else:
        return f"{value} is not valid"


def cmd_admin(operation=None, number=None,info=False):
    if info:
        return "Add/delet known phone number [a/d] [number]"
    if init_sim800l:
        if operation == None and number == None:
            return sim.known_numbers
        elif operation != None and number != None:
            # print(number)
            # print(bool(re.match(r"^\+\d{1,3}\d{9}$", number)))
            if operation == "a":  # and re.match(r"^\+\d{1,3}\d{9}$", number.strip()):
                sim.known_numbers.append(number)
                return f"number {number} was added"
            elif operation == "a":
                return f"number is in bad format or prefix is mising"
            elif operation == "d" and number in sim.known_numbers:
                buff = []
                for i in range(len(sim.known_numbers)):
                    if number != sim.known_numbers[i]:
                        buff.append(sim.known_numbers[i])
                sim.known_numbers = buff
                return "number was removed"
            elif operation == "d" and not number in sim.known_numbers:
                return "unknown number"
    else:
        return "SIM800L is not enabeled in config"


def cmd_atcmd(command=None,info=False):
    if info:
        return "Send an ATcommand [at+command]"
    if init_sim800l:
        if command == None:
            return "no AT command given"
        else:
            return sim.send_raw_command(command)
    else:
        return "SIM800L is not enabeled in config"


def cmd_light(state=None,info=False):
    if info: return "Get/set state of light relay [o/f]"
    if state == None:
        return true_false[light.read()]
    if state == "o" or "f":
        light.write(on_off[state])
        light.pin.value(on_off[state])
        return f"light turned {true_false[light.read()]}"


def cmd_heater(state=None,info=False):
    if info: return "Get/set state of heater relay [o/f]"
    if state == None:
        return true_false[heater.read()]
    if state == "o" or "f":
        heater.write(on_off[state])
        heater.pin.value(on_off[state])
        return f"heater turned {true_false[heater.read()]}"


def cmd_door(state=None,info=False):
    if info: return "Get/set state of door [o/c]"
    if state == None:
        return door_state[door.state()]
    if state == "o" or "c":
        door.numA = 9999
        door.request(open_close[state])
        if door.action():
            monitor_motor(3000, curr, door)
        return door_state[door.state()]


def cmd_doormin(value=None,info=False):
    if info: return "Get/set minimal temperature where doors can open"
    if value == None:
        return door.numB
    try:
        door.numB = float(value)
    except ValueError:
        return "not a valid value"
    else:
        return f"new min temperature is {door.numB}"


def cmd_temp(info=False):
    if info: return "Get temperature form sensor"
    if init_bmp280:
        readout = bmp280_i2c.measurements
        return f"Temperature: {readout['t']} °C"
    else:
        return "BMP280 is not enabeled in config"


def cmd_press(info=False):
    if info: return "Get preasure form sensor"
    if init_bmp280:
        readout = bmp280_i2c.measurements
        return f"Pressure: {readout['p']} hPa"
    else:
        return "BMP280 is not enabeled in config"
    
def cmd_freeze(info=False):
    if info: return "Simulate system freeze"
    time.sleep(10)


COMMANDS = {
    "help": cmd_help,
    "test": test,
    "time": cmd_time,
    "date": cmd_date,
    "admin": cmd_admin,
    "atcmd": cmd_atcmd,
    "light": cmd_light,
    "heater": cmd_heater,
    "door": cmd_door,
    "doormin": cmd_doormin,
    "temp": cmd_temp,
    "press": cmd_press,
    "freeze": cmd_freeze,
    "smsr": cmd_sms_read,
    "smss": cmd_sms_send,
}
