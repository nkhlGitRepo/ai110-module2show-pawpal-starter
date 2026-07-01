from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    is_completed: bool = False

    def __post_init__(self):
        if self.priority not in ["low", "medium", "high"]:
            raise ValueError(f"Priority must be low, medium, or high. Got: {self.priority}")
        if self.duration_minutes <= 0:
            raise ValueError(f"Duration must be positive. Got: {self.duration_minutes}")

    def get_priority_value(self) -> int:
        priority_map = {"low": 1, "medium": 2, "high": 3}
        return priority_map[self.priority]

    def mark_complete(self) -> None:
        self.is_completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Pet name cannot be empty.")
        if not self.species or not self.species.strip():
            raise ValueError("Pet species cannot be empty.")

    def get_info(self) -> str:
        return f"{self.name} ({self.species}) - {len(self.tasks)} tasks"

    def add_task(self, task: Task) -> None:
        if task in self.tasks:
            raise ValueError(f"Task '{task.title}' is already added to {self.name}.")
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        if task in self.tasks:
            self.tasks.remove(task)


@dataclass
class Owner:
    name: str
    available_minutes_per_day: int
    pets: List[Pet] = field(default_factory=list)

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Owner name cannot be empty.")
        if self.available_minutes_per_day <= 0:
            raise ValueError(f"Available time must be positive. Got: {self.available_minutes_per_day}")

    def get_available_time(self) -> int:
        return self.available_minutes_per_day

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        if pet in self.pets:
            self.pets.remove(pet)


@dataclass
class Scheduler:
    scheduled_tasks: List[Task] = field(default_factory=list)
    total_duration_minutes: int = 0
    explanation: str = ""

    @classmethod
    def generate(cls, owner: Owner, pet: Pet) -> "Scheduler":
        sorted_tasks = cls._sort_by_priority(pet.tasks)
        filtered_tasks = cls._filter_by_time(sorted_tasks, owner)
        total_duration = sum(task.duration_minutes for task in filtered_tasks)

        skipped_count = len(pet.tasks) - len(filtered_tasks)
        explanation = f"Scheduled {len(filtered_tasks)}/{len(pet.tasks)} tasks. Total: {total_duration} min. "
        if skipped_count > 0:
            explanation += f"{skipped_count} task(s) skipped due to time constraints."

        return cls(
            scheduled_tasks=filtered_tasks,
            total_duration_minutes=total_duration,
            explanation=explanation,
        )

    @staticmethod
    def _sort_by_priority(tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda task: task.get_priority_value(), reverse=True)

    @staticmethod
    def _filter_by_time(tasks: List[Task], owner: Owner) -> List[Task]:
        available_time = owner.get_available_time()
        total_time = 0
        filtered_tasks = []

        for task in tasks:
            if total_time + task.duration_minutes <= available_time:
                filtered_tasks.append(task)
                total_time += task.duration_minutes

        return filtered_tasks
