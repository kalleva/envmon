import logging
import smbus2 as smbus
import time
import appcontext
from collections import namedtuple

SHT4X_Result = namedtuple("SHT4X_Result", ["temperature", "humidity"])

SHT4X_I2C_ADDRESS = 0x44
SHT4X_MEASUREMENT_HIGH_PRECISION = 0xFD
SHT4X_MEASUREMENT_RESPONSE_LENGTH = 6
SHT4X_MEASUREMENT_TIMEOUT = 0.02

logger = logging.getLogger("envmon.hardware.sht4x")


def _crc(data: bytes) -> int:
    """CRC-8 with polynomial 0x31, init 0xFF (Sensirion standard)."""
    crc = 0xFF
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ 0x31
            else:
                crc <<= 1
            crc &= 0xFF
    return crc


def get_temp_and_rh(ctx: appcontext.AppContext):
    bus = ctx.sht4x_ctx.i2c_bus
    try:
        msg = smbus.i2c_msg.write(SHT4X_I2C_ADDRESS, [SHT4X_MEASUREMENT_HIGH_PRECISION])
        bus.i2c_rdwr(msg)

        time.sleep(SHT4X_MEASUREMENT_TIMEOUT)

        read_msg = smbus.i2c_msg.read(
            SHT4X_I2C_ADDRESS, SHT4X_MEASUREMENT_RESPONSE_LENGTH
        )
        bus.i2c_rdwr(read_msg)
        rx_bytes = bytes(read_msg)
        if not rx_bytes or len(rx_bytes) != SHT4X_MEASUREMENT_RESPONSE_LENGTH:
            raise IOError(f"Invalid SHT4X response length {len(rx_bytes)}")

        t_ticks = rx_bytes[0] * 256 + rx_bytes[1]
        t_check = rx_bytes[2]
        rh_ticks = rx_bytes[3] * 256 + rx_bytes[4]
        rh_check = rx_bytes[5]
        temp = -45 + 175 * t_ticks / 65535
        rh = -6 + 125 * rh_ticks / 65535
        if _crc(rx_bytes[0:2]) != t_check or _crc(rx_bytes[3:5]) != rh_check:
            raise ValueError("SHT4x CRC check failed")
        ctx.sht4x_ctx.msr.ts = time.time_ns()
        ctx.sht4x_ctx.msr.rh = rh
        ctx.sht4x_ctx.msr.temp = temp
        return
    except Exception as e:
        logger.error(e)
        return
