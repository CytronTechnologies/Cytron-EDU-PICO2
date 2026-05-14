import board, time, neopixel, busio, array, math, audiobusio, adafruit_ssd1306
from analogio import AnalogIn

i2c = busio.I2C(board.GP5, board.GP4)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
potentiometer = AnalogIn(board.GP28)

pixels = neopixel.NeoPixel(board.GP14, 5, brightness=0.2)
pixels.fill(0)

mic = audiobusio.PDMIn(board.GP3, board.GP2, sample_rate=32000, bit_depth=16) # see note on sampling rate value below
samples = array.array('H', [0] * 1024)

sound_min = 30
sound_max = 80

def log10(x):
    return math.log(x) / math.log(10)

def normalized_rms(values):
    minbuf = sum(values) / len(values)
    samples_sum = sum(float(sample - minbuf) * (sample - minbuf)for sample in values)
    return math.sqrt(samples_sum / len(values))

while True:
    oled.fill(0)
    mic.record(samples, len(samples))
    magnitude = normalized_rms(samples)
    
    if magnitude > 0:
        pot_value = potentiometer.value / 65535 * (sound_max - sound_min) + sound_min
        oled.text(f"Threshold: {pot_value:.1f} dB", 10, 35, 1)
        
        sound_level_dB = 20 * log10(magnitude)
        oled.text("Sound Level (dB):", 15, 5, 1)
        oled.text(f"{sound_level_dB:.2f} dB", 40, 20, 1)
        
        if sound_level_dB > pot_value:
            pixels.fill((255, 0, 0))
            oled.text("SOUND LEVEL HIGH!", 15, 50, 1)
        else:
            pixels.fill((0, 255, 0))
            oled.text("SOUND LEVEL LOW!", 20, 50, 1)
        
    oled.show()
    time.sleep(0.1)
    
# =========================================================
# NOTE
# =========================================================
# The sampling rate of the PDM microphone can be adjusted
# depending on the application requirements.
#
# PDM Clock Frequency:
#     Clock Frequency = Sampling Rate × 64
#
# Supported Clock Frequency Range:
# (min)   1.20 MHz  -> 18.75 kHz sampling rate
# (typ)   2.40 MHz  -> 37.50 kHz sampling rate 
# (max)   3.25 MHz  -> 50.78 kHz sampling rate
# =========================================================
    
