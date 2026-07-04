from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner(name="Jordan")

dog = Pet(name="Mochi", species="dog")
owner.add_pet(dog)

dog.add_task(Task(description="Morning walk", duration_minutes=30, priority="high", pet_name="Mochi"))
dog.add_task(Task(description="Feeding", duration_minutes=10, priority="high", pet_name="Mochi"))
dog.add_task(Task(description="Brushing", duration_minutes=15, priority="low", pet_name="Mochi"))
dog.add_task(Task(description="Training practice", duration_minutes=20, priority="medium", pet_name="Mochi"))
dog.add_task(Task(description="Evening walk", duration_minutes=90, priority="high", pet_name="Mochi"))

scheduler = Scheduler(owner, available_minutes=60)

plan = scheduler.generate_plan()

print("=== Today's Plan ===")
print(scheduler.explain_plan(plan))