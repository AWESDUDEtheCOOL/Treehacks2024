from circuitpython_adapter import not_SMBus as SMBus
import time
import math
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

def send_command(command, debug=False):
    uart0.write(command)
    time.sleep(1)  # Adjust delay as needed
    response = uart0.readline()
    if response and debug:
        print(response.decode().strip())

def alarm(freq, duration):
    buzzer.frequency = freq
    buzzer.duty_cycle = ON
    time.sleep(duration)
    buzzer.duty_cycle = OFF

def transmit_lora(packet, target, alert="N"):
    packet_hex = binascii.hexlify((f'{ID}.{target}.{alert}::'+packet).encode()).decode()
    command = f'AT+TEST=TXLRPKT,"3C{packet_hex}3E"'
    send_command(bytes(command, 'utf-8'))
    print(f"Transmitting to Device {target} with alert {alert}")

def heading():
    # Read magnetometer data
    data = bus.read_i2c_block_data(0x0E, 0x01, 6)
    
    # Convert data to 16-bit integers
    x = (data[0] << 8) | data[1]
    if x > 32767:
        x -= 65536
    
    y = (data[2] << 8) | data[3]
    if y > 32767:
        y -= 65536
    
    # Apply hard iron offset
    x_calibrated = x - hard_iron_offsets[0]
    y_calibrated = y - hard_iron_offsets[1]
    
    # Calc heading
    heading = math.atan2(y_calibrated, x_calibrated)
    if heading < 0:
        heading += 2 * math.pi
    heading_degrees = math.degrees(heading)
    
    return heading_degrees

def decode(data):
    data = data.split("::")
    origin, target, priority = data[0].split(".")
    data = data[1]
    # Message from command
    if origin == "0":
        # Alert message
        if priority == "A":
            alarm(440, .05)
        print(f"MSG from Device {origin}: {data}")
    # Network alert
    elif target == "0" and priority == "A":
        alarm(440, .05)
        print(f"MSG from Device {origin}: {data}")
    # Local message
    elif ID == target:
        print(f"MSG from Device {origin}: {data}")


tr = DigitalInOut(board.BUTTON_1)
tr.direction = Direction.INPUT
tr.pull = Pull.UP

pr = DigitalInOut(board.BUTTON_2)
pr.direction = Direction.INPUT
pr.pull = Pull.UP

ar = DigitalInOut(board.BUTTON_3)
ar.direction = Direction.INPUT
ar.pull = Pull.UP

buzzer = pwmio.PWMOut(board.BUZZER, variable_frequency=True)

# Get I2C bus
bus = SMBus(1)
bus.write_byte_data(0x0E, 0x10, 0x01)

time.sleep(0.5)

# Calibration samples
NUM_SAMPLES = 100

# Init min/max values
min_val = [float('inf'), float('inf')]
max_val = [float('-inf'), float('-inf')]

print(f'Device ID: {ID}')
print("Compass calibration")
for _ in range(NUM_SAMPLES):
    data = bus.read_i2c_block_data(0x0E, 0x01, 6)
    
    # X/Y Data to 16-bit ints
    x = (data[0] << 8) | data[1]
    if x > 32767:
        x -= 65536
    
    y = (data[2] << 8) | data[3]
    if y > 32767:
        y -= 65536
    
    # Update min/max
    min_val = [min(x, min_val[0]), min(y, min_val[1])]
    max_val = [max(x, max_val[0]), max(y, max_val[1])]
    
    time.sleep(0.1)

print("Automatic iron calibration complete.")

# Calc hard iron offsets
hard_iron_offsets = [(max_val + min_val) / 2 for max_val, min_val in zip(max_val, min_val)]


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
    if not tr.value:
        print("Transmit Mode")
        while not tr.value:
            
            # Network alert
            if not ar.value:
                target = "0"
                alert = "A"
                alarm(440, .05)
                transmit_lora('Network Alert!', target, alert)
            # Local message
            elif not pr.value:
                target = "1"
                alert = "N"
                alarm(660, .05)
                transmit_lora(f'Local Message from Device {ID}', target, alert)
            # Command message
            else:
                target = "0"
                alert = "N"
                alarm(880, .05)
                transmit_lora(f'Heading {heading()} degrees', target, alert)
            

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
                            clr_str = binascii.unhexlify(data_read).decode("utf8")
                            decode(clr_str)

                    allstring = ""
                    printshow = False