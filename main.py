import logging
import applog
import hardware.sht4x as sht4x
import time
import appcontext
import smbus2 as smbus
import threading

applog.setup()
logger = logging.getLogger("envmon.main")
sht4x_read_stop_event = threading.Event()

app_ctx = appcontext.AppContext(
    sht4x_ctx=appcontext.SHT4XContext(
        i2c_bus=smbus.SMBus(1), msr=appcontext.SHT4XMeasurement(temp=0, rh=0, ts=0)
    )
)


def sht4x_read_loop(ctx: appcontext.AppContext, stop_event: threading.Event):
    ctx.sht4x_ctx.i2c_bus.open(1)
    while not stop_event.is_set():
        sht4x.get_temp_and_rh(ctx)
        time.sleep(1)
    ctx.sht4x_ctx.i2c_bus.close()


def main():
    logger.info("App started")
    sht4x_read_thread = threading.Thread(
        target=sht4x_read_loop,
        args=(
            app_ctx,
            sht4x_read_stop_event,
        ),
        daemon=True,
    )
    sht4x_read_thread.start()
    time.sleep(1)
    try:
        while True:
            logger.info(
                f"ts: {int(app_ctx.sht4x_ctx.msr.ts // 1e6)}, temp: {app_ctx.sht4x_ctx.msr.temp:0.2f}, rh: {app_ctx.sht4x_ctx.msr.rh:0.2f}"
            )
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("Stopping the app...")
        sht4x_read_stop_event.set()
        sht4x_read_thread.join()
        logger.info("App stopped")
    except Exception as ex:
        logger.error(ex)
    finally:
        pass


if __name__ == "__main__":
    main()
