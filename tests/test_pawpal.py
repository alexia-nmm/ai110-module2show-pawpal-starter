"""
tests/test_pawpal.py
Automated test suite for PawPal+ core logic.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import datetime, date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler, TaskType, Recurrence


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def make_task(title="Test task", hour=9, minute=0,
              recurrence=Recurrence.NONE, priority=1,
              on_date=None) -> Task:
    """Return a task due today at the given hour/minute (defaults: 09:00, no recurrence)."""
    target = on_date or date.today()
    return Task(
        title=title,
        task_type=TaskType.FEEDING,
        due_datetime=datetime.combine(target, datetime.min.time().replace(hour=hour, minute=minute)),
        priority=priority,
        recurrence=recurrence,
    )

def make_pet(name="Buddy") -> Pet:
    """Return a basic dog Pet with no tasks."""
    return Pet(name=name, species="Dog", breed="Lab", age=2, weight=25.0)

def make_owner(*pets) -> Owner:
    """Return an Owner with the given pets already registered."""
    owner = Owner(name="Alex", email="alex@test.com")
    for pet in pets:
        owner.add_pet(pet)
    return owner


# ---------------------------------------------------------------------------
# Existing tests (kept from Phase 2)
# ---------------------------------------------------------------------------

def test_task_completion():
    """Calling complete() should flip is_complete from False to True."""
    task = make_task()
    assert task.is_complete is False
    task.complete()
    assert task.is_complete is True


def test_add_task_increases_pet_task_count():
    """Adding a task to a Pet should increase its task list length by 1."""
    pet = make_pet()
    assert len(pet.tasks) == 0
    pet.add_task(make_task())
    assert len(pet.tasks) == 1


# ---------------------------------------------------------------------------
# Sorting correctness
# ---------------------------------------------------------------------------

def test_sort_by_time_returns_chronological_order():
    """Tasks added out of order should come back sorted earliest-first."""
    scheduler = Scheduler()
    t1 = make_task("Walk",    hour=7)
    t2 = make_task("Feed",    hour=12)
    t3 = make_task("Meds",    hour=9)

    # Add deliberately out of order
    scheduler.add_task(t2)
    scheduler.add_task(t3)
    scheduler.add_task(t1)

    result = scheduler.sort_by_time(scheduler.tasks)
    assert [t.title for t in result] == ["Walk", "Meds", "Feed"]


def test_sort_by_time_uses_priority_as_tiebreaker():
    """When two tasks share the same time, the lower priority number comes first."""
    scheduler = Scheduler()
    t_low  = make_task("Grooming",    hour=10, priority=3)
    t_high = make_task("Vet visit",   hour=10, priority=1)

    scheduler.add_task(t_low)
    scheduler.add_task(t_high)

    result = scheduler.sort_by_time(scheduler.tasks)
    assert result[0].title == "Vet visit"
    assert result[1].title == "Grooming"


def test_sort_by_time_empty_list():
    """Sorting an empty list should return an empty list without error."""
    scheduler = Scheduler()
    assert scheduler.sort_by_time([]) == []


def test_sort_by_priority_orders_lowest_number_first():
    """sort_by_priority should put P1 before P2 before P3."""
    scheduler = Scheduler()
    t1 = make_task("Low",    priority=3)
    t2 = make_task("High",   priority=1)
    t3 = make_task("Medium", priority=2)

    scheduler.add_task(t1)
    scheduler.add_task(t2)
    scheduler.add_task(t3)

    result = scheduler.sort_by_priority(scheduler.tasks)
    assert [t.priority for t in result] == [1, 2, 3]


# ---------------------------------------------------------------------------
# Recurrence logic
# ---------------------------------------------------------------------------

def test_daily_recurrence_creates_next_day_task():
    """Completing a daily task should auto-create one due exactly 1 day later."""
    pet = make_pet()
    task = make_task("Morning walk", recurrence=Recurrence.DAILY)
    pet.add_task(task)

    scheduler = Scheduler()
    scheduler.add_task(task)
    next_task = scheduler.mark_task_complete(task.id, pet)

    assert next_task is not None
    assert next_task.due_datetime.date() == task.due_datetime.date() + timedelta(days=1)


def test_weekly_recurrence_creates_next_week_task():
    """Completing a weekly task should auto-create one due exactly 7 days later."""
    pet = make_pet()
    task = make_task("Flea meds", recurrence=Recurrence.WEEKLY)
    pet.add_task(task)

    scheduler = Scheduler()
    scheduler.add_task(task)
    next_task = scheduler.mark_task_complete(task.id, pet)

    assert next_task is not None
    assert next_task.due_datetime.date() == task.due_datetime.date() + timedelta(weeks=1)


def test_non_recurring_task_returns_none():
    """Completing a non-recurring task should return None — no new task created."""
    pet = make_pet()
    task = make_task("Vet checkup", recurrence=Recurrence.NONE)
    pet.add_task(task)

    scheduler = Scheduler()
    scheduler.add_task(task)
    next_task = scheduler.mark_task_complete(task.id, pet)

    assert next_task is None


def test_recurring_next_task_added_to_pet():
    """The auto-generated next task should appear on the pet's own task list."""
    pet = make_pet()
    task = make_task("Feed", recurrence=Recurrence.DAILY)
    pet.add_task(task)

    scheduler = Scheduler()
    scheduler.add_task(task)
    next_task = scheduler.mark_task_complete(task.id, pet)

    assert next_task in pet.tasks


