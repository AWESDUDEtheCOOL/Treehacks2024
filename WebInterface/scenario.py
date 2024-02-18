import json
import time
import requests


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
        "http://127.0.0.1:5000",
        data=f"ER1,{status['ER1']['GPS'][0]},{status['ER1']['GPS'][1]}",
    )
    requests.post(
        "http://127.0.0.1:5000",
        data=f"ER2,{status['ER2']['GPS'][0]},{status['ER2']['GPS'][1]}",
    )
    requests.post(
        "http://127.0.0.1:5000",
        data=f"ER3,{status['ER3']['GPS'][0]},{status['ER3']['GPS'][1]}",
    )

    time.sleep(1)
