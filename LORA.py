import board
import busio
import digitalio
import time
import supervisor

# Set UART Pin to the pin where Grove Lora E5 is connected
uart = busio.UART(board.TX, board.RX, baudrate=9600)
get_input = True
message_started = False
message_print = []
allstring = ""
printshow = False

while True:
    if supervisor.runtime.serial_bytes_available:
        allstring=""
        # wait for user input
        userinput = input().strip() #input command
        # convert to byte
        b = bytes(userinput, 'utf-8')
        # write out the byte
        uart.write(b)
        continue
    byte_read = uart.readline()# read one line
    if byte_read != None:
        allstring += byte_read.decode()
        printshow = True
    else:
        if printshow == True:
            if allstring != "":
                print(allstring)
            allstring=""
            printshow ==False