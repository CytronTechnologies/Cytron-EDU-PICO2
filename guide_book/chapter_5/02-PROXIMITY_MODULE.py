import board, time, busio
import edupico2_paj7620

i2c = busio.I2C(board.GP5, board.GP4)
sensor = edupico2_paj7620.PAJ7620(i2c)

while True:
    gesture = sensor.gesture()
    proximity = sensor.proximity()

    if gesture & sensor.FAR:
        print(f"Proximity: {proximity}  |  Gesture: Far")
    elif gesture & sensor.NEAR:
        print(f"Proximity: {proximity}  |  Gesture: Near")
    else:
        print(f"Proximity: {proximity}")
    time.sleep(0.5)
