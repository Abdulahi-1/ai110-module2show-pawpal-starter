# PawPal+ (Module 2 Project)


## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan



## Screenshot

<img width="564" height="719" alt="Screenshot 2026-03-29 at 9 35 22 PM" src="https://github.com/user-attachments/assets/d5325a07-387e-403d-a285-3d0a6190edc1" />



## Features

### Priority-Based Schedule Sorting
Tasks are automatically sorted in descending order by priority score when you click **Generate Schedule**. The algorithm uses Python's stable `sorted()` on the task pool, keyed by `priority` (0–10 scale), so the highest-urgency care — medication, feeding — always leads the plan. Tasks with equal priority preserve their insertion order.

### Conflict Detection
Before generating a plan, the scheduler runs three automated checks and surfaces each issue as a distinct warning in the UI:

| Check | Trigger |
|---|---|
| **Time budget overage** | Total task duration exceeds the owner's available minutes; shows exact overage in minutes |
| **Duplicate task types** | The same task name (e.g. "Feeding") appears more than once in the pool |
| **All tasks completed** | Every task in the pool is already marked done, making a new plan redundant |

If no conflicts are found, a green success banner confirms the plan is clean.

### Priority Filtering
The task list supports live multi-select filtering by priority tier (🟢 Low / 🟡 Medium / 🔴 High). The table updates instantly without regenerating the schedule, letting you inspect any subset of tasks before committing to a plan.

### Time Budget Tracking
A progress bar and three summary metrics (task count, total time, time remaining) update in real time as tasks are added. The bar fills proportionally to the owner's daily minute budget, giving an immediate visual signal when the plan is approaching or over capacity.

### High-Priority Flagging
Each task exposes an `is_high_priority()` method (threshold: priority ≥ 8). This surfaces as a dedicated **High Priority?** column in both the task list and the generated schedule so urgent items are visually distinct without needing to read the raw score.

### Task Management
Owners can add tasks with a title, duration, and priority level, and remove tasks by type. The scheduler maintains a separate task pool and scheduled plan — the plan can be reset and regenerated without losing the original task list.

### Owner & Pet Profiles
Each session stores a named owner with a configurable daily time budget linked to a pet profile (name, breed, size, species, age). All scheduling decisions — conflict thresholds, budget warnings, plan generation — are scoped to this owner/pet pair.

> **Not yet implemented:** Daily recurrence — tasks are currently treated as single one-time entries per session.

---

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
