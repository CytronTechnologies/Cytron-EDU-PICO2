import time, board, busio
from adafruit_opt4048 import OPT4048, Mode

i2c = busio.I2C(board.GP5, board.GP4)
sensor = OPT4048(i2c)
sensor.mode = Mode.CONTINUOUS

MAX_LUX = 1000

while True:
    R, G, B, LUX = sensor.rgb
    brightness_percent = min((LUX / MAX_LUX)*100, 100)
    print(f"Brightness: {brightness_percent:.1f}%")
    time.sleep(1)


