import machine
import utime

# Inicializace UART0 pro SIM800L (RX na 17, TX na 16)
uart0 = machine.UART(0, baudrate=9600, tx=machine.Pin(16), rx=machine.Pin(17), timeout=500)

# Inicializace UART1 pro výstup zpráv (TX na 4, RX na 5)
uart1 = machine.UART(1, baudrate=115200, tx=machine.Pin(4), rx=machine.Pin(5), timeout=500)

def send_at_command(command, delay=1):
    """ Odešle AT příkaz a počká na odpověď """
    uart0.write(command + "\r\n")
    utime.sleep(delay)
    response = uart0.read()
    if response:
        uart1.write(response)  # Výstup na UART1

# Nastavení SIM800L do správného režimu
send_at_command("AT")                # Test komunikace
send_at_command("AT+CMGF=1")          # Přepnutí do textového režimu SMS
send_at_command("AT+CNMI=2,1,0,0,0")  # Automatická notifikace o nové zprávě

uart1.write("📡 Čekám na SMS...\n")

while True:
    if uart0.any():  # Pokud jsou dostupná data na UART0
        data = uart0.read().decode(errors='ignore')
        uart1.write("📩 Přijatá data: " + data + "\n")

        if "+CMTI:" in data:  # Indikace nové SMS zprávy
            index = data.split(",")[1].strip()
            uart1.write(f"📥 Nová zpráva na indexu: {index}\n")

            # Přečtení obsahu zprávy
            send_at_command(f"AT+CMGR={index}")

    utime.sleep(0.5)  # Krátká prodleva
