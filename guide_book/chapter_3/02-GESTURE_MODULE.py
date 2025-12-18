import board, busio
import edupico2_paj7620

i2c = busio.I2C(board.GP5, board.GP4)
sensor = edupico2_paj7620.PAJ7620(i2c)

while True:
    gesture = sensor.gesture()
    if gesture & sensor.UP:
        print("up")
    if gesture & sensor.DOWN:
        print("down")
    if gesture & sensor.LEFT:
        print("left")
    if gesture & sensor.RIGHT:
        print("right")
    if gesture & sensor.CW:
        print("clockwise")
    if gesture & sensor.CCW:
        print("counter clockwise")

