# https://pypi.org/project/RPi.bme280/
import sys
import io
import time
from datetime import datetime, timezone
import mariadb
import smbus2
import bme280
from gpiozero import CPUTemperature, DigitalOutputDevice
import adafruit_dht
import board
from dotenv import dotenv_values

config = dotenv_values(".env")

# Instantiate Connection
try:
  conn = mariadb.connect(
    user=config['USER'],
    password=config['PASSWORD'],
    host="localhost",
    port=3306,
    database=config['DATABASE'])
except mariadb.Error as e:
  print(f"Error connecting to MariaDB Platform: {e}")
  sys.exit(1)

cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS data (timestamp DATETIME, temp DOUBLE, humidity DOUBLE, pressure DOUBLE, CPUtemp DOUBLE, enclosureTemp DOUBLE, enclosureHumidity DOUBLE)')

now = datetime.now(timezone.utc)

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
    # print("Could not read bme280 through i2c. Trying soon again...")
    time.sleep(.2)
  else:
    break

bme280_pwr.off()
# the sample method will take a single reading and return a
# compensated_reading object
# the compensated_reading class has the following attributes
if (data is None):
  class data: pass
  data.timestamp = now
  data.temperature = None
  data.pressure = None
  data.humidity = None

cpu_temp = CPUTemperature().temperature

dht = adafruit_dht.DHT22(board.D4)
dht_t = None
dht_h = None
for i in range(10):
  try:
    dht_t = dht.temperature
    dht_h = dht.humidity
  except RuntimeError:
    time.sleep(1)
    continue
  else:
    if dht_t is not None:
      break
    else:
      time.sleep(1)

cur.execute("INSERT INTO environmentMetrics.data(timestamp, temp, humidity, pressure, CPUtemp, enclosureTemp, enclosureHumidity) VALUES (?, ?, ?, ?, ?, ?, ?)",
(now, data.temperature, data.humidity, data.pressure, cpu_temp, dht_t, dht_h))
conn.commit()
conn.close()
print(f"Time {now}, sensor values added to database.")
print((now, data.temperature, data.humidity, data.pressure, cpu_temp, dht_t, dht_h))
