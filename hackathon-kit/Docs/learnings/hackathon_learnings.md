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

### [INSTINCT-007] Re-entrant Locking for Mock Database Singletons
- **Date / Phase**: Track 01 Civic Complaint Agent / Backend Architecture
- **Trigger**: Singleton database service initializing files on first `get_instance()` invocation.
- **The Trap**: Standard `threading.Lock()` in Python is non-reentrant. If `get_instance()` acquires the lock and calls `__init__()`, which internally calls `_ensure_initialized()` trying to acquire the same lock, the application deadlocks silently during module import.
- **The Defensive Pattern**: Always use `threading.RLock()` for singleton database managers or avoid acquiring locks inside constructors when already holding instance-creation locks.
- **Agents Impacted**: `engine-data-integrator`, `architect-scaffolder`


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

---

### [INSTINCT-011] Precedence Shield in Multimodal Geo-Triage & Atomic Mock Stores
- **Date / Phase**: Civic Complaint Agent / Geolocation & Mock Storage
- **Trigger**: Resolving municipal jurisdiction when citizens upload photos with EXIF metadata without typing an area.
- **The Trap**: Defaulting `user_area` to a fallback string (e.g. "Navrangpura") before inspecting photo GPS coordinates causes the fallback to unconditionally trigger, completely ignoring real photo EXIF coordinates. Furthermore, non-atomic writes to mock JSON files can corrupt state under rapid demo clicks.
- **The Defensive Pattern**: 
  1. Inspect `user_area` only if non-empty; if unprovided or unrecognized, fall back immediately to `extract_exif_coordinates(image_bytes)` before applying any municipal central default.
  2. Implement atomic file writes via temporary files and `os.replace` to prevent corrupted database state.
  3. Never use tautological test assertions (`assert ... or True`) to mask uncopied seed templates in test fixtures.
- **Agents Impacted**: `agent-engine-developer`, `quality-verifier`

### [INSTINCT-009] Daylight Asphalt Road Texture Classification & Critical Section Concurrency
- **Date / Phase**: Civic Complaint Agent / Vision Model Hardening & Concurrency Audit
- **Trigger**: Testing real-world daylight pothole images with neutral camera filenames and running concurrent ticket filings.
- **The Trap**: 
  1. Naive downsampled color threshold heuristics (`avg_g > 95 and avg_r > 90` intended for organic waste/garbage) trigger false positives on ordinary sunlit road asphalt, where mean R and G naturally reach 110–165. Real road photos get misclassified as solid waste.
  2. In database mock engines, generating sequential ticket IDs (`AMC-2026-XXXXXX`) across separate read and write lock acquisitions causes race conditions under concurrent requests where multiple threads read the same `max_id` and generate identical duplicate tracking numbers.
- **The Defensive Pattern**:
  1. In on-device computer vision classifiers, asphalt must be identified through **achromatic saturation filtering** (`HSV S < 60`, `|R-G| + |G-B| + |R-B| < 35`) combined with **Laplacian edge gradient energy** (`ImageFilter.FIND_EDGES`). Real road craters generate high edge fracture energy (`> 20`), whereas diffuse organic waste exhibits high color saturation without fracture structure.
  2. Compute localized bounding boxes dynamically via peak edge/depression grid convolution (`_detect_cavity_hotspot`) rather than static percentage boxes.
  3. Protect the entire read-generate-write sequence inside an atomic critical section using `with self._lock:` (`threading.RLock`).
### [INSTINCT-012] Boundary-Safe Hotspot Clamping & Low-Light Road Hazard Disambiguation
- **Date / Phase**: Civic Complaint Agent / Vision Edge Hardening & Quality Review
- **Trigger**: Craters occurring at extreme image borders (x/y >= 95%) and road pothole images captured in dusk/night low illumination.
- **The Trap**:
  1. Clamping bounding boxes with `bw = 96.0 - bx` without shifting `bx` causes negative widths (`bw = -0.9`) when `bx > 96.0`, corrupting bounding box DTOs and breaking downstream UI renders.
  2. Unconditionally applying localized cavity bounding boxes (`bbox = dynamic_bbox if has_real_image`) applies asphalt depression coordinates to overhead streetlight poles and garbage heaps.
  3. Simple low-luminance checks (`mean_v < 50` or `RGB < 55`) misclassify dark/wet asphalt road surfaces as `streetlight`.
- **The Defensive Pattern**:
  1. Enforce mathematical boundary clamping: `if bx + bw > 96.0: bx = max(2.0, 96.0 - bw)` and `bw = round(min(bw, 98.0 - bx), 1)`. Guaranteed positive width/height (`width > 0`, `height > 0`) across 100% of grid permutations.
  2. Gate dynamic bounding boxes strictly to matching hazard types: `bbox = dynamic_bbox if (dynamic_bbox and has_real_image and matched_issue == "pothole") else pattern["boundingBox"]`.
  3. Disambiguate dark road asphalt from streetlights: check achromatic saturation (`mean_s < 45 and channel_diff < 25`) and fracture edges before declaring an unlit streetlight corridor.
- **Agents Impacted**: `vision-engineer`, `quality-verifier`, `agent-engine-developer`
