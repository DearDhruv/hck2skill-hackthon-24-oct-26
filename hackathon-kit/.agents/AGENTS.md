# Hackathon Agent Workspace Index

Canonical agent pointer, commands, and rules reference for hackathon pair-programming.

## Core Assistant Invariants
- **INV-BOOST-01**: Prompt Auto-Expansion Protocol (PEP) — Automatically expands terse, plain-English user instructions into Clean Architecture, MVI contracts, and edge cases. Active implicitly on ALL prompts.
- **INV-EDGE-01**: Edge-Case Defense Matrix — Mandatory EmptyStateCard, ErrorStateCard with retry, LoadingSkeletonCard, text overflow ellipsis, AdaptiveFormLayout (imePadding), ValidatedInputField, DemoModeBanner, debouncedClickable (with ripple), and 1200dp max-width clamping.
- **INV-LEARN-01**: Continuous Learning — Records debugging insights and platform traps into `Docs/learnings/hackathon_learnings.md` via `/learn`. Consults instincts during every expansion.
- **INV-DEVICE-01**: Multi-Device Support across Mobile, Tablet, Desktop, and Web Wasm.
- **INV-ARCH-01**: Clean Architecture (Domain is pure Kotlin; zero UI/Android deps).
- **INV-MOCK-01**: Mock-First offline data engine for zero-flake live demo defense with `resetToSeedData()`.
- **INV-UI-01**: Spacing design tokens (`Spacing.kt`, 48dp touch targets, capsule buttons).
- **INV-THREAD-01**: Zero main thread blocking; all I/O and AI on `Dispatchers.IO`/`Default`.
- **INV-NAV-01**: Adaptive Navigation with `NavigationSuiteScaffold`.
- **INV-DOCS-01**: Relative Markdown links only.
- **INV-SKILL-01**: Installed Skills Utilization — Proactively consult and leverage installed skills (`adaptive`, `navigation-3`, `edge-to-edge`, `litert-lm`, `testing-setup`, `verify`, `styles`, etc.).
- **INV-COMMIT-01**: DO NOT COMMIT or run git push commands.

## Built-In Slash Commands
- [boost.md](commands/boost.md): `/boost [instruction]` — Prompt auto-expansion & feature completion.
- [plan.md](commands/plan.md): `/plan [concept]` — 4-hour hackathon execution planner.
- [learn.md](commands/learn.md): `/learn [lesson]` — Continuous learning & instinct recording.

## Specialized Agent Roster
- [architect-scaffolder.md](agents/architect-scaffolder.md): Problem deconstruction, prompt auto-expansion, and domain modeling.
- [cmp-ui-designer.md](agents/cmp-ui-designer.md): Adaptive Compose UI builder, Material 3 styling, and Edge-Case components.
- [engine-data-integrator.md](agents/engine-data-integrator.md): Reactive mock fixtures, live offline toggle, Ktor HTTP, and AI hooks.
- [quality-verifier.md](agents/quality-verifier.md): Fast unit testing, edge-case defense audits, and continuous learning trigger.
- [pitch-submission-lead.md](agents/pitch-submission-lead.md): Hack2Skill pitch deck, README, and video script.

## Rules Reference
- [hackathon-4hr-protocol.md](rules/hackathon-4hr-protocol.md): 4-hour time matrix and volunteer balance protocol.
- [clean-architecture-kmp.md](rules/clean-architecture-kmp.md): Layer contracts and MVI state machine.
- [adaptive-ui-multiplatform.md](rules/adaptive-ui-multiplatform.md): Responsive breakpoints and design tokens.
- [mock-first-resilience.md](rules/mock-first-resilience.md): Mock-first data architecture.
- [hack2skill-judging-rubric.md](rules/hack2skill-judging-rubric.md): Hack2Skill scoring optimization.
- [ai-edge-intelligence.md](rules/ai-edge-intelligence.md): On-device and cloud AI patterns.
- [prompt-expansion-protocol.md](rules/prompt-expansion-protocol.md): Prompt auto-expansion formula.
- [edge-case-defense-matrix.md](rules/edge-case-defense-matrix.md): Mandatory edge-case safeguards.
- [hackathon-planning-protocol.md](rules/hackathon-planning-protocol.md): Time-boxed roadmap planning.
- [continuous-learning-protocol.md](rules/continuous-learning-protocol.md): Memory preservation & instinct lifecycle.
- [installed-skills-usage.md](rules/installed-skills-usage.md): Installed skills catalog & domain execution protocol.
