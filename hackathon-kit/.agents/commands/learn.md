---
description: "Continuous Learning & Instinct Engine: Captures debugging lessons, Compose/Wasm platform traps, and user feedback into permanent project memory."
---

# Command: `/learn` (Continuous Learning & Instinct Recording)

Use `/learn [lesson, observation, or bug fix]` whenever you encounter a tricky bug, a platform quirk (especially in Kotlin/Wasm or Compose Multiplatform), or when Dhruv expresses a preference. The system records the observation into `Docs/learnings/hackathon_learnings.md` and updates the agent system's memory so the issue is never repeated.

## Usage Examples
- `/learn Wasm crashes when accessing Dispatchers.IO; always use Dispatchers.Default for browser target`
- `/learn On ultrawide monitors, clamp the main dashboard to 1200dp max width using AdaptiveContainer`
- `/learn In debouncedClickable, do not set indication=null because it removes the ripple effect`
- `/learn LazyColumn crashes with IllegalArgumentException if two items share identical mock timestamps; append monotonic counter to ID`
- `/learn` (analyzes recent conversation context and extracts the key learning)

---

## What Happens When You Run `/learn`:

1. **Instinct Extraction**:
   - Deconstructs the insight into a structured format:
     - **Trigger**: When does this scenario occur?
     - **The Trap**: What fails, hangs, or degrades UX?
     - **Defensive Pattern**: The exact code pattern or rule that prevents it.
     - **Agents Impacted**: Which specialized personas must adhere to it.

2. **Memory Persistence**:
   - Appends the instinct to [Docs/learnings/hackathon_learnings.md](../Docs/learnings/hackathon_learnings.md).

3. **Active System Feedback**:
   - Automatically incorporates the learning into all future `/boost` and `/plan` generations.
   - Proactively prevents regressions in subsequent coding phases.