def test_mark_task_complete_unknown_id_returns_none():
    """Passing a non-existent task ID should return None without crashing."""
    scheduler = Scheduler()
    pet = make_pet()
    result = scheduler.mark_task_complete("does-not-exist", pet)
    assert result is None


# ---------------------------------------------------------------------------
# Conflict detection
# ---------------------------------------------------------------------------

def test_no_conflict_when_tasks_at_different_times():
    """Tasks at different times should produce no warnings."""
    pet = make_pet()
    pet.add_task(make_task("Walk", hour=8))
    pet.add_task(make_task("Feed", hour=12))
    owner = make_owner(pet)

    scheduler = Scheduler()
    scheduler.load_from_owner(owner)

    assert scheduler.get_conflict_warnings(owner) == []


def test_same_pet_conflict_detected():
    """Two tasks for the same pet at the same time should produce a warning."""
    pet = make_pet()
    pet.add_task(make_task("Vet",      hour=10))
    pet.add_task(make_task("Grooming", hour=10))
    owner = make_owner(pet)

    scheduler = Scheduler()
    scheduler.load_from_owner(owner)

    warnings = scheduler.get_conflict_warnings(owner)
    assert len(warnings) == 1
    assert "Buddy" in warnings[0]


def test_cross_pet_conflict_detected():
    """Tasks for different pets at the same time should flag an owner overlap."""
    buddy = make_pet("Buddy")
    luna  = make_pet("Luna")
    buddy.add_task(make_task("Walk",  hour=14))
    luna.add_task( make_task("Vet",   hour=14))
    owner = make_owner(buddy, luna)

    scheduler = Scheduler()
    scheduler.load_from_owner(owner)

    warnings = scheduler.get_conflict_warnings(owner)
    assert len(warnings) == 1
    assert "owner overlap" in warnings[0]


def test_completed_tasks_excluded_from_conflict_check():
    """A completed task should not be counted as a conflict even if times match."""
    pet = make_pet()
    done = make_task("Done task", hour=10)
    done.complete()
    pending = make_task("Pending task", hour=10)
    pet.add_task(done)
    pet.add_task(pending)
    owner = make_owner(pet)

    scheduler = Scheduler()
    scheduler.load_from_owner(owner)

    assert scheduler.get_conflict_warnings(owner) == []


def test_owner_with_no_pets_returns_no_warnings():
    """An owner with no pets should return an empty conflict list without error."""
    owner = Owner(name="Empty", email="empty@test.com")
    scheduler = Scheduler()
    assert scheduler.get_conflict_warnings(owner) == []


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------

def test_filter_by_status_incomplete():
    """filter_by_status(False) should exclude completed tasks."""
    scheduler = Scheduler()
    done    = make_task("Done")
    pending = make_task("Pending")
    done.complete()
    scheduler.add_task(done)
    scheduler.add_task(pending)

    result = scheduler.filter_by_status(scheduler.tasks, complete=False)
    assert len(result) == 1
    assert result[0].title == "Pending"


def test_filter_by_pet_returns_correct_tasks():
    """filter_by_pet should return only the named pet's tasks."""
    buddy = make_pet("Buddy")
    luna  = make_pet("Luna")
    buddy_task = make_task("Buddy walk")
    luna_task  = make_task("Luna feed")
    buddy.add_task(buddy_task)
    luna.add_task(luna_task)
    owner = make_owner(buddy, luna)

    scheduler = Scheduler()
    scheduler.load_from_owner(owner)

    result = scheduler.filter_by_pet(scheduler.tasks, "Buddy", owner)
    assert len(result) == 1
    assert result[0].title == "Buddy walk"


def test_filter_by_pet_unknown_name_returns_empty():
    """filter_by_pet with a name that doesn't exist should return an empty list."""
    pet = make_pet("Buddy")
    owner = make_owner(pet)
    scheduler = Scheduler()

    result = scheduler.filter_by_pet([], "Ghost", owner)
    assert result == []


def test_load_from_owner_does_not_duplicate_tasks():
    """Calling load_from_owner twice should not add the same tasks twice."""
    pet = make_pet()
    pet.add_task(make_task("Walk"))
    owner = make_owner(pet)

    scheduler = Scheduler()
    scheduler.load_from_owner(owner)
    scheduler.load_from_owner(owner)   # second load — should be a no-op

    assert len(scheduler.tasks) == 1
