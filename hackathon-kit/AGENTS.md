# Workspace Coding Assistant Rules: Hackathon Velocity & Architecture

This file defines the non-negotiable workspace-scoped rules for AI assistants (Antigravity, Cursor, Claude Code, GitHub Copilot) pair programming with **Dhruv** during high-intensity hackathons (4-hour duration, Hack2Skill platform).

---

## ⚡ The 4-Hour Volunteer-Hacker Protocol

Dhruv is participating in a **4-hour hackathon** while simultaneously **volunteering**. This means:
1. **Autonomous High-Velocity Delivery**: When instructed to implement a feature, generate complete, working, compilation-ready code. Do NOT leave `// TODO: implement later` placeholders.
2. **Self-Enhancing Prompt Booster (`INV-BOOST-01`)**: Dhruv will provide terse, plain-English instructions. Dhruv is NOT an expert prompt engineer. Assistants MUST automatically deconstruct, expand, and deliver features at full technical depth without demanding prompt engineering or asking clarifying questions. **ANY instruction (even without `/boost`) triggers automatic PEP expansion.**
3. **Volunteer Handoff Mode**: When Dhruv steps away to volunteer (e.g. registration desk, judging setup), the assistant must continue writing full, production-quality implementations autonomously rather than stopping. Leave a concise Volunteer Return Brief with files created and test instructions.
4. **Anti-Rabbit-Hole Rule**: Never spend more than 15 minutes debugging a secondary dependency or exotic SDK. Fall back immediately to a clean in-memory mock or local Kotlin implementation.
5. **Mock-First Demo Defense (`INV-MOCK-01`)**: The hackathon demo MUST NOT fail due to bad venue Wi-Fi, rate-limited API keys, or backend outages. Always build a robust, reactive in-memory mock engine with toggle capability and `resetToSeedData()`.

---

## 🛡️ Mandatory Architectural & Engineering Invariants

| Invariant ID | Name | Mandatory Rule |
|---|---|---|
| **INV-BOOST-01**| Prompt Auto-Expansion | Automatically expand terse user prompts into Clean Architecture, MVI state machines, adaptive layouts, and full edge-case defenses. Active on ALL prompts. |
| **INV-EDGE-01** | Edge-Case Defense Matrix | Every screen MUST implement EmptyStateCard, ErrorStateCard with retry, LoadingSkeletonCard, TextOverflow ellipsis, AdaptiveFormLayout (imePadding), ValidatedInputField, DemoModeBanner, debouncedClickable (with ripple), and 1200dp max-width clamping. |
| **INV-LEARN-01**| Continuous Learning | Capture debugging insights, Wasm quirks, and layout anomalies into `Docs/learnings/hackathon_learnings.md` via `/learn`. Consult instincts during every expansion. |
| **INV-DEVICE-01**| Multi-Device Support | The UI MUST adapt smoothly across **Mobile** (Android, iOS), **Tablet / Foldable** (Dual-pane), **Desktop** (macOS, Windows, Linux), and **Web** (Kotlin/Wasm). Never hardcode static pixel widths. |
| **INV-ARCH-01** | Clean Architecture | Strict separation: `domain` (pure Kotlin, zero UI/Android deps), `data` (DTOs, Ktor, local DB, mock engine), `presentation` (MVI/MVVM with StateFlow), `ui` (Compose Multiplatform). |
| **INV-MOCK-01** | Zero-Flake Mock Engine | Repositories must support an offline mock data engine with realistic simulated delay (`kotlinx.coroutines.delay`), seed fixtures, and `resetToSeedData()`. Instant live/mock toggle. |
| **INV-UI-01** | Design Tokens & Capsule Styling | Use `Spacing.kt` tokens (`minTouchTarget = 48.dp`, `cardCornerRadius = 24.dp`, `buttonCornerRadius = 100.dp` / `CircleShape`). Section headers use unified styling. |
| **INV-THREAD-01**| Zero Main Thread Blocking | ALL disk I/O, database queries, network requests, and heavy computation MUST run on `Dispatchers.IO` or `Dispatchers.Default`. Compose functions must be pure and free of side-effects. |
| **INV-NAV-01** | Adaptive Navigation | Use `NavigationSuiteScaffold` (Bottom Navigation on mobile compact <600dp, Navigation Rail on medium 600-840dp, Permanent/Modal Navigation Drawer on expanded >840dp). |
| **INV-DOCS-01** | Relative Markdown Links | All inter-document links MUST use relative paths with short visible text (`[architecture.md](Docs/architecture.md)`). Never use machine-absolute paths (`/Users/...`). |
| **INV-COMMIT-01**| DO NOT COMMIT | AI assistants MUST NOT execute `git commit` or `git push` unless explicitly approved by Dhruv. |

---

## 🚀 Built-In Slash Commands

