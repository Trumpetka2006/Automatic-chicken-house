import machine
import utime

# Inicializace UART pro SIM800L
uart = machine.UART(0, baudrate=9600, tx=machine.Pin(16), rx=machine.Pin(17), timeout=500)

def send_at_command(command, delay=1):
    """ Odešle AT příkaz a počká na odpověď """
    uart.write(command + "\r\n")
    utime.sleep(delay)
    response = uart.read()
    if response:
        print(response.decode('utf-8'))  # Ignoruje neplatné znaky

# Nastavení SIM800L do správného režimu
send_at_command("AT")                # Test komunikace
send_at_command("AT+CMGF=1")          # Přepnutí do textového režimu SMS
send_at_command("AT+CNMI=2,1,0,0,0")  # Automatická notifikace o nové zprávě

print("📡 Čekám na SMS...")

while True:
    if uart.any():  # Pokud jsou dostupná data na UARTu
        data = uart.read().decode('utf-8')
        print("📩 Přijatá data:", data)

        if "+CMTI:" in data:  # Indikace nové SMS zprávy
            index = data.split(",")[1].strip()
            print(f"📥 Nová zpráva na indexu: {index}")

            # Přečtení obsahu zprávy
            send_at_command(f"AT+CMGR={index}")

    utime.sleep(0.5)  # Krátká prodleva
