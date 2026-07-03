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

The scheduler considers time, priority, recurrence, completion status, and pet/owner constraints.  When deciding which constraints to use, I thought of which ones would be absolutely necessary for the app to have minimum basic functionality.  Things like prioritizing certain tasks or making sure the same task is not being performed multiple times are absolutely essential for the app to have value to a user.  I had the AI assistant confirm this way of thinking.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff is that the conflict detection only checks if the tasks have the exact same scheduled time, for example that they are both at 9:00, while ignoring task durations.  This tradeoff is reasonable because it helps with speed and simplicity.  Detecting overlapping durations would add far more time complexity and even without it, obvious conflicts are still caught.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI tools to design the project framework both in UML and at an algorithmic level.  I often asked the assistant for tips on how to implement certain pieces of logic or how something could be made more intuitive.  AI was also instrumental in the debugging process, as after I went through and manually found several bugs the assistant was able to quickly identify the source of the issues, usually only taking one or two prompts.  AI was also very helpful in explaining certain parts of the code that I was unsure of the logic in, and asking for these explanations sometimes helped reveal bugs.

The most helpful prompts were typically ones that gave the AI several restrictions under which to implement logic, as otherwise some of the code would become unreadable and out of control.  I would often ask the assistant to "create a simple and readable implementation without breaking any of the core logic".  I would also often challenge the AI's UI implementation by asking "Is this the most intuitive way to have a user interact with this feature".

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When the AI suggested making a seperate Schedule and Scheduler class, I rejected the idea.  It seemed like a lot of of unnecessary complication for little to no significat benefit.  The assistant insisted on this numerous times but I always steered away from it.

I evaluated AI suggestions by reading through the code it recommended and analyzing to see if it would contradict or break the current code.  I would also try to find where the AI would expand the scope of a feature on its own and create an inefficient implementation.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

The tests I created covered sorting correctness, recurrence logic, conflict detection, filtering, validation, and duplicate prevention. The individual tests verified that tasks were sorted properly by time and priority, that daily and weekly recurring tasks created next occurrences automatically, that conflicts were detected when multiple tasks scheduled at the same time, and that invalid inputs like bad priorities or missing dates for recurring tasks were properly rejected.

These tests were important because they protected the core features that users needed to use the app. Sorting ensures users see a logical schedule, recurring tasks save users from creating daily chores over and over, and conflict detection prevents scheduling mishaps. Validation prevents crashes from bad data, and duplicate prevention keeps the task list clean. If these features were not tested properly, they could fail while giving no warning or cause the app to suddenly break, making it highly inconvinent for end users.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am pretty confident that the scheduler, with all of the features that were within the scope of this project, works correctly.  I created numerous tests to ensure that all of the core logic works correctly.  I also spent a long time manually using the app and testing out every feature.  This lead to the discovery of several bugs, all of which I was able to fix.

There are a couple of edge cases I would have wanted to test, one of those being what happens during large scale usage.  If there were hundreds of tasks and pets, along with multiple owners in the app, it would be important to see if the scheduling scales correctly.   I would also want to test the case where an owner has very little time for any tasks to see if the conflict handling holds up.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I think that I was able to improve my workflow with the AI on this project, to the point were I was able to premptively catch issues that would arise when the assistant wrote larger sections of code.  I was also happy with my debugging process, as I was able to find several mistakes, especially in the UI, that the AI did not recognize.  My ability to work with the AI to identify the root causes of these problems and fix them also improved over the couse of the project.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

In another iteration, I would definitely want to add some features, such as dependent tasks that would require other tasks to be performed first.  I would also like to implement a reminders feature that would look at the time and send a reminder that it was almost time to complete a certain task.  Redesigning the scheduling so that users can edit and remove tasks from a generated schedule directly rather than having to keep removing and adding things each time would also make the app much more user friendly.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

AI often adds a lot of complexity, so asking it to constantly explain what it is doing and questioning its reasoning is necessary to ensure the code remains both readable and logically sound.  Often times, questioning the AI on its implementation will lead it to find flaws in its own conclusions and fix them premptively.