from dataclasses import dataclass
from typing import Optional


@dataclass
class Pet:
    name: str
    breed: str
    size: str
    species: str
    age_years: int
    health_notes: str = ""

    def get_profile(self) -> dict:
        pass

    def update_health_notes(self, notes: str) -> None:
        pass


@dataclass
class CareTask:
    task_type: str
    duration_minutes: int
    priority: int
    notes: str = ""
    is_completed: bool = False

    def complete(self) -> None:
        pass

    def is_high_priority(self) -> bool:
        pass

    def get_summary(self) -> str:
        pass


class Owner:
    def __init__(self, name: str, email: str, available_minutes: int):
        self.name = name
        self.email = email
        self.available_minutes = available_minutes
        self.preferences: list[str] = []
        self.pet: Optional[Pet] = None

    def add_pet(self, pet: Pet) -> None:
        pass

    def set_available_time(self, minutes: int) -> None:
        pass

    def get_preferences(self) -> list[str]:
        pass


class DailyScheduler:
    def __init__(self, owner: Owner, pet: Pet):
        self.owner = owner
        self.pet = pet
        self.tasks: list[CareTask] = []
        self.scheduled_plan: list[CareTask] = []

    def add_task(self, task: CareTask) -> None:
        pass

    def remove_task(self, task_type: str) -> None:
        pass

    def generate_plan(self) -> list[CareTask]:
        pass

    def explain_plan(self) -> str:
        pass

    def get_total_duration(self) -> int:
        pass

    def reset_plan(self) -> None:
        pass
