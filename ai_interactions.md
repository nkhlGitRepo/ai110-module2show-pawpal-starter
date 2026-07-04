# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

1. Can you add a third algorithmic capability that goes beyond what has already been implemented? Give me a list of suggestions of what a new capability should be.

2. Create a basic implementation of a method that suggests optimal time slots.

3. Add the test to main.py in its own section before running it.

4. Create tests for the new feature that comprehensively ensure the logic is sould in test_pawpal.py

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

Based on the first prompt listed above:

1. Agent displayed a list of suggestions: Suggest optimal time slots, Schedule efficiency score, Task load balancing, Intelligent taks suggestion

Based on the second prompt:

2. Edited pawpal.py by adding a new method "suggested_time_slots" that takes an owner, pet, and unscheduled taks as an an input, identifies already scheduled times for the pet and conflicting times for other pets, creates a score based on priority and conflict penalty, and returns the top 3 ranked suggestions with conflict warnings.

3. Created a test to verify that the method worked as intended, tried to run from bash shell.

Based on the third prompt:

4. Edited main.py with a test that added an owner and multiple pets and tried to suggest a new task.

5. Ran the bash command 'python3 main.py 2>&1 | tail -30' to output the relevant part of the test and verified that suggest_time_slots was working correctly.

6. Displayed a list of features that the new algorithmic capability provided.

Based of the fourth prompt:

7. Edited test_pawpal.py with seven comprehensive new tests:
test_suggest_time_slots_basic — Verifies basic functionality and ensures occupied times are excluded
test_suggest_time_slots_avoids_pet_conflicts — Confirms suggestions skip times already scheduled for the same pet
test_suggest_time_slots_prioritizes_high_priority_early — Validates that high-priority tasks get earlier time suggestions
test_suggest_time_slots_detects_other_pet_conflicts — Checks that conflicts with other pets' schedules are detected and noted
test_suggest_time_slots_returns_multiple_options — Ensures the method returns ranked suggestions
test_suggest_time_slots_empty_pet_schedule — Tests the algorithm with pets that have no tasks yet
test_suggest_time_slots_respects_num_suggestions — Verifies the method returns the exact number of suggestions requested

8. Ran the following bash commands:
'python3 -m pytest tests/test_pawpal.py::test_suggest_time_slots_basic -v' - for running new time slot suggestion tests

'python3 -m pytest tests/test_pawpal.py -k "suggest_time_slots" -v' - for running all time slot suggestion tests

'python3 -m pytest tests/test_pawpal.py -v' - for running all of the existing tests in the file

9. Generated a message listing all of the tests and what they did, and verified that they all passed with no failures.


**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

I had to manually go through each of the tests that were created to make sure that they all actually did what the AI claimed they did.  However, the tests all made sense so I simply asked the AI to proceed.  I also had to make sure the AI was writing to the correct files, as it was trying to put all of the tests into a giant bash command and run it.  I had to instruct the AI to specifically edit main.py and test_pawpal.py.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | | |
| **Prompt** | | |
| **Response summary** | | |
| **What was useful** | | |
| **Problems noticed** | | |
| **Decision** | | |

**Which approach did you use in your final implementation and why?**

<!-- Your conclusion -->
