from machine import UART, Pin
import time

# Inicializace UART (UART1 na pinech GPIO4 = TX a GPIO5 = RX)
uart = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))

# Funkce pro odeslání příkazu a čtení odpovědi
def send_at_command(command, delay=1):
    uart.write(command + '\r\n')  # Odeslání příkazu s ukončením \r\n
    time.sleep(delay)            # Počkejte na odpověď
    response = uart.read()       # Přečtení odpovědi z modulu
    if response:
        print(response.decode('utf-8'))  # Dekódování a zobrazení odpovědi
    else:
        print("No response received.")

# Testovací smyčka
print("Testing SIM800L communication...")
#time.sleep(2)

# Odeslání základního příkazu AT
send_at_command("AT")

# Odeslání příkazu pro kontrolu signálu
send_at_command("AT+CSQ")

# Odeslání příkazu pro kontrolu registrace do sítě
send_at_command("AT+CREG?")

# Odeslání příkazu pro kontrolu operátora
send_at_command("AT+COPS?")

send_at_command("AT+CPOWD=1")
