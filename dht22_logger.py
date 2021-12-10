#!/usr/bin/env python3

__version__ = "0.3.0"

import Adafruit_DHT
import time
import requests
import json

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 10

THINGSPEAK_KEY = "Your ThingSpeak API key"
IOTP_KEY = "Your IoTPlotter API key"
IOTP_FEED_ID = "Your IoTPlotter feed ID"

def thingspeak_write_data(temperature, humidity):
    api_url = "https://api.thingspeak.com/update.json"
    data = {"api_key": THINGSPEAK_KEY,
            "field1": round(temperature, 1),
            "field2": round(humidity, 1)}
    response = requests.post(api_url, json=data)
    if response.ok:
        print("Posted to ThingSpeak")
    else:
        print("Error posting data to ThingSpeak: \n" + response.json())

def IoTPlotter_write_data(temperature, humidity):
    api_url = "http://iotplotter.com/api/v2/feed/" + IOTP_FEED_ID

    headers = {"api-key": IOTP_KEY}
    payload = {}
    payload["data"] = {}
    payload["data"]["Temperature"] = [{"value": round(temperature, 1)}]  # ["Temperature"] has to match the graph name in the feed
    payload["data"]["Humidity"] = [{"value": round(humidity, 1)}]

    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    if response.ok:
        print("Posted to IoTPlotter")
    else:
        print("Error posting data to IoTPlotter! code: %d\n" % response.status_code)

if __name__ == "__main__":
    print("DHT22 logger v" + __version__)
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity != None and temperature != None:
            t = time.strftime("%D %T", time.localtime(time.time()))
            print("[%s] Temp = %0.1f oC Humidity = %0.1f" % (t, temperature, humidity))
            #thingspeak_write_data(temperature, humidity)    # TODO: do it in parallel
            IoTPlotter_write_data(temperature, humidity)
        else:
            print("Failed to read DHT22 data")

        # TODO: Make it wait until the next minute
        time.sleep(60)
