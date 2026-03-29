"""
main.py
PawPal+ — Demo: sorting, filtering, recurrence, and conflict detection.
"""

from datetime import datetime, date
from pawpal_system import Owner, Pet, Task, Scheduler, TaskType, Recurrence

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

today = date.today()

def at(hour: int, minute: int = 0) -> datetime:
    return datetime.combine(today, datetime.min.time().replace(hour=hour, minute=minute))

def section(title: str) -> None:
    print(f"\n{'=' * 52}")
    print(f"  {title}")
    print('=' * 52)

def print_tasks(tasks: list[Task], owner: Owner) -> None:
    if not tasks:
        print("  (none)")
        return
    for t in tasks:
        pet_name = next(
            (p.name for p in owner.pets if any(x.id == t.id for x in p.tasks)), "?"
        )
        status = "[x]" if t.is_complete else "[ ]"
        recur  = f" [{t.recurrence.value}]" if t.recurrence.value != "none" else ""
        print(f"  {status} {t.due_datetime.strftime('%I:%M %p')}  {pet_name:<8}  "
              f"P{t.priority}  {t.title}{recur}")

# ---------------------------------------------------------------------------
# Setup — tasks added deliberately OUT OF ORDER
# ---------------------------------------------------------------------------

owner = Owner(name="Alex", email="alex@pawpal.com")

buddy = Pet(name="Buddy", species="Dog", breed="Golden Retriever", age=3, weight=30.5)
luna  = Pet(name="Luna",  species="Cat", breed="Siamese",          age=5, weight=4.2)

owner.add_pet(buddy)
owner.add_pet(luna)

# Buddy — added out of order (afternoon before morning)
buddy.add_task(Task("Afternoon walk",   TaskType.WALK,        at(15, 0), priority=2, recurrence=Recurrence.DAILY))
buddy.add_task(Task("Flea medication",  TaskType.MEDICATION,  at(9, 0),  priority=2, recurrence=Recurrence.MONTHLY, notes="Give with food"))
buddy.add_task(Task("Morning walk",     TaskType.WALK,        at(7, 30), priority=1, recurrence=Recurrence.DAILY))

# Luna — added out of order (vet before breakfast)
luna.add_task(Task("Vet appointment",   TaskType.APPOINTMENT, at(14, 0), priority=2, notes="Annual checkup"))
luna.add_task(Task("Breakfast feeding", TaskType.FEEDING,     at(8, 0),  priority=1, recurrence=Recurrence.DAILY))

# Intentional conflict: two Luna tasks at the same time
luna.add_task(Task("Grooming session",  TaskType.GROOMING,    at(14, 0), priority=3))

# ---------------------------------------------------------------------------
# Load scheduler
# ---------------------------------------------------------------------------

scheduler = Scheduler()
scheduler.load_from_owner(owner)
all_tasks = scheduler.get_todays_tasks()

# ---------------------------------------------------------------------------
# 1. Sorted by time (chronological + priority tiebreak)
# ---------------------------------------------------------------------------

section("1. Today's Schedule — sorted by TIME")
print_tasks(scheduler.sort_by_time(all_tasks), owner)

# ---------------------------------------------------------------------------
# 2. Sorted by priority
# ---------------------------------------------------------------------------

section("2. Today's Schedule — sorted by PRIORITY")
print_tasks(scheduler.sort_by_priority(all_tasks), owner)

# ---------------------------------------------------------------------------
# 3. Filter — incomplete only (all tasks start incomplete)
# ---------------------------------------------------------------------------

section("3. Filter — INCOMPLETE tasks only")
incomplete = scheduler.filter_by_status(all_tasks, complete=False)
print_tasks(scheduler.sort_by_time(incomplete), owner)

# ---------------------------------------------------------------------------
# 4. Filter — complete only (mark a couple done first)
# ---------------------------------------------------------------------------

buddy.tasks[2].complete()   # Morning walk → done
luna.tasks[1].complete()    # Breakfast feeding → done

section("4. Filter — COMPLETE tasks only")
complete = scheduler.filter_by_status(all_tasks, complete=True)
print_tasks(scheduler.sort_by_time(complete), owner)

# ---------------------------------------------------------------------------
# 5. Filter by pet name
# ---------------------------------------------------------------------------

section("5. Filter — BUDDY's tasks only")
buddy_tasks = scheduler.filter_by_pet(all_tasks, "Buddy", owner)
print_tasks(scheduler.sort_by_time(buddy_tasks), owner)

section("6. Filter — LUNA's tasks only")
luna_tasks = scheduler.filter_by_pet(all_tasks, "Luna", owner)
print_tasks(scheduler.sort_by_time(luna_tasks), owner)

# ---------------------------------------------------------------------------
# 6. Conflict detection
# ---------------------------------------------------------------------------

section("7. Conflict Detection")
for pet in owner.pets:
    conflicts = scheduler.detect_conflicts(pet)
    if conflicts:
        for a, b in conflicts:
            print(f"  !! {pet.name}: '{a.title}' and '{b.title}' both at "
                  f"{a.due_datetime.strftime('%I:%M %p')}")
    else:
        print(f"  {pet.name}: no conflicts")

# ---------------------------------------------------------------------------
# 7. Recurring task generation
# ---------------------------------------------------------------------------

section("8. Recurring Task Generation")
before = len(scheduler.tasks)
scheduler.generate_recurring_tasks()
after  = len(scheduler.tasks)
new_count = after - before
print(f"  {new_count} new occurrence(s) generated from completed recurring tasks.")
for t in scheduler.tasks[before:]:
    print(f"    >> '{t.title}' rescheduled for {t.due_datetime.strftime('%Y-%m-%d %I:%M %p')}")

print()
