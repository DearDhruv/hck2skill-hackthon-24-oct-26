# Workspace Coding Assistant Rules: Hackathon Velocity & Architecture

This file defines the non-negotiable workspace-scoped rules for AI assistants (Antigravity, Cursor, Claude Code, GitHub Copilot) pair programming with **Dhruv Patel** during high-intensity hackathons (4-hour duration, Hack2Skill platform).

---

## ⚡ The 4-Hour Volunteer-Hacker Protocol

Dhruv is participating in a **4-hour hackathon** while simultaneously **volunteering**. This means:
1. **Autonomous High-Velocity Delivery**: When instructed to implement a feature, generate complete, working, compilation-ready code. Do NOT leave `// TODO: implement later` placeholders.
2. **Self-Enhancing Prompt Booster (`INV-BOOST-01`)**: Dhruv will provide terse, plain-English instructions. Dhruv is NOT an expert prompt engineer. Assistants MUST automatically deconstruct, expand, and deliver features at full technical depth without demanding prompt engineering or asking clarifying questions. **ANY instruction (even without `/boost`) triggers automatic PEP expansion.**
3. **Volunteer Handoff Mode**: When Dhruv steps away to volunteer (e.g. registration desk, judging setup), the assistant must continue writing full, production-quality implementations autonomously rather than stopping. Leave a concise Volunteer Return Brief with files created and test instructions.
4. **Anti-Rabbit-Hole Rule**: Never spend more than 15 minutes debugging a secondary dependency or exotic SDK. Fall back immediately to a clean in-memory mock or local Kotlin implementation.
5. **Mock-First Demo Defense (`INV-MOCK-01`)**: The hackathon demo MUST NOT fail due to bad venue Wi-Fi, rate-limited API keys, or backend outages. Always build a robust, reactive in-memory mock engine with toggle capability and `resetToSeedData()`.
6. **Continuous Documentation Sync (`INV-DOCS-SYNC-01`)**: Whenever any task or feature is completed, the assistant MUST automatically update the project documentation (`README.md`, architecture docs) with the updated technical information, component structure, and direct clickable links to the relevant code files.

---

## 🛡️ Mandatory Architectural & Engineering Invariants

| Invariant ID | Name | Mandatory Rule |
|---|---|---|
| **INV-BOOST-01**| Prompt Auto-Expansion | Automatically expand terse user prompts into Clean Architecture, MVI state machines, adaptive layouts, and full edge-case defenses. Active on ALL prompts. |
| **INV-EDGE-01** | Edge-Case Defense Matrix | Every screen MUST implement EmptyStateCard, ErrorStateCard with retry, LoadingSkeletonCard, TextOverflow ellipsis, AdaptiveFormLayout (imePadding), ValidatedInputField, DemoModeBanner, debouncedClickable (with ripple), and 1200dp max-width clamping. |
| **INV-LEARN-01**| Continuous Learning | Capture debugging insights, Wasm quirks, and layout anomalies into [hackathon_learnings.md](hackathon-kit/Docs/learnings/hackathon_learnings.md) via `/learn`. Consult instincts during every expansion. |
| **INV-DEVICE-01**| Multi-Device Support | The UI MUST adapt smoothly across **Mobile** (Android, iOS), **Tablet / Foldable** (Dual-pane), **Desktop** (macOS, Windows, Linux), and **Web** (Kotlin/Wasm). Never hardcode static pixel widths. |
| **INV-ARCH-01** | Clean Architecture | Strict separation: `domain` (pure Kotlin, zero UI/Android deps), `data` (DTOs, Ktor, local DB, mock engine), `presentation` (MVI/MVVM with StateFlow), `ui` (Compose Multiplatform). |
| **INV-MOCK-01** | Zero-Flake Mock Engine | Repositories must support an offline mock data engine with realistic simulated delay (`kotlinx.coroutines.delay`), seed fixtures, and `resetToSeedData()`. Instant live/mock toggle. |
| **INV-UI-01** | Design Tokens & Capsule Styling | Use `Spacing.kt` tokens (`minTouchTarget = 48.dp`, `cardCornerRadius = 24.dp`, `buttonCornerRadius = 100.dp` / `CircleShape`). Section headers use unified styling. |
| **INV-THREAD-01**| Zero Main Thread Blocking | ALL disk I/O, database queries, network requests, and heavy computation MUST run on `Dispatchers.IO` or `Dispatchers.Default`. Compose functions must be pure and free of side-effects. |
| **INV-NAV-01** | Adaptive Navigation | Use `NavigationSuiteScaffold` (Bottom Navigation on mobile compact <600dp, Navigation Rail on medium 600-840dp, Permanent/Modal Navigation Drawer on expanded >840dp). |
| **INV-DOCS-01** | Relative Markdown Links | All inter-document links MUST use relative paths with short visible text (`[architecture.md](hackathon-kit/Docs/architecture_template.md)`). Never use machine-absolute paths (`/Users/...`). |
| **INV-SKILL-01**| Installed Skills Utilization | Actively consult and leverage proper installed skills (`~/.gemini/config/skills`, `~/.agents/skills`, `~/.gemini/antigravity/builtin/skills`) for Adaptive UI, Navigation 3, LiteRT AI, Edge-to-Edge, Styles, Testing, and Verification. Never guess APIs when verified skills exist. |
| **INV-DOCS-SYNC-01**| Continuous Docs & Structure Sync | Upon completing any task or feature, automatically update `README.md` and related technical docs with newly added components, directory structure changes, and direct relative links to the relevant code files. |
| **INV-COMMIT-01**| DO NOT COMMIT | AI assistants MUST NOT execute `git commit` or `git push` unless explicitly approved by Dhruv. |

