#Import necessary libraries
import board
import busio
import adafruit_ssd1306
import time
import edupico2_paj7620

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
    #Initialize the PAJ7620 sensor
    global paj7620_sensor
    paj7620_sensor = edupico2_paj7620.PAJ7620(i2c)
    
    global interval
    interval = time.monotonic()

def run_module(duration, oled):
    global interval
    #Read the proximity on specific interval
    if time.monotonic() > interval:
        interval = time.monotonic() + duration
        
        proximity = paj7620_sensor.proximity()
        
        #Clear the OLED display
        oled.fill(0)
        
        #Write the data: ('text', x , y, pixel colour)
        #Pixel colour: 0 = false, 1 = true
        oled.text('PAJ7620', 40, 0, 1)
            
        oled.text("Proximity:{}".format(proximity), 25, 25, 1)
        
        # -------- Proximity Bar --------
        # PAJ7620 proximity usually 0–255
        bar_max_width = 120       # pixels
        bar_height = 8
        bar_x = 4
        bar_y = 40

        # Scale proximity to bar width
        bar_width = int((proximity / 255) * bar_max_width)
        bar_width = max(0, min(bar_width, bar_max_width))

        # Draw bar outline
        oled.rect(bar_x, bar_y, bar_max_width, bar_height, 1)

        # Fill bar
        if bar_width > 0:
            oled.fill_rect(bar_x, bar_y, bar_width, bar_height, 1)
        # --------------------------------
        
        oled.text('(4)', 0, 0, 1)
        
        oled.text('BACK (A)', 0, 57, 1)
        oled.text('(B) NEXT', 80, 57, 1)
        oled.show()

def deinit_module():
    pass
if __name__ == "__main__":
    pass
    try:
        init_oled()
        init_module(i2c)
        while True:
            #Run the module with interval 0.5s
            run_module(0.5, oled)
    finally:
        deinit_module()
        deinit_oled()
