import board, digitalio, busio, adafruit_ssd1306
from pwmio import PWMOut
from adafruit_motor import motor
import edupico2_paj7620

i2c = busio.I2C(board.GP5, board.GP4)
sensor = edupico2_paj7620.PAJ7620(i2c)

PWM_M1A = PWMOut(board.GP10, frequency=10000)
PWM_M1B = PWMOut(board.GP11, frequency=10000)
motor_instance = motor.DCMotor(PWM_M1A, PWM_M1B)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
relay = digitalio.DigitalInOut(board.GP22)
relay.direction = digitalio.Direction.OUTPUT

class_num = 0
current_speed = 0.0

oled.invert(True)
oled.text("--------------------", 5, 15, 1)
oled.text("--------------------", 5, 40, 1)
oled.text("ROOM CAPACITY: ", 5, 7, 1)
oled.text("Light:", 5, 50, 1)
oled.text("Fan:", 65, 50, 1)
oled.text("<< EXIT    ENTER >>", 7, 27, 1)
oled.show()

def handle_gesture():
    global class_num, current_speed

    oled.fill_rect(90, 7, 35, 7, 0)
    oled.fill_rect(40, 50, 20, 7, 0)
    oled.fill_rect(90, 50, 35, 7, 0)
    gesture = sensor.gesture()

    if gesture & sensor.LEFT:
        class_num = max(0, class_num - 1)
    elif gesture & sensor.RIGHT:
        class_num = min(5, class_num + 1)

    current_speed = class_num * 0.2
    motor_instance.throttle = current_speed
    oled.text("{}%".format(current_speed * 100), 90, 50, 1)

    relay.value = class_num > 0
    oled.text("ON" if class_num > 0 else "OFF", 40, 50, 1)

    class_status = f"{class_num} PAX" if class_num < 5 else "FULL"
    oled.text(class_status, 90, 7, 1)
    oled.show()

try:
    while True:
        handle_gesture()

finally:
    oled.fill(1)
    oled.show()
    print("deinit I2C")
    i2c.deinit()
