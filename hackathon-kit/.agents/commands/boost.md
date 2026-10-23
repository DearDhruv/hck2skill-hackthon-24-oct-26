---
description: "Prompt Auto-Expansion Engine: Transforms short, plain, or high-level user instructions into production-grade Clean Architecture Kotlin Multiplatform code with full edge-case defense."
---

# Command: `/boost` (Prompt Auto-Expansion & Feature Completion)

Use `/boost [instruction]`—or simply provide any feature idea or instruction in plain English—and the multi-agent system will automatically deconstruct, enhance, and implement it to the highest engineering standards without you having to write a detailed prompt or be an expert prompt engineer.

> **Note on Automatic Activation**: You do not have to type `/boost` every time. The AI assistant treats **any short, plain, or high-level instruction as an implicit `/boost` request** and automatically applies the [Prompt Auto-Expansion Protocol (PEP)](../rules/prompt-expansion-protocol.md).

## Usage Examples
- `/boost add search and filter for events`
- `/boost create patient vitals monitoring screen with error handling`
- `/boost add offline sync status indicator with toggle`
- `build expense logging form` (automatically boosted via PEP)
- `/boost` (enhances and executes the immediately preceding instruction)

---

## What Happens When `/boost` Runs:

1. **Autonomous Requirement Expansion**:
   - The system intercepts your instruction and deconstructs it using the [prompt-expansion-protocol.md](../rules/prompt-expansion-protocol.md).
   - Enforces the **1-Flow Rule**: keeps the primary user journey tightly focused and compelling for judges.
   - Consults active instincts in [hackathon_learnings.md](../../Docs/learnings/hackathon_learnings.md) to proactively avoid known multiplatform traps.

2. **Full Clean Architecture Synthesis**:
   - **Domain**: Pure Kotlin immutable entities and repository interfaces (`INV-ARCH-01`).
   - **Data**: Reactive mock engine (`MockEngineFixture.kt`) with realistic seed data, latency simulation, offline toggle, and `resetToSeedData()` (`INV-MOCK-01`).
   - **Presentation**: MVI ViewModel (`UiState`, `UiIntent`, `UiEffect`) extending `BaseMviViewModel` with `safeLaunch` and coroutine exception handling.
   - **UI**: Compose Multiplatform adaptive layout with `NavigationSuiteScaffold`, `AdaptiveContainer` (1200dp width clamp), and `Spacing.kt` tokens (`INV-UI-01`, `INV-NAV-01`).

3. **Mandatory Edge-Case Shielding (`INV-EDGE-01`)**:
   - `EmptyStateCard` with action button when lists or queries return 0 items.
   - `ErrorStateCard` with retry action when operations fail.
   - `LoadingSkeletonCard` shimmer placeholders during data fetches.
   - Dynamic text truncation (`maxLines`, `overflow = TextOverflow.Ellipsis`).
   - `AdaptiveFormLayout` with `imePadding()` and vertical scrolling for keyboard avoidance.
   - `ValidatedInputField` with clear button, character limits, and inline errors.
   - Monotonic `debouncedClickable()` with ripple preserved on buttons.
   - `DemoModeBanner` with an instant offline mock toggle switch for live stage demo resilience.

4. **Instant Production Code Output**:
   - Delivers fully compilable, complete Kotlin files.
   - Zero `// TODO` or placeholder stubs.
