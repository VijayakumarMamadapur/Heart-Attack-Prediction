import serial
import sys
import io

# Set the standard output encoding to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

# Initialize serial connection (adjust the port and baud rate as needed)
try:
    ser = serial.Serial(port='COM7', baudrate=115200, timeout=1)  # Replace 'COM7' with your serial port
    print("Serial connection established on COM7")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    sys.exit(1)

current_bpm = None  # Variable to store the current heart rate

def read_data():
    global current_bpm
    while True:
        if ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8').rstrip()
                if line:  # Ensure the line is not empty
                    print(line)
                    sys.stdout.flush()  # Flush the output to ensure real-time display
                    if "BPM:" in line:  # Check if the line contains heart rate data
                        bpm = line.split("BPM:")[1].strip()
                        current_bpm = int(bpm)
            except UnicodeDecodeError as e:
                print(f"Unicode decode error: {e}")
                sys.stdout.flush()  # Flush the output on error

def get_current_bpm():
    return current_bpm

if __name__ == "_main_":
    try:
        read_data()
    except KeyboardInterrupt:
        print("Exiting...")
        ser.close()
    except serial.serialutil.SerialException as e:
        print(f"Serial error: {e}")
        ser.close()