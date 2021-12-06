#!/usr/bin/env python3

__version__ = "0.2.0"

import Adafruit_DHT
import time
import requests

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 10

THINGSPEAK_KEY = "Your ThingSpeak API key"

def thingspeak_write_data(temperature, humidity):
    api_url = "https://api.thingspeak.com/update.json"
    data = {"api_key": THINGSPEAK_KEY, "field1": temperature, "field2": humidity}
    response = requests.post(api_url, json=data)
    if response.ok:
        print("Posted to ThingSpeak")
    else:
        print("Error posting data to ThingSpeak: \n" + response.json())

if __name__ == "__main__":
    print("DHT22 logger v" + __version__)
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity != None and temperature != None:
            t = time.strftime("%D %T", time.localtime(time.time()))
            print("[%s] Temp = %0.1f oC Humidity = %0.1f" % (t, temperature, humidity))
            thingspeak_write_data(temperature, humidity)    # TODO: do it in parallel
        else:
            print("Failed to read DHT22 data")

        # TODO: Make it wait until the next minute
        time.sleep(60)
