import time
import busio
import digitalio
import board
import threading
import RPi.GPIO as GPIO
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

chan_ldr = None
chan_temp = None
btn = 23
rate = 1
start_time = 0

runtime = 'Runtime'
read = "Reading"
temp = "Temp"
lr = "LDR Reading"
lv = "LDR Voltage"

def values_thread():

    thread = threading.Timer(rate, values_thread)
    thread.daemon = True
    thread.start()

    current_time = int( time.time() - start_time )

    print("{:<15}{:<15}{:<15.2f}{:<15}{:<15.2f}".format( str(current_time) + "s",
                                                        chan_temp.value,
                                                        (chan_temp.voltage - 0.5)/0.01,
                                                        chan_ldr.value, chan_ldr.voltage))



def btn_pressed(channel):

    global rate
    if rate == 1:
        rate = 5
    elif rate == 5:
        rate = 10
    else:
        rate = 1
    
    print(f"Sampling at : {rate}s")
    print("{:<15}{:<15}{:<15}{:<15}{:<15}".format( runtime, read, temp, lr, lv))


def setup():

    global chan_ldr
    global chan_temp
    
    # create the spi bus
    spi = busio.SPI( clock = board.SCK, MISO = board.MISO, MOSI = board.MOSI )

    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)

    # create the mcp object
    mcp = MCP.MCP3008( spi, cs )

    # create an analog input channel on pin 0
    chan_ldr = AnalogIn( mcp, MCP.P0)
    chan_temp = AnalogIn( mcp, MCP.P1)

    #GPIO.setmode(GPIO.BOARD)
    GPIO.setup(btn, GPIO.IN)
    GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(btn, GPIO.FALLING, callback=btn_pressed, bouncetime=200)



if __name__ == "__main__":
    try:
        setup()
        start_time = time.time()

        print("{:<15}{:<15}{:<15}{:<15}{:<15}".format( runtime, read, temp, lr, lv))

        values_thread()
        while True:
            pass
    except KeyboardInterrupt:
        print("\nExiting Gracefully..")
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()