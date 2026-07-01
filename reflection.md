# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

Three core actions that a user should be able to perform:
1. Add a task - in order to track pet care tasks users have to be able to add tasks.
2. Generate a plan - This is one of the basic functionalities, producing a daily plan and explaining why it chose that plan
3. View the Plan - After generating the plan, the user should be able to view what they generated

Classes Created + responsibilities:
1. Task: This class represents individual pet care tasks like walking and feeding and has properties like name, duration, and priority.
2. Pet: This class represents the pet being taken care of, and contains name, species, and other info relevant to tasks.
3. Owner: This class represents a person with certain constraints such as their name, available time per day, and preferences.
4. Scheduler: This class takes the owner, pet, and tasks and creates an optimized daily plan.


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, my design did change.  I observed that the dependencies the AI created were very simplistic and did not account for every relationship, so I asked for further suggestions.  The AI recommended making it so Pets have Tasks, so each task is tailored to a specific pet, which was a design choice I chose to implement.  It also suggested adding an extra Schedule/Plan class, which I ignored for now.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
