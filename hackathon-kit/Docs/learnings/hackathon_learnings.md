# Hackathon Knowledge Base & Instinct Registry

This file records continuous learnings, platform anomalies (Kotlin/Wasm, Compose Multiplatform, Desktop), and architectural safeguards captured during hackathons. Updated automatically via the `/learn` command.

---

## 🧠 Active Instincts Registry

### [INSTINCT-001] Kotlin/Wasm Single-Thread Dispatcher Safety
- **Date / Phase**: Pre-Hackathon Scaffolding / Concurrency
- **Trigger**: Launching coroutines or switching dispatchers in Web (Wasm) targets.
- **The Trap**: Calling `Dispatchers.IO` directly on Wasm browser runtime can fail or behave unpredictably because the browser runs a single-threaded event loop.
- **The Defensive Pattern**: Use `Dispatchers.Default` for CPU-bound tasks in shared code, or abstract network I/O through Ktor's asynchronous engine which bridges natively to browser Fetch API.
- **Agents Impacted**: `engine-data-integrator`, `quality-verifier`

---

### [INSTINCT-002] Ultrawide Desktop Viewport Clamping
- **Date / Phase**: Pre-Hackathon Scaffolding / Adaptive UI
- **Trigger**: Running Compose Multiplatform on Desktop (JVM) or Web widescreen monitors (> 1440px).
- **The Trap**: If content uses simple `fillMaxWidth()`, cards and form fields stretch across the entire 4K monitor, ruining visual balance and failing judge UX scrutiny.
- **The Defensive Pattern**: Wrap screen bodies in `AdaptiveContainer(maxWidth = 1200.dp)` to clamp content width and center it horizontally with generous margins.
- **Agents Impacted**: `cmp-ui-designer`

---

### [INSTINCT-003] Rapid Double-Tap Button Submission
- **Date / Phase**: Pre-Hackathon Scaffolding / Edge Cases
- **Trigger**: User or judge repeatedly clicks "Submit" or "Generate" in rapid succession.
- **The Trap**: Duplicate items get inserted into the database/StateFlow or concurrent network requests collide, causing state corruption or jarring UI flicker.
- **The Defensive Pattern**: Use `Modifier.debouncedClickable(debounceMs = 500)` or disable the action button immediately via `enabled = !uiState.isLoading` during processing.
- **Agents Impacted**: `cmp-ui-designer`, `quality-verifier`

---

### [INSTINCT-004] Live Stage Demo Wi-Fi Outage Defense
- **Date / Phase**: Pre-Hackathon Scaffolding / Mock Engine
- **Trigger**: Live 2-minute pitch before judges at the hackathon venue.
- **The Trap**: Venue Wi-Fi drops, blocks non-standard ports, or third-party API rate limits hit, resulting in an instant 0 for "Working Prototype".
- **The Defensive Pattern**: Default to `isMockMode = true` in repository fixtures. Add a visible `DemoModeBanner` with an instant toggle so judges can see both real and simulated data without fear of network crashes.
- **Agents Impacted**: `engine-data-integrator`, `pitch-submission-lead`

---

### [INSTINCT-005] Mobile Soft Keyboard (IME) Occlusion
- **Date / Phase**: Pre-Hackathon Scaffolding / Mobile Form Factor
- **Trigger**: Entering text in input fields on compact mobile phone viewports (< 600dp).
- **The Trap**: The on-screen keyboard rises and covers the input field, the submit button, or the error message, leaving the user unable to tap or see their typing.
- **The Defensive Pattern**: Always wrap form bodies in `AdaptiveFormLayout` which attaches `.imePadding()` and `Modifier.verticalScroll(rememberScrollState())`.
- **Agents Impacted**: `cmp-ui-designer`

---

### [INSTINCT-006] Preservation of CancellationException in ViewModel Coroutine Handlers
- **Date / Phase**: Scaffolding Hardening / Concurrency
- **Trigger**: ViewModel coroutine cancellation when a screen is popped, job cancelled, or ViewModel cleared.
- **The Trap**: If a `CoroutineExceptionHandler` or catch block treats `CancellationException` as an unexpected error, it logs false errors or breaks structured concurrency teardown.
- **The Defensive Pattern**: In `CoroutineExceptionHandler` and `safeLaunch`, always ignore `CancellationException` or rethrow it (`if (throwable is CancellationException) return`), ensuring clean coroutine cancellation.
- **Agents Impacted**: `quality-verifier`, `cmp-ui-designer`

---

### [INSTINCT-007] Collision-Proof ID Generation in Mock Fixtures
- **Date / Phase**: Scaffolding Hardening / Data Layer
- **Trigger**: Creating multiple mock items in a loop, test, or rapid successive clicks.
- **The Trap**: Relying solely on `Clock.System.now().toEpochMilliseconds()` causes duplicate IDs if items are generated in the same millisecond. Duplicate IDs crash Compose `LazyColumn(items(items, key = { it.id }))` with `IllegalArgumentException: Key was already used`.
- **The Defensive Pattern**: Append a monotonically increasing counter: `mock_${Clock.System.now().toEpochMilliseconds()}_${++idCounter}`.
- **Agents Impacted**: `engine-data-integrator`

---

### [INSTINCT-008] Ripple & Accessibility Preservation in Debounced Clickables
- **Date / Phase**: Scaffolding Hardening / Compose UI
- **Trigger**: Applying click debouncing to cards, list items, and custom buttons.
- **The Trap**: Setting `indication = null` removes the Material ripple feedback, making clicks feel unresponsive. Omitting `enabled` and `role` breaks accessibility and disabled states.
- **The Defensive Pattern**: In `debouncedClickable`, delegate to standard Compose `clickable(enabled, onClickLabel, role)` using `rememberUpdatedState(onClick)` and monotonic multiplatform timestamp checking.
- **Agents Impacted**: `cmp-ui-designer`

---

### [INSTINCT-009] Pre-Demo State Reset in In-Memory Mock Engines
- **Date / Phase**: Scaffolding Hardening / Demo Resilience
- **Trigger**: Rehearsing user flows before the live judge demonstration.
- **The Trap**: Rehearsal entries clutter the list or trigger unintended validation errors right before judges arrive.
- **The Defensive Pattern**: Always implement `resetToSeedData()` on `MockEngineFixture` and repository interfaces, restoring clean, pristine seed state instantly with one tap.
- **Agents Impacted**: `engine-data-integrator`, `pitch-submission-lead`

---

### [INSTINCT-010] AI Engine Exception & Timeout Dual-Shielding
- **Date / Phase**: Scaffolding Hardening / Edge AI
- **Trigger**: Running on-device LiteRT/Gemini Nano inference during a live pitch.
- **The Trap**: Corrupted model files, missing native libraries, or unexpected prompts cause uncaught runtime exceptions or hang indefinitely, freezing the app.
- **The Defensive Pattern**: Wrap inference in both `withTimeoutOrNull(4000L)` and `runCatching { ... }`, providing immediate fallback to deterministic heuristic analysis if anything fails.
- **Agents Impacted**: `engine-data-integrator`, `quality-verifier`
