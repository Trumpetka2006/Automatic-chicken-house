from machine import Pin, UART, I2C, ADC
from utime import sleep
from bmp280 import BMP280I2C
from sim800l import SIM800L
from modules import ACS712, MotorDriver, Relay

init_bmp280 = False
init_sim800l = True
init_debug = False



LED = Pin(25,Pin.OUT)

relA = Pin(10, Pin.OUT)
relB = Pin(22, Pin.OUT)

motA = Pin(14, Pin.OUT)
motB = Pin(15, Pin.OUT)

curr = ACS712(ADC(Pin(26)))

door = MotorDriver(motA,motB)

light = Relay(relA)
heater = Relay(relB)

if init_debug:
    debug = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

if init_sim800l:
    uart0 = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))
    sim = SIM800L(uart0)
    
if init_bmp280:
    i2c1 = I2C(1, sda=Pin(18), scl=Pin(19), freq=400000)
    bmp280_i2c = BMP280I2C(0x76, i2c1)
