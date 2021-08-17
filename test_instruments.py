# https://pypi.org/project/RPi.bme280/
from plantpi_bme280 import BME280
import bme280
from gpiozero import CPUTemperature, DigitalOutputDevice, MCP3001
import adafruit_dht
import board
import time
from datetime import datetime, timezone
from dotenv import dotenv_values

config = dotenv_values(".env")
print(f"dotenv user: {config['USER']}")
print(f"dotenv user password: {config['PASSWORD']}")
print(f"dotenv database: {config['DATABASE']}")

now = datetime.now(timezone.utc)
print(f"Current datetime now is {now}.")
print(f"Datetime.today() is {datetime.today()}.")

data = None
bme280 = BME280()
with bme280:
    bme280.measure()
data = bme280.data
if (data is None):
    print("Could not read bme280 through i2c.")
else:
    print(f"BME280 timestamp: {data.timestamp}")
    print(f"BME280 temperature: {data.temperature}")
    print(f"BME280 pressure: {data.pressure}")
    print(f"BME280 humidity: {data.humidity}")


cpu_temp = CPUTemperature().temperature
print(f"CPU temp: {cpu_temp}")

dht = adafruit_dht.DHT22(board.D4, use_pulseio=False)
dht_t = None
dht_h = None
for i in range(10):
  try:
    print("Reading DHT22...")
    dht_t = dht.temperature
    dht_h = dht.humidity
  except RuntimeError:
    print("Could not read DHT22. Trying again...")
    time.sleep(1)
    continue
  else:
    if dht_t is not None:
      break
    else:
      time.sleep(1)

print(f"Enclosure temp: {dht_t}")
print(f"Enclosure humidity: {dht_h}")
  
