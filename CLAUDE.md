# Claude Code Guidelines: Hack2Skill Hackathon System

Follow all architectural, velocity, and design rules defined in [AGENTS.md](AGENTS.md) and [hackathon-kit/.agents/rules/](hackathon-kit/.agents/rules/).

## Essential Slash Commands

- `/boost [instruction]`: Auto-expands short instructions into complete Clean Architecture Multiplatform code with edge cases.
- `/plan [concept]`: Rapidly maps any problem statement into the 4-Hour Time Matrix with agent roles.
- `/learn [lesson]`: Logs debugging insights and platform quirks into `hackathon-kit/Docs/learnings/hackathon_learnings.md`.

## Build & Verification Commands

- **Audit Hackathon Invariants & Structure**: `./hackathon-kit/scripts/check-hackathon-readiness.sh`
- **Run Multiplatform Unit Tests**: `./gradlew test` (or `./gradlew :shared:allTests`)
- **Run Android Debug Build**: `./gradlew :composeApp:assembleDebug`
- **Run Desktop (JVM) App**: `./gradlew :composeApp:run`
- **Run Web (Wasm) App**: `./gradlew :composeApp:wasmJsBrowserDevelopmentRun`

## Critical Hackathon Invariants

1. **Self-Enhancing Instructions (`INV-BOOST-01`)**: Dhruv will send terse, plain-English instructions. Always auto-expand into domain models, mock fixtures, MVI state, adaptive UI, and edge cases. Active implicitly on ALL prompts.
2. **Edge-Case Defense Matrix (`INV-EDGE-01`)**: Always include EmptyStateCard, ErrorStateCard (with retry), LoadingSkeletonCard, text ellipsis, AdaptiveFormLayout (imePadding), ValidatedInputField, DemoModeBanner, debouncedClickable (with ripple), and 1200dp max-width clamping.
3. **Continuous Learning (`INV-LEARN-01`)**: Record all tricky bugs or Wasm/Compose quirks into `hackathon_learnings.md` via `/learn`. Proactively consult instincts during every expansion.
4. **Continuous Docs & Structure Sync (`INV-DOCS-SYNC-01`)**: When tasks are done, update project documentation (`README.md`, architecture docs) with updated technical info, directory structure, and links to relevant code.
5. **Installed Skills (`INV-SKILL-01`)**: Proactively consult and leverage installed skills (`adaptive`, `navigation-3`, `navigation-event`, `edge-to-edge`, `styles`, `litert-lm`, `litert-runtime`, `ml-kit-genai-prompt-api`, `testing-setup`, `verify`, `jetpack-compose-performance`) rather than guessing APIs.
6. **4-Hour Time Limit & Volunteer Handoff**: Deliver working code immediately; no stubbed placeholders. When Dhruv steps away to volunteer, execute full flows autonomously and leave a test brief.
7. **Multi-Device**: Android, iOS, Desktop, and Web (Wasm) adaptive UI with `NavigationSuiteScaffold`.
8. **Mock-First Engine (`INV-MOCK-01`)**: Always maintain realistic offline data fixtures with `resetToSeedData()` for stage presentation.
9. **Clean Architecture**: Pure Kotlin domain, MVI StateFlow presentation, Compose Multiplatform UI.
10. **Capsule Styling (`INV-UI-01`)**: Use `Spacing.kt` tokens (`minTouchTarget = 48.dp`, `buttonCornerRadius = 100.dp` / `CircleShape`).
11. **Zero Main-Thread Blocking**: All I/O, heavy calculations, and AI inference on `Dispatchers.IO` / `Dispatchers.Default`.
12. **DO NOT COMMIT**: Do not run `git commit` or `git push` unless explicitly approved.
