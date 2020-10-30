import busio
import digitalio
import board
import threading
import adafruit_mcp3xxx.mcp3008 as MCP
import RPi.GPIO as GPIO
import time
from adafruit_mcp3xxx.analog_in import AnalogIn


chan0 = None # ADC channel 0 input
chan1 = None # ADC channel 1 input
samplingRate = {0:10, 1:5, 2:1} # different sampling times that the program can switch between
curRate = 0 # Current sampling rate selected
startTime = None # current starting time for comparison
btn_changeRate =  23 # Button to change sampling rate (BCM)

def setup():
    global chan0
    global chan1
    global startTime

    # create the spi bus
    spi = busio.SPI( clock = board.SCK, MISO = board.MISO, MOSI = board.MOSI )

    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)

    # create the mcp object
    mcp = MCP.MCP3008( spi, cs )

    # create an analog input channel on pin 0
    chan0 = AnalogIn( mcp, MCP.P0)

    # create an analog input channel on pin 1
    chan1 = AnalogIn( mcp, MCP.P1)

    # Setup debouncing and callback btn
    GPIO.setup(btn_changeRate, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(btn_changeRate, GPIO.FALLING, callback=changeThreshold, bouncetime=200)


def changeThreshold(channel):
    global curRate

    curRate = (curRate + 1) % 3

    print(curRate)

def main():
    pass

def tick():
    global startTime

    startTime = time.time()

def tock()
    global startTime

    return time.time() - startTime
    
if __name__ == "__main__":
    try:

        setup()
        while True:
            main()

    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()