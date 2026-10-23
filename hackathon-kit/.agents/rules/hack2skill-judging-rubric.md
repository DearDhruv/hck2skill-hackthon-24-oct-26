---
trigger: always_on
description: "Optimization guide and scoring checklist tailored specifically to Hack2Skill hackathon judging rubrics."
---

# Rule: Hack2Skill Judging Rubric Alignment

Hack2Skill hackathons evaluate submissions across five core pillars. This checklist ensures maximum scoring across every evaluation dimension:

---

## Pillar 1: Problem Statement Alignment & Innovation (25%)
- [ ] **Real Pain Point**: The problem statement is explicitly cited in the README and pitch deck.
- [ ] **Target Persona**: Clear description of who experiences this problem and why existing alternatives fail.
- [ ] **Novel Angle / Innovation**: Highlight unique algorithmic approach, edge AI processing, or multi-device integration that sets the solution apart.

---

## Pillar 2: Technical Architecture & Code Quality (25%)
- [ ] **Clean Architecture Layers**: Strict separation between `domain`, `data`, `presentation`, and `ui`.
- [ ] **Pure Kotlin Business Logic**: Domain layer has zero Android or UI framework dependencies.
- [ ] **Unidirectional Data Flow**: MVI / StateFlow state management.
- [ ] **No Monolithic Files**: Code organized into focused sub-packages by feature and single responsibility.
- [ ] **Version Catalog**: Standard `gradle/libs.versions.toml` used cleanly.

---

## Pillar 3: Execution & Working Prototype (25%)
- [ ] **Flawless End-to-End Demo**: Primary user journey works without errors or freezing.
- [ ] **Mock-First Insurance (`INV-MOCK-01`)**: Working demo guaranteed even without Wi-Fi.
- [ ] **Empty & Error States**: Graceful UI when lists are empty or errors occur.
- [ ] **Realistic Data**: Rich, believable seed fixtures populated in the app.

---

## Pillar 4: Multi-Device Scalability & UI/UX Polish (15%)
- [ ] **Responsive Breakpoints**: Seamless experience across Mobile (<600dp), Tablet (600-840dp), and Desktop/Web (>840dp).
- [ ] **Adaptive Navigation**: `NavigationSuiteScaffold` (Bottom Bar, Nav Rail, Nav Drawer).
- [ ] **Capsule Styling & Touch Targets**: `CircleShape` buttons, 48dp min touch targets.
- [ ] **Dark / Light Theme**: Full contrast fidelity across both themes.

---

## Pillar 5: Pitch, Demo & Documentation (10%)
- [ ] **Executive README**: Clean badges, problem-solution summary, architecture diagram (Mermaid), and run instructions.
- [ ] **7-Slide Pitch Deck**: Crisp `pitch.md` covering Problem, Solution, Architecture, Market, Roadmap.
- [ ] **2-Minute Demo Video Script**: Crisp, timed walkthrough script covering the killer feature.
- [ ] **Hack2Skill Submission Copy**: Complete submission form ready for copy-paste before deadline.
