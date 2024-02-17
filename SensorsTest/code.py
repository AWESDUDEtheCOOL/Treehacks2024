import time
import board
from analogio import AnalogIn

"""
BUZZER
BUTTON_1
BUTTON_2
BUTTON_3

DISPLAY
GYROSCOPE_INT
GYROSCOPE_SCL
GYROSCOPE_SDA
I2C
SDA
MIC
RX
TX
board_id
"""

analog_in = AnalogIn(board.LIGHT)  # Light Sensor pin on Wio Terminal
# e_mic_pin = AnalogIn(board["A0"])
# i_mic_pin = AnalogIn(board["MICROPHONE_DATA"])

e_mic_pin = AnalogIn(board.A0)
i_mic_pin = AnalogIn(board.MIC)
# button1_pin = AnalogIn()


def get_voltage(pin):
    return (pin.value * 3.3) / 65536


print("== RUNNING RESPONSIO ==")
while True:
    print(get_voltage(e_mic_pin))
    print(get_voltage(i_mic_pin))

# while True:
#     # print("Light Sensor Voltage: ", get_voltage(analog_in))
#     print(e_mic_pin.value)
#     time.sleep(0.5)
