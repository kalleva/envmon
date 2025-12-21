import logging
import logging.handlers
import os

def setup():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    logging.basicConfig(level=logging.DEBUG, format=formatter._fmt)
    rotating_handler = logging.handlers.RotatingFileHandler(
        filename="logs/app.log", mode="a",
        maxBytes= 5 * 1024 * 1024
    )

    rotating_handler.setFormatter(formatter)

    logger = logging.getLogger("envmon")
    logger.addHandler(rotating_handler)