| Command | Engine File | Primary Purpose |
|---|---|---|
| `/boost [instruction]` | [.agents/commands/boost.md](.agents/commands/boost.md) | Auto-expands simple prompts into complete Clean Architecture Multiplatform code with edge cases. (Also active implicitly on all prompts). |
| `/plan [concept]` | [.agents/commands/plan.md](.agents/commands/plan.md) | Maps any problem into the 4-Hour Time Matrix with agent roles and milestones. |
| `/learn [lesson]` | [.agents/commands/learn.md](.agents/commands/learn.md) | Logs debugging insights and platform quirks into permanent project memory. |

---

## 🏗️ Clean Architecture Package Structure

All multiplatform modules follow this exact package organization:

```
com.deardhruv.<project_name>/
├── domain/
│   ├── model/                  # Pure Kotlin domain data classes
│   ├── repository/             # Pure Kotlin repository interfaces
│   └── usecase/                # Single-responsibility business use cases
├── data/
│   ├── dto/                    # API DTOs and serialization models
│   ├── remote/                 # Ktor HTTP client & API services
│   ├── local/                  # SQLite/SQLDelight/Room entities & DAOs
│   ├── mock/                   # Deterministic offline mock engine & fixtures
│   └── repository/             # Repository implementations (switching Mock vs Remote)
├── presentation/
│   ├── <feature>/
│   │   ├── <Feature>Contract.kt # UI State, Intent/Event, Single-shot Effect
│   │   └── <Feature>ViewModel.kt# StateFlow-based presentation logic with safeLaunch
├── ui/
│   ├── theme/                  # Color, Typography, Shapes, Spacing design tokens
│   ├── components/             # EdgeCaseComponents, cards, pills, badges
│   ├── navigation/             # NavigationSuiteScaffold and screen routing
│   └── <feature>/              # Feature screens and responsive sub-composables
└── platform/                   # Kotlin expect/actual declarations (Audio, Storage, System)
```

---

## 🎨 UI/UX & Design Token Invariants

1. **Design Tokens (`Spacing.kt`)**:
   - `Spacing.xxs = 2.dp`, `Spacing.xs = 4.dp`, `Spacing.s = 8.dp`, `Spacing.m = 16.dp`, `Spacing.l = 24.dp`, `Spacing.xl = 32.dp`.
   - `Spacing.minTouchTarget = 48.dp` (All buttons, chips, and interactive rows MUST satisfy this).
   - `Spacing.cardCornerRadius = 24.dp` (All cards, bottom sheets, and dialog surfaces).
   - `Spacing.buttonCornerRadius = 100.dp` / `CircleShape` (Capsule shape for all action buttons, chips, and pills).

2. **Adaptive Layout Strategy**:
   - Phone (<600dp): Single column `LazyColumn`, bottom navigation bar.
   - Foldable/Tablet (600dp–840dp): Two-pane layout (`AdaptiveTwoPaneLayout` or 2-column grid), navigation rail.
   - Desktop & Web (>840dp): Multi-column grid, navigation drawer, wide preview pane, keyboard shortcuts.
   - Ultra-Wide Viewport Clamping: Wrap content in `AdaptiveContainer(maxContentWidth = 1200.dp)`.

3. **Theme & Contrast**:
   - Support both Dark and Light modes out of the box using Material 3 `ColorScheme`.
   - Primary accents: Slate grey, Kotlin violet (`#7F52FF`), Compose blue-green (`#00A88F` / `#4285F4`).

---

## ⏱️ 4-Hour Sprint Schedule & Agent Coordination

| Hackathon Hour | Phase & Milestone | Active Agent | Key Action |
|---|---|---|---|
| **Hour 1 (00:00 - 01:00)** | Problem Assessment & Domain Lock | `architect-scaffolder` & `engine-data-integrator` | Narrow scope to 1 killer flow. Define domain models and mock data engine. |
| **Hour 2 (01:00 - 02:00)** | Adaptive UI & Navigation Scaffold | `cmp-ui-designer` | Build responsive screens with NavigationSuiteScaffold, Material 3, and Spacing tokens. |
| **Hour 3 (02:00 - 03:00)** | Feature Polish & Live Integrations | `cmp-ui-designer` & `quality-verifier` | Connect ViewModels, wire animations, test tablet/desktop viewports, verify edge cases. |
| **Hour 4 (03:00 - 04:00)** | Submission Freeze & Pitch Deck | `pitch-submission-lead` | Finalize README, Mermaid diagrams, pitch slides (`pitch.md`), demo video script. Lock submission. |

---

## 🚫 What NOT to Do (Time Traps to Avoid)

1. **Do NOT build custom authentication from scratch** in a 4-hour hackathon. Use a simulated user profile or lightweight local session.
2. **Do NOT fight third-party backend bugs**. If an API is slow or requires complex OAuth tokens, switch immediately to the mock data engine.
3. **Do NOT create monolithic files**. Keep screens and ViewModels concise and split into sub-packages.
4. **Do NOT skip documentation**. Judges on Hack2Skill read the README and watch the 2-minute demo video first before testing the code. Excellent documentation wins hackathons.
