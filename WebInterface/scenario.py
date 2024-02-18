import json
import time
import requests
import datetime
import serial

serial_port = "/dev/cu.usbmodem11201"
baud_rate = 115200

ser = serial.Serial(serial_port, baud_rate, timeout=1)


def send_command(command):
    ser.write((command + "\r\n").encode())


def receive_data():
    data = ser.readline().decode().strip()
    return data


def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%m:%S")


def load_gps(filename):
    with open(filename) as f:
        ER = f.read()

    ER = ER.split("\n")
    ER = [row.split(", ") for row in ER]
    for i in range(len(ER)):
        ER[i] = [float(ER[i][0]), float(ER[i][1])]

    return ER


ER1 = load_gps("audioclips/ER1.txt")
ER2 = load_gps("audioclips/ER2.txt")
ER3 = load_gps("audioclips/ER3.txt")

status = {
    "ER1": {"GPS": ER1[0]},
    "ER2": {"GPS": ER2[0]},
    "ER3": {"GPS": ER3[0]},
}

frame = 0

sent_msg1 = False

while True:

    print(f"ER1 at location {status['ER1']['GPS']}")
    print(f"ER2 at location {status['ER2']['GPS']}")
    print(f"ER3 at location {status['ER3']['GPS']}")
    print()

    frame += 1
    status["ER1"]["GPS"] = ER1[frame % len(ER1)]
    status["ER2"]["GPS"] = ER2[frame % len(ER2)]
    status["ER3"]["GPS"] = ER3[frame % len(ER3)]

    requests.post(
        "http://127.0.0.1:5000/gps",
        data=f"ER1,{status['ER1']['GPS'][0]},{status['ER1']['GPS'][1]},{now()}",
    )
    requests.post(
        "http://127.0.0.1:5000/gps",
        data=f"ER2,{status['ER2']['GPS'][0]},{status['ER2']['GPS'][1]},{now()}",
    )
    requests.post(
        "http://127.0.0.1:5000/gps",
        data=f"ER3,{status['ER3']['GPS'][0]},{status['ER3']['GPS'][1]},{now()}",
    )

    response = receive_data()
    if response:
        if "Device 1" in response and "Heading" in response:
            print("Sending ER1...")
            requests.post("http://127.0.0.1:5000/ER1", data=response[19:])
        if "Device 2" in response and "Heading" in response:
            print("Sending ER2...")
            requests.post("http://127.0.0.1:5000/ER2", data=response[19:])

    with open("static/networkalert.txt") as f:
        content = f.read()

    if content == "TRUE":
        print("Sending alert!")
        send_command("Fire Nearby!;0;A")
        with open("static/networkalert.txt", "w") as f:
            f.write("FALSE")

    time.sleep(1)


# "MSG from Device 1: Heading 357.862 degrees"
