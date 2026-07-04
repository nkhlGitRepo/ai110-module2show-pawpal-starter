from pawpal_system import Task, Pet, Owner, Scheduler

# Create owner and pets
owner = Owner(name="Jordan", available_minutes_per_day=480)
dog = Pet(name="Biscuit", species="Golden Retriever")
cat = Pet(name="Whiskers", species="Cat")

# Add dog tasks OUT OF ORDER with scheduled times
dog.add_task(Task(title="Evening walk", duration_minutes=30, priority="high", scheduled_time="18:00"))
dog.add_task(Task(title="Feeding", duration_minutes=10, priority="high", scheduled_time="08:00"))
dog.add_task(Task(title="Playtime", duration_minutes=20, priority="medium", scheduled_time="14:00"))
dog.add_task(Task(title="Grooming", duration_minutes=45, priority="low", scheduled_time="16:00"))

# Add cat tasks OUT OF ORDER with scheduled times
cat.add_task(Task(title="Afternoon nap", duration_minutes=20, priority="low", scheduled_time="15:00"))
cat.add_task(Task(title="Feeding", duration_minutes=5, priority="high", scheduled_time="08:30"))
cat.add_task(Task(title="Litter box", duration_minutes=10, priority="high", scheduled_time="12:00"))

# Mark some as completed
dog.tasks[1].mark_complete()  # Feeding
cat.tasks[1].mark_complete()  # Feeding

owner.add_pet(dog)
owner.add_pet(cat)

# Test 1: Sort by time
print("=" * 50)
print("SORT BY TIME (out-of-order → chronological)")
print("=" * 50)
for pet in [dog, cat]:
    print(f"\n{pet.name}:")
    sorted_tasks = Scheduler._sort_by_time(pet.tasks)
    for task in sorted_tasks:
        time_str = task.scheduled_time or "Unscheduled"
        print(f"  {time_str} — {task.title} ({task.duration_minutes} min)")

# Test 2: Filter by status
print("\n" + "=" * 50)
print("FILTER BY STATUS")
print("=" * 50)
for pet in [dog, cat]:
    print(f"\n{pet.name}:")
    pending = Scheduler._filter_by_status(pet.tasks, is_completed=False)
    completed = Scheduler._filter_by_status(pet.tasks, is_completed=True)
    print(f"  Pending ({len(pending)}): {', '.join(t.title for t in pending)}")
    print(f"  Completed ({len(completed)}): {', '.join(t.title for t in completed)}")

# Test 3: Filter by pet
print("\n" + "=" * 50)
print("FILTER BY PET")
print("=" * 50)
for pet_name in ["Biscuit", "Whiskers"]:
    pet_tasks = Scheduler._filter_by_pet(owner, pet_name)
    print(f"\n{pet_name}'s tasks: {len(pet_tasks)} total")
    for task in pet_tasks:
        print(f"  - {task.title}")

print("\n" + "=" * 50)

# Test 4: Recurring tasks
print("\nRECURRING TASKS TEST")
print("=" * 50)

dog_recurring = Pet(name="Max", species="Labrador")
dog_recurring.add_task(Task(title="Morning walk", duration_minutes=30, priority="high", scheduled_time="08:00", recurrence="daily", due_date="2026-07-02"))
dog_recurring.add_task(Task(title="Feeding", duration_minutes=10, priority="high", scheduled_time="18:00", recurrence="daily", due_date="2026-07-02"))
dog_recurring.add_task(Task(title="Grooming", duration_minutes=45, priority="low", scheduled_time="16:00", recurrence="once", due_date="2026-07-02"))

print(f"\nInitial tasks ({len(dog_recurring.tasks)}):")
for i, task in enumerate(dog_recurring.tasks, 1):
    print(f"  {i}. {task.title} [{task.recurrence}]")

print("\n--- Marking 'Morning walk' as complete ---")
morning_walk = dog_recurring.tasks[0]
dog_recurring.mark_task_complete(morning_walk)

