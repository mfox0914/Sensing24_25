from machine import Pin
import time

led = Pin("LED", Pin.OUT)
while True:
    led.value(1)
    time.sleep_ms(500)
    led.value(0)
    time.sleep_ms(500)
