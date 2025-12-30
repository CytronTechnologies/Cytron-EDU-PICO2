#Import necessary libraries
import board
import busio
import adafruit_ssd1306
import time
from adafruit_opt4048 import OPT4048, Mode

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
    #Initialize the OPT4048 sensor
    global opt4048_sensor
    opt4048_sensor = OPT4048(i2c)
    opt4048_sensor.mode = Mode.CONTINUOUS
    
    global interval
    interval = time.monotonic()
    
def run_module(duration, oled):
    global interval
    #Read the colours on specific interval
    if time.monotonic() > interval:
        interval = time.monotonic() + duration
        #Clear the OLED display
        oled.fill(0)
        
        #Write the data: ('text', x , y, pixel colour)
        #Pixel colour: 0 = false, 1 = true
        oled.text('OPT4048', 40, 0, 1)
        

        # get the data
        r, g, b, c = opt4048_sensor.rgb
        CIEx, CIEy, lux = opt4048_sensor.cie
    
        oled.text("Color Temp: {:.2f}".format(opt4048_sensor.calculate_color_temperature(CIEx, CIEy)), 3, 20, 1)
        oled.text("Light Lux : {:.2f}".format(c), 3, 35, 1)
        
        oled.text('(5)', 0, 0, 1)
        
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
            #Run the module with interval 0.5s
            run_module(0.5, oled)
    finally:
        deinit_module()
        deinit_oled()       

