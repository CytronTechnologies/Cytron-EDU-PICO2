import board, digitalio, time, simpleio, busio, random
import adafruit_ssd1306, edupico2_paj7620

tone_map = {"Up": 261, "Down": 293, "Left": 329, "Right": 349}  # DO RE MI FA
tone_keys = ["Up", "Down", "Left", "Right"]

buzzer = board.GP21
button_tone = digitalio.DigitalInOut(board.GP0)
button_start = digitalio.DigitalInOut(board.GP1)
button_tone.direction = digitalio.Direction.INPUT
button_start.direction = digitalio.Direction.INPUT

i2c = busio.I2C(board.GP5, board.GP4)
sensor = edupico2_paj7620.PAJ7620(i2c)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

def gamestart():
    oled.fill(0)
    oled.text("Ready", 50, 25, 1)
    oled.show()
    time.sleep(1)
    oled.text("Swipe!", 50, 40, 1)
    oled.show()

def get_gesture():
    gesture = sensor.gesture()
    if gesture & sensor.UP:
        return "Up"
    elif gesture & sensor.DOWN:
        return "Down"
    elif gesture & sensor.LEFT:
        return "Left"
    elif gesture & sensor.RIGHT:
        return "Right"
    return None

def flush_gesture():
    sensor.gesture()
    time.sleep(0.1)

while True:
    oled.fill(0)
    oled.text("Button A: Test Tone", 10, 25, 1)
    oled.text("Button B: Play Game", 10, 40, 1)
    oled.show()
    
    if not button_tone.value:
        oled.fill(0)
        oled.text("Playing Test Tone", 15, 35, 1)
        oled.show()            
        for key in tone_keys:
            simpleio.tone(buzzer, tone_map[key], 0.3)
            
    if not button_start.value:
        gamestart()
        tone_gesture = random.choice(list(tone_map))
        selected_tone = tone_map[tone_gesture]
        simpleio.tone(buzzer, selected_tone, 1)
        flush_gesture()

        while True:
            gesture_value = get_gesture()
            if not gesture_value:
                continue
            if gesture_value == tone_gesture:
                oled.fill(0)
                oled.text("Good Job!", 35, 30, 1)
                oled.show()
                for i in range(3):
                    simpleio.tone(buzzer, 1100, 0.1)
                    time.sleep(0.1)
                break
            else:
                oled.fill(0)
                oled.text("Try Again!", 35, 30, 1)
                oled.show()
                for i in range(3):
                    simpleio.tone(buzzer, 100, 0.1)
                    time.sleep(0.1)