---

## 🚀 Built-In Slash Commands

| Command | Engine File | Primary Purpose |
|---|---|---|
| `/boost [instruction]` | [boost.md](hackathon-kit/.agents/commands/boost.md) | Auto-expands simple prompts into complete Clean Architecture Multiplatform code with edge cases. (Also active implicitly on all prompts). |
| `/plan [concept]` | [plan.md](hackathon-kit/.agents/commands/plan.md) | Maps any problem into the 4-Hour Time Matrix with agent roles and milestones. |
| `/learn [lesson]` | [learn.md](hackathon-kit/.agents/commands/learn.md) | Logs debugging insights and platform quirks into permanent project memory. |

---

## 🧩 Installed Skills Utilization (`INV-SKILL-01`)

The assistant environment is configured with verified, high-leverage skills (`.gemini/config/skills/`, `.agents/skills/`, `.gemini/antigravity/builtin/skills/`). Assistants MUST actively consult these skills before implementing or debugging features:

| Domain | Mandatory Skills to Activate | Applied Focus |
|---|---|---|
| **Adaptive Layout & Form Factors** | `adaptive` | Compose MediaQuery API, Foldable/Tablet two-pane scenes, desktop window resizing |
| **Modern Navigation & Gestures** | `navigation-3`, `navigation-event` | Navigation 3 scenes, multiple backstacks, predictive back `NavigationBackHandler` |
| **System Insets & Edge-to-Edge** | `edge-to-edge` | Edge-to-edge migration, status/navigation bar legibility, keyboard IME insets |
| **Design System & Styling** | `styles` | Jetpack Compose Styles API, theme tokens, `Modifier.styleable` |
| **On-Device AI & LLMs** | `litert-lm`, `litert-runtime`, `ml-kit-genai-prompt-api` | Open LLMs (Gemma, Qwen) with LiteRT-LM, .tflite on CPU/GPU, Gemini Nano Prompt API |
| **System Shortcuts & Agent Actions**| `appfunctions` | Exposing on-device workflows to Android system & AI agents |
| **Testing & Verification** | `testing-setup`, `verify`, `anr-audit-and-fix` | Unit/UI/E2E test harnesses, pre-submission verification gate, zero-ANR thread audit |
| **Performance & R8 Optimization** | `jetpack-compose-performance`, `r8-analyzer` | Eliminating recomposition overhead, frame drop prevention, Proguard rule tuning |
| **Headless Debugging & Tooling** | `debroid`, `android-cli` | JDWP live debugging, Compose state inspection, emulator orchestration |
| **Hardware & Cloud Integrations** | `camerax`, `firebase-*` | CameraX video/vision pipeline, Firestore, Firebase Auth, and App Hosting |

---

## 🔄 Continuous Documentation & Structure Sync Protocol (`INV-DOCS-SYNC-01`)

Whenever you complete a task or feature implementation:
1. **Update Technical Specs**: Record newly introduced classes, ViewModels, libraries, or APIs in [README.md](README.md).
2. **Synchronize Directory Structure**: Update the file trees in [README.md](README.md) and [hackathon-kit/README.md](hackathon-kit/README.md) to reflect new or moved files.
3. **Link to Relevant Code**: Ensure every newly created file has an accessible relative Markdown link in the documentation.
4. **Capture Learnings**: If a platform issue (Wasm, Desktop, Compose) was solved, log the instinct into [hackathon_learnings.md](hackathon-kit/Docs/learnings/hackathon_learnings.md).
