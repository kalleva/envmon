import logging
import applog
import appsys

applog.setup()
logger = logging.getLogger("envmon.main")


def main():
    env = appsys.check_environment()
    if env == appsys.Deployment.DEV:
        logger.info("App started in DEV mode")
        import appdev

        appdev.run()
    else:
        logger.info("App started in PROD mode")
        import appprod

        appprod.run()


if __name__ == "__main__":
    main()
