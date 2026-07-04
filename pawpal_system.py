from dataclasses import dataclass, field

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    description: str
    duration_minutes: int
    priority: str  # "high", "medium", or "low"
    pet_name: str
    completed: bool = False

    def mark_complete(self):
        """Marks this task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Adds a care task to this pet's task list."""
        self.tasks.append(task)


@dataclass
class Owner:
    name: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet):
        
        self.pets.append(pet)

    def get_all_tasks(self) -> list:
        
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner, available_minutes: int = 120):
        
        self.owner = owner
        self.available_minutes = available_minutes

    def sort_by_priority(self, tasks: list) -> list:
        
        return sorted(tasks, key=lambda t: PRIORITY_ORDER.get(t.priority, 3))

    def generate_plan(self) -> list:
        
        candidates = self.sort_by_priority(self.owner.get_all_tasks())
        plan = []
        minutes_used = 0
        for task in candidates:
            if minutes_used + task.duration_minutes <= self.available_minutes:
                plan.append(task)
                minutes_used += task.duration_minutes
        return plan

    def explain_plan(self, plan: list) -> str:
        
        if not plan:
            return "No tasks fit in the available time."
        lines = []
        total = 0
        for task in plan:
            total += task.duration_minutes
            lines.append(
                f"- {task.description} ({task.pet_name}): {task.duration_minutes} min, "
                f"{task.priority} priority — included because higher-priority tasks "
                f"were scheduled first and time remained."
            )
        lines.append(f"\nTotal time used: {total}/{self.available_minutes} minutes.")
        return "\n".join(lines)