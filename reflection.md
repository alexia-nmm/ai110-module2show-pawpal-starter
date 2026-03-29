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

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
