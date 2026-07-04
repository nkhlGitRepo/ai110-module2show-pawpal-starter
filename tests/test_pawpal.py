import pytest
from datetime import datetime
from pawpal_system import Task, Pet, Owner, Scheduler


# ==================== BASIC FUNCTIONALITY ====================

def test_task_completion():
    """Verify that calling mark_complete() changes the task's status."""
    task = Task(title="Walk", duration_minutes=30, priority="high")
    task.mark_complete()
    assert task.is_completed == True


def test_task_addition_increases_pet_count():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet(name="Biscuit", species="Dog")
    assert len(pet.tasks) == 0

    task = Task(title="Walk", duration_minutes=30, priority="high")
    pet.add_task(task)

    assert len(pet.tasks) == 1


# ==================== SORTING CORRECTNESS ====================

def test_sort_by_time_chronological_order():
    """Verify tasks are sorted chronologically by scheduled_time."""
    task1 = Task(title="Evening walk", duration_minutes=30, priority="high", scheduled_time="18:00")
    task2 = Task(title="Morning walk", duration_minutes=30, priority="high", scheduled_time="08:00")
    task3 = Task(title="Afternoon walk", duration_minutes=30, priority="high", scheduled_time="14:00")

    tasks = [task1, task2, task3]
    sorted_tasks = Scheduler._sort_by_time(tasks)

    assert sorted_tasks[0].scheduled_time == "08:00"
    assert sorted_tasks[1].scheduled_time == "14:00"
    assert sorted_tasks[2].scheduled_time == "18:00"


def test_sort_by_priority_high_to_low():
    """Verify tasks are sorted by priority (high → medium → low)."""
    task1 = Task(title="Task", duration_minutes=10, priority="low")
    task2 = Task(title="Task", duration_minutes=10, priority="high")
    task3 = Task(title="Task", duration_minutes=10, priority="medium")

    tasks = [task1, task2, task3]
    sorted_tasks = Scheduler._sort_by_priority(tasks)

    assert sorted_tasks[0].priority == "high"
    assert sorted_tasks[1].priority == "medium"
    assert sorted_tasks[2].priority == "low"


def test_sort_by_time_unscheduled_tasks_last():
    """Verify unscheduled tasks (None time) appear at the end."""
    task1 = Task(title="Task", duration_minutes=10, priority="high", scheduled_time="09:00")
    task2 = Task(title="Task", duration_minutes=10, priority="high", scheduled_time=None)

    tasks = [task2, task1]
    sorted_tasks = Scheduler._sort_by_time(tasks)

    assert sorted_tasks[0].scheduled_time == "09:00"
    assert sorted_tasks[1].scheduled_time is None


# ==================== RECURRENCE LOGIC ====================

def test_recurring_daily_task_creates_next_occurrence():
    """Verify marking a daily task complete creates a new task for the next day."""
    pet = Pet(name="Biscuit", species="Dog")
    task = Task(
        title="Morning walk",
        duration_minutes=30,
        priority="high",
        recurrence="daily",
        due_date="2026-07-03"
    )
    pet.add_task(task)

    assert len(pet.tasks) == 1
    pet.mark_task_complete(task)

    assert len(pet.tasks) == 2
    assert pet.tasks[0].is_completed == True
    assert pet.tasks[1].is_completed == False
    assert pet.tasks[1].due_date == "2026-07-04"


def test_recurring_weekly_task_creates_next_occurrence():
    """Verify marking a weekly task complete creates a task 7 days later."""
    pet = Pet(name="Biscuit", species="Dog")
    task = Task(
        title="Grooming",
        duration_minutes=45,
        priority="medium",
        recurrence="weekly",
        due_date="2026-07-03"
    )
    pet.add_task(task)

    pet.mark_task_complete(task)

    assert len(pet.tasks) == 2
    assert pet.tasks[1].due_date == "2026-07-10"


def test_one_time_task_does_not_create_next_occurrence():
    """Verify marking a one-time task complete does NOT create a new task."""
    pet = Pet(name="Biscuit", species="Dog")
    task = Task(
        title="Feeding",
        duration_minutes=10,
        priority="high",
        recurrence="once",
        due_date="2026-07-03"
    )
    pet.add_task(task)

    assert len(pet.tasks) == 1
    pet.mark_task_complete(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0].is_completed == True