print(f"After marking complete ({len(dog_recurring.tasks)} total):")
for i, task in enumerate(dog_recurring.tasks, 1):
    status = "✓" if task.is_completed else "○"
    print(f"  {i}. {status} {task.title} [{task.recurrence}]")

print("\n--- Marking 'Grooming' (one-time) as complete ---")
grooming = [t for t in dog_recurring.tasks if t.title == "Grooming"][0]
dog_recurring.mark_task_complete(grooming)

print(f"After marking complete ({len(dog_recurring.tasks)} total):")
print("  (No new Grooming task created - it's one-time)")
for i, task in enumerate(dog_recurring.tasks, 1):
    status = "✓" if task.is_completed else "○"
    print(f"  {i}. {status} {task.title} [{task.recurrence}]")

print("\n" + "=" * 50)

# Test 5: Conflict detection
print("\nCONFLICT DETECTION TEST")
print("=" * 50)

owner_conflicts = Owner(name="Alex", available_minutes_per_day=600)
dog_conflict = Pet(name="Rex", species="Bulldog")
cat_conflict = Pet(name="Luna", species="Siamese")

# Add conflicting tasks (same time for different pets)
dog_conflict.add_task(Task(title="Walk", duration_minutes=30, priority="high", scheduled_time="09:00"))
cat_conflict.add_task(Task(title="Feeding", duration_minutes=10, priority="high", scheduled_time="09:00"))

# Add non-conflicting tasks
dog_conflict.add_task(Task(title="Playtime", duration_minutes=20, priority="medium", scheduled_time="14:00"))
cat_conflict.add_task(Task(title="Grooming", duration_minutes=25, priority="low", scheduled_time="16:00"))

# Add another conflict in same pet
dog_conflict.add_task(Task(title="Training", duration_minutes=30, priority="high", scheduled_time="14:00"))

owner_conflicts.add_pet(dog_conflict)
owner_conflicts.add_pet(cat_conflict)

print(f"\nSchedule for {owner_conflicts.name}:")
for pet in owner_conflicts.pets:
    print(f"  {pet.name}:")
    for task in pet.tasks:
        print(f"    - {task.scheduled_time} | {task.title}")

conflicts = Scheduler.detect_conflicts(owner_conflicts)
print(f"\nConflicts detected: {len(conflicts)}")
for conflict in conflicts:
    print(f"  {conflict}")

if not conflicts:
    print("  ✓ No conflicts found!")

print("\n" + "=" * 50)

# Test 6: Suggest optimal time slots
print("\nTIME SLOT SUGGESTION TEST")
print("=" * 50)

owner_slots = Owner(name="Sam", available_minutes_per_day=600)
dog_slots = Pet(name="Max", species="Labrador")
cat_slots = Pet(name="Luna", species="Siamese")

dog_slots.add_task(Task(title="Walk", duration_minutes=30, priority="high", scheduled_time="08:00"))
dog_slots.add_task(Task(title="Feeding", duration_minutes=10, priority="high", scheduled_time="12:00"))
cat_slots.add_task(Task(title="Feeding", duration_minutes=5, priority="high", scheduled_time="09:00"))
cat_slots.add_task(Task(title="Playtime", duration_minutes=15, priority="medium", scheduled_time="17:00"))

owner_slots.add_pet(dog_slots)
owner_slots.add_pet(cat_slots)

print("\nCurrent schedule:")
print(f"  Max: 08:00 (Walk), 12:00 (Feeding)")
print(f"  Luna: 09:00 (Feeding), 17:00 (Playtime)")

new_task_high = Task(title="Training", duration_minutes=20, priority="high")
suggestions = Scheduler.suggest_time_slots(owner_slots, dog_slots, new_task_high)

print(f"\nSuggested times for Max's 'Training' (high priority):")
for slot, note in suggestions:
    print(f"  {note}")

new_task_medium = Task(title="Nap time", duration_minutes=30, priority="medium")
suggestions_medium = Scheduler.suggest_time_slots(owner_slots, cat_slots, new_task_medium)

print(f"\nSuggested times for Luna's 'Nap time' (medium priority):")
for slot, note in suggestions_medium:
    print(f"  {note}")

print("\n" + "=" * 50)
