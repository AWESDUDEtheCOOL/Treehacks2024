import time
import board
import busio
import binascii
import sys
import re
from digitalio import DigitalInOut, Direction, Pull
import pwmio


ID = "2"  # Change this to a unique ID for each device
OFF = 0
ON = 2**15

def send_command(command):
    uart0.write(command)
    time.sleep(1)  # Adjust delay as needed
    response = uart0.readline()
    if response:
        print(response.decode().strip())

def transmit_lora(packet):
    packet_hex = binascii.hexlify((f'{ID}:'+packet).encode()).decode()
    command = f'AT+TEST=TXLRPKT,"3C{packet_hex}3E"'
    send_command(bytes(command, 'utf-8'))

tr = DigitalInOut(board.BUTTON_1)
tr.direction = Direction.INPUT
tr.pull = Pull.UP

buzzer = pwmio.PWMOut(board.BUZZER, variable_frequency=True)
buzzer.frequency = 440  # set a note, like Middle C
buzzer.duty_cycle = ON  # enable the buzzer to play the note
buzzer.duty_cycle = OFF # turn off the note

uart0 = busio.UART(board.TX, board.RX, baudrate=9600)

cmds = [
        "AT+TEST=RFCFG,866,SF7,500,15,15,22,ON,OFF,OFF",
        "AT+MODE=TEST"]
for cmd in cmds:
    send_command(bytes(cmd + '\r\n', 'utf-8'))
print("LORA Configured")

allstring = ""
printshow = False

while True:
    buzzer.duty_cycle = OFF
    if not tr.value:
        buzzer.duty_cycle = ON  # enable the buzzer to play the note
        print("Transmit Mode")
        msgnum = 1

        while not tr.value:
            transmit_lora(f"Hello World #{msgnum}")
            msgnum += 1

    else:
        send_command(bytes("AT+TEST=RXLRPKT\r\n", 'utf-8'))
        print("Receive Mode")
        
        
        regex_pattern = re.compile(r'"3C(.*?)(3E)"')

        while tr.value:

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
                            clear_string = binascii.unhexlify(data_read).decode("utf8")
                            print(clear_string)

                    allstring = ""
                    printshow = False