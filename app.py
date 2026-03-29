import streamlit as st
from datetime import datetime, date
from pawpal_system import Owner, Pet, Task, Scheduler, TaskType, Recurrence

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ---------------------------------------------------------------------------
# Session state — initialise once, persist across reruns
# ---------------------------------------------------------------------------
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="", email="")

owner: Owner = st.session_state.owner

# ---------------------------------------------------------------------------
# Section 1 — Owner setup
# ---------------------------------------------------------------------------
st.subheader("Owner")
col1, col2 = st.columns(2)
with col1:
    name_input = st.text_input("Name", value=owner.name or "Jordan")
with col2:
    email_input = st.text_input("Email", value=owner.email or "jordan@example.com")

if name_input:
    owner.name = name_input
if email_input:
    owner.email = email_input

# ---------------------------------------------------------------------------
# Section 2 — Add a Pet  →  owner.add_pet(Pet(...))
# ---------------------------------------------------------------------------
st.divider()
st.subheader("Add a Pet")

col1, col2, col3 = st.columns(3)
with col1:
    pet_name    = st.text_input("Pet name", value="Mochi")
with col2:
    species     = st.selectbox("Species", ["dog", "cat", "bird", "other"])
with col3:
    breed       = st.text_input("Breed", value="Mixed")

col4, col5 = st.columns(2)
with col4:
    age    = st.number_input("Age (years)", min_value=0, max_value=30, value=2)
with col5:
    weight = st.number_input("Weight (kg)", min_value=0.1, max_value=200.0, value=5.0)

if st.button("Add pet"):
    # Guard: don't add a duplicate name
    existing_names = [p.name for p in owner.pets]
    if pet_name in existing_names:
        st.warning(f"'{pet_name}' is already registered.")
    else:
        new_pet = Pet(name=pet_name, species=species, breed=breed,
                      age=int(age), weight=float(weight))
        owner.add_pet(new_pet)          # <-- Owner.add_pet() called here
        st.success(f"Added {pet_name} to {owner.name}'s profile.")

if owner.pets:
    st.markdown(f"**{owner.name}'s pets:** " +
                ", ".join(f"{p.name} ({p.species})" for p in owner.pets))
else:
    st.info("No pets yet — add one above.")

# ---------------------------------------------------------------------------
# Section 3 — Add a Task to a Pet  →  pet.add_task(Task(...))
# ---------------------------------------------------------------------------
st.divider()
st.subheader("Add a Task")

if not owner.pets:
    st.info("Add a pet first before scheduling tasks.")
else:
    pet_names    = [p.name for p in owner.pets]
    selected_pet = st.selectbox("Assign to pet", pet_names)

    col1, col2 = st.columns(2)
    with col1:
        task_title   = st.text_input("Task title", value="Morning walk")
        task_type    = st.selectbox("Type", [t.value for t in TaskType])
        priority     = st.number_input("Priority (1 = highest)", min_value=1, max_value=5, value=1)
    with col2:
        task_date    = st.date_input("Due date", value=date.today())
        task_time    = st.time_input("Due time", value=datetime.now().time().replace(second=0, microsecond=0))
        recurrence   = st.selectbox("Recurrence", [r.value for r in Recurrence])
    notes = st.text_input("Notes (optional)", value="")

    if st.button("Add task"):
        due_dt  = datetime.combine(task_date, task_time)
        pet_obj = next(p for p in owner.pets if p.name == selected_pet)
        new_task = Task(
            title        = task_title,
            task_type    = TaskType(task_type),
            due_datetime = due_dt,
            priority     = int(priority),
            recurrence   = Recurrence(recurrence),
            notes        = notes,
        )
        pet_obj.add_task(new_task)      # <-- Pet.add_task() called here
        st.success(f"Task '{task_title}' added to {selected_pet}.")

    # Show all tasks for the selected pet
    pet_obj    = next(p for p in owner.pets if p.name == selected_pet)
    pet_tasks  = pet_obj.get_tasks()
    if pet_tasks:
        st.markdown(f"**{selected_pet}'s tasks ({len(pet_tasks)}):**")
        st.table([
            {
                "Title":      t.title,
                "Type":       t.task_type.value,
                "Due":        t.due_datetime.strftime("%Y-%m-%d %H:%M"),
                "Priority":   t.priority,
                "Recurrence": t.recurrence.value,
                "Done":       "✓" if t.is_complete else "—",
            }
            for t in pet_tasks
        ])
    else:
        st.info(f"No tasks for {selected_pet} yet.")

# ---------------------------------------------------------------------------
# Section 4 — Generate Schedule  →  Scheduler.load_from_owner() + sort
# ---------------------------------------------------------------------------
st.divider()
st.subheader("Today's Schedule")

if st.button("Generate schedule"):
    if not owner.pets:
        st.warning("Add a pet and some tasks first.")
    else:
        scheduler = Scheduler()
        scheduler.load_from_owner(owner)        # <-- pulls tasks from all pets
        todays = scheduler.sort_by_priority(scheduler.get_todays_tasks())

        if not todays:
            st.info("No tasks due today.")
        else:
            st.success(f"{len(todays)} task(s) scheduled for today.")
            st.table([
                {
                    "Time":     t.due_datetime.strftime("%I:%M %p"),
                    "Pet":      next((p.name for p in owner.pets
                                     if any(x.id == t.id for x in p.tasks)), "?"),
                    "Task":     t.title,
                    "Type":     t.task_type.value,
                    "Priority": t.priority,
                    "Recurs":   t.recurrence.value,
                }
                for t in todays
            ])
