---
trigger: always_on
description: "Clean Architecture standards for Kotlin Multiplatform and Compose Multiplatform projects. Enforces strict layer boundaries, pure domain models, and MVI/UDF state flow."
---

# Rule: Clean Architecture for Kotlin Multiplatform (KMP)

This rule enforces strict Clean Architecture separation across all multiplatform targets (Android, iOS, Desktop JVM, Web Wasm/JS).

## 1. Architectural Layers & Boundaries

```
[UI Layer: Compose MP] ──► [Presentation: MVI/StateFlow] ──► [Domain: Pure Kotlin] ◄── [Data: Repositories/Mock/Ktor]
```

### 1.1 Domain Layer (`com.deardhruv.<app>.domain.*`)
- **Strictly Pure Kotlin**: Zero Android dependencies (`android.*`) and zero Compose UI dependencies (`androidx.compose.*`).
- Contains:
  - `model/`: Pure Kotlin immutable data classes (`data class TaskItem(...)`).
  - `repository/`: Repository interfaces declaring suspending functions and Flows (`interface TaskRepository { fun observeTasks(): Flow<List<TaskItem>> }`).
  - `usecase/`: Single-responsibility use cases (`class GetTasksUseCase(...)`).

### 1.2 Data Layer (`com.deardhruv.<app>.data.*`)
- Implements domain repository interfaces.
- Contains:
  - `mock/`: `MockEngineFixture.kt` generating instant, rich seed data with realistic latency.
  - `remote/`: Ktor HTTP client, DTOs with `@Serializable`, API endpoints.
  - `local/`: Local persistence (SQLDelight / Room / in-memory cache).
  - `repository/`: Unified repository implementation dynamically delegating between Mock and Remote engines based on `isMockModeEnabled`.

### 1.3 Presentation Layer (`com.deardhruv.<app>.presentation.*`)
- Unidirectional Data Flow (UDF) / MVI:
  - `UiState`: Single immutable data class representing the whole screen state.
  - `UiIntent` / `UiAction`: Sealed interface for all user interactions.
  - `UiEffect`: Single-shot events (e.g. `ShowSnackbar`, `NavigateToDetails`).
- ViewModels expose `StateFlow<UiState>` created using `stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), InitialState)`.

### 1.4 UI Layer (`com.deardhruv.<app>.ui.*`)
- Pure declarative Compose Multiplatform.
- Screens MUST be split into small sub-composables in `ui/<feature>/components/`.
- No business logic or I/O inside Composable functions.

---

## 2. Dependency Inversion Rules
- Outer layers (UI, Data) depend on Domain abstractions.
- Domain NEVER imports or depends on Data or UI.
- Use simple constructor injection or lightweight Service Locator / Koin `singleOf(...)`. Avoid complex reflection-based DI frameworks.