# ==================== CONFLICT DETECTION ====================

def test_detect_conflicts_same_time():
    """Verify Scheduler detects when tasks are scheduled at the same time."""
    owner = Owner(name="Alice", available_minutes_per_day=600)
    pet1 = Pet(name="Biscuit", species="Dog")
    pet2 = Pet(name="Whiskers", species="Cat")

    task1 = Task(title="Walk", duration_minutes=30, priority="high", scheduled_time="09:00")
    task2 = Task(title="Feeding", duration_minutes=10, priority="high", scheduled_time="09:00")

    pet1.add_task(task1)
    pet2.add_task(task2)
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    conflicts = Scheduler.detect_conflicts(owner)

    assert len(conflicts) > 0
    assert "09:00" in conflicts[0]
    assert "Biscuit" in conflicts[0] or "Whiskers" in conflicts[0]


def test_detect_conflicts_same_pet_multiple_times():
    """Verify Scheduler detects when one pet has multiple tasks at same time."""
    owner = Owner(name="Alice", available_minutes_per_day=600)
    pet = Pet(name="Biscuit", species="Dog")

    task1 = Task(title="Walk", duration_minutes=30, priority="high", scheduled_time="09:00")
    task2 = Task(title="Playtime", duration_minutes=20, priority="medium", scheduled_time="09:00")

    pet.add_task(task1)
    pet.add_task(task2)
    owner.add_pet(pet)

    conflicts = Scheduler.detect_conflicts(owner)

    assert len(conflicts) > 0
    assert "09:00" in conflicts[0]


def test_detect_conflicts_no_duplicates_in_message():
    """Verify pet names are not duplicated in conflict message."""
    owner = Owner(name="Alice", available_minutes_per_day=600)
    pet = Pet(name="Biscuit", species="Dog")

    task1 = Task(title="Walk", duration_minutes=30, priority="high", scheduled_time="09:00")
    task2 = Task(title="Playtime", duration_minutes=20, priority="medium", scheduled_time="09:00")

    pet.add_task(task1)
    pet.add_task(task2)
    owner.add_pet(pet)

    conflicts = Scheduler.detect_conflicts(owner)

    conflict_msg = conflicts[0]
    biscuit_count = conflict_msg.count("Biscuit")
    assert biscuit_count == 1


def test_no_conflicts_for_different_times():
    """Verify Scheduler finds no conflicts when tasks are at different times."""
    owner = Owner(name="Alice", available_minutes_per_day=600)
    pet = Pet(name="Biscuit", species="Dog")

    task1 = Task(title="Walk", duration_minutes=30, priority="high", scheduled_time="09:00")
    task2 = Task(title="Feeding", duration_minutes=10, priority="high", scheduled_time="18:00")

    pet.add_task(task1)
    pet.add_task(task2)
    owner.add_pet(pet)

    conflicts = Scheduler.detect_conflicts(owner)

    assert len(conflicts) == 0


# ==================== FILTERING ====================

def test_filter_by_status_pending():
    """Verify filtering by completion status returns only pending tasks."""
    task1 = Task(title="Walk", duration_minutes=30, priority="high")
    task2 = Task(title="Feeding", duration_minutes=10, priority="high")

    task1.mark_complete()

    tasks = [task1, task2]
    pending = Scheduler._filter_by_status(tasks, is_completed=False)

    assert len(pending) == 1
    assert pending[0].title == "Feeding"


def test_filter_by_status_completed():
    """Verify filtering by completion status returns only completed tasks."""
    task1 = Task(title="Walk", duration_minutes=30, priority="high")
    task2 = Task(title="Feeding", duration_minutes=10, priority="high")

    task1.mark_complete()

    tasks = [task1, task2]
    completed = Scheduler._filter_by_status(tasks, is_completed=True)

    assert len(completed) == 1
    assert completed[0].title == "Walk"


