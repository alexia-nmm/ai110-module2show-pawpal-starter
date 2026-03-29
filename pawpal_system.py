"""
pawpal_system.py
PawPal+ Backend Logic Layer — Core Implementation
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from enum import Enum
from typing import Optional
import uuid



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
        self.is_complete = True

    def reschedule(self, new_datetime: datetime) -> None:
        """Update the task's due date/time."""
        self.due_datetime = new_datetime

    def is_due_today(self) -> bool:
        """Return True if the task is due today."""
        return self.due_datetime.date() == date.today()

    def generate_next_occurrence(self) -> Optional[Task]:
        """Return a new Task for the next occurrence, or None if non-recurring."""
        if self.recurrence == Recurrence.NONE:
            return None

        if self.recurrence == Recurrence.DAILY:
            next_dt = self.due_datetime + timedelta(days=1)
        elif self.recurrence == Recurrence.WEEKLY:
            next_dt = self.due_datetime + timedelta(weeks=1)
        elif self.recurrence == Recurrence.MONTHLY:
            month = self.due_datetime.month + 1
            year = self.due_datetime.year + (month - 1) // 12
            month = ((month - 1) % 12) + 1
            next_dt = self.due_datetime.replace(year=year, month=month)

        return Task(
            title=self.title,
            task_type=self.task_type,
            due_datetime=next_dt,
            priority=self.priority,
            recurrence=self.recurrence,
            notes=self.notes,
        )




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
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove a task by its ID."""
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def get_tasks(self) -> list[Task]:
        """Return all tasks for this pet."""
        return list(self.tasks)

    def get_tasks_by_date(self, target_date: date) -> list[Task]:
        """Return tasks due on a specific date."""
        return [t for t in self.tasks if t.due_datetime.date() == target_date]




class Owner:
    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Register a new pet under this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        """Remove a pet by name."""
        self.pets = [p for p in self.pets if p.name != pet_name]

    def get_all_tasks(self) -> list[Task]:
        """Aggregate and return all tasks across all pets."""
        return [task for pet in self.pets for task in pet.tasks]




class Scheduler:
    """
    The Scheduler maintains its own flat task list and works with Owner/Pet
    objects passed in by the caller — it does not hold a reference to an Owner.

    Typical flow:
        scheduler.load_from_owner(owner)   # pull in all tasks
        scheduler.get_todays_tasks()       # work with them
    """

    def __init__(self) -> None:
        self.tasks: list[Task] = []

    # --- Population ---

    def load_from_owner(self, owner: Owner) -> None:
        """Import all tasks from every pet belonging to the given Owner, skipping duplicates."""
        existing_ids = {t.id for t in self.tasks}
        for task in owner.get_all_tasks():
            if task.id not in existing_ids:
                self.tasks.append(task)
                existing_ids.add(task.id)

    def add_task(self, task: Task) -> None:
        """Add a single task to the scheduler."""
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove a task by ID."""
        self.tasks = [t for t in self.tasks if t.id != task_id]

    # --- Retrieval ---

    def get_todays_tasks(self) -> list[Task]:
        """Return all incomplete tasks due today."""
        return [t for t in self.tasks if t.is_due_today() and not t.is_complete]

    def get_tasks_for_pet(self, pet: Pet) -> list[Task]:
        """Return all scheduler tasks that belong to the given pet, matched by task ID."""
        pet_task_ids = {t.id for t in pet.tasks}
        return [t for t in self.tasks if t.id in pet_task_ids]

    # --- Organisation ---

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Return tasks sorted by priority ascending (1 = highest first)."""
        return sorted(tasks, key=lambda t: t.priority)

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return tasks sorted chronologically; priority is the tiebreaker."""
        return sorted(tasks, key=lambda t: (t.due_datetime, t.priority))

    def filter_by_status(self, tasks: list[Task], complete: bool) -> list[Task]:
        """Return only tasks whose is_complete matches the given status."""
        return [t for t in tasks if t.is_complete == complete]

    def filter_by_pet(self, tasks: list[Task], pet_name: str, owner: Owner) -> list[Task]:
        """Return only tasks belonging to the named pet."""
        pet = next((p for p in owner.pets if p.name == pet_name), None)
        if pet is None:
            return []
        pet_ids = {t.id for t in pet.tasks}
        return [t for t in tasks if t.id in pet_ids]

    def detect_conflicts(self, pet: Pet) -> list[tuple[Task, Task]]:
        """Return pairs of tasks for the given pet that share the same due_datetime."""
        pet_tasks = self.get_tasks_for_pet(pet)
        conflicts: list[tuple[Task, Task]] = []

        for i, task_a in enumerate(pet_tasks):
            for task_b in pet_tasks[i + 1:]:
                if task_a.due_datetime == task_b.due_datetime:
                    conflicts.append((task_a, task_b))

        return conflicts

    def generate_recurring_tasks(self) -> None:
        """Append the next occurrence for each completed recurring task not yet scheduled."""
        existing_titles_datetimes = {(t.title, t.due_datetime) for t in self.tasks}
        new_tasks: list[Task] = []

        for task in self.tasks:
            if task.is_complete and task.recurrence != Recurrence.NONE:
                next_task = task.generate_next_occurrence()
                if next_task and (next_task.title, next_task.due_datetime) not in existing_titles_datetimes:
                    new_tasks.append(next_task)
                    existing_titles_datetimes.add((next_task.title, next_task.due_datetime))

        self.tasks.extend(new_tasks)
