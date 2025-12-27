import logging
import smbus2 as smbus
import time
from collections import namedtuple

SHT4X_Result = namedtuple("SHT4X_Result", ["temperature", "humidity"])


SHT4X_I2C_ADDRESS = 0x44
SHT4X_MEASURE_HIGH_PRECISION = 0xFD
SHT4X_MEASUREMENT_RESPONSE_LENGTH = 6

logger = logging.getLogger("envmon.hardware.sht4x")


def get_temperature_and_humidity():
    """
    Returns result of the reques of the temperature and humidity from SHT4X sensor over I2C.
    Returns SHT4X_Result on Success or None on Error.
    """
    with smbus.SMBus(1) as bus:
        try:
            write_msg = smbus.i2c_msg.write(SHT4X_I2C_ADDRESS, [SHT4X_MEASURE_HIGH_PRECISION])
            bus.i2c_rdwr(write_msg)
            time.sleep(0.02)
               # 3. Read 6 bytes: T_MSB, T_LSB, T_CRC, RH_MSB, RH_LSB, RH_CRC
            read_msg = smbus.i2c_msg.read(SHT4X_I2C_ADDRESS, 6)
            bus.i2c_rdwr(read_msg)
            rx_bytes = bytes(read_msg)
            if not rx_bytes:
                raise Exception("No data from the sensor")
            if not len(rx_bytes) == SHT4X_MEASUREMENT_RESPONSE_LENGTH:
                raise Exception("Invalid length of the data from sensor")
            temperature_ticks = rx_bytes[0] * 256 + rx_bytes[1]
            temperature_checksum = rx_bytes[2]
            humidity_ticks = rx_bytes[3] * 256 + rx_bytes[4]
            humidity_checksum = rx_bytes[5]
            temperature_degC = -45 + 175 * temperature_ticks / 65535
            humidity_prH = -6 + 125 * humidity_ticks / 65535
            return SHT4X_Result(temperature=temperature_degC, humidity=humidity_prH)
        except Exception as e:
            logger.error(e)
            return None
        
