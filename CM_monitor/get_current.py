from machine import Pin, I2C, RTC
from ina219 import INA219
from logging import INFO
import time
import _thread

SHUNT_OHMS = 0.1

# Initialize I2C
i2c = I2C(1, scl=Pin(22), sda=Pin(21))

# Initialize INA219
ina = INA219(SHUNT_OHMS, i2c, log_level=INFO)

# Configure INA219
try:
    ina.configure()
    print("INA219 configured")
except Exception as e:
    print(f"Error configuring INA219: {e}")

def get_info():
    try:
        voltage = ina.voltage()
        current = ina.current()
        power = ina.power()
        return voltage, current, power
    except Exception as e:
        print(f"Error getting INA219 data: {e}")
        return None, None, None

def write_to_csv():
    filename = "power_data.csv"
    
    # Create and write header to CSV file
    with open(filename, "a") as f:
        f.write("Timestamp,Voltage(V),Current(mA),Power(mW)\n")

    start_time = time.time()
    
    while True:
        voltage, current, power = get_info()
        if voltage is not None:
            current_time = time.time() - start_time
            total_seconds = int(current_time)
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            time_str = "{:02d}:{:02d}".format(minutes, seconds)
            
            # Append data to CSV file
            with open(filename, "a") as f:
                f.write(f"{time_str},{voltage:.2f},{current:.2f},{power:.2f}\n")
            
            print(f"Data written: {time_str}, {voltage:.2f}V, {current:.2f}mA, {power:.2f}mW")
        
        time.sleep(1)  # Wait for 1 second

_thread.start_new_thread(write_to_csv,())

# Start writing data to CSV
# write_to_csv()