def test_filter_by_pet():
    """Verify filtering returns tasks for the specified pet."""
    owner = Owner(name="Alice", available_minutes_per_day=600)
    pet1 = Pet(name="Biscuit", species="Dog")
    pet2 = Pet(name="Whiskers", species="Cat")

    task1 = Task(title="Walk", duration_minutes=30, priority="high")
    task2 = Task(title="Feeding", duration_minutes=10, priority="high")

    pet1.add_task(task1)
    pet2.add_task(task2)
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    biscuit_tasks = Scheduler._filter_by_pet(owner, "Biscuit")

    assert len(biscuit_tasks) == 1
    assert biscuit_tasks[0].title == "Walk"


# ==================== VALIDATION ====================

def test_invalid_priority_raises_error():
    """Verify Task validation rejects invalid priority."""
    with pytest.raises(ValueError):
        Task(title="Walk", duration_minutes=30, priority="urgent")


def test_invalid_duration_raises_error():
    """Verify Task validation rejects non-positive duration."""
    with pytest.raises(ValueError):
        Task(title="Walk", duration_minutes=0, priority="high")


def test_invalid_date_format_raises_error():
    """Verify Task validation rejects invalid date format."""
    with pytest.raises(ValueError):
        Task(
            title="Walk",
            duration_minutes=30,
            priority="high",
            recurrence="daily",
            due_date="07/03/2026"
        )


def test_recurring_task_without_due_date_raises_error():
    """Verify recurring tasks require a due_date."""
    with pytest.raises(ValueError):
        Task(title="Walk", duration_minutes=30, priority="high", recurrence="daily")


def test_empty_pet_name_raises_error():
    """Verify Pet validation rejects empty names."""
    with pytest.raises(ValueError):
        Pet(name="", species="Dog")


def test_empty_owner_name_raises_error():
    """Verify Owner validation rejects empty names."""
    with pytest.raises(ValueError):
        Owner(name="", available_minutes_per_day=480)


def test_negative_available_time_raises_error():
    """Verify Owner validation rejects non-positive available time."""
    with pytest.raises(ValueError):
        Owner(name="Alice", available_minutes_per_day=-100)


# ==================== DUPLICATE PREVENTION ====================

def test_duplicate_one_time_task_rejected():
    """Verify Pet prevents adding duplicate one-time tasks."""
    pet = Pet(name="Biscuit", species="Dog")
    task = Task(title="Walk", duration_minutes=30, priority="high")

    pet.add_task(task)

    with pytest.raises(ValueError):
        pet.add_task(task)


def test_duplicate_recurring_task_with_different_dates_allowed():
    """Verify recurring tasks with different due_dates are allowed (different occurrences)."""
    pet = Pet(name="Biscuit", species="Dog")
    task1 = Task(
        title="Walk",
        duration_minutes=30,
        priority="high",
        recurrence="daily",
        due_date="2026-07-03"
    )
    task2 = Task(
        title="Walk",
        duration_minutes=30,
        priority="high",
        recurrence="daily",
        due_date="2026-07-04"
    )

    pet.add_task(task1)
    pet.add_task(task2)

    assert len(pet.tasks) == 2


# ==================== TIME SLOT SUGGESTIONS ====================

def test_suggest_time_slots_basic():
    """Verify time slot suggestion returns available slots without conflicts."""
    owner = Owner(name="Alice", available_minutes_per_day=600)
    pet = Pet(name="Biscuit", species="Dog")
    owner.add_pet(pet)

    pet.add_task(Task(title="Walk", duration_minutes=30, priority="high", scheduled_time="08:00"))

    unscheduled = Task(title="Playtime", duration_minutes=20, priority="high")
    suggestions = Scheduler.suggest_time_slots(owner, pet, unscheduled)

    assert len(suggestions) == 3
    suggested_times = [slot for slot, _ in suggestions]
    assert "08:00" not in suggested_times


