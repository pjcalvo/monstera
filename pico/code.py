from machine import Pin, ADC
import machine
import network
import time
from api import send_humidity_values

######### constants
READ_DELAY =  60 # delay between readings every minute
WIFI_DELAY =  0.5 # delay between readings every minute

MAX_MOISTURE = 208
MIN_MOISTURE = 49300
MOISTURE_THRESHOLD = 40

SSID="Emolija"
PASSWORD="Pachamama2022"
#################

######### Set up the pins
led_pin = Pin('LED', Pin.OUT)
soil_pin = ADC(Pin(26))
wifi_led_pin = Pin(3, Pin.OUT)
moisture_on_led_pin = Pin(0, Pin.OUT)
moisture_off_led_pin = Pin(1, Pin.OUT)
##################

# run the program 
led_pin.on()

########## start wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
##################

########## start pins
wifi_led_pin.low()

# eternal loop to run the app constantly
while True:
    # try until it is connected
    if not wlan.isconnected():
        wlan.connect(SSID, PASSWORD)
        wifi_led_pin.low()
    else:
        wifi_led_pin.high() #find a way to set this only once
   
    ########
    #  still collect metrics for visual aid
    ########

    # read moisture value and convert to percentage within the calibration range
    value = soil_pin.read_u16()
    moisture = (MAX_MOISTURE - value) * 100 / (MAX_MOISTURE - MIN_MOISTURE)
    # print values
    print("Moisture: " + "%.2f" % moisture + "% (ADC: " + str(value) + ")")
    print(f"Is internet working: {wlan.isconnected()}")

    if moisture >= MOISTURE_THRESHOLD:
        moisture_on_led_pin.high()
        moisture_off_led_pin.low()
    else:
        moisture_on_led_pin.low()
        moisture_off_led_pin.high()

    if wlan.isconnected():
        send_humidity_values(MIN_MOISTURE, MAX_MOISTURE, value, moisture)
        time.sleep(READ_DELAY)
    else:
        time.sleep(WIFI_DELAY)
    