import board, digitalio, time, simpleio, neopixel, busio, random
from adafruit_opt4048 import OPT4048, Mode
import adafruit_ssd1306

i2c = busio.I2C(board.GP5, board.GP4)
sensor = OPT4048(i2c)
sensor.mode = Mode.CONTINUOUS

buzzer = board.GP21
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

button_start = digitalio.DigitalInOut(board.GP0)
button_start.direction = digitalio.Direction.INPUT

num_pixels = 5
pixel_pin = board.GP14
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2)

MELODY_NOTE = [523, 659, 784, 0, 659, 784]
MELODY_DURATION = [0.12, 0.12, 0.12, 0.1, 0.12, 0.2]

colours = ["Red", "Green", "Blue", "Yellow", "Purple"]

oled.fill(0)
oled.text("Press A to", 35, 25, 1)
oled.text("Start a New Game", 15, 35, 1)
oled.show()

while True:
    pixels.fill((0, 0, 0))
    while button_start.value:
        pass
    oled.fill(0)
    oled.show()
    random_colour = random.choice(colours)
    oled.text("Find this colour:", 10, 10, 1)
    oled.text("{}".format(random_colour), 20, 25, 1)
    oled.show()
    time.sleep(2)
    pixels.fill((255, 255, 255))
    oled.text("Time left:   seconds", 5, 50, 1)

    for countdown in range(5, -1, -1):
        oled.fill_rect(70, 50, 10, 7, 0)
        oled.text("{}".format(countdown), 70, 50, 1)
        oled.show()
        time.sleep(1)

    R, G, B, LUX = sensor.rgb
    if (R > G) and (R > B):
        if G > B:
            detected_colour = "Yellow"
        else:
            detected_colour = "Red"
    elif (B > R) and (B > G):
        if R > G:
            detected_colour = "Purple"
        else:
            detected_colour = "Blue"
    elif (G > R) and (G > B):
        detected_colour = "Green"

    oled.fill(0)
    oled.text("Detected: {}".format(detected_colour), 10, 5, 1)
    oled.show()

    if detected_colour == random_colour:
        oled.text("Well Done!", 35, 25, 1)
        oled.text("Press A to", 35, 45, 1)
        oled.text("Start a New Game", 15, 55, 1)
        oled.show()
        for i in range(len(MELODY_NOTE)):
            simpleio.tone(buzzer, MELODY_NOTE[i], MELODY_DURATION[i])
    else:
        oled.text("Try Again.", 35, 25, 1)
        oled.text("Press A to", 35, 45, 1)
        oled.text("Start a New Game", 15, 55, 1)
        oled.show()
        for i in range(3):
            simpleio.tone(buzzer, 100, 0.1)
            simpleio.tone(buzzer, 0, 0.1)
