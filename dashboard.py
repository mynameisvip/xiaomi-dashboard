import time
import os
from micloud import MiCloud
from miio import AirPurifierMiot
from prometheus_client import start_http_server, Gauge

MI_USERNAME = os.environ.get('MI_USERNAME')
MI_PASSWORD = os.environ.get('MI_PASSWORD')
MI_DEVICE_NAME = "Xiaomi Smart Air Purifier 4 Lite"
MI_REFRESH_RATE = 10


def get_device():
    mc = MiCloud(MI_USERNAME, MI_PASSWORD)
    mc.login()
    token = mc.get_token()
    device_list = mc.get_devices()
    for device in device_list:
        if device["name"] == MI_DEVICE_NAME:
            print(device["localip"])
            print(device["token"])
            return device["localip"], device["token"]


def get_data():
    airpurifier = AirPurifierMiot(*get_device())
    print(airpurifier.status().aqi)
    print(airpurifier.status().temperature)
    return airpurifier.status().aqi, airpurifier.status().temperature


def push_metrics():
    aqi_gauge = Gauge('aqi', 'Air Quality Index')
    temperature_gauge = Gauge('temperature', 'Temperature')
    while True:
        aqi, temperature = get_data()
        aqi_gauge.set(aqi)
        temperature_gauge.set(temperature)
        time.sleep(MI_REFRESH_RATE)


if __name__ == '__main__':
    start_http_server(8000)
    push_metrics()
