# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Add a pet: Owner registers a pet with its info (name, species, age, etc.)
Schedule a task: Owner creates a task for a pet (feeding, walk, medication, vet appointment)
View today's tasks:  System shows all tasks due today, sorted by priority/time

Building Blocks: 
Owner: holds name, email, list of pets. User can add/remove pets, get all tasks
Pet : holds name, species, breed, age, weight. User can add/remove tasks, get tasks by date
Task: holds title, type, due date, priority, recurrence . User can be completed, rescheduled, check if due today
Scheduler:  holds list of tasks. User can sort by priority, detect conflicts, generate recurring tasks


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

I initially used a simpler skeletonthat used plain strings for task type and recurrence. I switched to a more complete version still using AI's feedback and ideas that uses Python dataclasses for Task and Pet, adds TaskType and Recurrence enums, and includes a uuid for unique task IDs. This makes the system more robust and easier to build on in later phases.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler looks at three things: when a task is due (time), how urgent it is (priority), and whether it's already been done (completion status). Time comes first because pet care stuff is time-sensitive — you can't feed a pet "whenever." Priority is the tiebreaker when two tasks land at the same time, so something like a vet appointment wins over a grooming session. Completion status keeps the schedule clean so finished tasks don't clutter the view or trigger false conflict warnings.

**b. Tradeoffs**

The scheduler only flags a conflict when two tasks share the exact same `due_datetime` down to the minute. It doesn't know how long a task takes, so a 30-minute walk at 9:00 AM and a grooming at 9:20 AM won't trigger any warning even though they clearly overlap in real life.

This is fine for now because `Task` doesn't have a duration field, and honestly guessing how long a vet visit takes would probably cause more false alarms than it prevents. The exact-match approach is simple and predictable. If this were a real app, the next step would be adding an optional `duration_minutes` to `Task` and updating the conflict check to compare time windows instead of single timestamps.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