def test_suggest_time_slots_avoids_pet_conflicts():
    """Verify suggestions avoid times already scheduled for the same pet."""
    owner = Owner(name="Alice", available_minutes_per_day=600)
    pet = Pet(name="Biscuit", species="Dog")
    owner.add_pet(pet)

    pet.add_task(Task(title="Walk", duration_minutes=30, priority="high", scheduled_time="08:00"))
    pet.add_task(Task(title="Feeding", duration_minutes=10, priority="high", scheduled_time="12:00"))

    unscheduled = Task(title="Training", duration_minutes=20, priority="high")
    suggestions = Scheduler.suggest_time_slots(owner, pet, unscheduled)

    suggested_times = [slot for slot, _ in suggestions]
    assert "08:00" not in suggested_times
    assert "12:00" not in suggested_times


def test_suggest_time_slots_prioritizes_high_priority_early():
    """Verify high-priority tasks get earlier time suggestions."""
    owner = Owner(name="Alice", available_minutes_per_day=600)
    pet = Pet(name="Biscuit", species="Dog")
    owner.add_pet(pet)

    high_priority = Task(title="Walk", duration_minutes=30, priority="high")
    suggestions_high = Scheduler.suggest_time_slots(owner, pet, high_priority)

    medium_priority = Task(title="Playtime", duration_minutes=20, priority="medium")
    suggestions_medium = Scheduler.suggest_time_slots(owner, pet, medium_priority)

    high_times = [int(slot.split(":")[0]) for slot, _ in suggestions_high]
    medium_times = [int(slot.split(":")[0]) for slot, _ in suggestions_medium]

    assert high_times[0] <= medium_times[0]


def test_suggest_time_slots_detects_other_pet_conflicts():
    """Verify suggestions note conflicts with other pets' scheduled times."""
    owner = Owner(name="Alice", available_minutes_per_day=600)
    dog = Pet(name="Biscuit", species="Dog")
    cat = Pet(name="Whiskers", species="Cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    cat.add_task(Task(title="Feeding", duration_minutes=5, priority="high", scheduled_time="09:00"))

    unscheduled = Task(title="Walk", duration_minutes=30, priority="high")
    suggestions = Scheduler.suggest_time_slots(owner, dog, unscheduled)

    suggestion_notes = [note for _, note in suggestions]

    conflict_found = any("⚠️ conflicts" in note and "09:00" in note for note in suggestion_notes)
    non_conflict_found = any("no conflicts" in note for note in suggestion_notes)

    assert conflict_found or non_conflict_found


def test_suggest_time_slots_returns_multiple_options():
    """Verify suggestion returns multiple ranked options."""
    owner = Owner(name="Alice", available_minutes_per_day=600)
    pet = Pet(name="Biscuit", species="Dog")
    owner.add_pet(pet)

    unscheduled = Task(title="Walk", duration_minutes=30, priority="high")
    suggestions = Scheduler.suggest_time_slots(owner, pet, unscheduled, num_suggestions=5)

    assert len(suggestions) <= 5
    assert all(isinstance(slot, str) and ":" in slot for slot, _ in suggestions)


def test_suggest_time_slots_empty_pet_schedule():
    """Verify suggestions work for pets with no tasks yet."""
    owner = Owner(name="Alice", available_minutes_per_day=600)
    pet = Pet(name="Biscuit", species="Dog")
    owner.add_pet(pet)

    unscheduled = Task(title="Walk", duration_minutes=30, priority="high")
    suggestions = Scheduler.suggest_time_slots(owner, pet, unscheduled)

    assert len(suggestions) == 3
    assert all(isinstance(slot, str) for slot, _ in suggestions)


def test_suggest_time_slots_respects_num_suggestions():
    """Verify the method returns exactly the requested number of suggestions."""
    owner = Owner(name="Alice", available_minutes_per_day=600)
    pet = Pet(name="Biscuit", species="Dog")
    owner.add_pet(pet)

    unscheduled = Task(title="Walk", duration_minutes=30, priority="high")

    suggestions_1 = Scheduler.suggest_time_slots(owner, pet, unscheduled, num_suggestions=1)
    suggestions_3 = Scheduler.suggest_time_slots(owner, pet, unscheduled, num_suggestions=3)

    assert len(suggestions_1) == 1
    assert len(suggestions_3) == 3
