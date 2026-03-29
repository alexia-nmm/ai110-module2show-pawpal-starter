"""
tests/test_pawpal.py
Simple unit tests for PawPal+ core logic.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import datetime
from pawpal_system import Task, Pet, TaskType, Recurrence


def make_task() -> Task:
    """Helper: return a basic task due today."""
    return Task(
        title="Test task",
        task_type=TaskType.FEEDING,
        due_datetime=datetime.now(),
    )


def test_task_completion():
    """Calling complete() should flip is_complete from False to True."""
    task = make_task()
    assert task.is_complete is False, "Task should start incomplete"
    task.complete()
    assert task.is_complete is True, "Task should be complete after calling complete()"


def test_add_task_increases_pet_task_count():
    """Adding a task to a Pet should increase its task list length by 1."""
    pet = Pet(name="Buddy", species="Dog", breed="Lab", age=2, weight=25.0)
    assert len(pet.tasks) == 0, "Pet should start with no tasks"
    pet.add_task(make_task())
    assert len(pet.tasks) == 1, "Pet should have 1 task after add_task()"
