import logging
import applog
import hardware.sht4x as sht4x
import time

applog.setup()
logger = logging.getLogger("envmon.main")


def main():
    logger.info("App started")
    while True:
        result = sht4x.get_temperature_and_humidity()
        logger.info(f"temp: {result.temperature:0.2f}, humid: {result.humidity:0.2f}")
        time.sleep(60)



if __name__ == "__main__":
    main()
