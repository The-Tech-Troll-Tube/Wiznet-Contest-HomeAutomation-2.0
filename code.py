# Albin's Code Mode

import board
import busio
 import digitalio
from digitalio import DigitalInOut
from digitalio import Direction
import time
from random import randint


from adafruit_io.adafruit_io import IO_MQTT
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from secrets import secrets

from time import sleep


# /////////////Display Import\\\\\\\\

import displayio
import terminalio
import adafruit_displayio_ssd1306
from adafruit_display_text import label

# ///////////////////////////////////////


displayio.release_displays()

# ///////////////LIVE SERIAL DISPLAY///////////////
i2c = busio.I2C (scl=board.GP1, sda=board.GP0) # This RPi Pico way to call I2C
display_bus = displayio.I2CDisplay (i2c, device_address = 0x3C) # The address of my Board
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=55)
# ///////////////LIVE SERIAL DISPLAY///////////////






print("  ""HOME AUTOMATION" "\n"   "  WIZNET CONTEST" "\n" "      " "2022")
sleep(4)
print("\n" "   Created by" "\n"  "                    " "Albin Joseph")
sleep(4)


#///////////////////////////////////////////////////////////////////////////

# ESP32 AT
from adafruit_espatcontrol import (
    adafruit_espatcontrol,
    adafruit_espatcontrol_wifimanager,
)

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# Debug Level
# Change the Debug Flag if you have issues with AT commands
debugflag = False


RX = board.GP5
TX = board.GP4
resetpin = DigitalInOut(board.GP20)
rtspin = False
uart = busio.UART(TX, RX, baudrate=11520, receiver_buffer_size=2048)
status_light = None


print("ESP AT commands")
esp = adafruit_espatcontrol.ESP_ATcontrol(
    uart, 115200, reset_pin=resetpin, rts_pin=rtspin, debug=debugflag
)
esp.hard_reset()
wifi = adafruit_espatcontrol_wifimanager.ESPAT_WiFiManager(esp, secrets, status_light,attempts=5)


counter = 0
result = None #variable for cleaning data
#set the topics

#Connect to adafruitio (please remember to set the above settings before connect to adafruit io)
wifi.IO_Con("MQTT")
while True:
    #Collect information from subscribe channel (test)
    data = wifi.MQTT_sub()
    print (data)
    # find the data and the topic name from WizFi360 to further use.
    sub,result = wifi.clean_data(data,"test",result)
    print (sub, result)
    #publish to related channel (test)
    wifi.MQTT_pub(str(counter))

    counter += 1
    time.sleep(0.5)
    if counter > 5:
        wifi.MQTT_disconnect() #disconnect with adafruit io
        counter = 0
        time.sleep(15)
        wifi.IO_Con("MQTT") #reconnect with adafruit io

