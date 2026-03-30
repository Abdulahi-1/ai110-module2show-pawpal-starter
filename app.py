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

    # Preserve any tasks already added before this save
    existing_tasks = []
    if st.session_state.scheduler is not None:
        existing_tasks = list(st.session_state.scheduler.tasks)

    new_scheduler = DailyScheduler(owner=owner, pet=pet)
    for task in existing_tasks:
        new_scheduler.add_task(task)

    st.session_state.owner = owner
    st.session_state.scheduler = new_scheduler
    st.success(f"Saved {owner_name} and {pet_name}!")

st.divider()

# ---------------------------------------------------------------------------
# Add tasks
# ---------------------------------------------------------------------------

PRIORITY_MAP = {"low": 3, "medium": 6, "high": 9}
PRIORITY_LABEL = {3: "🟢 Low", 6: "🟡 Medium", 9: "🔴 High"}

st.subheader("Add a Task")

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
            priority=PRIORITY_MAP[priority_label],
        )
        st.session_state.scheduler.add_task(task)
        st.success(f"Added '{task_title}'.")

st.divider()

# ---------------------------------------------------------------------------
# Current task list with filter
# ---------------------------------------------------------------------------

st.subheader("Current Tasks")

scheduler = st.session_state.scheduler

if scheduler and scheduler.tasks:
    # Summary metrics
    total_duration = scheduler.get_total_duration()
    budget = scheduler.owner.available_minutes
    time_left = budget - total_duration

    m1, m2, m3 = st.columns(3)
    m1.metric("Tasks", len(scheduler.tasks))
    m2.metric("Total time", f"{total_duration} min")
    m3.metric("Time remaining", f"{max(time_left, 0)} min", delta=time_left if time_left >= 0 else None, delta_color="normal")

    # Time budget progress bar
    fill = min(total_duration / budget, 1.0)
    st.progress(fill, text=f"Budget used: {total_duration} / {budget} min")

    # Priority filter
    filter_priority = st.multiselect(
        "Filter by priority",
        options=["🟢 Low", "🟡 Medium", "🔴 High"],
        default=["🟢 Low", "🟡 Medium", "🔴 High"],
    )
    label_to_value = {"🟢 Low": 3, "🟡 Medium": 6, "🔴 High": 9}
    allowed = {label_to_value[l] for l in filter_priority}

    filtered = [t for t in scheduler.tasks if t.priority in allowed]

    if filtered:
        st.dataframe(
            [
                {
                    "Task": t.task_type,
                    "Duration (min)": t.duration_minutes,
                    "Priority": PRIORITY_LABEL.get(t.priority, str(t.priority)),
                    "High Priority?": "Yes" if t.is_high_priority() else "No",
                    "Summary": t.get_summary(),
                    "Status": "✅ Done" if t.is_completed else "⏳ Pending",
                }
                for t in filtered
            ],
            column_config={
                "Duration (min)": st.column_config.ProgressColumn(
                    "Duration (min)",
                    min_value=0,
                    max_value=budget,
                    format="%d min",
                ),
                "Priority": st.column_config.TextColumn("Priority", width="small"),
                "High Priority?": st.column_config.TextColumn("High Priority?", width="small"),
                "Status": st.column_config.TextColumn("Status", width="small"),
            },
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No tasks match the selected filter.")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# ---------------------------------------------------------------------------
# Generate schedule
# ---------------------------------------------------------------------------

st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if scheduler is None:
        st.warning("Save an owner and pet first.")
    elif not scheduler.tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        # Conflict detection
        conflicts = scheduler.check_conflicts()
        if conflicts:
            for conflict in conflicts:
                st.warning(conflict)
        else:
            st.success("No conflicts detected.")

        plan = scheduler.generate_plan()
        total = scheduler.get_total_duration()
        budget = scheduler.owner.available_minutes

        # Schedule summary metrics
        s1, s2, s3 = st.columns(3)
        s1.metric("Tasks scheduled", len(plan))
        s2.metric("Total time", f"{total} min")
        s3.metric("Budget", f"{budget} min")

        if total > budget:
            st.error(f"Schedule exceeds time budget by {total - budget} min.")
        else:
            st.success(f"Plan fits within budget — {budget - total} min to spare.")

        st.caption(scheduler.explain_plan())

        st.dataframe(
            [
                {
                    "Order": i + 1,
                    "Task": t.task_type,
                    "Duration (min)": t.duration_minutes,
                    "Priority": PRIORITY_LABEL.get(t.priority, str(t.priority)),
                    "High Priority?": "Yes" if t.is_high_priority() else "No",
                    "Summary": t.get_summary(),
                }
                for i, t in enumerate(plan)
            ],
            column_config={
                "Order": st.column_config.NumberColumn("Order", width="small"),
                "Duration (min)": st.column_config.ProgressColumn(
                    "Duration (min)",
                    min_value=0,
                    max_value=budget,
                    format="%d min",
                ),
                "Priority": st.column_config.TextColumn("Priority", width="small"),
                "High Priority?": st.column_config.TextColumn("High Priority?", width="small"),
            },
            use_container_width=True,
            hide_index=True,
        )
