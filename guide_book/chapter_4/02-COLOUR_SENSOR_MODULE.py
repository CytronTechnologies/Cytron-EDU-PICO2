import time, board, busio, neopixel
from adafruit_opt4048 import OPT4048, Mode

num_pixels = 5
pixel_pin = board.GP14
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2)  

i2c = busio.I2C(board.GP5, board.GP4)
sensor = OPT4048(i2c)
sensor.mode = Mode.CONTINUOUS

while True:
    pixels.fill((255, 255, 255))
    R, G, B, LUX = sensor.rgb
    print(f"red: {R}, green: {G}, blue: {B}, lux: {LUX:.2f}")
    time.sleep(1)
