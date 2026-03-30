# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The basic idea was pretty straightforward. An owner registers their pets, each pet gets a list of tasks, and the app shows what needs to get done today. I broke it into four classes to keep things organized.

Owner holds the owner's name, email, and list of pets. You can add or remove pets and grab all tasks at once.
Pet holds the pet's info like name, species, breed, age, and weight. It has its own task list and you can filter tasks by date.
Task holds everything about a single care activity: the title, type, due date, priority, recurrence, and whether it's been done.
Scheduler is the brain. It loads all tasks from the owner's pets and handles sorting, filtering, conflict detection, and recurring task generation.

**b. Design changes**

Yes, the design changed a lot once I actually started building. I started with a really bare bones skeleton that used plain strings for things like task type and recurrence. That felt fine at first but got messy fast. I switched over to using Python dataclasses for Task and Pet, added proper enums for TaskType and Recurrence, and gave every task a unique ID using uuid. The enums especially made a big difference because they prevent typos and make the code way easier to read. The uuid thing also turned out to be super important later when I needed to match tasks across the scheduler and pet lists without things getting mixed up.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler looks at three things: when a task is due (time), how urgent it is (priority), and whether it's already been done (completion status). Time comes first because pet care stuff is time-sensitive. You can't feed a pet "whenever." Priority is the tiebreaker when two tasks land at the same time, so something like a vet appointment wins over a grooming session. Completion status keeps the schedule clean so finished tasks don't clutter the view or trigger false conflict warnings.

**b. Tradeoffs**

The scheduler only flags a conflict when two tasks share the exact same `due_datetime` down to the minute. It doesn't know how long a task takes, so a 30-minute walk at 9:00 AM and a grooming at 9:20 AM won't trigger any warning even though they clearly overlap in real life.

This is fine for now because `Task` doesn't have a duration field, and honestly guessing how long a vet visit takes would probably cause more false alarms than it prevents. The exact match approach is simple and predictable. If this were a real app, the next step would be adding an optional `duration_minutes` to `Task` and updating the conflict check to compare time windows instead of single timestamps.

---

## 3. AI Collaboration

**a. How you used AI**

AI helped me throughout the whole project. In the beginning it helped me think through the class structure and turn my rough ideas into a proper UML diagram. Once I had the skeleton set up, I used it to help implement the actual logic for things like recurring tasks and conflict detection. It was also really useful for writing docstrings and cleaning up code that worked but wasn't super readable.

The prompts that worked best were pretty specific ones. Like asking "how should the Scheduler talk to the Owner to get pet data" or "what edge cases should I test for conflict detection." Vague questions got vague answers, but when I gave it context it gave me stuff I could actually use.

**b. Judgment and verification**

One moment that stood out was when the AI suggested using a manual nested loop with a `frozenset` to deduplicate conflict pairs. It worked, but it was kind of hard to follow. I looked into it and found that `itertools.combinations` already handles unique pairs by design, so I could replace like 10 lines with 2 and it was actually more readable. I ran the tests to confirm the output was identical before keeping the change. That felt like a good example of using AI as a starting point but still thinking through whether the suggestion was actually the best fit.

---

## 4. Testing and Verification

**a. What you tested**

I wrote 20 tests covering four main areas. For sorting I checked that tasks added out of order come back in the right sequence, and that priority works as a tiebreaker when two tasks share the same time. For recurrence I verified that completing a daily task creates a new one the next day, weekly adds seven days, and non-recurring tasks just return None without creating anything extra. For conflict detection I tested the happy path where different times produce no warnings, same-pet clashes, cross-pet owner overlap, and made sure completed tasks don't get flagged. I also tested filtering by status, filtering by pet name, and that loading the same owner twice doesn't create duplicate tasks.

These tests mattered because the whole point of the app is that the schedule is trustworthy. If sorting is wrong or conflicts are missed, the owner can't rely on what they're seeing.

**b. Confidence**

Pretty confident in the core logic, around 4 out of 5. All 20 tests pass and the edge cases are covered for the main features. The areas I'm less sure about are monthly recurrence near month-end boundaries (like what happens with January 31), the Streamlit UI behavior since that's not tested automatically, and the batch recurring task generation which I didn't write separate tests for. Those would be my next targets if I kept working on this.

---

## 5. Reflection

**a. What went well**

The thing I'm most happy with is how the Scheduler turned out. It started as just a class that sorted tasks and by the end it had over a dozen methods that all work together. The conflict detection especially felt satisfying because it handles two different types of conflicts and still manages to be pretty short code once I switched to `combinations`. The fact that everything is tested and all 20 pass makes it feel solid.

**b. What you would improve**

If I had more time I'd add a `duration_minutes` field to Task so conflict detection could catch overlapping windows instead of just exact time matches. I'd also clean up the Streamlit UI a bit, right now it works but it's a little cluttered. Adding the ability to remove a task from the UI would also be useful since right now you can only add them. And I'd write tests for the monthly recurrence edge cases just to be safe.

**c. Key takeaway**

The biggest thing I learned is that AI is most useful when you already have some idea of what you're trying to do. When I just asked it to "build the scheduler" I got generic code. When I asked it specific questions like "how do I detect conflicts across pets without duplicating pairs" I got something actually useful that I could read, test, and decide whether to keep. The judgment part is on you, the AI just gives you options.
