import board
import digitalio
import storage

print("hi there")
switch = digitalio.DigitalInOut(board.D4)
switch.direction = digitalio.Direction.INPUT
# switch.pull = digitalio.Pull.UP
print(switch.value) 

# If the D0 is connected to ground with a wire
# CircuitPython can write to the drive
storage.remount("/", readonly=switch.value)

# for some reason this is reversed: readonly=True means not readonly