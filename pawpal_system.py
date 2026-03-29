"""
pawpal_system.py
PawPal+ Backend Logic Layer — Class Skeletons
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
from typing import Optional
import uuid


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class TaskType(Enum):
    FEEDING = "feeding"
    WALK = "walk"
    MEDICATION = "medication"
    APPOINTMENT = "appointment"
    GROOMING = "grooming"


class Recurrence(Enum):
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Task:
    title: str
    task_type: TaskType
    due_datetime: datetime
    priority: int = 1                          # 1 = highest priority
    recurrence: Recurrence = Recurrence.NONE
    notes: str = ""
    is_complete: bool = False
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def complete(self) -> None:
        """Mark this task as completed."""
        pass

    def reschedule(self, new_datetime: datetime) -> None:
        """Update the task's due date/time."""
        pass

    def is_due_today(self) -> bool:
        """Return True if the task is due today."""
        pass

    def generate_next_occurrence(self) -> Optional[Task]:
        """
        If this task recurs, return a new Task for the next occurrence.
        Returns None if recurrence is NONE.
        """
        pass


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    weight: float
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        pass

    def remove_task(self, task_id: str) -> None:
        """Remove a task by its ID."""
        pass

    def get_tasks(self) -> list[Task]:
        """Return all tasks for this pet."""
        pass

    def get_tasks_by_date(self, target_date: date) -> list[Task]:
        """Return tasks due on a specific date."""
        pass


# ---------------------------------------------------------------------------
# Regular Classes
# ---------------------------------------------------------------------------

class Owner:
    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Register a new pet under this owner."""
        pass

    def remove_pet(self, pet_name: str) -> None:
        """Remove a pet by name."""
        pass

    def get_all_tasks(self) -> list[Task]:
        """Aggregate and return all tasks across all pets."""
        pass


class Scheduler:
    def __init__(self) -> None:
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler."""
        pass

    def remove_task(self, task_id: str) -> None:
        """Remove a task by ID."""
        pass

    def get_todays_tasks(self) -> list[Task]:
        """Return all tasks due today."""
        pass

    def get_tasks_for_pet(self, pet: Pet) -> list[Task]:
        """Return all scheduled tasks for a specific pet."""
        pass

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Return tasks sorted by priority (ascending = highest first)."""
        pass

    def detect_conflicts(self, pet: Pet) -> list[tuple[Task, Task]]:
        """
        Detect scheduling conflicts for a pet.
        A conflict occurs when two tasks overlap in time.
        Returns a list of conflicting task pairs.
        """
        pass

    def generate_recurring_tasks(self) -> None:
        """
        Scan completed recurring tasks and generate their next occurrences
        if not already scheduled.
        """
        pass