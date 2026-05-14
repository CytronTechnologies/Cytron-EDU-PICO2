import board, time, array, math, audiobusio

mic = audiobusio.PDMIn(board.GP3, board.GP2, sample_rate=32000, bit_depth=16) # see note below on sampling rate
samples = array.array('H', [0] * 1024)

def log10(x):
    return math.log(x) / math.log(10)

def normalized_rms(values):
    minbuf = sum(values) / len(values)
    samples_sum = sum(float(sample - minbuf) * (sample - minbuf)for sample in values)
    return math.sqrt(samples_sum / len(values))

while True:
    mic.record(samples, len(samples))
    magnitude = normalized_rms(samples)
    if magnitude > 0:
        sound_level_dB = 20 * log10(magnitude)
        print(f"Sound Level (dB): {sound_level_dB:.2f}")
    else:
        print("Magnitude is too small to calculate dB.")
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