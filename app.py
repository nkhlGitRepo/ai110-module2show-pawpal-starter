import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler
from datetime import datetime

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")
st.title("🐾 PawPal+ — Pet Care Scheduler")

# Helper functions for UI enhancements
def get_species_emoji(species):
    """Return emoji for pet species."""
    emoji_map = {"dog": "🐕", "cat": "🐱", "other": "🐾"}
    return emoji_map.get(species.lower(), "🐾")

def get_priority_emoji(priority):
    """Return emoji for task priority."""
    emoji_map = {"high": "🔴", "medium": "🟡", "low": "🟢"}
    return emoji_map.get(priority.lower(), "⚪")

def get_status_badge(is_completed):
    """Return status badge with emoji."""
    return "✅ Done" if is_completed else "⏳ Pending"

# Initialize session state
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes_per_day=480)
if "pets" not in st.session_state:
    st.session_state.pets = []

# ==================== SECTION 1: SETUP ====================
with st.expander("📋 Setup", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        owner_name = st.text_input("Owner name:", value=st.session_state.owner.name, key="owner_input")
        available_time = st.number_input(
            "Available time per day (minutes):",
            min_value=60,
            max_value=1440,
            value=st.session_state.owner.available_minutes_per_day,
            key="time_input"
        )
        if st.button("Update Owner"):
            st.session_state.owner = Owner(name=owner_name, available_minutes_per_day=available_time)
            st.success(f"✅ Updated to {owner_name}")

    with col2:
        st.write(f"**Current Owner:** {st.session_state.owner.name}")
        st.write(f"**Available Time:** {st.session_state.owner.available_minutes_per_day} min/day")

st.divider()

# ==================== SECTION 2: PET MANAGEMENT ====================
st.subheader("🐕 Pets")

col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name:", value="Mochi", key="pet_name")
with col2:
    species = st.selectbox("Species:", ["dog", "cat", "other"], format_func=lambda s: f"{get_species_emoji(s)} {s.capitalize()}")
with col3:
    if st.button("Add Pet"):
        try:
            new_pet = Pet(name=pet_name, species=species)
            st.session_state.pets.append(new_pet)
            st.session_state.owner.add_pet(new_pet)
            st.success(f"✅ {pet_name} added!")
            st.rerun()
        except ValueError as e:
            st.error(f"Error: {e}")

if st.session_state.pets:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("**Pets:**")
        for i, pet in enumerate(st.session_state.pets):
            st.caption(f"{i+1}. {get_species_emoji(pet.species)} {pet.get_info()}")
    with col2:
        if st.button("Reset Pets"):
            st.session_state.pets = []
            st.session_state.owner.pets = []
            st.rerun()
else:
    st.info("No pets yet. Add one above.")

st.divider()

# ==================== SECTION 3: TASK MANAGEMENT ====================
st.subheader("✅ Task Management")

if st.session_state.pets:
    # Select pet
    selected_pet_name = st.selectbox("Select pet:", [p.name for p in st.session_state.pets], key="task_pet")
    current_pet = next(p for p in st.session_state.pets if p.name == selected_pet_name)

    # Add task form
    with st.form("task_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            task_title = st.text_input("Task title:")
        with col2:
            duration = st.number_input("Duration (min):", min_value=1, max_value=240, value=30)
        with col3:
            priority = st.selectbox("Priority:", ["low", "medium", "high"], format_func=lambda p: f"{get_priority_emoji(p)} {p.capitalize()}")

        col4, col5, col6 = st.columns(3)
        with col4:
            scheduled_time = st.text_input("Time (HH:MM):", placeholder="e.g., 08:00", value="")
        with col5:
            recurrence = st.selectbox("Recurrence:", ["once", "daily", "weekly"])
        with col6:
            due_date = st.date_input("Due date (for recurring):")

        submitted = st.form_submit_button("Add Task")
        if submitted:
            try:
                # Build task with all options
                task_kwargs = {
                    "title": task_title,
                    "duration_minutes": int(duration),
                    "priority": priority,
                    "scheduled_time": scheduled_time if scheduled_time else None,
                    "recurrence": recurrence,
                }

                # Add due_date for recurring tasks
                if recurrence != "once":
                    task_kwargs["due_date"] = due_date.strftime("%Y-%m-%d")

                task = Task(**task_kwargs)
                current_pet.add_task(task)
                st.success(f"✅ Task '{task_title}' added to {current_pet.name}!")
                st.rerun()
            except ValueError as e:
                st.error(f"Error: {e}")

    # Display tasks with filtering and sorting options
    if current_pet.tasks:
        st.write(f"**Tasks for {current_pet.name}:**")

        # Filtering options
        col1, col2, col3 = st.columns(3)
        with col1:
            show_pending = st.checkbox("Show pending", value=True)
        with col2:
            show_completed = st.checkbox("Show completed", value=True)
        with col3:
            sort_by = st.selectbox("Sort by:", ["priority", "time", "duration"])

        # Filter tasks
        filtered_tasks = []
        if show_pending:
            filtered_tasks.extend(Scheduler._filter_by_status(current_pet.tasks, False))
        if show_completed:
            filtered_tasks.extend(Scheduler._filter_by_status(current_pet.tasks, True))

        # Sort tasks
        if sort_by == "priority":
            sorted_tasks = Scheduler._sort_by_priority(filtered_tasks)
        elif sort_by == "time":
            sorted_tasks = Scheduler._sort_by_time(filtered_tasks)
        else:  # duration
            sorted_tasks = sorted(filtered_tasks, key=lambda t: t.duration_minutes, reverse=True)

        # Display tasks
        task_data = []
        for t in sorted_tasks:
            status = get_status_badge(t.is_completed)
            priority_badge = f"{get_priority_emoji(t.priority)} {t.priority.upper()}"
            recur_info = f"🔄 {t.recurrence}" if t.recurrence != "once" else ""
            task_data.append({
                "Status": status,
                "Title": t.title,
                "Time": t.scheduled_time or "—",
                "Duration": f"{t.duration_minutes} min",
                "Priority": priority_badge,
                "Recurrence": recur_info,
            })

        st.table(task_data)

        # Mark task as complete
        st.write("**Mark task as complete:**")
        pending_tasks = [t for t in current_pet.tasks if not t.is_completed]
        if pending_tasks:
            task_to_complete = st.selectbox("Select task:", [t.title for t in pending_tasks], key="complete_task")
            if st.button("✓ Mark Complete"):
                task_obj = next(t for t in pending_tasks if t.title == task_to_complete)
                current_pet.mark_task_complete(task_obj)
                st.success(f"✅ {task_to_complete} completed!")
                if task_obj.recurrence != "once":
                    st.info(f"📅 Next occurrence created for {task_obj.title}")
                st.rerun()
    else:
        st.info(f"No tasks for {current_pet.name}. Add one above.")
else:
    st.info("Add a pet first to manage tasks.")

st.divider()

# ==================== SECTION 4: SCHEDULE GENERATION ====================
st.subheader("📅 Generate Schedule")

if st.button("🚀 Generate Daily Schedule", use_container_width=True):
    if not st.session_state.pets:
        st.error("❌ Add at least one pet first.")
    elif not any(pet.tasks for pet in st.session_state.pets):
        st.error("❌ Add tasks to at least one pet.")
    else:
        # Check for conflicts
        conflicts = Scheduler.detect_conflicts(st.session_state.owner)
        if conflicts:
            st.warning("⚠️ Scheduling conflicts detected:")
            for conflict in conflicts:
                st.write(conflict)

        # Generate schedules
        st.success("✅ Schedule generated!")

        for pet in st.session_state.pets:
            if pet.tasks:
                schedule = Scheduler.generate(st.session_state.owner, pet)

                with st.container(border=True):
                    st.subheader(f"{get_species_emoji(pet.species)} {pet.name}'s Schedule")
                    st.info(schedule.explanation)

                    if schedule.scheduled_tasks:
                        # Display scheduled tasks
                        schedule_data = []
                        for i, task in enumerate(schedule.scheduled_tasks, 1):
                            priority_badge = f"{get_priority_emoji(task.priority)} {task.priority.upper()}"
                            schedule_data.append({
                                "Order": i,
                                "Time": f"🕐 {task.scheduled_time}" if task.scheduled_time else "—",
                                "Task": task.title,
                                "Duration": f"⏱️ {task.duration_minutes} min",
                                "Priority": priority_badge,
                            })
                        st.table(schedule_data)
                    else:
                        st.warning("No tasks fit in the available time.")
            else:
                st.write(f"*{get_species_emoji(pet.species)} {pet.name}: No tasks to schedule*")

st.divider()

# ==================== FOOTER ====================
st.caption("🎯 **PawPal+ Features:** Task sorting (priority/time) • Filtering (status/pet) • Time constraints • Conflict detection • Recurring tasks with auto-renewal")
