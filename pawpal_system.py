from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    is_completed: bool = False

    def __post_init__(self):
        """Validate task priority and duration on creation."""
        if self.priority not in ["low", "medium", "high"]:
            raise ValueError(f"Priority must be low, medium, or high. Got: {self.priority}")
        if self.duration_minutes <= 0:
            raise ValueError(f"Duration must be positive. Got: {self.duration_minutes}")

    def get_priority_value(self) -> int:
        """Return numeric value of task priority for sorting."""
        priority_map = {"low": 1, "medium": 2, "high": 3}
        return priority_map[self.priority]

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.is_completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def __post_init__(self):
        """Validate pet name and species on creation."""
        if not self.name or not self.name.strip():
            raise ValueError("Pet name cannot be empty.")
        if not self.species or not self.species.strip():
            raise ValueError("Pet species cannot be empty.")

    def get_info(self) -> str:
        """Return a formatted string with pet name, species, and task count."""
        return f"{self.name} ({self.species}) - {len(self.tasks)} tasks"

    def add_task(self, task: Task) -> None:
        """Add a task to the pet, preventing duplicates."""
        if task in self.tasks:
            raise ValueError(f"Task '{task.title}' is already added to {self.name}.")
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from the pet if it exists."""
        if task in self.tasks:
            self.tasks.remove(task)


@dataclass
class Owner:
    name: str
    available_minutes_per_day: int
    pets: List[Pet] = field(default_factory=list)

    def __post_init__(self):
        """Validate owner name and available time on creation."""
        if not self.name or not self.name.strip():
            raise ValueError("Owner name cannot be empty.")
        if self.available_minutes_per_day <= 0:
            raise ValueError(f"Available time must be positive. Got: {self.available_minutes_per_day}")

    def get_available_time(self) -> int:
        """Return the owner's available minutes per day."""
        return self.available_minutes_per_day

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's collection."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner's collection if it exists."""
        if pet in self.pets:
            self.pets.remove(pet)


@dataclass
class Scheduler:
    scheduled_tasks: List[Task] = field(default_factory=list)
    total_duration_minutes: int = 0
    explanation: str = ""

    @classmethod
    def generate(cls, owner: Owner, pet: Pet) -> "Scheduler":
        """Generate an optimized schedule by sorting tasks by priority and filtering by time constraints."""
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
        """Sort tasks by priority in descending order (high to low)."""
        return sorted(tasks, key=lambda task: task.get_priority_value(), reverse=True)

    @staticmethod
    def _filter_by_time(tasks: List[Task], owner: Owner) -> List[Task]:
        """Filter tasks to fit within owner's available time using a greedy algorithm."""
        available_time = owner.get_available_time()
        total_time = 0
        filtered_tasks = []

        for task in tasks:
            if total_time + task.duration_minutes <= available_time:
                filtered_tasks.append(task)
                total_time += task.duration_minutes

        return filtered_tasks
