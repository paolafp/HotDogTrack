#!/usr/bin/env python3

import serial
import json
import time
import pynmea2
import pandas as pd
import os
from datetime import datetime
from os.path import join

def open_serial_port():
    """Try to open the serial port with different common baud rates."""
    baud_rates = [115200]
    for baud in baud_rates:
        try:
            print(f"Trying baud rate: {baud}")
            ser = serial.Serial('/dev/ttyACM0', baud, timeout=1)
            time.sleep(2)  # Wait for connection to establish
            return ser
        except Exception as e:
            print(f"Failed at {baud} baud: {e}")
    return None

def main():
        
    while True:  # Main loop that keeps the program running
        try:
            ser = open_serial_port()
            if not ser:     #automatic reconnection if open serial port fails
                print("Could not open serial port. Retrying in 5 seconds...")
                time.sleep(5)
                continue

            print("Serial port opened successfully")
        
            while True:  # Data reading loop
                try:
                    if ser.in_waiting:
                        line = ser.readline().decode('utf-8').strip()
                        
                        # Handle NMEA sentences that start with "$GPRMC"
                        if line.startswith("$GPRMC"):
                            # Get the current timestamp as a datetime object
                            current_time = datetime.now()
                            
                            # Format the timestamp and date parts
                            timestamp_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
                            date_str = current_time.strftime("%Y-%m-%d")
                            
                            # Create a daily filename and a file directory
                            data_directory = "/home/paola/CSV_data/"
                            os.makedirs(data_directory, exist_ok=True)
                            csv_filename = join(data_directory, f"gps_data_{date_str}.csv")
                            
                            # Parse the NMEA sentence using pynmea2
                            msg = pynmea2.parse(line)
                            
                            # Print formatted output for debugging or logging purposes
                            print(f"UTC: {timestamp_str} - Position: {line}")
                            
                            # Create a DataFrame for the current measurement
                            df_new = pd.DataFrame({
                                "timestamp": [timestamp_str],
                                "GPRMC": [line],
                                "latitude": [msg.latitude],
                                "longitude": [msg.longitude],
                                "Speed kmh": [msg.spd_over_grnd * 1.852]
                            })
                            
                            # Append the measurement to the CSV file.
                            # If the file does not exist yet (new day), include the header.
                            df_new.to_csv(csv_filename, mode="a", index=False, 
                                        header=not os.path.exists(csv_filename))
                            
                except UnicodeDecodeError:
                    print("Received invalid data - possible baud rate mismatch")
                    break  # Break inner loop to reconnect
                except serial.SerialException as e:
                    print(f"Serial error: {e}")
                    break  # Break inner loop to reconnect
                
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\nExiting...")
            if 'ser' in locals() and ser is not None:
                ser.close()
                print("Serial port closed")
            return  # Exit the program completely
        except Exception as e:
            print(f"Unexpected error: {e}")
            if 'ser' in locals() and ser is not None:
                ser.close()
                print("Serial port closed")
            print("Attempting to reconnect in 5 seconds...")
            time.sleep(5)


if __name__ == "__main__":
    main()