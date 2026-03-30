import pytest
from pawpal_system import Pet, CareTask, Owner, DailyScheduler


# --- Pet ---

def test_pet_get_profile():
    "tests the get_profile method of the Pet class"
    pet = Pet(name="Buddy", breed="Golden Retriever", size="Large", species="Dog", age_years=3)
    assert pet.get_profile() == {
        "name": "Buddy",
        "breed": "Golden Retriever",
        "size": "Large",
        "species": "Dog",
        "age_years": 3,
        "health_notes": ""
    }

def test_pet_update_health_notes():
    "tests the update_health_notes method of the Pet class"
    pet = Pet(name="Buddy", breed="Golden Retriever", size="Large", species="Dog", age_years=3)
    pet.update_health_notes("Healthy")
    assert pet.health_notes == "Healthy"


# --- CareTask ---

def test_care_task_complete():
    "tests the complete method of the CareTask class"
    task = CareTask(task_type="Feeding", duration_minutes=10, priority=5)
    task.complete()
    assert task.is_completed == True

def test_care_task_is_high_priority():
    "tests the is_high_priority method of the CareTask class"
    task = CareTask(task_type="Feeding", duration_minutes=10, priority=5)
    assert task.is_high_priority() == False

    task2 = CareTask(task_type="Grooming", duration_minutes=20, priority=8)
    assert task2.is_high_priority() == True

def test_care_task_get_summary():
    "tests the get_summary method of the CareTask class"
    task = CareTask(task_type="Feeding", duration_minutes=10, priority=5)
    assert task.get_summary() == "Feeding - 10 mins - Priority: 5"


# --- Owner ---

def test_owner_add_pet():
    "tests the add_pet method of the Owner class"
    owner = Owner(name="Alice", email="alice@example.com", available_minutes=120)
    pet = Pet(name="Buddy", breed="Golden Retriever", size="Large", species="Dog", age_years=3)
    owner.add_pet(pet)
    assert len(owner.pets) == 1

def test_owner_set_available_time():
    "tests the set_available_time method of the Owner class"
    owner = Owner(name="Alice", email="alice@example.com", available_minutes=120)
    owner.set_available_time(180)
    assert owner.available_minutes == 180

def test_owner_get_preferences():
    "tests the get_preferences method of the Owner class"
    owner = Owner(name="Alice", email="alice@example.com", available_minutes=120)
    assert owner.get_preferences() == []


# --- DailyScheduler ---

def test_scheduler_add_task():
    "tests the add_task method of the DailyScheduler class"
    owner = Owner(name="Alice", email="alice@example.com", available_minutes=120)
    pet = Pet(name="Buddy", breed="Golden Retriever", size="Large", species="Dog", age_years=3)
    pawpal_system = DailyScheduler(owner=owner, pet=pet)
    task = CareTask(task_type="Feeding", duration_minutes=10, priority=5)
    pawpal_system.add_task(task)
    assert len(pawpal_system.tasks) == 1

def test_scheduler_remove_task():
    "tests the remove_task method of the DailyScheduler class"
    owner = Owner(name="Alice", email="alice@example.com", available_minutes=120)
    pet = Pet(name="Buddy", breed="Golden Retriever", size="Large", species="Dog", age_years=3)
    pawpal_system = DailyScheduler(owner=owner, pet=pet)
    task = CareTask(task_type="Feeding", duration_minutes=10, priority=5)
    pawpal_system.add_task(task)
    pawpal_system.remove_task("Feeding")
    assert len(pawpal_system.tasks) == 0

def test_scheduler_generate_plan():
    "tests the generate_plan method of the DailyScheduler class"
    owner = Owner(name="Alice", email="alice@example.com", available_minutes=120)
    pet = Pet(name="Buddy", breed="Golden Retriever", size="Large", species="Dog", age_years=3)
    pawpal_system = DailyScheduler(owner=owner, pet=pet)
    task = CareTask(task_type="Feeding", duration_minutes=10, priority=5)
    pawpal_system.add_task(task)
    plan = pawpal_system.generate_plan()
    assert len(plan) == 1

def test_scheduler_get_total_duration():
    "tests the get_total_duration method of the DailyScheduler class"
    owner = Owner(name="Alice", email="alice@example.com", available_minutes=120)
    pet = Pet(name="Buddy", breed="Golden Retriever", size="Large", species="Dog", age_years=3)
    pawpal_system = DailyScheduler(owner=owner, pet=pet)
    task = CareTask(task_type="Feeding", duration_minutes=10, priority=5)
    pawpal_system.add_task(task)
    assert pawpal_system.get_total_duration() == 10

def test_scheduler_reset_plan():
    "tests the reset_plan method of the DailyScheduler class"
    owner = Owner(name="Alice", email="alice@example.com", available_minutes=120)
    pet = Pet(name="Buddy", breed="Golden Retriever", size="Large", species="Dog", age_years=3)
    pawpal_system = DailyScheduler(owner=owner, pet=pet)
    task = CareTask(task_type="Feeding", duration_minutes=10, priority=5)
    pawpal_system.add_task(task)
    pawpal_system.reset_plan()
    assert len(pawpal_system.scheduled_plan) == 0
