import dataclasses
import datetime
import tomllib
from enum import Enum
from functools import cached_property
from typing import Dict, List, Iterable, Any

from colour import Color


class EventType(Enum):
    GENERAL = 'None'
    BIRTHDAY = "birthday"
    DEATH = "death"


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
            yield Event(name, prefs["date"], EventType(prefs.get("type", 'None')))

    def __getitem__(self, dates) -> List[Event]:
        start, end = dates
        assert type(start is datetime.datetime), type(start)
        assert type(end is datetime.datetime), type(end)
        return [e for e in self.all if start.date() <= e.date < end.date()]


class PhaseType(Enum):
    GENERAL = 'None'
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
            yield Phase(name, prefs["from_date"], prefs["to_date"], PhaseType(prefs.get("layer", 'None')))


class Config:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def load(filename: str) -> "Config":
        with open(filename, 'rb') as f:
            return Config(tomllib.load(f))

    @property
    def events(self) -> Events: return Events(self.data.get('events', {}))

    @property
    def phases(self) -> Phases: return Phases(self.data.get('phases', {}))

    @cached_property
    def event_colors(self) -> Dict[EventType, Color]:
        return dict(
            (EventType(event_type), Color(color_spec).rgb)
            for event_type, color_spec in self.data.get("event-colors", {}).items())

    @cached_property
    def phase_colors(self) -> Dict[PhaseType, Color]:
        return dict(
            (PhaseType(phase_type), Color(color_spec).rgb)
            for phase_type, color_spec in self.data.get("phase-colors", {}).items())


if __name__ == "__main__":
    config = Config.load("my_config.toml")

    for event in config.events.all:
        print(event)

    for phase in config.phases.all:
        print(phase)

    for event_type, color in config.event_colors.items():
        print(event_type, color)

    for phase_type, color in config.phase_colors.items():
        print(phase_type, color)
