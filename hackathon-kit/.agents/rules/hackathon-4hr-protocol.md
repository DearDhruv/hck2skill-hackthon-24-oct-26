---
trigger: always_on
description: "Rules for executing a 4-hour hackathon sprint while managing volunteer commitments. Enforces time-boxing, MVP scoping, and anti-rabbit-hole triage."
---

# Rule: 4-Hour Hackathon Operating Protocol

This rule governs the execution velocity, time budgeting, and scope triage during a **4-hour hackathon sprint** where Dhruv is also fulfilling on-site volunteer duties.

## 1. The 4-Hour Time Matrix

| Time Window | Phase | Primary Objective | Deliverable Gate |
|---|---|---|---|
| **00:00 - 00:30** | **Phase 0: Scope & Architecture Lock** | Problem analysis, MVP pruning, domain models, entity schemas | Domain models in pure Kotlin, Mermaid diagram in `Docs/architecture.md` |
| **00:30 - 01:15** | **Phase 1: Domain & Mock Data Engine** | Repositories, Use Cases, Mock Engine with realistic seed fixtures | `MockEngineFixture.kt` working with StateFlow, unit test passing |
| **01:15 - 02:45** | **Phase 2: Adaptive Compose UI** | Responsive NavigationSuiteScaffold, Screen layouts, Cards, Design Tokens | Multi-device UI rendering smoothly on Phone, Tablet, and Desktop/Web |
| **02:45 - 03:30** | **Phase 3: Integration & Edge-Case QA** | Wire ViewModel state, connect live API/AI if ready, test empty/error states | Zero crash paths, dark/light theme verified, fast responsiveness |
| **03:30 - 04:00** | **Phase 4: Pitch, Demo & Submission Freeze** | Finalize README, 7-slide pitch deck (`pitch.md`), 2-min video script, submission form | Hack2Skill submission locked, release tag created |

---

## 2. Volunteer-Hacker Execution Rules

Because Dhruv's attention will be periodically required for volunteering tasks:
1. **Zero Waiting / Unblocked Assistant**: Whenever Dhruv steps away to volunteer, the assistant must continue writing full, production-quality implementations rather than stopping at questions.
2. **Atomic Self-Contained Deliveries**: All code generated must compile cleanly on its own.
3. **No Intermediate Git Commits**: AI assistant MUST NOT run `git commit` or `git push` (`INV-COMMIT-01`). Dhruv will review diffs and commit when ready.

---

## 3. Scope Pruning & Anti-Rabbit-Hole Rules

1. **The 1-Flow Rule**: In 4 hours, build **ONE end-to-end, jaw-dropping user flow** flawlessly rather than 5 half-finished screens.
2. **The 15-Minute Rule**: If a 3rd-party library, Gradle plugin, or cloud API takes more than 15 minutes to configure or fails to compile, **ABANDON IT IMMEDIATELY** and switch to an in-memory mock engine or local Kotlin implementation.
3. **Authentication Shortcut**: Replace complex social auth (OAuth/Google Sign-In) with an instant "Select Persona" or guest profile switcher unless auth is the explicit hackathon theme.
4. **Mock-First Insurance**: Build the mock data engine FIRST before attempting external cloud API connections. That way, even if the venue Wi-Fi drops, the app remains 100% demoable.
