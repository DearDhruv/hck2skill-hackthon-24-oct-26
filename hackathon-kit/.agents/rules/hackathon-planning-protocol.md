# Rule: Hackathon Planning Protocol & /plan Engine

This rule governs how the `/plan` command breaks down ambiguous hackathon goals, feature requests, or problem statements into a time-budgeted, 4-hour execution roadmap strictly aligned with Hack2Skill judging rubrics and Dhruv's on-site volunteer duties.

---

## 1. The 4-Hour Hackathon Time Matrix

When `/plan` is invoked, the AI must formulate an actionable execution roadmap strictly bounded by the 4-hour matrix:

```
[00:00 - 00:30] Phase 0: Scope & Domain Lock (architect-scaffolder)
[00:30 - 01:15] Phase 1: Core Domain & Mock Data Engine (engine-data-integrator)
[01:15 - 02:45] Phase 2: Adaptive Compose UI & Styling (cmp-ui-designer)
[02:45 - 03:30] Phase 3: Integration, Edge-Cases & QA (quality-verifier)
[03:30 - 04:00] Phase 4: Submission Freeze & Pitch Deck (pitch-submission-lead)
```

---

## 2. The Volunteer Handoff Protocol

Dhruv will periodically step away to fulfill on-site volunteering duties (registration, stage setup, participant support).
When Dhruv states they are stepping away (e.g. *"I'm stepping away for 20 minutes, build the analytics dashboard"*), assistants MUST operate under **Autonomous Handoff Mode**:
1. **Never Stop for Questions**: Make authoritative engineering decisions aligned with Clean Architecture, MVI, and the Edge-Case Defense Matrix.
2. **Execute Full Vertical Flow**: Generate the domain model, mock engine fixture, MVI ViewModel, responsive Compose UI, and edge-case wrappers.
3. **Leave a Volunteer Return Brief**:
   - 🎯 **What Was Built**: 2-sentence summary of the completed flow.
   - 📂 **Key Files Created**: Markdown links to each new file.
   - 🧪 **Quick Verification Steps**: How Dhruv can immediately test or preview the change.

---

## 3. Scope Pruning & Anti-Rabbit-Hole Invariants

Every plan generated MUST enforce these four scoping invariants:

1. **The 1-Flow Rule**: In 4 hours, build **ONE jaw-dropping, end-to-end user flow** rather than 5 half-finished screens. (Step 1: Input/Trigger -> Step 2: Processing/Intelligence -> Step 3: Actionable Output).
2. **The 15-Minute Rule**: If any third-party SDK, cloud API, or Gradle plugin takes >15 minutes to configure or fails to compile, immediately abandon it and use the in-memory mock engine.
3. **Authentication Shortcut**: Replace complex social auth (OAuth/Google Sign-In) with an instant "Select Persona" profile switcher unless authentication is the central problem statement.
4. **Mock-First Insurance (`INV-MOCK-01`)**: Build the reactive mock data engine FIRST before attempting external cloud API connections. That way, the live demo remains 100% functional even if the venue Wi-Fi fails completely.

---

## 4. Hack2Skill Rubric Scoring Alignment

Plans must explicitly allocate effort to maximize scoring across all 5 evaluation pillars:
- **Pillar 1: Problem Alignment & Innovation (25%)**: Solves a real pain point with a clear target persona.
- **Pillar 2: Technical Architecture (25%)**: Clean Architecture, pure Kotlin domain, MVI StateFlow, zero main thread blocking.
- **Pillar 3: Working Prototype (25%)**: Flawless live demo guaranteed by MockEngineFixture and offline toggle.
- **Pillar 4: Multi-Device Polish (15%)**: Adaptive layouts across Phone (<600dp), Tablet (600-840dp), and Desktop (>840dp) with capsule design tokens.
- **Pillar 5: Pitch & Documentation (10%)**: 7-slide deck (`pitch_deck_template.md`), 2-minute demo video script (`demo_video_script.md`), and README.

---

## 5. Plan Output Format

When `/plan` is executed, output the plan using this crisp, actionable structure:

```markdown
# ⚡ 4-Hour Hackathon Execution Plan: [Project Name]

## 🎯 1. Problem & The 1 Killer Flow
- **Target Persona**: [Who is the user]
- **Core Value Prop**: [One punchy sentence]
- **The Killer Flow**:
  1. *Input*: [User action / data entry]
  2. *Intelligence*: [On-device LiteRT analysis / rule calculation]
  3. *Output*: [Adaptive multi-pane view / export]

## 🏛️ 2. Clean Architecture Contracts
- **Domain Entities**: `[Entity1]`, `[Entity2]` with validation
- **Repository Interface**: `fun observeData(): Flow<List<Entity>>`, `suspend fun performAction(...)`
- **Mock Engine**: `MockEngineFixture` with seed data, offline toggle, and `resetToSeedData()`
- **MVI Contract**: `UiState` (Loading/Content/Empty/Error), `UiIntent`, `UiEffect`

## 📱 3. Multi-Device Adaptive Breakpoints
- **Mobile (<600dp)**: Single column, Bottom Navigation bar, `AdaptiveFormLayout`.
- **Tablet (600-840dp)**: Dual-pane master-detail (`AdaptiveTwoPaneLayout`), Navigation Rail.
- **Desktop/Web (>840dp)**: Multi-column grid, Navigation Drawer, clamped max-width (1200dp).

## ⏱️ 4. Time-Boxed Milestones & Agent Assignment
- **Phase 0 (00:00 - 00:30)**: Scope & Domain Lock (`architect-scaffolder`).
- **Phase 1 (00:30 - 01:15)**: Mock Data Engine with seed fixtures (`engine-data-integrator`).
- **Phase 2 (01:15 - 02:45)**: Adaptive Compose UI + EdgeCaseComponents (`cmp-ui-designer`).
- **Phase 3 (02:45 - 03:30)**: ViewModel state binding + LiteRT AI + QA (`quality-verifier`).
- **Phase 4 (03:30 - 04:00)**: Pitch deck (`pitch.md`), README, 2-min video script (`pitch-submission-lead`).

## 🛡️ 5. Edge-Case Defense Checklist
- [ ] Empty state view (`EmptyStateCard`)
- [ ] Error state view (`ErrorStateCard`) with retry
- [ ] Loading skeleton (`LoadingSkeletonCard`)
- [ ] Text overflow ellipsis
- [ ] Soft keyboard avoidance (`AdaptiveFormLayout`)
- [ ] Validated text input (`ValidatedInputField`)
- [ ] Double-tap debounce (`debouncedClickable`)
- [ ] Demo mode toggle banner (`DemoModeBanner`)
- [ ] Pre-demo reset hook (`resetToSeedData()`)
```
