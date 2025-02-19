from w1thermsensor import W1ThermSensor
import time
from datetime import datetime
from statistics import mean

# Initialize the sensor
sensor = W1ThermSensor()

# Set temperature array
temp_array = []

for i in range(5):
    # Read temperature in Celsius
    temperature_c = round(sensor.get_temperature(),2)
    temp_array.append(temperature_c)
    time.sleep(1)
       
# Calculate temperature mean
mean_temp = mean(temp_array)

# Capture the current timestamp
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print(f"UTC: {current_time} - Temperature: {mean_temp:.2f}°C")