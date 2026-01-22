import machine
import time

# The Internal Temperature Sensor is connected to ADC Channel 4
temp_sensor = machine.ADC(4)

# Conversion factor: 3.3V / 65535 (16-bit)
conversion_factor = 3.3 / 65535

print("RP2040 Internal Temperature Monitor")
print("------------------------------------")

while True:
    # 1. Read the raw ADC value
    reading = temp_sensor.read_u16() * conversion_factor
    
    # 2. Convert voltage to Celsius
    # The formula is from the RP2040 Datasheet: 
    # T = 27 - (Reading - 0.706) / 0.001721
    temperature = 27 - (reading - 0.706) / 0.001721
    
    # 3. Print the result
    print(f"Chip Temp: {temperature:.2f} °C")
    
    # Wait for a second
    time.sleep(1)