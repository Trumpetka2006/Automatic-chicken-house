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

on_off = {"O": True, "F": False}
true_false = {1: "ON", 0: "OFF"}
open_close = {"O": 0, "C": 1}
door_state = {0: "OPEN", 1: "CLOSE", -1: "UNKNOWN"}


def cmd_help():
    return COMMANDS.keys()


def test():
    return "Hello World!"


def cmd_time(value=None):
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


def cmd_date(value=None):
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


def cmd_admin(operation=None, number=None):
    if init_sim800l:
        if operation == None and number == None:
            return sim.konwnnumbers
        elif operation != None and number != None:
            # print(number)
            # print(bool(re.match(r"^\+\d{1,3}\d{9}$", number)))
            if operation == "A":  # and re.match(r"^\+\d{1,3}\d{9}$", number.strip()):
                sim.konwnnumbers.append(number)
                return f"number {number} was added"
            elif operation == "A":
                return f"number is in bad format or prefix is mising"
            elif operation == "D" and number in sim.konwnnumbers:
                buff = []
                for i in range(len(sim.konwnnumbers)):
                    if number != sim.konwnnumbers[i]:
                        buff.append(sim.konwnnumbers[i])
                sim.konwnnumbers = buff
                return "number was removed"
            elif operation == "D" and not number in sim.konwnnumbers:
                return "unknown number"
    else:
        return "SIM800L is not enabeled in config"


def cmd_atcmd(command=None):
    if init_sim800l:
        if command == None:
            return "no AT command given"
        else:
            return sim.send_raw_command(command)
    else:
        return "SIM800L is not enabeled in config"


def cmd_light(state=None):
    if state == None:
        return true_false[light.read()]
    if state == "O" or "F":
        light.write(on_off[state])
        light.pin.value(on_off[state])
        return f"light turned {true_false[light.read()]}"


def cmd_heater(state=None):
    if state == None:
        return true_false[heater.read()]
    if state == "O" or "F":
        heater.write(on_off[state])
        heater.pin.value(on_off[state])
        return f"light turned {true_false[heater.read()]}"


def cmd_door(state=None):
    if state == None:
        return door_state[door.state()]
    if state == "O" or "C":
        door.numA = 9999
        door.request(open_close[state])
        if door.action():
            monitor_motor(3000, curr, door)
        return door_state[door.state()]


def cmd_doormin(value=None):
    if value == None:
        return door.numB
    try:
        door.numB = float(value)
    except ValueError:
        return "not a valid value"
    else:
        return f"new min temperature is {door.numB}"


def cmd_temp():
    if init_bmp280:
        readout = bmp280_i2c.measurements
        return f"Temperature: {readout['t']} ^C"
    else:
        return "BMP280 is not enabeled in config"


def cmd_press():
    if init_bmp280:
        readout = bmp280_i2c.measurements
        return f"Temperature: {readout['p']} hPa"
    else:
        return "BMP280 is not enabeled in config"


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
}
