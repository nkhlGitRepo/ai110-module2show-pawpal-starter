from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str

    def get_priority_value(self):
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: list = field(default_factory=list)

    def get_info(self):
        pass


@dataclass
class Owner:
    name: str
    available_minutes_per_day: int
    pets: list = field(default_factory=list)

    def get_available_time(self):
        pass


class Scheduler:
    def generate_schedule(self, owner, pet, tasks):
        pass

    def sort_by_priority(self, tasks):
        pass

    def filter_by_time(self, tasks, available_time):
        pass
