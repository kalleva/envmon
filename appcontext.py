from dataclasses import dataclass
import smbus2 as smbus


@dataclass
class SHT4XMeasurement:
    temp: float
    rh: float
    ts: int


@dataclass
class SHT4XContext:
    i2c_bus: smbus.SMBus
    msr: SHT4XMeasurement


@dataclass
class TgBotConfig:
    chat_id: str
    token: str


@dataclass
class AppContext:
    sht4x_ctx: SHT4XContext
    tg_bot_cfg: TgBotConfig
