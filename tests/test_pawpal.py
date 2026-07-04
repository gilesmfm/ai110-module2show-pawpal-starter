from pawpal_system import Owner, Pet, Task, Scheduler


def test_mark_complete_changes_status():
    task = Task(description="Feed", duration_minutes=10, priority="high", pet_name="Mochi")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_sort_by_priority_orders_high_first():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    pet.add_task(Task(description="Brushing", duration_minutes=15, priority="low", pet_name="Mochi"))
    pet.add_task(Task(description="Walk", duration_minutes=30, priority="high", pet_name="Mochi"))
    pet.add_task(Task(description="Training", duration_minutes=20, priority="medium", pet_name="Mochi"))

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_priority(pet.tasks)

    assert sorted_tasks[0].priority == "high"
    assert sorted_tasks[1].priority == "medium"
    assert sorted_tasks[2].priority == "low"


def test_generate_plan_respects_time_budget():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    pet.add_task(Task(description="Walk", duration_minutes=30, priority="high", pet_name="Mochi"))
    pet.add_task(Task(description="Feeding", duration_minutes=10, priority="high", pet_name="Mochi"))
    pet.add_task(Task(description="Long groom", duration_minutes=90, priority="high", pet_name="Mochi"))

    scheduler = Scheduler(owner, available_minutes=60)
    plan = scheduler.generate_plan()

    total_minutes = sum(t.duration_minutes for t in plan)
    assert total_minutes <= 60
    assert any(t.description == "Walk" for t in plan)
    assert any(t.description == "Feeding" for t in plan)
    assert not any(t.description == "Long groom" for t in plan)