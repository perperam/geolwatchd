import pynmea2  # Install with: pip install pynmea2
import serial

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
                    print(f"Latitude: {msg.latitude} {msg.lat_dir}")
                    print(f"Longitude: {msg.longitude} {msg.lon_dir}")
                    print(f"Altitude: {msg.altitude} meters")
                    print(f"Number of Satellites: {msg.num_sats}")
                    # Add more fields as needed

            except pynmea2.ParseError:
                print(f"Error parsing NMEA sentence: {line}")