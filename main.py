"""
main.py
PawPal+ — Quick test drive of the core logic.
"""

from datetime import datetime, date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler, TaskType, Recurrence


# ---------------------------------------------------------------------------
# Setup: Owner & Pets
# ---------------------------------------------------------------------------

owner = Owner(name="Alex", email="alex@pawpal.com")

buddy = Pet(name="Buddy", species="Dog", breed="Golden Retriever", age=3, weight=30.5)
luna  = Pet(name="Luna",  species="Cat", breed="Siamese",          age=5, weight=4.2)

owner.add_pet(buddy)
owner.add_pet(luna)

# ---------------------------------------------------------------------------
# Tasks — all due today at different times
# ---------------------------------------------------------------------------

today = date.today()

def at(hour: int, minute: int = 0) -> datetime:
    return datetime.combine(today, datetime.min.time().replace(hour=hour, minute=minute))

# Buddy's tasks
buddy.add_task(Task(
    title="Morning walk",
    task_type=TaskType.WALK,
    due_datetime=at(7, 30),
    priority=1,
    recurrence=Recurrence.DAILY,
))

buddy.add_task(Task(
    title="Flea medication",
    task_type=TaskType.MEDICATION,
    due_datetime=at(9, 0),
    priority=2,
    recurrence=Recurrence.MONTHLY,
    notes="Give with food",
))

# Luna's tasks
luna.add_task(Task(
    title="Breakfast feeding",
    task_type=TaskType.FEEDING,
    due_datetime=at(8, 0),
    priority=1,
    recurrence=Recurrence.DAILY,
))

luna.add_task(Task(
    title="Vet appointment",
    task_type=TaskType.APPOINTMENT,
    due_datetime=at(14, 0),
    priority=2,
    notes="Annual checkup — bring vaccination records",
))

# ---------------------------------------------------------------------------
# Scheduler: load all tasks and print today's schedule
# ---------------------------------------------------------------------------

scheduler = Scheduler()
scheduler.load_from_owner(owner)

todays_tasks = scheduler.sort_by_priority(scheduler.get_todays_tasks())

print("=" * 48)
print(f"  PawPal+ — Today's Schedule  ({today})")
print("=" * 48)

if not todays_tasks:
    print("  No tasks scheduled for today.")
else:
    for task in todays_tasks:
        time_str   = task.due_datetime.strftime("%I:%M %p")
        recur_str  = f"  [{task.recurrence.value}]" if task.recurrence != Recurrence.NONE else ""
        notes_str  = f"\n      Note: {task.notes}" if task.notes else ""
        status_str = "[x]" if task.is_complete else "[ ]"

        # Find which pet owns this task
        pet_name = next(
            (p.name for p in owner.pets if any(t.id == task.id for t in p.tasks)),
            "Unknown"
        )

        print(f"\n  {status_str} {time_str}  |  {pet_name}  |  {task.title}")
        print(f"      Type: {task.task_type.value}  |  Priority: {task.priority}{recur_str}{notes_str}")

print("\n" + "=" * 48)
print(f"  {len(todays_tasks)} task(s) scheduled today across {len(owner.pets)} pet(s).")
print("=" * 48)
