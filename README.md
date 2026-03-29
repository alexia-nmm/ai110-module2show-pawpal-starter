# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

Beyond basic task storage, the `Scheduler` class includes several algorithms that make the schedule actually useful:

**Chronological sorting** — `sort_by_time()` orders tasks by `due_datetime` so the daily view reads like a real agenda. When two tasks land at the same time, priority breaks the tie so the more urgent one appears first.

**Flexible filtering** — `filter_by_status()` separates done tasks from pending ones, and `filter_by_pet()` narrows the view to a single pet. Both return new lists so the original data is never mutated.

**Automatic recurring tasks** — `mark_task_complete()` does more than flip a flag. When a recurring task is completed, it immediately generates the next occurrence using Python's `timedelta` (daily = +1 day, weekly = +7 days, monthly = +1 calendar month) and registers it on both the scheduler and the pet — no manual follow-up needed.

**Conflict detection** — `get_conflict_warnings()` scans all incomplete tasks grouped by timestamp and uses `itertools.combinations` to find every conflicting pair. It catches two types: same-pet conflicts (a pet can't be in two places) and owner-overlap conflicts (the owner can't attend two different pets at the same time). Each conflict surfaces as a plain warning string rather than an exception.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
classDiagram
    class Owner {
        +String name
        +String email
        +List~Pet~ pets
        +add_pet(pet: Pet)
        +remove_pet(pet: Pet)
        +get_all_tasks() List~Task~
    }

    class Pet {
        +String name
        +String species
        +String breed
        +int age
        +float weight
        +List~Task~ tasks
        +add_task(task: Task)
        +remove_task(task: Task)
        +get_tasks_by_date(date: Date) List~Task~
    }

    class Task {
        +String title
        +String type
        +Date due_date
        +String priority
        +String recurrence
        +bool completed
        +complete()
        +reschedule(new_date: Date)
        +is_due_today() bool
    }

    class Scheduler {
        +List~Task~ tasks
        +sort_by_priority() List~Task~
        +detect_conflicts() List~Task~
        +generate_recurring_tasks()
    }

    Owner "1" --> "0..*" Pet : owns
    Pet "1" --> "0..*" Task : has
    Scheduler "1" --> "0..*" Task : manages
