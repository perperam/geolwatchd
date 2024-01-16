import pynmea2  # Install with: pip install pynmea2
import serial
import datetime

port = "/dev/ttyACM0"
baud_rate = 9600

with serial.Serial(port, baud_rate, timeout=1) as ser:
    while True:
        line = ser.readline().decode("utf-8").strip()

        # Check if the line is a valid NMEA sentence
        if line.startswith('$'):
            try:
                msg = pynmea2.parse(line)

                # Check the type of NMEA sentence
                if isinstance(msg, pynmea2.GGA):
                    print(f"Lat: {msg.latitude} {msg.lat_dir} | "
                          f"Lon: {msg.longitude} {msg.lon_dir} | "
                          f"Alt: {msg.altitude} | "
                          f"NumSats: {msg.num_sats}")
                    # Add more fields as needed
                    # with open("./sample_data.txt", "a") as f:
                      #  f.write(str(datetime.datetime.now())+str(msg.fields)+'\n')

            except pynmea2.ParseError:
                print(f"Error parsing NMEA sentence: {line}")