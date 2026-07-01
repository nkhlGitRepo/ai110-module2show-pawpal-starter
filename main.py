from pawpal_system import Task, Pet, Owner, Scheduler


# Create an owner
owner = Owner(name="Jordan", available_minutes_per_day=120)

# Create two pets
dog = Pet(name="Biscuit", species="Golden Retriever")
cat = Pet(name="Whiskers", species="Cat")

# Add tasks to the dog
dog.add_task(Task(title="Morning walk", duration_minutes=30, priority="high"))
dog.add_task(Task(title="Feeding", duration_minutes=10, priority="high"))
dog.add_task(Task(title="Playtime", duration_minutes=20, priority="medium"))

# Add tasks to the cat
cat.add_task(Task(title="Feeding", duration_minutes=5, priority="high"))
cat.add_task(Task(title="Litter box", duration_minutes=10, priority="high"))
cat.add_task(Task(title="Play session", duration_minutes=15, priority="medium"))

# Add pets to owner
owner.add_pet(dog)
owner.add_pet(cat)

# Generate schedules
dog_schedule = Scheduler.generate(owner, dog)
cat_schedule = Scheduler.generate(owner, cat)

# Print today's schedule
print("=" * 50)
print(f"TODAY'S SCHEDULE FOR {owner.name}")
print("=" * 50)
print()
print(f"{dog.name}:")
print(f"  {dog_schedule.explanation}")
for task in dog_schedule.scheduled_tasks:
    print(f"    - {task.title} ({task.duration_minutes} min)")
print()
print(f"{cat.name}:")
print(f"  {cat_schedule.explanation}")
for task in cat_schedule.scheduled_tasks:
    print(f"    - {task.title} ({task.duration_minutes} min)")
print()
print("=" * 50)
