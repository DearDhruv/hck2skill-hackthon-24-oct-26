# Rule: Prompt Auto-Expansion Protocol (PEP) & /boost Engine (`INV-BOOST-01`)

This rule governs how AI assistants automatically enhance, expand, and enrich terse user instructions into production-grade Kotlin Multiplatform implementations without requiring the user to do prompt engineering.

---

## 1. The Non-Prompt-Engineer & Volunteer Reality

Dhruv is not an expert prompt engineer and is volunteering on-site during a high-intensity 4-hour hackathon. Consequently:
- **Terse Instructions are the Norm**: Dhruv will send brief, high-level, or colloquial instructions (e.g. *"add search and tags"*, *"create patient registration form"*, *"make an offline expense log"*, *"fix button double-clicks"*).
- **MANDATORY AUTOMATIC ACTIVATION**: **Every prompt received—whether prefixed with `/boost` or not—MUST be treated as a candidate for automatic PEP expansion.**
- **The Golden Rule**: **NEVER stall, ask a barrage of clarifying questions, or ask Dhruv to refine or rephrase their prompt.**
- Instantly deconstruct the instruction, expand it into the complete Clean Architecture stack, cover every edge case in the Edge-Case Defense Matrix, and produce complete, compilable Kotlin code.

---

## 2. The 6-Dimensional Auto-Expansion Formula

Every prompt received is automatically expanded across seven architectural dimensions:

```
Plain / Terse User Input ──► [Prompt Auto-Expansion Protocol (PEP)]
                                      │
                                      ├── 1. Persona & 1-Flow Value Mapping (Who, Why, Primary Journey)
                                      ├── 2. Pure Domain Layer (Entities, Validation, Flow Interfaces)
                                      ├── 3. Resilient Data Engine (MockEngineFixture, Seed Data, Offline Toggle, Reset)
                                      ├── 4. MVI Presentation Machine (UiState, UiIntent, UiEffect, safeLaunch)
                                      ├── 5. Adaptive Compose UI (NavigationSuiteScaffold, 1200dp Clamping, Spacing Tokens)
                                      ├── 6. Edge-Case Defense Matrix (Empty, Error, Shimmer, Insets, Debounce, Banner)
                                      └── 7. Installed Skills Activation (INV-SKILL-01: adaptive, navigation-3, litert, styles)
```

### Dimension 1: Persona & 1-Flow Value Mapping
- Identify target persona and primary real-world pain point.
- Enforce the **1-Flow Rule**: In 4 hours, build **ONE jaw-dropping, end-to-end user flow** rather than 5 shallow or half-finished screens. (Trigger -> Intelligence / Calculation -> Actionable Output).
- Prune secondary distraction: Use simulated demo personas / guest switcher instead of full OAuth; use in-memory reactive fixtures instead of remote database provisioning.

### Dimension 2: Pure Domain Model (`domain/`)
- Pure Kotlin immutable data classes (`data class Entity(...)`).
- Strictly zero Android (`android.*`) and zero Compose UI dependencies (`androidx.compose.*`).
- Repository interface with suspending methods and reactive `Flow` emissions.
- Built-in validation rules (e.g., non-blank strings, range checks, format checks).

### Dimension 3: Zero-Flake Data Engine (`data/mock/`)
- Implement the repository interface in `Mock<Feature>EngineFixture.kt`.
- Rich, believable seed fixtures matching the hackathon theme (no "Test 1", "Item 2").
- Support offline toggle (`isOfflineMode = true`) and error simulation (`setSimulateError(true)`).
- Provide `resetToSeedData()` to instantly restore pristine data before judging.
- Monotonic ID collision prevention (`mock_${now()}_${++idCounter}`).

### Dimension 4: MVI Presentation Layer (`presentation/`)
- Immutable `UiState` with explicit states: `Loading`, `Content`, `Empty`, `Error`.
- Sealed interface `UiIntent` / `UiAction` covering every user interaction.
- Buffered `UiEffect` Channel for single-shot events (Snackbars, Navigation, Dialogs).
- Subclass `BaseMviViewModel` with `safeLaunch` (preserving `CancellationException`).

