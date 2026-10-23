---
trigger: always_on
description: "Adaptive UI and design system standards for Compose Multiplatform. Enforces NavigationSuiteScaffold, multi-pane layouts, Spacing tokens, and capsule styling."
---

# Rule: Adaptive UI & Design System Standards

This rule governs responsive UI design, multi-device adaptive navigation, and design token consistency across Mobile, Tablet, Desktop, and Web.

## 1. Multi-Device Adaptive Breakpoints

| Window Width | Form Factor | Navigation Pattern | Content Layout |
|---|---|---|---|
| **< 600dp (Compact)** | Mobile Phones | Bottom Navigation Bar | Single-column scrollable feed (`LazyColumn`) |
| **600dp - 840dp (Medium)** | Tablets, Unfolded Foldables | Navigation Rail (Left Edge) | Two-pane split (`ListDetailPaneScaffold` or 2-column grid) |
| **> 840dp (Expanded)** | Laptops, Desktop, Web Wasm | Navigation Drawer (Expanded/Modal) | Multi-column grid, responsive cards, preview panel |

---

## 2. Adaptive Navigation Scaffold (`NavigationSuiteScaffold`)

Always use `NavigationSuiteScaffold` from `androidx.compose.material3.adaptive.navigationsuite`:

```kotlin
@Composable
fun AppAdaptiveRoot(
    currentDestination: AppDestination,
    onNavigate: (AppDestination) -> Unit,
    content: @Composable () -> Unit
) {
    NavigationSuiteScaffold(
        navigationSuiteItems = {
            AppDestination.entries.forEach { destination ->
                item(
                    selected = currentDestination == destination,
                    onClick = { onNavigate(destination) },
                    icon = { Icon(destination.icon, contentDescription = destination.title) },
                    label = { Text(destination.title) }
                )
            }
        }
    ) {
        content()
    }
}
```

---

## 3. Dhruv's Design Tokens & Capsule Invariant (`INV-UI-01`)

Always use `Spacing.kt` tokens across all UI components:

```kotlin
object Spacing {
    val xxs = 2.dp
    val xs = 4.dp
    val s = 8.dp
    val m = 16.dp
    val l = 24.dp
    val xl = 32.dp
    val xxl = 48.dp

    // Invariants
    val minTouchTarget = 48.dp
    val cardCornerRadius = 24.dp
    val buttonCornerRadius = 100.dp // Capsule styling
}
```

### Invariants:
1. **Capsule Styling**: All buttons (`Button`, `OutlinedButton`, `FilledTonalButton`), action chips, search bars, and pills MUST use `CircleShape` or `RoundedCornerShape(Spacing.buttonCornerRadius)`.
2. **Cards & Containers**: Cards and bottom sheet surfaces MUST use `RoundedCornerShape(Spacing.cardCornerRadius)`.
3. **Touch Targets**: All clickable components MUST satisfy `Modifier.defaultMinSize(minWidth = Spacing.minTouchTarget, minHeight = Spacing.minTouchTarget)`.
4. **Section Headers**: Section headers MUST include an icon badge and clear typography.

---

## 4. Theme & High-Contrast Typography
- Support dynamic dark/light theme switching.
- Dark theme default palette: Surface `#121212`, Primary Slate `#1E293B`, Kotlin Violet `#7F52FF`, Accent Cyan/Teal `#00D2B4`.
- Light theme default palette: Surface `#F8FAFC`, Primary Slate `#0F172A`, Kotlin Violet `#6B38FB`, Accent Teal `#0D9488`.
