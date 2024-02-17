import time
import board
from analogio import AnalogIn

analog_in = AnalogIn(board.LIGHT)  # Light Sensor pin on Wio Terminal


def get_voltage(pin):
    return (pin.value * 3.3) / 65536


while True:
    print("Light Sensor Voltage: ", get_voltage(analog_in))
    time.sleep(0.1)
