import dataclasses
import datetime
import tomllib
from enum import Enum
from typing import Dict, List, Iterable, Any


class EventType(Enum):
    GENERAL = None
    BIRTHDAY = "birthday"


@dataclasses.dataclass
class Event:
    name: str
    date: datetime
    type: EventType


class Events:
    def __init__(self, events_data: Dict[str, Any]):
        self.events_data = events_data

    @property
    def all(self) -> Iterable[Event]:
        for name, prefs in self.events_data.items():
            yield Event(name, prefs["date"], EventType(prefs.get("type")))


class PhaseType(Enum):
    GENERAL = None
    JOB = "job"


@dataclasses.dataclass
class Phase:
    name: str
    from_date: datetime
    to_date: datetime
    layer: PhaseType


class Phases:
    def __init__(self, phases_data: Dict[str, Any]):
        self.phases_data = phases_data

    @property
    def all(self) -> Iterable[Phase]:
        for name, prefs in self.phases_data.items():
            yield Phase(name, prefs["from_date"], prefs["to_date"], PhaseType(prefs.get("layer")))


class Config:
    def __init__(self, filename: str):
        with open(filename, 'rb') as f:
            self.data = tomllib.load(f)

    @property
    def events(self) -> Events: return Events(self.data['events'])

    @property
    def phases(self) -> Phases: return Phases(self.data['phases'])


if __name__ == "__main__":
    config = Config("config.toml")

    for event in config.events.all:
        print(event)

    for phase in config.phases.all:
        print(phase)
