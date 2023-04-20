from time import sleep
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_mcp2515.canio import Message, RemoteTransmissionRequest
from adafruit_mcp2515 import MCP2515 as CAN
from analogio import AnalogIn

# Dictionary to convert between DIP switch positions and CAN IDs. Keys are
# tuples representing the values of 4 DIP switches.
#
# Pins default being pulled high, so a pin is pulled to GND and represented by
# "false" when the DIP switch is toggled on
DIP_TO_CAN_ID = {
    (True, True, True, True)  : 0x1111FFAA,
    (False, True, True, True) : 0x1111FFBB,
    (True, False, True, True) : 0x1111EEAA,
    (True, True, False, True) : 0x1111EEBB
}

# Configure DIP Switch inputs
dip0 = DigitalInOut(board.GP11)
dip1 = DigitalInOut(board.GP10)
dip2 = DigitalInOut(board.GP9)
dip3 = DigitalInOut(board.GP8)

# Add all DIP switches to a list to make it easier to assign properties to each
dip_switches = [dip0, dip1, dip2, dip3]

# Define ride height sensor analog input pin
sensor_in = AnalogIn(board.A0)

for switch in dip_switches:
    # Set each DIP switch as an input
    switch.direction = Direction.INPUT
    # Use an integrated pull-up resistor to prevent pins from floating; requires
    # pins to be pulled to GND in order to be active
    switch.pull = Pull.UP

# Determine CAN address (board identity) based on DIP switch position
dip_positions = (dip0.value, dip1.value, dip2.value, dip3.value)
try:
    can_id = DIP_TO_CAN_ID[dip_positions]
    print(f"Successfully set CAN ID. Current ID is: f{can_id}")
except KeyError:
    print("Invalid DIP position. Defaulting to CAD address of 0x00000000")
    can_id = "0x00000000"



cs = DigitalInOut(board.GP21)
cs.switch_to_output()
spi = busio.SPI(board.GP18, board.GP19, board.GP20)

# adafruit note: use loopback to test without another device
can_bus = CAN(spi, cs, loopback=True, silent=True)  

while True:
    with can_bus.listen(timeout=1.0) as listener:

        print(f"Current Sensor Value: {sensor_in.value}")
        message = Message(id=can_id, data=b"adafruit", extended=True)
        send_success = can_bus.send(message)
        print("Send success:", send_success)
        message_count = listener.in_waiting()
        print(message_count, "messages available")
        for _i in range(message_count):
            msg = listener.receive()
            print("Message from ", hex(msg.id))
            if isinstance(msg, Message):
                print("message data:", msg.data)
            if isinstance(msg, RemoteTransmissionRequest):
                print("RTR length:", msg.length)
    sleep(1)