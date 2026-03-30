import streamlit as st
from pawpal_system import Owner, Pet, CareTask, DailyScheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# ---------------------------------------------------------------------------
# Session state — initialise objects once per session
# ---------------------------------------------------------------------------

if "owner" not in st.session_state:
    st.session_state.owner = None

if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

# ---------------------------------------------------------------------------
# Owner + Pet setup
# ---------------------------------------------------------------------------

st.subheader("Owner & Pet Info")

owner_name = st.text_input("Owner name", value="Jordan")
available_minutes = st.number_input("Time available today (minutes)", min_value=10, max_value=480, value=120)

pet_name = st.text_input("Pet name", value="Mochi")
breed = st.text_input("Breed", value="Mixed")
size = st.selectbox("Size", ["small", "medium", "large"])
species = st.selectbox("Species", ["dog", "cat", "other"])
age = st.number_input("Age (years)", min_value=0, max_value=30, value=2)

if st.button("Save Owner & Pet"):
    pet = Pet(name=pet_name, breed=breed, size=size, species=species, age_years=age)
    owner = Owner(name=owner_name, email="", available_minutes=int(available_minutes))
    owner.add_pet(pet)
    st.session_state.owner = owner
    st.session_state.scheduler = DailyScheduler(owner=owner, pet=pet)
    st.success(f"Saved {owner_name} and {pet_name}!")

st.divider()

# ---------------------------------------------------------------------------
# Add tasks
# ---------------------------------------------------------------------------

st.subheader("Tasks")

priority_map = {"low": 3, "medium": 6, "high": 9}

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority_label = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    if st.session_state.scheduler is None:
        st.warning("Save an owner and pet first.")
    else:
        task = CareTask(
            task_type=task_title,
            duration_minutes=int(duration),
            priority=priority_map[priority_label],
        )
        st.session_state.scheduler.add_task(task)
        st.success(f"Added '{task_title}'.")

if st.session_state.scheduler and st.session_state.scheduler.tasks:
    st.write("Current tasks:")
    st.table([
        {
            "Task": t.task_type,
            "Duration (min)": t.duration_minutes,
            "Priority": t.priority,
            "Summary": t.get_summary(),
        }
        for t in st.session_state.scheduler.tasks
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# ---------------------------------------------------------------------------
# Generate schedule
# ---------------------------------------------------------------------------

st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if st.session_state.scheduler is None:
        st.warning("Save an owner and pet first.")
    elif not st.session_state.scheduler.tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        for conflict in st.session_state.scheduler.check_conflicts():
            st.warning(conflict)
        plan = st.session_state.scheduler.generate_plan()
        total = st.session_state.scheduler.get_total_duration()
        st.success(f"Plan generated — {total} min total.")
        st.write("Today's schedule:")
        st.table([
            {
                "Task": t.task_type,
                "Duration (min)": t.duration_minutes,
                "Priority": t.priority,
                "Summary": t.get_summary(),
            }
            for t in plan
        ])