#//////////////////////////////////////////////////////////////////////////


    ### Code ###
    # Define callback methods which are called when events occur
    # pylint: disable=unused-argument, redefined-outer-name
    def connected(clinet):
        # This function will be called when the mqtt_client is connected
        # successfully to the broker.
        print("Connected to Adafruit IO!")

        # Subscribe to Group
        io.subscribe(group_key=group_name)

    def disconnected(clinet):
        # This method is called when the mqtt_client disconnects
        # from the broker.
        print("Disconnected from Adafruit IO!")

    def subscribe(client, userdata, topic, granted_qos):
        # This method is called when the client subscribes to a new feed.
        print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))

    def message(client, topic, message):
        # Method called when a client's subscribed feed has a new value.
        print(" {0}: {1}".format(topic, message))

    # Board LED CONTROL ////////////////////////////////////////////////////////////////////////////////////
    BoardLed = digitalio.DigitalInOut(board.GP25)
    BoardLed.direction = digitalio.Direction.OUTPUT

    def on_BoardLed_msg(client, topic, message):
        # Method called when a client's subscribed feed has a new value.
        print(" {0}: {1}".format(topic, message))
        if message == "on":
            BoardLed.value = True
        elif message == "off":
            BoardLed.value = False
        else:
            print("Unexpected message on BoardLed feed")

    # External LED CONTROL ////////////////////////////////////////////////////////////////////////////////////
    ExternalLed = digitalio.DigitalInOut(board.GP2)
    ExternalLed.direction = digitalio.Direction.OUTPUT

    def on_ExternalLed_msg(client, topic, message):
        # Method called when a client's subscribed feed has a new value.
        print(" {0}: {1}".format(topic, message))
        if message == "on":
            ExternalLed.value = True
        elif message == "off":
            ExternalLed.value = False
        else:
            print("Unexpected message on ExternalLed feed")

    # KITCHEN FAN CONTROL ////////////////////////////////////////////////////////////////////////////////////
    KitchenFan = digitalio.DigitalInOut(board.GP7)
    KitchenFan.direction = digitalio.Direction.OUTPUT

    def on_KitchenFan_msg(client, topic, message):
        # Method called when a client's subscribed feed has a new value.
        print(" {0}: {1}".format(topic, message))
        if message == "on":
            KitchenFan.value = True
        elif message == "off":
            KitchenFan.value = False
        else:
            print("Unexpected message on KitchenFan feed")

    # BEDROOM FAN CONTROL ////////////////////////////////////////////////////////////////////////////////////
    BedroomFan = digitalio.DigitalInOut(board.GP6)
    BedroomFan.direction = digitalio.Direction.OUTPUT

    def on_BedroomFan_msg(client, topic, message):
        # Method called when a client's subscribed feed has a new value.
        print(" {0}: {1}".format(topic, message))
        if message == "on":
            BedroomFan.value = True
        elif message == "off":
            BedroomFan.value = False
        else:
            print("Unexpected message on BedroomFan feed")

    # HALL FAN CONTROL GPIO PIN CONTROL ////////////////////////////////////////////////////////////////////////////////////

    # HallFan = digitalio.DigitalInOut(board.GP22)
    # HallFan.direction = digitalio.Direction.OUTPUT

    # def on_HallFan_msg(client, topic, message):
    #    Method called when a client's subscribed feed has a new value.
    #     print(" {0}: {1}".format(topic, message))
    #     if message == "on":
    #         HallFan.value = True
    #     elif message == "off":
    #         HallFan.value = False
    #     else:
    #         print("Unexpected message on HallFan feed")


    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


    # Relay CONTROL System (Low/False is ON )////////////////////////////////////////////////////////////////////////////////////

    # //////// RelayTest \\\\\\\

    RelayTest = digitalio.DigitalInOut(board.GP9)
    RelayTest.direction = digitalio.Direction.OUTPUT
    RelayTest.value = True

    def on_RelayTest_msg(client, topic, message):
        # Method called when a client's subscribed feed has a new value.
        print(" {0}: {1}".format(topic, message))
        if message == "on":
            RelayTest.value = False
        elif message == "off":
            RelayTest.value = True
        else:
            print("Unexpected message on RelayTest feed")

    # //////// HALL FAN CONTROL (RELAY) \\\\\\\\

    HallFan = digitalio.DigitalInOut(board.GP15)
    HallFan.direction = digitalio.Direction.OUTPUT
    HallFan.value = True

    def on_HallFan_msg(client, topic, message):
    ##  Method called when a client's subscribed feed has a new value.
        print(" {0}: {1}".format(topic, message))
        if message == "on":
            HallFan.value = False
        elif message == "off":
            HallFan.value = True
        else:
            print("Unexpected message on HallFan feed")

    # HallFanRelay = digitalio.DigitalInOut(board.GP15)
    # HallFanRelay.direction = digitalio.Direction.OUTPUT
    # HallFanRelay.value = True

    # def on_HallFanRelay_msg(client, topic, message):
    ##  Method called when a client's subscribed feed has a new value.
    #     print(" {0}: {1}".format(topic, message))
    #     if message == "on":
    #         HallFanRelay.value = False
    #     elif message == "off":
    #         HallFanRelay.value = True
    #     else:
    #         print("Unexpected message on HallFanRelay feed")

    # //////// HALL LIGHT \\\\\\\

    HallLight = digitalio.DigitalInOut(board.GP14)
    HallLight.direction = digitalio.Direction.OUTPUT
    HallLight.value = True

    def on_HallLight_msg(client, topic, message):
        # Method called when a client's subscribed feed has a new value.
        print(" {0}: {1}".format(topic, message))
        if message == "on":
            HallLight.value = False
        elif message == "off":
            HallLight.value = True
        else:
            print("Unexpected message on HallLight feed")

    # //////// BEDROOM LIGHT \\\\\\\

    BedroomLight = digitalio.DigitalInOut(board.GP13)
    BedroomLight.direction = digitalio.Direction.OUTPUT
    BedroomLight.value = True

    def on_BedroomLight_msg(client, topic, message):
        # Method called when a client's subscribed feed has a new value.
        print(" {0}: {1}".format(topic, message))
        if message == "on":
            BedroomLight.value = False
        elif message == "off":
            BedroomLight.value = True
        else:
            print("Unexpected message on BedroomLight feed")

    # //////// KITCHEN LIGHT \\\\\\\

    KitchenLight = digitalio.DigitalInOut(board.GP12)
    KitchenLight.direction = digitalio.Direction.OUTPUT
    KitchenLight.value = True

    def on_KitchenLight_msg(client, topic, message):
        # Method called when a client's subscribed feed has a new value.
        print(" {0}: {1}".format(topic, message))
        if message == "on":
            KitchenLight.value = False
        elif message == "off":
            KitchenLight.value = True
        else:
            print("Unexpected message on KitchenLight feed")

    # *************GATE AUTOMATION*************
    # //////// GateButton \\\\\\\

    GateButton = digitalio.DigitalInOut(board.GP8)
    GateButton.direction = digitalio.Direction.OUTPUT
    GateButton.value = True

    def on_GateButton_msg(client, topic, message):
        # Method called when a client's subscribed feed has a new value.
        print(" {0}: {1}".format(topic, message))
        if message == "on":
            GateButton.value = False
            sleep(1)
            GateButton.value = True
            print("Gate triggered!!")
            message == "off"
        else:
            print("GATE Triggered" "\n" "with Adafruit IO" "\n" "    " "!!")


    # ////////////////////////////////////////////////////////////////////////////////////

    # Initialize MQTT interface with the ethernet interface
    MQTT.set_socket(socket, eth)

    # Initialize a new MQTT Client object
    mqtt_client = MQTT.MQTT(
        broker="io.adafruit.com",
        username=secrets["aio_username"],
        password=secrets["aio_key"],
        is_ssl=False,
    )

    # Initialize an Adafruit IO MQTT Client
    io = IO_MQTT(mqtt_client)

    # Setup the callback methods above
    io.on_connect = connected
    io.on_disconnect = disconnected
    io.on_message = message
    io.on_subscribe = subscribe

    # Set up a callback for the BoardLed feed //////////////////////////////////////////
    io.add_feed_callback("BoardLed", on_BoardLed_msg)

    # Set up a callback for the ExternalLed feed //////////////////////////////////////////
    io.add_feed_callback("ExternalLed", on_ExternalLed_msg)

    # Set up a callback for the KitchenFan feed //////////////////////////////////////////
    io.add_feed_callback("KitchenFan", on_KitchenFan_msg)

    # Set up a callback for the BedroomFan feed //////////////////////////////////////////
    io.add_feed_callback("BedroomFan", on_BedroomFan_msg)

    # Set up a callback for the HallFan feed //////////////////////////////////////////
    io.add_feed_callback("HallFan", on_HallFan_msg)

    # ////////////////////////////////////////////////////////////////////////////////////

    # Set up a callback for the RelayTest feed //////////////////////////////////////////
    io.add_feed_callback("RelayTest", on_RelayTest_msg)

    ## Set up a callback for the HallFanRelay feed //////////////////////////////////////////
    # io.add_feed_callback("HallFanRelay", on_HallFanRelay_msg)

    # Set up a callback for the HallLight feed //////////////////////////////////////////
    io.add_feed_callback("HallLight", on_HallLight_msg)

    # Set up a callback for the BedroomLight feed //////////////////////////////////////////
    io.add_feed_callback("BedroomLight", on_BedroomLight_msg)

    # Set up a callback for the KitchenLight feed //////////////////////////////////////////
    io.add_feed_callback("KitchenLight", on_KitchenLight_msg)

    # Set up a callback for the GateButton feed //////////////////////////////////////////
    io.add_feed_callback("GateButton", on_GateButton_msg)


    ## Group name
    group_name = "weatherstation" # Comenting Throws error need to check

    ## Feeds within the group
    temp_feed = "weatherstation.temperature" # omenting Throws error need to check
    humid_feed = "weatherstation.humidity"  # Comenting Throws error need to check

    # Connect to Adafruit IO
    print("Connecting to Adafruit IO...")
    io.connect()

    # ////////////////////////////ADD ON SUBSCRIPTION////////////////////////////////////////////////////////


    # # Subscribe to all messages on the BoardLed feed
    io.subscribe("BoardLed")

    # # Subscribe to all messages on the ExternalLed feed
    io.subscribe("ExternalLed")

    # Subscribe to all messages on the KitchenFan feed
    io.subscribe("KitchenFan")

    # Subscribe to all messages on the BedroomFan feed
    io.subscribe("BedroomFan")

    # # Subscribe to all messages on the HallFan feed
    io.subscribe("HallFan")

    # ////////////////////////////RELAY SUBSCRIPTION////////////////////////////////////////////////////////

    # # Subscribe to all messages on the RelayTest feed
    io.subscribe("RelayTest")

    # Subscribe to all messages on the HallFanRelay feed
    # io.subscribe("HallFanRelay")

    # # Subscribe to all messages on the HallLight feed
    io.subscribe("HallLight")

    # # Subscribe to all messages on the BedroomLight feed
    io.subscribe("BedroomLight")

    # # Subscribe to all messages on the KitchenLight feed
    io.subscribe("KitchenLight")

    # # Subscribe to all messages on the GateButton feed
    io.subscribe("GateButton")


    # ////////////////////////////////////////////////////////////////////////////////////


    print("Connected to Adafruit IO")
    print("    HandShake         SUCCESS!!")
    print("WAITING FOR INPUT")



    while True:
        io.loop()
