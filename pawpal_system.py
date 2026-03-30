from dataclasses import dataclass


@dataclass
class Pet:
    name: str
    breed: str
    size: str
    species: str
    age_years: int
    health_notes: str = ""

    def get_profile(self) -> dict:
        "gets the pet's profile information as a dictionary"
        return {
            "name": self.name,
            "breed": self.breed,
            "size": self.size,
            "species": self.species,
            "age_years": self.age_years,
            "health_notes": self.health_notes
        }

    def update_health_notes(self, notes: str) -> None:
        "updates the health notes for the pet"
        self.health_notes = notes


@dataclass
class CareTask:
    task_type: str
    duration_minutes: int
    priority: int
    notes: str = ""
    is_completed: bool = False

    def complete(self) -> None:
        self.is_completed = True

    def is_high_priority(self) -> bool:
        return self.priority >= 8

    def get_summary(self) -> str:
        return f"{self.task_type} - {self.duration_minutes} mins - Priority: {self.priority}"


class Owner:
    def __init__(self, name: str, email: str, available_minutes: int):
        self.name = name
        self.email = email
        self.available_minutes = available_minutes
        self.preferences: list[str] = []
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def set_available_time(self, minutes: int) -> None:
        self.available_minutes = minutes

    def get_preferences(self) -> list[str]:
        return self.preferences


class DailyScheduler:
    def __init__(self, owner: Owner, pet: Pet):
        self.owner = owner
        self.pet = pet
        self.tasks: list[CareTask] = []
        self.scheduled_plan: list[CareTask] = []

    def add_task(self, task: CareTask) -> None:
        self.tasks.append(task)

    def remove_task(self, task_type: str) -> None:
        self.tasks = [task for task in self.tasks if task.task_type != task_type]

    def generate_plan(self) -> list[CareTask]:
        # Placeholder for the actual scheduling algorithm
        self.scheduled_plan = sorted(self.tasks, key=lambda t: t.priority, reverse=True)
        return self.scheduled_plan

    def explain_plan(self) -> str:
        return "Here's your daily care plan!"

    def get_total_duration(self) -> int:
        return sum(task.duration_minutes for task in self.tasks)

    def reset_plan(self) -> None:
        self.scheduled_plan = []