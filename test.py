import network
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep

MQTT_SERVER = "192.168.43.241"
CLIENT_ID = "esp_1"
MQTT_TOPIC = b"TEST"
WIFI_SSID = "one"
WIFI_PASSWORD = "98765321"

led = Pin(2, Pin.Out)

#Wifi Connection function
def connectWIFI():
    wlan = network.WLAN
