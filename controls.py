from time import sleep_ms, ticks_ms, ticks_diff
from hardware import console


def monitor_motor(timeout, s_curr, motor):
    timestart = ticks_ms()
    timediff = 0
    while timediff < timeout:
        timediff = ticks_diff(ticks_ms(), timestart)
        if float(s_curr.read_mA()) > 4 and timediff > 500:
            motor.lock_error()
            break
        sleep_ms(1)
    motor.complete()
    
def stdout(prefix,message):
    if console:
        console.write(f"{prefix.upper()}:{message}\r\n")
    print(f"{prefix.upper()}:{message}\r\n")

