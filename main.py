"""
main.py
PawPal+ — Demo: conflict detection (same-pet and cross-pet).
"""

from datetime import datetime, date
from pawpal_system import Owner, Pet, Task, Scheduler, TaskType, Recurrence

today = date.today()

def at(hour: int, minute: int = 0) -> datetime:
    return datetime.combine(today, datetime.min.time().replace(hour=hour, minute=minute))

def section(title: str) -> None:
    print(f"\n{'=' * 56}")
    print(f"  {title}")
    print('=' * 56)

def print_tasks(tasks: list[Task], owner: Owner) -> None:
    if not tasks:
        print("  (none)")
        return
    for t in tasks:
        pet_name = next(
            (p.name for p in owner.pets if any(x.id == t.id for x in p.tasks)), "?"
        )
        recur = f" [{t.recurrence.value}]" if t.recurrence.value != "none" else ""
        print(f"  [ ] {t.due_datetime.strftime('%I:%M %p')}  {pet_name:<8}  P{t.priority}  {t.title}{recur}")

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

owner = Owner(name="Alex", email="alex@pawpal.com")

buddy = Pet(name="Buddy", species="Dog", breed="Golden Retriever", age=3, weight=30.5)
luna  = Pet(name="Luna",  species="Cat", breed="Siamese",          age=5, weight=4.2)

owner.add_pet(buddy)
owner.add_pet(luna)

# Normal tasks at distinct times
buddy.add_task(Task("Morning walk",     TaskType.WALK,        at(7, 30), priority=1, recurrence=Recurrence.DAILY))
luna.add_task( Task("Breakfast feeding",TaskType.FEEDING,     at(8,  0), priority=1, recurrence=Recurrence.DAILY))

# --- Deliberate conflict 1: SAME PET, same time ---
buddy.add_task(Task("Vet appointment",  TaskType.APPOINTMENT, at(10, 0), priority=2))
buddy.add_task(Task("Grooming session", TaskType.GROOMING,    at(10, 0), priority=3))  # clashes with vet

# --- Deliberate conflict 2: CROSS PET, same time (owner can't be in two places) ---
buddy.add_task(Task("Afternoon walk",   TaskType.WALK,        at(14, 0), priority=2, recurrence=Recurrence.DAILY))
luna.add_task( Task("Luna vet checkup", TaskType.APPOINTMENT, at(14, 0), priority=1))  # clashes with Buddy's walk

# Unique task — no conflict
luna.add_task(Task("Evening feeding",   TaskType.FEEDING,     at(18, 0), priority=1, recurrence=Recurrence.DAILY))

scheduler = Scheduler()
scheduler.load_from_owner(owner)

# ---------------------------------------------------------------------------
# Print today's schedule
# ---------------------------------------------------------------------------

section("Today's Schedule")
print_tasks(scheduler.sort_by_time(scheduler.get_todays_tasks()), owner)

# ---------------------------------------------------------------------------
# Conflict detection
# ---------------------------------------------------------------------------

section("Conflict Report")
warnings = scheduler.get_conflict_warnings(owner)

if not warnings:
    print("  No conflicts detected.")
else:
    for w in warnings:
        print(f"  {w}")

print(f"\n  {len(warnings)} conflict(s) found across {len(owner.pets)} pet(s).")
