import tomllib
from datetime import datetime
from pathlib import Path

from attrs import define, field


def parse_datetime(dt: str) -> str:
    dtp = datetime.strptime(dt, "%Y-%m-%dT%H:%M")
    return dtp.strftime("%A, %B %d @ %I:%M%p")


def load_config(config: Path | str):
    if isinstance(config, str):
        config = Path(config)
    return tomllib.loads(config.read_text())


@define
class Appointment:
    locationId: int
    startTimestamp: str = field(converter=parse_datetime)
    endTimestamp: str = field(converter=parse_datetime)
    active: bool
    duration: int
    remoteInd: bool
