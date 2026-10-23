# System Architecture & Technical Specification

> **Project**: [Project Name]  
> **Platform Target**: Android, iOS, Desktop (macOS/Windows/Linux), Web (Kotlin/Wasm)  
> **Architecture Pattern**: Clean Architecture + MVI (Model-View-Intent) + Unidirectional Data Flow  

---

## 1. High-Level Architecture Diagram

```mermaid
graph TD
    subgraph UI_Layer [UI Layer - Compose Multiplatform]
        MobileUI[Mobile Phone View - Bottom Bar]
        TabletUI[Tablet/Foldable View - Nav Rail + Two-Pane]
        DesktopWebUI[Desktop & Web Wasm - Nav Drawer + Grid]
    end

    subgraph Presentation_Layer [Presentation Layer - MVI]
        StateHolder[Feature ViewModel - StateFlow]
        UIState[Immutable UiState]
        UIIntent[Sealed UiIntent Actions]
    end

    subgraph Domain_Layer [Domain Layer - Pure Kotlin]
        UseCases[Feature Use Cases & Interactors]
        DomainModels[Pure Domain Models & Entities]
        RepoContracts[Repository Interfaces]
    end

    subgraph Data_Layer [Data Layer - Offline-First]
        RepoImpl[Unified Repository Implementation]
        MockEngine[Zero-Flake Mock Data Engine]
        RemoteAPI[Ktor HTTP Client / Cloud Backend]
        LocalDB[Offline Cache / SQLite]
        EdgeAI[On-Device LiteRT / Gemini Prompt API]
    end

    MobileUI --> UIIntent
    TabletUI --> UIIntent
    DesktopWebUI --> UIIntent
    UIIntent --> StateHolder
    StateHolder --> UIState
    UIState -.-> MobileUI
    UIState -.-> TabletUI
    UIState -.-> DesktopWebUI

    StateHolder --> UseCases
    UseCases --> DomainModels
    UseCases --> RepoContracts
    RepoImpl -.-> RepoContracts

    RepoImpl --> MockEngine
    RepoImpl --> RemoteAPI
    RepoImpl --> LocalDB
    RepoImpl --> EdgeAI
```

---

## 2. Multi-Device Adaptive Matrix

| Form Factor | Screen Width | Navigation Component | Content Layout Strategy |
|---|---|---|---|
| **Mobile (Phones)** | `< 600dp` (Compact) | `NavigationBar` (Bottom) | Single-column scroll, thumb-friendly touch targets (`48dp`) |
| **Foldables & Tablets** | `600dp - 840dp` (Medium) | `NavigationRail` (Left) | Two-pane master-detail (`ListDetailPaneScaffold`) |
| **Desktop & Web Wasm** | `> 840dp` (Expanded) | `NavigationDrawer` (Expanded) | Responsive multi-column grid, persistent sidebar, keyboard shortcuts |

---

## 3. Data Flow & Concurrency Guarantees

1. **Unidirectional Data Flow**:
   - UI emits explicit user intents (`UiIntent`).
   - ViewModel processes intents on `Dispatchers.Default` / `Dispatchers.IO`.
   - ViewModel updates `MutableStateFlow<UiState>`.
   - UI observes state reactively using `collectAsState()`.
2. **Zero Main Thread Blocking (`INV-THREAD-01`)**:
   - All I/O, database interactions, network queries, and on-device AI inference are executed off the main thread.
3. **Mock-First Live Fallback (`INV-MOCK-01`)**:
   - The application boots with a rich in-memory mock engine populated with seed fixtures.
   - If cloud connectivity is available and configured, queries seamlessly pass through to live endpoints without altering domain contracts.
