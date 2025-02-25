from machine import Pin
import time

LED = Pin(25, Pin.OUT)

while True :
    LED.value(not LED.value())
    time.sleep_ms(100)