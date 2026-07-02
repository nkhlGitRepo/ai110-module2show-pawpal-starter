import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs")

# Initialize owner once
if "owner" not in st.session_state:
    owner_name = st.text_input("Owner name", value="Jordan")
    st.session_state.owner = Owner(name=owner_name, available_minutes_per_day=480)
else:
    st.write(f"**Owner:** {st.session_state.owner.name}")

# Initialize pets list
if "pets" not in st.session_state:
    st.session_state.pets = []

# Pet creation
st.markdown("### Pets")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

col1, col2 = st.columns(2)
with col1:
    if st.button("Add Pet"):
        try:
            new_pet = Pet(name=pet_name, species=species)
            st.session_state.pets.append(new_pet)
            st.success(f"✅ {pet_name} added!")
        except ValueError as e:
            st.error(f"Error: {e}")

with col2:
    if st.button("Reset All"):
        st.session_state.pets = []
        st.rerun()

if st.session_state.pets:
    st.write("**Current pets:**")
    for i, pet in enumerate(st.session_state.pets):
        st.caption(f"{i+1}. {pet.get_info()}")

st.markdown("### Tasks")
st.caption("Add tasks to generate a schedule.")

if st.session_state.pets:
    selected_pet = st.selectbox("Select pet:", [p.name for p in st.session_state.pets])
    pet_index = [p.name for p in st.session_state.pets].index(selected_pet)
    current_pet = st.session_state.pets[pet_index]

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task"):
        try:
            task = Task(title=task_title, duration_minutes=int(duration), priority=priority)
            current_pet.add_task(task)
            st.success(f"Task '{task_title}' added to {current_pet.name}!")
        except ValueError as e:
            st.error(f"Error: {e}")

    if current_pet.tasks:
        st.write(f"**Tasks for {current_pet.name}:**")
        task_data = [
            {"Title": t.title, "Duration (min)": t.duration_minutes, "Priority": t.priority}
            for t in current_pet.tasks
        ]
        st.table(task_data)
    else:
        st.info("No tasks yet.")
else:
    st.info("Add a pet first.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate an optimized daily schedule based on priorities and available time.")

if st.button("Generate schedule"):
    if "owner" not in st.session_state or not st.session_state.pets:
        st.error("Please create an owner and at least one pet first.")
    else:
        has_tasks = any(pet.tasks for pet in st.session_state.pets)
        if not has_tasks:
            st.error("Please add at least one task before generating a schedule.")
        else:
            try:
                st.success("✅ Schedule generated!")
                for pet in st.session_state.pets:
                    if pet.tasks:
                        schedule = Scheduler.generate(st.session_state.owner, pet)
                        st.subheader(f"📌 {pet.name}'s Schedule")
                        st.info(schedule.explanation)
                        if schedule.scheduled_tasks:
                            for i, task in enumerate(schedule.scheduled_tasks, 1):
                                status = "✓" if task.is_completed else "○"
                                st.write(f"{i}. {status} **{task.title}** ({task.duration_minutes} min) [{task.priority}]")
                        else:
                            st.write("No tasks fit in the available time.")
                    else:
                        st.write(f"*{pet.name}: No tasks added*")
            except Exception as e:
                st.error(f"Error: {e}")
