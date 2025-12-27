import logging
from smbus2 import SMBus
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
    with SMBus(1) as bus:
        try:
            bus.write_byte(SHT4X_I2C_ADDRESS, SHT4X_MEASURE_HIGH_PRECISION)
            time.sleep(0.02)
            rx_bytes = bus.read_block_data(SHT4X_I2C_ADDRESS, 6)
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
        
