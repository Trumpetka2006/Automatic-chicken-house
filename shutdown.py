from machine import Pin

print("Powering down all pins")

for i in range(23):
    pin = Pin(i,Pin.OUT)
    pin.off()
    
print("Done!")