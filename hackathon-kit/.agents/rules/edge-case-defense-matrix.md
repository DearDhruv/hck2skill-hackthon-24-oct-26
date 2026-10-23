# Rule: Edge-Case Defense Matrix & Safeguards (`INV-EDGE-01`)

This rule mandates comprehensive edge-case handling across UI, Data, Concurrency, and Multiplatform targets. In a hackathon demo, unhandled edge cases are what cause app crashes, awkward freezes, and lost points.

---

## 1. The Edge-Case Defense Matrix

| Category | Potential Bug / Failure Mode | Mandatory Architectural Defense |
|---|---|---|
| **UI: Empty State** | Zero items in list renders blank, empty screen. | Render `EmptyStateCard` with themed icon, descriptive text, and a primary action button ("Create First Item"). |
| **UI: Error State** | API failure or network drop leaves user stuck. | Render `ErrorStateCard` with explicit error badge, human-readable reason, and "Retry" capsule button. |
| **UI: Loading Latency** | Screen freezes without user feedback during fetch. | Render `LoadingSkeletonCard` shimmer placeholders for lists, or centered progress with delayed timeout. |
| **UI: Text Overflow** | Long titles, names, or descriptions break layouts. | Apply `maxLines = 1` or `2` and `overflow = TextOverflow.Ellipsis` on all dynamic Text components. |
| **UI: Ultrawide Screens** | Desktop/Web 4K displays stretch cards to 2500px wide. | Wrap root content in `AdaptiveContainer(maxWidth = 1200.dp)` to clamp content and center gracefully (`INSTINCT-002`). |
| **UI: Soft Keyboard** | Mobile on-screen keyboard covers input fields and submit button. | Wrap forms in `AdaptiveFormLayout` applying `Modifier.imePadding()` and `verticalScroll(rememberScrollState())` (`INSTINCT-005`). |
| **UI: Form Validation** | Blank, whitespace, or invalid input causes crashes or bad data. | Use `ValidatedInputField` with inline error message, character counter, clear button, and IME action navigation. |
| **UI: Ripple Feedback** | Stripping ripple makes clicks feel unresponsive and buggy. | In `debouncedClickable()`, preserve Material ripple indication while enforcing monotonic time gating (`INSTINCT-008`). |
| **UI: Image Load Failures** | Missing avatar or broken image URL renders empty/crashing box. | Render `SafeAsyncImagePlaceholder` with icon badge and label fallback when image fails to load. |
| **UI: Demo Transparency** | Judges don't know whether app is offline or live. | Render `DemoModeBanner` at the top with live/mock toggle button and offline badge (`INSTINCT-004`). |
| **UI: Pointer States** | Desktop/Web lacks cursor feedback on clickable cards. | Add `.pointerHoverIcon(PointerIcon.Hand)` to all clickable surfaces and buttons. |
| **UI: Touch Targets** | Mobile users misclick small chips or icons. | Enforce `Modifier.defaultMinSize(minWidth = 48.dp, minHeight = 48.dp)` (`INV-UI-01`). |
| **Data: Empty Input** | Submitting blank or whitespace-only text causes validation crash. | Validate with `input.trim().isNotBlank()`; disable action button while input is invalid. |
| **Data: Rapid Double-Tap** | User clicks "Submit" twice rapidly, causing duplicate entries. | Use `Modifier.debouncedClickable()` and disable button during `isSubmitting = true` (`INSTINCT-003`). |
| **Data: Search Spam** | User types rapidly, triggering 20 concurrent queries. | Debounce search queries by 300ms using `Flow.debounce(300)` before filtering. |
| **Data: Key Collision** | Timestamp collision in rapid creation crashes LazyColumn keys. | Append monotonic counter to IDs: `mock_${now()}_${++idCounter}` (`INSTINCT-007`). |
| **Data: Rehearsal Clutter** | Test entries made before judging clutter demo state. | Provide `resetToSeedData()` on `MockEngineFixture` to restore pristine seed data instantly (`INSTINCT-009`). |
| **Data: Offline Outage** | Hotel Wi-Fi drops or blocks port during live judging. | **Mock-First Engine (`INV-MOCK-01`)** with instant offline switch. Never throw raw network exceptions to UI. |
| **Threading: Main Freeze** | Parsing large JSON or heavy compute on UI thread causes frame drops. | Wrap all disk, network, and heavy compute in `withContext(Dispatchers.IO)` or `Default` (`INV-THREAD-01`). |
| **Threading: Uncaught Crash** | Unexpected exception in Coroutine crashes app process. | Use `safeLaunch` with `CoroutineExceptionHandler` in `BaseMviViewModel` to catch and emit error state. |
| **Threading: Cancellation** | Swallowing CancellationException breaks structured coroutine teardown. | In `CoroutineExceptionHandler`, ignore `CancellationException` and rethrow in launch blocks (`INSTINCT-006`). |
| **Multiplatform: Wasm** | Multi-threaded dispatcher usage on Wasm browser runtime fails. | Use `Dispatchers.Default` for CPU work and standard coroutine delay; avoid blocking threads (`INSTINCT-001`). |
| **AI: Inference Hang/Crash** | On-device model hangs >4s or throws missing-library exception. | Wrap inference with both `withTimeoutOrNull(4000L)` and `runCatching`; fallback to heuristic simulation (`INSTINCT-010`). |

---

## 2. Invariant Checklist for Every Screen

Every Composable screen created must verify:
- [ ] Is there an **Empty State** view (`EmptyStateCard`) when items are empty?
- [ ] Is there an **Error State** view (`ErrorStateCard`) with a Retry button when state is Error?
- [ ] Is there a **Loading Skeleton** (`LoadingSkeletonCard`) while fetching data?
- [ ] Are all dynamic texts guarded with `maxLines` and `TextOverflow.Ellipsis`?
- [ ] Does the screen use `AdaptiveContainer` to clamp width on ultra-wide desktop monitors?
- [ ] Do forms use `AdaptiveFormLayout` with `imePadding()` for soft keyboard avoidance?
- [ ] Do text fields use `ValidatedInputField` with clear buttons and error messages?
- [ ] Do buttons and clickable items use `debouncedClickable()` with ripple preserved?
- [ ] Are all touch targets >= 48dp on mobile?
- [ ] Does the demo show `DemoModeBanner` with an instant offline mock toggle?
- [ ] Does the data engine implement `resetToSeedData()` for clean judging resets?
