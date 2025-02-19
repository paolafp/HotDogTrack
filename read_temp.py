#!/usr/bin/env python3

import os
import pandas as pd
from w1thermsensor import W1ThermSensor
import time
from datetime import datetime
from os.path import join

# Initialize the sensor
sensor = W1ThermSensor()

# Single dictionary to store all sensor readings
data = {"timestamp": [], "temperature_c": []}

try:
    while True:
               
        # Capture the current timestamp
        current_time = datetime.now()#.strftime("%Y-%m-%d %H:%M:%S")
        timestamp_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        date_str = current_time.strftime("%Y-%m-%d")

        # Create a daily filename and a file directory
        data_directory = "/home/paola/CSV_data/"
        os.makedirs(data_directory, exist_ok=True)
        csv_filename = join(data_directory, f"temp_data_{date_str}.csv")
        
        # Read temperature in Celsius
        temperature_c = round(sensor.get_temperature(),2)

        print(f"UTC: {timestamp_str} - Temperature: {temperature_c:.2f}°C")
        
        # Update the dictionary with the new reading
        data["timestamp"].append(timestamp_str)
        data["temperature_c"].append(temperature_c)
        
        # Create a DataFrame for the new measurement
        df_new = pd.DataFrame({
            "timestamp": [timestamp_str],
            "temperature_c": [temperature_c]
        })
        
        
        # Append the measurement to the CSV file.
        # The header is written only if the file does not exist.
        df_new.to_csv(csv_filename, mode="a", index=False, header=not os.path.exists(csv_filename))
        
        # Wait for 1 second before the next reading
        time.sleep(1)

except KeyboardInterrupt:
    print("\nProgram terminated.")

