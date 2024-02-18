import serial
import time

serial_port = 'COM19'
baud_rate = 115200

ser = serial.Serial(serial_port, baud_rate, timeout=1)

def send_command(command):
    ser.write((command + '\r\n').encode())

def receive_data():
    data = ser.readline().decode().strip()
    return data

while True:
    command = input("Mode (tx/rx): ").strip().lower()
    if command == 'tx':
        msg = input("msg: ").strip()
        send_command(msg)
    elif command == 'rx':
        print("Press Enter to stop")
        while True:
            response = receive_data()
            if response:
                print(response)
    else:
        print("Invalid command")