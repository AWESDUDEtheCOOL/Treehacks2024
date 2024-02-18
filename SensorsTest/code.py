import time
import board
import digitalio
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction
import audiocore
import audioio
import array
import math

INTERNAL_MIC_PIN = AnalogIn(board.MIC)
BUZZ_PIN = board.A0

MIC_FILENAME = "audiopacket.txt"

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

print("== RUNNING RESPONSIO ==")

# Sine wave
length = 8000 // 440
sine_wave = array.array("h", [0] * length)
for i in range(length):
    sine_wave[i] = int(math.sin(math.pi * 2 * i / length) * (2**15))

speaking = False
speaker_count = 2

# dac = audioio.AudioOut(BUZZ_PIN)
# sine_wave = audiocore.RawSample(sine_wave)
# dac.play(sine_wave, loop=True)

while True:

    min_value = 65536
    max_value = 0

    for i in range(1000):
        mic_reading = (INTERNAL_MIC_PIN.value * 3.3) / 65536
        min_value = min(min_value, mic_reading)
        max_value = max(max_value, mic_reading)

    delta = max_value - min_value
    print(f"Min = {min_value} Max = {max_value} Delta = {delta}")

    if delta > 1:
        speaking = True
        speaker_count = 2
    else:
        if speaker_count > 0:
            speaker_count -= 1
        else:
            speaking = False

    if speaking:
        print("Speaking")

    time.sleep(0.5)
    # dac.stop()

# intel developer cloud


# while True:
#     # print("Light Sensor Voltage: ", get_voltage(analog_in))
#     print(e_mic_pin.value)
#     time.sleep(0.5)
