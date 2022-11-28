from micloud import MiCloud
from miio import AirPurifierMiot

USERNAME = "MI_USERNAME"
PASSWORD = "MI_PWD"
DEVICE_NAME = "Xiaomi Smart Air Purifier 4 Lite"

def get_device():
        mc = MiCloud(USERNAME, PASSWORD)
        mc.login()
        token = mc.get_token()
        device_list = mc.get_devices()
        for device in device_list:
                if device["name"] == DEVICE_NAME:
                        print(device["localip"])
                        print(device["token"])
                        return device["localip"], device["token"]

airpurifier = AirPurifierMiot(*get_device())
print(airpurifier.status().aqi)
print(airpurifier.status().temperature)
