# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Note, you must create a feed called "test" in your AdafruitIO account.
# Your secrets file must contain your aio_username and aio_key

# import ssl
import time
import board
import busio
import digitalio
from digitalio import DigitalInOut
from digitalio import Direction

import adafruit_minimqtt.adafruit_minimqtt as MQTT
import adafruit_espatcontrol.adafruit_espatcontrol_socket as socket

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
wifi = adafruit_espatcontrol_wifimanager.ESPAT_WiFiManager(esp, secrets, status_light, attempts=5)

#//////////////

global externalled

#/////////////

counter = 0
result = None #variable for cleaning data
#set the topics
wifi.topic_set(
"externalled","feeds",
"boardled")
#select which topic that you wanted to publish
# wifi.IO_topics("externalled")

#Connect to adafruitio (please remember to set the above settings before connect to adafruit io)
# wifi.IO_Con("MQTT")
while True:

    
    ### Topic Setup ###

    # MQTT Topic
    # Use this topic if you'd like to connect to a standard MQTT broker
#     mqtt_topic = "/feeds/boardled"

    # Adafruit IO-style Topic
    # Use this topic if you'd like to connect to io.adafruit.com
    mqtt_topic = secrets["aio_username"] + "/feeds/boardled"

    ### Code ###
    # Define callback methods which are called when events occur
    # pylint: disable=unused-argument, redefined-outer-name
    def connect(mqtt_client, userdata, flags, rc):
        # This function will be called when the mqtt_client is connected
        # successfully to the broker.
        print("Connected to MQTT Broker!")
        print("Flags: {0}\n RC: {1}".format(flags, rc))


    def disconnect(mqtt_client, userdata, rc):
        # This method is called when the mqtt_client disconnects
        # from the broker.
        print("Disconnected from MQTT Broker!")


    def subscribe(mqtt_client, userdata, topic, granted_qos):
        # This method is called when the mqtt_client subscribes to a new feed.
        print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))


    def unsubscribe(mqtt_client, userdata, topic, pid):
        # This method is called when the mqtt_client unsubscribes from a feed.
        print("Unsubscribed from {0} with PID {1}".format(topic, pid))


    def publish(mqtt_client, userdata, topic, pid):
        # This method is called when the mqtt_client publishes data to a feed.
        print("Published to {0} with PID {1}".format(topic, pid))


    def message(client, topic, message):
        # Method callled when a client's subscribed feed has a new value.
        print("New message on topic {0}: {1}".format(topic, message))

    # Initialize MQTT interface with the esp interface
    MQTT.set_socket(socket, esp)

    # Set up a MiniMQTT Client
    mqtt_client = MQTT.MQTT(
        broker=secrets["broker"],
        username=secrets["aio_username"],
        password=secrets["aio_key"],
        # socket_pool=socket,
#         ssl_context=ssl.create_default_context(),
    )

    # Connect callback handlers to mqtt_client
    mqtt_client.on_connect = connect
    mqtt_client.on_disconnect = disconnect
    mqtt_client.on_subscribe = subscribe
    mqtt_client.on_unsubscribe = unsubscribe
    mqtt_client.on_publish = publish
    mqtt_client.on_message = message

    print("Attempting to connect to %s" % mqtt_client.broker)
    mqtt_client.connect()

    print("Subscribing to %s" % mqtt_topic)
    mqtt_client.subscribe(mqtt_topic)
    
    print("Log:Turn LED NOW!")
    time.sleep(5)

    print("Publishing to %s" % mqtt_topic)
    mqtt_client.publish(mqtt_topic, "Hello Broker!")

    print("Unsubscribing from %s" % mqtt_topic)
    mqtt_client.unsubscribe(mqtt_topic)

    print("Disconnecting from %s" % mqtt_client.broker)
    mqtt_client.disconnect()

#     time.sleep(0.5)
#         if counter > 5:
#             wifi.MQTT_disconnect() #disconnect with adafruit io
#             counter = 0
#             time.sleep(15)
#             wifi.IO_Con("MQTT") #reconnect with adafruit io
