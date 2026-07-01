import pytest
from pawpal_system import Task, Pet, Owner, Scheduler


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