### Dimension 5: Adaptive Multi-Device UI (`ui/`)
- Responsive across all breakpoints:
  - Compact (<600dp): Bottom Navigation, single-column scrollable feed.
  - Medium (600–840dp): Navigation Rail, dual-pane Master-Detail (`AdaptiveTwoPaneLayout`).
  - Expanded (>840dp): Navigation Drawer, multi-column grid, clamped container max-width (1200dp).
- **Dhruv's Design Tokens (`INV-UI-01`)**:
  - Capsule buttons (`CircleShape` / `Spacing.buttonCornerRadius = 100.dp`).
  - 48dp minimum touch target (`Modifier.defaultMinSize(minWidth = 48.dp, minHeight = 48.dp)`).
  - 24dp card corner radius (`RoundedCornerShape(Spacing.cardCornerRadius)`).
  - High contrast in both Dark and Light themes.

### Dimension 6: Edge-Case Defense Matrix Injection (`INV-EDGE-01`)
- Render `EmptyStateCard` when data is empty.
- Render `ErrorStateCard` with retry action when failures occur.
- Render `LoadingSkeletonCard` shimmer placeholders while fetching.
- Add text truncation with `maxLines` and `overflow = TextOverflow.Ellipsis`.
- Wrap forms in `AdaptiveFormLayout` for soft keyboard avoidance (`imePadding()`).
- Use `ValidatedInputField` with inline errors and clear button.
- Use `debouncedClickable()` with ripple preserved (`INSTINCT-008`).
- Display `DemoModeBanner` with an instant offline toggle switch.

### Dimension 7: Installed Skills Activation (`INV-SKILL-01`)
- Cross-reference requirement against installed skills (`.agents/skills/`, `.gemini/config/skills/`).
- Use `adaptive` for Compose MediaQuery and responsive multi-pane setups.
- Use `navigation-3` & `navigation-event` for Jetpack Navigation 3 scenes and predictive back.
- Use `edge-to-edge` for IME keyboard and system bar insets.
- Use `litert-lm` or `litert-runtime` when building local on-device AI experiences.
- Use `styles` for styleable design components.
- Never write deprecated or improvised code when verified skill guidance exists.

---

## 3. Concrete Before & After Expansion Examples

### Example A: Terse Input = *"Add a search bar"*
- **Terse Input**: "Add search"
- **Automatic Expansion**:
  - *Domain*: `searchItems(query: String): Flow<List<Entity>>` splitting multi-token keywords.
  - *Data*: Query trimming, lowercase case-insensitive matching across title, subtitle, and tags.
  - *Presentation*: `UiIntent.SearchQueryChanged(val query: String)` debounced by 300ms.
  - *UI*: `ValidatedInputField` with `Icons.Default.Clear` trailing icon, `ImeAction.Search`, and instant `EmptyStateCard` ("No results found for '$query'") with "Clear Search" button.

### Example B: Terse Input = *"Create item form"*
- **Terse Input**: "Let users create a new task"
- **Automatic Expansion**:
  - *Domain*: `CreateTaskUseCase` with title length limits (1-80 chars) and category validation.
  - *Data*: Monotonic collision-safe ID generation and reactive `StateFlow` insertion.
  - *Presentation*: `safeLaunchWithLoading` toggling `isSubmitting`, emitting `ShowSnackbar("Task created")` effect.
  - *UI*: `AdaptiveFormLayout` with `imePadding()`, `ValidatedInputField` for title and details, capsule submit button disabled while title is blank, and `debouncedClickable` protection.

---

## 4. Autonomous Execution Rules

1. **Zero Placeholders**: Never generate `// TODO: implement later` or empty stubs. All delivered code must be fully written and ready to compile.
2. **Delivery Format**:
   - ⚡ **Expanded Scope**: Summary of how the plain instruction was decomposed.
   - 🛡️ **Edge Cases Covered**: Explicit list of empty, error, loading, and device defenses applied.
   - 💻 **Complete Implementation**: Clean Architecture code files.
