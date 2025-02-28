from machine import Pin, UART, I2C, ADC, RTC
from utime import sleep
from bmp280 import BMP280I2C
from sim800l import SIM800L
from modules import ACS712, MotorDriver, Relay

init_bmp280 = False
init_sim800l = False
init_console = True

rtc = RTC()
wdt = None

LED = Pin(25,Pin.OUT)

relA = Pin(10, Pin.OUT)
relB = Pin(22, Pin.OUT)

motA = Pin(14, Pin.OUT)
motB = Pin(15, Pin.OUT)

debugMode = Pin(1, Pin.IN, Pin.PULL_UP)

curr = ACS712(ADC(Pin(26)))

door = MotorDriver(motA,motB)

light = Relay(relA)
heater = Relay(relB)

console_buff = ""

console = None
bmp280_i2c = None
sim = None

if init_console:
    console = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5), timeout=10)

if init_sim800l:
    uart0 = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))
    sim = SIM800L(uart0)
    
if init_bmp280:
    i2c1 = I2C(1, sda=Pin(18), scl=Pin(19), freq=400000)
    bmp280_i2c = BMP280I2C(0x76, i2c1)
    
def read_console(uart):
    global console_buff
    command = ""
    read = uart.read()
    if read == None:
        return
    else:
        read = read.decode("ascii")
    if read in "\r":
        console_buff += read
        uart.write(bytes(read,"ascii"))
        command = []
        for char in console_buff:
            if char == '\x7f' or char =='\x08':
                if command:
                    command.pop()
            else: 
                command.append(char)
        command = ''.join(command)
        console_buff = ""
        uart.write('\r\n')
        if command == "":
            return None
        return command
    else :
        console_buff += read
        uart.write(bytes(read,"ascii"))
        return None
