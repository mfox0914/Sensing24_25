from time import sleep
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_mcp2515.canio import Message, RemoteTransmissionRequest
from adafruit_mcp2515 import MCP2515 as CAN

# Configure DIP Switch inputs
dip0 = DigitalInOut(board.GP2)
dip1 = DigitalInOut(board.GP3)
dip2 = DigitalInOut(board.GP4)
dip3 = DigitalInOut(board.GP5)

# Set each DIP switch as an input
dip0.direction = Direction.INPUT
dip0.direction = Direction.INPUT
dip0.direction = Direction.INPUT
dip0.direction = Direction.INPUT

# Use an integrated pull-up resistor to prevent pins from floating; requires
# pins to be pulled to GND in order to be active
dip0.pull = Pull.UP
dip1.pull = Pull.UP
dip2.pull = Pull.UP
dip3.pull = Pull.UP



cs = DigitalInOut(board.D5)
cs.switch_to_output()
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

# adafruit note: use loopback to test without another device
can_bus = CAN(spi, cs, loopback=True, silent=True)  

while True:
    with can_bus.listen(timeout=1.0) as listener:

        message = Message(id=0x1234ABCD, data=b"adafruit", extended=True)
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