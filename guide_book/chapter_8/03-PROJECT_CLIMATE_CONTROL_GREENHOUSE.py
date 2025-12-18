import board, busio, time, adafruit_ssd1306, neopixel
import adafruit_ahtx0
from pwmio import PWMOut
from adafruit_motor import servo, motor
from adafruit_opt4048 import OPT4048, Mode

i2c = busio.I2C(board.GP5, board.GP4)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
oled.invert(True)

aht20 = adafruit_ahtx0.AHTx0(i2c)
opt = OPT4048(i2c)
opt.mode = Mode.CONTINUOUS

pixels = neopixel.NeoPixel(board.GP14, 5, brightness=0.2)

PWM_Servo = PWMOut(board.GP6, frequency=50)
servo = servo.Servo(PWM_Servo, min_pulse=500, max_pulse=2500)

PWM_M1A = PWMOut(board.GP10, frequency=10000)
PWM_M1B = PWMOut(board.GP11, frequency=10000)
motor = motor.DCMotor(PWM_M1A, PWM_M1B)

def light_on():
    pixels.fill((255, 0, 255))
    oled.text("Light Status: On", 5, 52, 1)
    
def light_off():
    pixels.fill((0, 0, 0))
    oled.text("Light Status: Off", 5, 52, 1)
    
def servo_on():
    servo.angle = 60
    oled.text("Servo Status: On", 5, 15, 1)
    
def servo_off():
    servo.angle = 120
    oled.text("Servo Status: Off", 5, 15, 1)

def temp_control(temp_threshold):
    temperature = aht20.temperature
    oled.text("Temperature: {:.1f} C".format(temperature), 5, 3, 1)
    if temperature >= temp_threshold:
        servo_on()
        motor.throttle = 0.25
        oled.text("Fan Status: On", 5, 27, 1)
    else:
        servo_off()
        motor.throttle = 0
        oled.text("Fan Status: Off", 5, 27, 1)
        
def light_control(light_threshold):
    R, G, B, lux = opt.rgb
    oled.text("Light Lux: {:.1f}".format(lux), 5, 39, 1)
    if lux < light_threshold:
        light_on()
    else:
        light_off()

try:
    while True:
        oled.fill(0)
        temp_control(temp_threshold=27)
        light_control(light_threshold=100)
        oled.show()
        time.sleep(2)

finally:
    oled.fill(1)
    oled.show()
    print("Deinit I2C")
    i2c.deinit()
