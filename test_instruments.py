# https://pypi.org/project/RPi.bme280/
import smbus2
import bme280
from gpiozero import CPUTemperature, DigitalOutputDevice
import adafruit_dht
import board
import time
from datetime import datetime, timezone
from dotenv import dotenv_values

config = dotenv_values(".env")
print(f"dotenv user: {config['USER']}")
print(f"dotenv user password: {config['PASSWORD']}")
print(f"dotenv database: {config['DATABASE']}")

# turn on the BME280 sensor only when its metrics should be read
bme280_pwr = DigitalOutputDevice(24)
bme280_pwr.on()
time.sleep(.1)

port = 1
address = 0x76
bus = smbus2.SMBus(port)
calibration_params = None
data = None
for i in range(5):
  try:
    calibration_params = bme280.load_calibration_params(bus, address)
    data = bme280.sample(bus, address, calibration_params)
  except OSError:
    print("Could not read bme280 through i2c. Trying soon again...")
    time.sleep(.2)
  else:
    break
now = datetime.now(timezone.utc)
print(f"Current datetime now is {now}.")
print(f"Datetime.today() is {datetime.today()}.")
# the sample method will take a single reading and return a
# compensated_reading object
# the compensated_reading class has the following attributes
if (data is None):
  class data: pass
  data.timestamp = now
  data.temperature = None
  data.pressure = None
  data.humidity = None
  print("Could not read bme280 through i2c.")
else:
  print("Could read bme280 through i2c!")
  print(f"BME280 timestamp: {data.timestamp}")
  print(f"BME280 temperature: {data.temperature}")
  print(f"BME280 pressure: {data.pressure}")
  print(f"BME280 humidity: {data.humidity}")
print(data.timestamp)

bme280_pwr.off()

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
  
