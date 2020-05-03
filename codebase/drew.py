import serial 
import time
import Adafruit_MCP9808.MCP9808 as MCP9808
import smbus2
import board
import busio
import adafruit_bme280
import datetime
import adafruit_sgp30

# system variables
upTime = 0
storeTimer = 0
pollInterval = 10
storeInterval = 1200
storeFile = '/home/pi/codebase/store.txt'

# SenseAir S8 | co2
ser = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=.5)
ser.flushInput()

# BME280 | humidity, pressure, altitiude
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# MCP9808 | high accuracy temperature
mcp = MCP9808.MCP9808()
mcp.begin()

# SGP30 | voc, co2
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)         
sgp30.iaq_init()

# SGP30 set saved calibration
store = open(storeFile, 'r')
cBase = int(store.readline())
vBase = int(store.readline())
store.close()
sgp30.set_iaq_baseline(cBase, vBase)


def getCO2():
    ser.flushInput()
    ser.write(b'\xFE\x44\x00\x08\x02\x9F\x25')
    resp = ser.read(7)
    high = resp[3]
    low = resp[4]
    C = (resp[3] * 256) + resp[4]
    return C 

def mbar_to_iMerc(mbar):
    return round((P * 100) / 3386.39, 2)

def c_to_f(c):
    return round(c * 9.0 / 5.0 + 32.0, 1)

def sec_to_time(sec):
    return str(datetime.timedelta(seconds=sec))

def set_baseline(sec):
    if sec >= storeInterval:
        storeTimer = 0
        co2eq_base, tvoc_base = sgp30.baseline_eCO2, sgp30.baseline_TVOC
        temp = open(storeFile, 'w')
        temp.write(str(co2eq_base))
        temp.write('\n')
        temp.write(str(tvoc_base))
        temp.close()
        print("new baseline")


while True:
    hum = int(bme280.humidity)
    pres = int(bme280.pressure) # unit: mbar
    #alt = int(bme280.altitude)
 
    voc = sgp30.TVOC
    #C2 = sgp30.eCO2

    co2 = getCO2()
    temp = mcp.readTempC()

    print('C={0}, T={1}, V={2}, H={3}, P={4}, {5}'.format(co2, c_to_f(temp), voc, hum, pres, sec_to_time(upTime)))

    set_baseline(storeTimer)
    storeTimer += pollInterval
    upTime += pollInterval
    time.sleep(pollInterval)

    
