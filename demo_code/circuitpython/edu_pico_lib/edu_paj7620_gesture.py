#Import necessary libraries
import board
import busio
import edupico2_paj7620
import adafruit_ssd1306
import time

def init_oled():
    # Define the i2c GPIOs on SCL=GP5 and SDA=GP4
    global i2c
    i2c = busio.I2C(board.GP5, board.GP4)

    # Define the OLED display using the above pins
    global oled
    oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

def deinit_oled():
    #Clear the OLED display
    oled.fill(0)
    oled.show()
    print("deinit I2C")
    i2c.deinit()

def init_module(i2c):
    #Initialize the APDS9960 colour
    global paj7620_sensor
    paj7620_sensor = edupico2_paj7620.PAJ7620(i2c)
    
    global current_gesture
    current_gesture = "Move hand"
    
    global interval
    interval = time.monotonic()
    
def run_module(duration, oled):
    global interval
    global current_gesture
    #Read the gesture on specific interval
    if time.monotonic() > interval:
        interval = time.monotonic() + duration
        #Clear the OLED display
        oled.fill(0)
        
        #Write the data: ('text', x , y, pixel colour)
        #Pixel colour: 0 = false, 1 = true
        oled.text('PAJ7620', 40, 0, 1)

        gesture = paj7620_sensor.gesture()
        
        if gesture & paj7620_sensor.UP:
            current_gesture = "Up"
        elif gesture & paj7620_sensor.DOWN:
            current_gesture = "Down"
        elif gesture & paj7620_sensor.LEFT:
            current_gesture = "Left"
        elif gesture & paj7620_sensor.RIGHT:
            current_gesture = "Right"
        elif gesture & paj7620_sensor.CW:
            current_gesture = "Rotate CW"
        elif gesture & paj7620_sensor.CCW:
            current_gesture = "Rotate CCW"
            
        oled.text("Gesture: {}".format(current_gesture), 10, 30, 1)
        
        oled.text('(6)', 0, 0, 1)
        
        oled.text('BACK (A)', 0, 57, 1)
        oled.text('(B) NEXT', 80, 57, 1)
        oled.show()

def deinit_module():
    pass
    
if __name__ == "__main__":
    try:
        init_oled()
        init_module(i2c)
        while True:
            #Run the module with interval 0.05s
            run_module(0.05, oled)
    finally:
        deinit_module()
        deinit_oled()       

