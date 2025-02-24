import machine
import utime

# Nastavení UART (TX=GP0, RX=GP1 na Raspberry Pi Pico)
uart = machine.UART(0, baudrate=9600, tx=machine.Pin(16), rx=machine.Pin(17))

def send_at_command(command, delay=1):
    """ Odešle AT příkaz do modulu a počká na odpověď """
    uart.write(command + "\r\n")
    utime.sleep(delay)
    response = uart.read()
    if response:
        print(response.decode())

# 1️⃣ Ověření komunikace s modulem
send_at_command("AT", 2)  # Modul by měl odpovědět "OK"

# 2️⃣ Přepnutí do textového režimu SMS
send_at_command("AT+CMGF=1", 1)

# 3️⃣ Zadání telefonního čísla a odeslání SMS
phone_number = "+420723748913"  # Změňte na cílové číslo
send_at_command(f'AT+CMGS="{phone_number}"', 1)

# 4️⃣ Odeslání textu zprávy
sms_text = "Hello from Raspberry Pi Pico!"
uart.write(sms_text + "\r\n")

# 5️⃣ Odeslání CTRL+Z (konec zprávy)
uart.write(chr(26))  # ASCII 26 = CTRL+Z
utime.sleep(3)  # Počkat na odpověď modulu

# 6️⃣ Výpis odpovědi modulu
response = uart.read()
if response:
    print(response.decode())
