# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial UML had four classes: `Owner`, `Pet`, `CareTask`, and `DailyScheduler`. `Owner` was responsible for storing personal info and a time budget. `Pet` held profile data like breed, size, and species. `CareTask` represented a single care activity with a type, duration, and priority. `DailyScheduler` was the central class that connected everything, it held a reference to both the owner and pet, maintained the task pool, and was responsible for generating the daily plan.

**b. Design changes**

Yes, the design changed in a few ways. The most significant was that `get_profile()` on `Pet` was originally designed to return a formatted string like `"Buddy, a 3-year-old Golden Retriever."` During implementation I changed it to return a dictionary instead, since a dict is more flexible and easier to work with programmatically, a string is fine for display but harder to use if you want to access individual fields. I also added three methods to `DailyScheduler` that weren't in the original UML: `add_task()`, `check_conflicts()`, and `explain_plan()`. I didn't anticipate needing a separate conflict detection step until I started wiring up the UI and realized the schedule could silently exceed the owner's time budget.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers two main constraints: task priority (a score from 0–10) and the owner's daily time budget in minutes. Priority determines the order tasks appear in the plan, higher priority tasks always come first. The time budget is used for conflict detection, if the total duration of all tasks exceeds what the owner has available, the app warns them. I decided priority mattered most because in pet care, some tasks are genuinely urgent (medication, feeding) and can't be pushed back, while others like grooming are flexible. Time budget is important too but it's more of a soft constraint, the scheduler warns about overages rather than automatically trimming the plan.

**b. Tradeoffs**

The main tradeoff is that the scheduler sorts all tasks by priority but doesn't cut any out if the plan runs over time, it warns you instead of auto-removing low-priority tasks. This means a technically over-budget plan can still be generated. I think this is reasonable for pet care because the owner should decide what to drop, not the app. Automatically removing a task could accidentally cut something important that just happened to have a lower score, like a medication with a priority of 5 that is still non-negotiable.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI throughout the project at different stages. Early on I used it for design feedback, I described the scenario and asked what classes made sense, which helped me think through responsibilities before writing any code. During implementation I used it for debugging, particularly when my tests were failing and I wasn't sure if the bug was in the test or the source code. I also used it to improve the Streamlit UI, asking it to suggest better components for displaying the filtered and sorted data. The most helpful prompts were specific ones — like "why is this test failing, and is the bug in the test or the implementation?" rather than vague ones like "fix my code."

**b. Judgment and verification**

When AI suggested upgrading from `st.table` to `st.dataframe` with `column_config`, I didn't just paste it in, I checked the Streamlit docs to understand what `ProgressColumn` actually does and what the `min_value` / `max_value` parameters control. I wanted to make sure the progress bar would scale to the owner's time budget and not some arbitrary default. I also verified the `hide_index=True` behavior by running the app locally, because the suggestion looked right on paper but I wanted to confirm the index column actually disappeared in the rendered output.

---

## 4. Testing and Verification

**a. What you tested**

I wrote unit tests for all four classes. For `CareTask` I tested `complete()`, `is_high_priority()`, and `get_summary()`. For `Pet` I tested `get_profile()` and `update_health_notes()`. For `Owner` I tested `add_pet()`, `set_available_time()`, and `get_preferences()`. For `DailyScheduler` I tested `add_task()`, `remove_task()`, `generate_plan()`, `get_total_duration()`, and `reset_plan()`. These tests mattered because the scheduler's correctness depends on each method doing exactly what it promises, if `get_total_duration()` is wrong, the conflict detection is wrong, and the UI shows a misleading progress bar.

**b. Confidence**

I'm reasonably confident in the core behaviors — sorting, duration totaling, and conflict detection all pass their tests. The area I'm less confident about is edge cases: what happens if someone adds a task with `duration_minutes=0`, or sets `priority` outside the 0–10 range, or clicks "Save Owner & Pet" multiple times in a row. Those scenarios aren't tested yet. If I had more time I'd test the boundary condition where total duration exactly equals the budget (should not trigger a warning), and I'd add a test for `check_conflicts()` with an empty task list to make sure it doesn't crash.

---

## 5. Reflection

**a. What went well**

I'm most satisfied with the conflict detection system. It started as a single time-budget check and grew into three distinct warnings that each catch a different kind of scheduling problem. I like that they're surfaced in the UI as Streamlit warnings rather than hidden in the console, so the feedback is immediate and actionable. The fact that it's all driven by one method (`check_conflicts()`) on the scheduler class rather than scattered through the UI code also feels clean.

**b. What you would improve**

If I had another iteration I would add recurring tasks — the ability to mark a task as "daily" so it auto-populates the plan every session without being manually re-added. Right now the task list resets whenever the page is refreshed, which is a significant limitation for a real pet care app. I'd also redesign the owner/pet setup to support multiple active pets with separate task pools per pet, rather than one scheduler tied to one pet at a time.

**c. Key takeaway**

The most important thing I learned is that design and implementation are not two separate phases — they're a loop. I thought the UML was done before I started coding, but I ended up adding methods and changing return types once I hit real problems. Starting with a design is still worth it because it forces you to think about responsibilities upfront, but you have to be willing to update it as the code teaches you things the diagram couldn't predict. The same applies to working with AI: it's a starting point, not a final answer.
