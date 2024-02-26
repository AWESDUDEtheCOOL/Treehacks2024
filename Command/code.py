import time
import math
import board
import busio
import binascii
import sys
import re
from digitalio import DigitalInOut, Direction, Pull
import pwmio
import supervisor

ID = "0"  # Change to unique ID
OFF = 0
ON = 2 ** 15

def send_command(command, debug=False):
    uart0.write(command)
    time.sleep(1)
    response = uart0.readline()
    if response and debug:
        print(response.decode().strip())

def alarm(freq, duration):
    buzzer.frequency = freq
    buzzer.duty_cycle = ON
    time.sleep(duration)
    buzzer.duty_cycle = OFF

def transmit_lora(packet, target, alert="N"):
    packet_hex = binascii.hexlify((f'{ID}.{target}.{alert}::' + packet).encode()).decode()
    command = f'AT+TEST=TXLRPKT,"3C{packet_hex}3E"'
    send_command(bytes(command, 'utf-8'))
    print(f"Transmitting to Device {target} with alert {alert}")
    # Wait for transmission to complete before exiting
    time.sleep(5)

def decode(data):
    data = data.split("::")
    origin, target, priority = data[0].split(".")
    data = data[1]
    # Network alert
    if target == "0" and priority == "A":
        alarm(440, .05)
        print(f"MSG from Device {origin}: {data}")
    # Message from device
    elif target == "0":
        print(f"MSG from Device {origin}: {data}")

def command():
    while True:
        if supervisor.runtime.serial_bytes_available:
            user_input = input().strip()
            data, target, alert = user_input.split(";")
            return data, target, alert

buzzer = pwmio.PWMOut(board.BUZZER, variable_frequency=True)

uart0 = busio.UART(board.TX, board.RX, baudrate=9600)

cmds = [
    "AT+TEST=RFCFG,866,SF7,500,15,15,22,ON,OFF,OFF",
    "AT+MODE=TEST"]
for cmd in cmds:
    send_command(bytes(cmd + '\r\n', 'utf-8'))
print("LORA Configured")

tx = DigitalInOut(board.BUTTON_3)
tx.direction = Direction.INPUT
tx.pull = Pull.UP

allstring = ""
printshow = False

while True:
    if not tx.value:
        print("Transmit Mode")
        data, target, alert = command()
        # Network alert
        if target == "" and alert == "A":
            alarm(440, .05)
            transmit_lora(data, target, alert)
        # Command message and alert
        elif alert == "A":
            alarm(880, .05)
            transmit_lora(data, target, alert)
        # Command message
        else:
            alarm(660, .05)
            transmit_lora(data, target, alert)

    else:
        send_command(bytes("AT+TEST=RXLRPKT\r\n", 'utf-8'))
        print("Receive Mode")
        
        regex_pattern = re.compile(r'"3C(.*?)(3E)"')

        while tx.value:
            byte_read = uart0.readline()  # read up to 32 bytes
            if byte_read:
                allstring += byte_read.decode()
                printshow = True
            else:
                if printshow:
                    if allstring:
                        match = regex_pattern.search(allstring)
                        if match:
                            data_read = match.group(1)
                            clr_str = binascii.unhexlify(data_read).decode("utf8")
                            decode(clr_str)
                    allstring = ""
                    printshow = False
