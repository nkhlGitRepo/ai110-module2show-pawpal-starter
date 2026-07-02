from dataclasses import dataclass, field
from typing import List
from datetime import datetime, timedelta


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    scheduled_time: str = None
    recurrence: str = "once"
    due_date: str = None
    is_completed: bool = False

    def __post_init__(self):
        """Validate task priority, duration, and due_date on creation."""
        if self.priority not in ["low", "medium", "high"]:
            raise ValueError(f"Priority must be low, medium, or high. Got: {self.priority}")
        if self.duration_minutes <= 0:
            raise ValueError(f"Duration must be positive. Got: {self.duration_minutes}")
        if self.recurrence not in ["once", "daily", "weekly"]:
            raise ValueError(f"Recurrence must be once, daily, or weekly. Got: {self.recurrence}")
        if self.recurrence != "once" and not self.due_date:
            raise ValueError("Recurring tasks must have a due_date (YYYY-MM-DD format).")
        if self.due_date:
            try:
                datetime.strptime(self.due_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"due_date must be in YYYY-MM-DD format. Got: {self.due_date}")

    def __eq__(self, other):
        """Compare tasks: for recurring tasks include due_date, for one-time ignore it."""
        if not isinstance(other, Task):
            return False
        base_equal = (self.title == other.title and
                      self.duration_minutes == other.duration_minutes and
                      self.priority == other.priority and
                      self.recurrence == other.recurrence)

        # For recurring tasks, due_date must also match (to distinguish occurrences)
        if self.recurrence != "once":
            return base_equal and self.due_date == other.due_date
        return base_equal

    def __hash__(self):
        """Hash based on content, including due_date for recurring tasks."""
        if self.recurrence != "once":
            return hash((self.title, self.duration_minutes, self.priority, self.recurrence, self.due_date))
        return hash((self.title, self.duration_minutes, self.priority, self.recurrence))

    def get_priority_value(self) -> int:
        """Return numeric value of task priority for sorting."""
        priority_map = {"low": 1, "medium": 2, "high": 3}
        return priority_map[self.priority]

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.is_completed = True

    def create_next_occurrence(self) -> "Task":
        """Create next occurrence with updated due_date for daily/weekly tasks."""
        if self.recurrence == "once":
            return None

        # Calculate next due date
        next_due_date = None
        if self.due_date:
            current_date = datetime.strptime(self.due_date, "%Y-%m-%d").date()
            if self.recurrence == "daily":
                next_date = current_date + timedelta(days=1)
            elif self.recurrence == "weekly":
                next_date = current_date + timedelta(days=7)
            next_due_date = next_date.strftime("%Y-%m-%d")

        return Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            scheduled_time=self.scheduled_time,
            recurrence=self.recurrence,
            due_date=next_due_date,
            is_completed=False,
        )


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

    def mark_task_complete(self, task: Task) -> None:
        """Mark a task complete and create next occurrence if recurring."""
        if task not in self.tasks:
            raise ValueError(f"Task '{task.title}' not found in {self.name}'s tasks.")

        task.mark_complete()

        # Create next occurrence if task is recurring
        if task.recurrence in ["daily", "weekly"]:
            next_task = task.create_next_occurrence()
            if next_task:
                self.add_task(next_task)


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
    def _sort_by_time(tasks: List[Task]) -> List[Task]:
        """Sort tasks by scheduled time in ascending order (earliest first)."""
        return sorted(tasks, key=lambda task: task.scheduled_time or "23:59")

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

    @staticmethod
    def _filter_by_status(tasks: List[Task], is_completed: bool) -> List[Task]:
        """Filter tasks by completion status (True for completed, False for pending)."""
        return [task for task in tasks if task.is_completed == is_completed]

    @staticmethod
    def _filter_by_pet(owner: Owner, pet_name: str) -> List[Task]:
        """Filter tasks by pet name, returning tasks for the specified pet."""
        for pet in owner.pets:
            if pet.name == pet_name:
                return pet.tasks
        return []

    @staticmethod
    def detect_conflicts(owner: Owner) -> List[str]:
        """Detect scheduling conflicts across all pets and return warning messages."""
        conflicts = []

        # Build a map of scheduled_time -> list of (pet, task) tuples
        time_slots = {}
        for pet in owner.pets:
            for task in pet.tasks:
                if task.scheduled_time and not task.is_completed:
                    time_key = task.scheduled_time
                    if time_key not in time_slots:
                        time_slots[time_key] = []
                    time_slots[time_key].append((pet, task))

        # Check for conflicts at each time slot
        for time_key, items in time_slots.items():
            if len(items) > 1:
                pet_names = [pet.name for pet, _ in items]
                task_titles = [task.title for _, task in items]
                conflict_msg = (
                    f"⚠️  CONFLICT at {time_key}: "
                    f"{', '.join(pet_names)} both scheduled for "
                    f"{', '.join(task_titles)}"
                )
                conflicts.append(conflict_msg)

        return conflicts
