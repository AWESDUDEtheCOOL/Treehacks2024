"""
File: code.py
Send commands via the controller.
"""

#### IMPORTS
import time
import board
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
import audiocore
import audioio
import array
import math


#### PIN SETUP
MIC = AnalogIn(board.MIC)

BUTTON_LEFT = DigitalInOut(board.BUTTON_3)
BUTTON_LEFT.direction = Direction.INPUT
BUTTON_LEFT.pull = Pull.UP

BUTTON_MIDDLE = DigitalInOut(board.BUTTON_2)
BUTTON_MIDDLE.direction = Direction.INPUT
BUTTON_MIDDLE.pull = Pull.UP

BUTTON_RIGHT = DigitalInOut(board.BUTTON_1)
BUTTON_RIGHT.direction = Direction.INPUT
BUTTON_RIGHT.pull = Pull.UP


#### FUNCTIONS
def get_voltage(pin, v=3.3):
    return (pin.value * v) / 65536


def is_pressed(button_pin):
    return not button_pin.value


#### INITIALIZATION
audio_array = []
is_recording = False

#### LOOP
print("== RUNNING RESPONSIO ==")

counter = 0
while True:

    # LEFT BUTTON: START / STOP RECORDING
    if is_pressed(BUTTON_LEFT):
        if not is_recording:
            print("[*] Recording started...")
            audio_array = []
            is_recording = True
        else:
            print("[*] Recording stopped...")
            is_recording = False

    # MIDDLE BUTTON: SEND LORA PACKETS
    if is_pressed(BUTTON_MIDDLE):
        print("[*] Sending audio data over LoRA...")
        print(audio_array)

    # SAVE AUDIO TO ARRAY
    if is_recording:
        min_value = 65536
        max_value = 0

        for i in range(100):
            mic_reading = get_voltage(MIC)
            min_value = min(min_value, mic_reading)
            max_value = max(max_value, mic_reading)

        delta = max_value - min_value
        audio_array.append(delta)

        if counter == 0:
            print(f"Min = {min_value} Max = {max_value} Delta = {delta}")

    counter = (counter + 1) % 10
    time.sleep(0.1)
