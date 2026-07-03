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

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

```
==================================================
TODAY'S SCHEDULE FOR Jordan
==================================================

Biscuit:
  Scheduled 3/3 tasks. Total: 60 min. 
    - Morning walk (30 min)
    - Feeding (10 min)
    - Playtime (20 min)

Whiskers:
  Scheduled 3/3 tasks. Total: 30 min. 
    - Feeding (5 min)
    - Litter box (10 min)
    - Play session (15 min)

==================================================
```



## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with verbose output:
python -m pytest -v

# Run with coverage:
python -m pytest --cov
```

All Tests + What they cover:

There are 24 total tests covering:
- Sorting Correctness — Tasks sorted chronologically by time and priority
- Recurrence Logic — Daily/weekly tasks auto-create next occurrences
- Conflict Detection — Multiple tasks at same time are flagged
- Filtering — Tasks filtered by completion status and pet name
- Validation — Invalid inputs (priority, duration, dates) are rejected
- Duplicate Prevention — Duplicate tasks are prevented appropriately

Sample test output:

```
============================= test session starts ==============================
collected 24 items

tests/test_pawpal.py::test_task_completion PASSED                        [  4%]
tests/test_pawpal.py::test_sort_by_time_chronological_order PASSED       [ 12%]
tests/test_pawpal.py::test_recurring_daily_task_creates_next_occurrence PASSED [ 25%]
tests/test_pawpal.py::test_detect_conflicts_same_time PASSED             [ 37%]
tests/test_pawpal.py::test_filter_by_status_pending PASSED               [ 54%]
tests/test_pawpal.py::test_invalid_priority_raises_error PASSED          [ 66%]
tests/test_pawpal.py::test_duplicate_one_time_task_rejected PASSED       [ 95%]

============================== 24 passed in 0.03s ===============================
```

I would give my confidence level 4 out of 5 stars.  I think that I covered all the core logic and basic functionality, but given more time I may have been able to think of more edge cases that I did not account for here.  If I felt I had exhausted every possible break point, that would make my confidence go up to a 5.

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | _sort_by_priority(), _sort_by_time() | Sorts by priority level (high first) and by scheduled time (earliest first). |
| Filtering | _filter_by_time(), _filter_by_status(), _filter_by_pet() | Removes tasks that exceed available time and filters by completion status and pet name. |
| Conflict handling | detect_conflicts() | Detects when multiple tasks are scheduled at the same time and shows warnings. |
| Recurring tasks | create_next_occurrence(), mark_task_complete() | Daily and weekly tasks automatically create a new instance for the next occurrence. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Open PawPal+ and see the default owner (Jordan) with 480 minutes available per day.
2. Update the owner name and available time, then click "Update Owner".
3. Add a pet by entering its name, selecting species (dog/cat/other), and clicking "Add Pet".
4. Add a second pet to see how the app handles multiple pets.
5. Select a pet from the dropdown in the Task Management section.
6. Create a task with a title, duration (minutes), priority, scheduled time (HH:MM), and recurrence type.
7. For recurring tasks, set a due date in YYYY-MM-DD format.
8. View all tasks in a table with filtering options (show/hide pending or completed).
9. Sort tasks by priority, scheduled time, or duration.
10. Switch to another pet and add different tasks for that pet.
11. Select a pending task and click "Mark Complete" to change its status.
12. Observe that daily/weekly tasks automatically create a new occurrence for the next day/week.
13. Click "Generate Daily Schedule" to create an optimized schedule for all pets.
14. Review any conflict warnings if tasks overlap at the same scheduled time.
15. See each pet's schedule with an explanation of how many tasks fit within available time.
16. Notice tasks are sorted by priority (high to low) and filtered to respect time constraints.
17. Try resetting all pets to start over with a fresh schedule.


Sample CLI Output from running main.py:
```
==================================================
SORT BY TIME (out-of-order → chronological)
==================================================

Biscuit:
  08:00 — Feeding (10 min)
  14:00 — Playtime (20 min)
  16:00 — Grooming (45 min)
  18:00 — Evening walk (30 min)

Whiskers:
  08:30 — Feeding (5 min)
  12:00 — Litter box (10 min)
  15:00 — Afternoon nap (20 min)

==================================================
FILTER BY STATUS
==================================================

Biscuit:
  Pending (3): Evening walk, Playtime, Grooming
  Completed (1): Feeding

Whiskers:
  Pending (2): Afternoon nap, Litter box
  Completed (1): Feeding

==================================================
RECURRING TASKS TEST
==================================================

Initial tasks (3):
  1. Morning walk [daily]
  2. Feeding [daily]
  3. Grooming [once]

--- Marking 'Morning walk' as complete ---
After marking complete (4 total):
  1. ✓ Morning walk [daily]
  2. ○ Feeding [daily]
  3. ○ Grooming [once]
  4. ○ Morning walk [daily]

==================================================
CONFLICT DETECTION TEST
==================================================

Conflicts detected: 2
  ⚠️  CONFLICT at 09:00: Rex, Luna both scheduled for Walk, Feeding
  ⚠️  CONFLICT at 14:00: Rex both scheduled for Playtime, Training

==================================================
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
