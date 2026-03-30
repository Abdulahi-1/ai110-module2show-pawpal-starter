from dataclasses import dataclass
from typing import Optional


# ---------------------------------------------------------------------------
# Data classes — clean, lightweight objects for structured data
# ---------------------------------------------------------------------------

@dataclass
class Pet:
    name: str
    breed: str
    size: str                   # e.g. "small", "medium", "large"
    species: str                # e.g. "dog", "cat"
    age_years: int
    health_notes: str = ""

    def get_profile(self) -> dict:
        """Return pet attributes as a dictionary."""
        return {
            "name": self.name,
            "breed": self.breed,
            "size": self.size,
            "species": self.species,
            "age_years": self.age_years,
            "health_notes": self.health_notes,
        }

    def update_health_notes(self, notes: str) -> None:
        """Append or replace health notes."""
        self.health_notes = notes


@dataclass
class CareTask:
    task_type: str              # e.g. "walk", "feeding", "meds", "grooming"
    duration_minutes: int
    priority: int               # 1 = highest priority
    notes: str = ""
    is_completed: bool = False

    def complete(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True

    def is_high_priority(self) -> bool:
        """Return True if priority is 1 (highest)."""
        return self.priority == 1

    def get_summary(self) -> str:
        """Return a short human-readable summary of the task."""
        status = "done" if self.is_completed else "pending"
        return f"[{status}] {self.task_type} ({self.duration_minutes} min, priority {self.priority})"


# ---------------------------------------------------------------------------
# Regular classes — stateful objects with behaviour
# ---------------------------------------------------------------------------

class Owner:
    def __init__(self, name: str, email: str, available_minutes: int = 120):
        self.name = name
        self.email = email
        self.available_minutes = available_minutes
        self.preferences: list[str] = []
        self.pet: Optional[Pet] = None

    def add_pet(self, pet: Pet) -> None:
        """Attach a pet to this owner."""
        self.pet = pet

    def set_available_time(self, minutes: int) -> None:
        """Update the owner's daily time budget."""
        self.available_minutes = minutes

    def get_preferences(self) -> list[str]:
        """Return the owner's care preferences."""
        return self.preferences


class DailyScheduler:
    def __init__(self, owner: Owner, pet: Pet):
        self.owner = owner
        self.pet = pet
        self.tasks: list[CareTask] = []
        self.scheduled_plan: list[CareTask] = []

    def add_task(self, task: CareTask) -> None:
        """Add a care task to the task pool."""
        self.tasks.append(task)

    def remove_task(self, task_type: str) -> None:
        """Remove all tasks matching task_type from the pool."""
        self.tasks = [t for t in self.tasks if t.task_type != task_type]

    def generate_plan(self) -> list[CareTask]:
        """
        Sort tasks by priority and fit them within the owner's
        available time budget. Returns the scheduled plan.
        """
        sorted_tasks = sorted(self.tasks, key=lambda t: t.priority)
        plan: list[CareTask] = []
        time_used = 0

        for task in sorted_tasks:
            if time_used + task.duration_minutes <= self.owner.available_minutes:
                plan.append(task)
                time_used += task.duration_minutes

        self.scheduled_plan = plan
        return self.scheduled_plan

    def explain_plan(self) -> str:
        """Return a plain-English explanation of the scheduled plan."""
        if not self.scheduled_plan:
            return "No plan generated yet. Call generate_plan() first."
        lines = [f"Daily plan for {self.pet.name} ({self.get_total_duration()} min total):"]
        for task in self.scheduled_plan:
            lines.append(f"  • {task.get_summary()}")
        return "\n".join(lines)

    def get_total_duration(self) -> int:
        """Return the total duration of all scheduled tasks in minutes."""
        return sum(t.duration_minutes for t in self.scheduled_plan)

    def reset_plan(self) -> None:
        """Clear the current scheduled plan."""
        self.scheduled_plan = []
