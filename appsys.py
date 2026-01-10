from enum import Enum


class Deployment(Enum):
    DEV = (1,)
    PI = 2


def check_environment() -> Deployment:
    try:
        with open("/proc/device-tree/model", "r") as f:
            if "raspberry pi" in f.read().lower():
                return Deployment.PI
    except FileNotFoundError:
        return Deployment.DEV
