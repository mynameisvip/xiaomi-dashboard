import time
import os
from micloud import MiCloud
from miio import AirPurifierMiot
from prometheus_client import start_http_server, Gauge

MI_USERNAME = os.environ.get('MI_USERNAME')
MI_PASSWORD = os.environ.get('MI_PASSWORD')
MI_DEVICE_NAME = "Xiaomi Smart Air Purifier 4 Lite"
MI_REFRESH_RATE = 5
PROMETHEUS_SERVICE_PORT = 8000


def get_device():
	try:
		mc = MiCloud(MI_USERNAME, MI_PASSWORD)
		mc.login()
		device_list = mc.get_devices()
		for device in device_list:
			if device["name"] == MI_DEVICE_NAME:
				print(f'Device found. IP: {device["localip"]}')
				return device["localip"], device["token"]
	except Exception as e:
		print(f"Error: Cannot find device. ({e})")
		exit(1)


def get_data(ip, token):
	airpurifier = AirPurifierMiot(ip, token)
	print(f"AQI: {airpurifier.status().aqi} Temperature: {airpurifier.status().temperature}", end='\r')
	return airpurifier.status().aqi, airpurifier.status().temperature


def push_metrics(ip, token):
	aqi_gauge = Gauge('aqi', 'Air Quality Index')
	temperature_gauge = Gauge('temperature', 'Temperature')
	while True:
		try:
			aqi, temperature = get_data(ip, token)
		except Exception as e:
			print(f"Error: Cannot connect to device... retry in 5 seconds. ({e})")
			time.sleep(5)
			continue
		aqi_gauge.set(aqi)
		temperature_gauge.set(temperature)
		time.sleep(MI_REFRESH_RATE)


if __name__ == '__main__':
		print("Searching device...")
		ip, token = get_device()
		print("Starting Prometheus client...")
		try:
			start_http_server(PROMETHEUS_SERVICE_PORT)
		except Exception as e:
			print(f"Cannot start Prometheus client. ({e})")
		print("Sending data...")
		push_metrics(ip, token)
