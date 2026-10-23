---
description: "4-Hour Hackathon Rapid Execution Planner: Maps any problem statement into a time-budgeted, multi-agent sprint roadmap with clean architecture, volunteer handoff mode, and edge-case defenses."
---

# Command: `/plan` (4-Hour Hackathon Rapid Execution Planner)

Use `/plan [problem statement or app concept]` at the beginning of a hackathon sprint or when tackling a major new feature flow. The system will deconstruct your input into a focused, time-budgeted roadmap strictly following the 4-Hour Time Matrix and Hack2Skill judging rubrics.

## Usage Examples
- `/plan AI-powered offline triage assistant for rural clinics`
- `/plan decentralized carbon credit tracker with verified ledger`
- `/plan stepping away for 30 minutes to volunteer at registration desk; implement donation flow` (activates Volunteer Handoff Mode)
- `/plan` (analyzes [Docs/problem_assessment_worksheet.md](../Docs/problem_assessment_worksheet.md) and creates the sprint plan)

---

## What Happens When You Run `/plan`:

1. **Phase 0: Scope & Domain Lock (00:00 - 00:30)**:
   - Formulates the **1 Killer Flow** (Input -> Intelligence -> Actionable Output).
   - Generates pure Kotlin domain entities and repository interfaces (`architect-scaffolder`).
   - Produces a Mermaid architecture diagram ready for the README.

2. **Phase 1: Domain & Mock Data Engine (00:30 - 01:15)**:
   - Generates `MockEngineFixture.kt` with rich, realistic domain data fixtures (`engine-data-integrator`).
   - Supports live toggle (`isOfflineMode`), error simulation, and `resetToSeedData()` (`INV-MOCK-01`).
   - Verifies unit tests pass with zero network dependency.

3. **Phase 2: Adaptive Compose UI (01:15 - 02:45)**:
   - Sets up `NavigationSuiteScaffold` with Mobile, Tablet, and Desktop/Web breakpoints (`cmp-ui-designer`).
   - Applies Dhruv's design tokens: capsule buttons, 48dp touch targets, 24dp card corners (`INV-UI-01`).
   - Integrates `AdaptiveContainer` (1200dp max-width) and `AdaptiveTwoPaneLayout`.

4. **Phase 3: Integration & Edge-Case QA (02:45 - 03:30)**:
   - Connects MVI ViewModels to state contracts (`quality-verifier`).
   - Verifies the **Edge-Case Defense Matrix** (`EmptyStateCard`, `ErrorStateCard`, `LoadingSkeletonCard`, `AdaptiveFormLayout`, `ValidatedInputField`, `DemoModeBanner`).
   - Wires on-device AI inference (`LiteRTQuickEngine.kt`) with timeout and exception shielding.

5. **Phase 4: Submission Freeze & Pitch (03:30 - 04:00)**:
   - Drafts the 7-slide pitch deck (`pitch_deck_template.md`).
   - Generates the 2-minute demo video script (`demo_video_script.md`).
   - Prepares copy-paste Hack2Skill submission form (`pitch-submission-lead`).

---

## Volunteer Handoff Mode
If Dhruv mentions stepping away to volunteer, the assistant executes autonomously across all phases without stalling, delivering complete, compilable Kotlin files, and leaving a concise test briefing.
