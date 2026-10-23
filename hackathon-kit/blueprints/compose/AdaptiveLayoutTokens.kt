package com.deardhruv.hackathon.ui.theme

import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.platform.LocalWindowInfo
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp

/**
 * Window width size classes conforming to Material 3 adaptive specifications.
 */
enum class WindowWidthClass {
    Compact,
    Medium,
    Expanded
}

/**
 * Window height size classes conforming to Material 3 adaptive specifications.
 */
enum class WindowHeightClass {
    Compact,
    Medium,
    Expanded
}

/**
 * Encapsulates adaptive screen geometry, window classes, and device postures
 * (such as foldable book mode or flip tabletop mode) to power responsive layouts.
 */
data class AdaptivePaneConfig(
    val widthClass: WindowWidthClass,
    val heightClass: WindowHeightClass,
    val screenWidthDp: Dp,
    val screenHeightDp: Dp,
    val isDualPanePreferred: Boolean,
    val isTabletopMode: Boolean,
    val isBookPosture: Boolean,
    val isUltraTallAspect: Boolean = false,
    val isCompactCoverScreen: Boolean = false,
)

/**
 * Canonical Material 3 breakpoint thresholds for adaptive layout classification.
 */
object AdaptiveBreakpointTokens {
    val EXPANDED_WIDTH_BREAKPOINT: Dp = 840.dp
    val MEDIUM_WIDTH_BREAKPOINT: Dp = 600.dp
    val EXPANDED_HEIGHT_BREAKPOINT: Dp = 900.dp
    val MEDIUM_HEIGHT_BREAKPOINT: Dp = 480.dp
    val FALLBACK_CONTAINER_WIDTH: Dp = 360.dp
    val FALLBACK_CONTAINER_HEIGHT: Dp = 640.dp
    val COMPACT_COVER_SCREEN_MAX_BOUND: Dp = 420.dp
}

/**
 * Pure calculation function for [AdaptivePaneConfig], enabling straightforward unit testing
 * and headless validation without requiring active Android/JVM Compose hosts.
 */
fun calculateAdaptivePaneConfig(
    screenWidthDp: Dp,
    screenHeightDp: Dp,
): AdaptivePaneConfig {
    val widthClass = when {
        screenWidthDp >= AdaptiveBreakpointTokens.EXPANDED_WIDTH_BREAKPOINT -> WindowWidthClass.Expanded
        screenWidthDp >= AdaptiveBreakpointTokens.MEDIUM_WIDTH_BREAKPOINT -> WindowWidthClass.Medium
        else -> WindowWidthClass.Compact
    }

    val heightClass = when {
        screenHeightDp >= AdaptiveBreakpointTokens.EXPANDED_HEIGHT_BREAKPOINT -> WindowHeightClass.Expanded
        screenHeightDp >= AdaptiveBreakpointTokens.MEDIUM_HEIGHT_BREAKPOINT -> WindowHeightClass.Medium
        else -> WindowHeightClass.Compact
    }

    val isDualPanePreferred = (widthClass >= WindowWidthClass.Medium && heightClass != WindowHeightClass.Compact)
    val isTabletopMode = heightClass == WindowHeightClass.Compact && widthClass >= WindowWidthClass.Medium
    val isBookPosture = widthClass == WindowWidthClass.Medium && heightClass != WindowHeightClass.Compact

    val aspectRatio = if (screenWidthDp.value > 0f) screenHeightDp.value / screenWidthDp.value else 1f
    val isUltraTallAspect = aspectRatio >= 2.1f
    val isCompactCoverScreen = screenWidthDp <= AdaptiveBreakpointTokens.COMPACT_COVER_SCREEN_MAX_BOUND &&
            screenHeightDp <= AdaptiveBreakpointTokens.COMPACT_COVER_SCREEN_MAX_BOUND

    return AdaptivePaneConfig(
        widthClass = widthClass,
        heightClass = heightClass,
        screenWidthDp = screenWidthDp,
        screenHeightDp = screenHeightDp,
        isDualPanePreferred = isDualPanePreferred,
        isTabletopMode = isTabletopMode,
        isBookPosture = isBookPosture,
        isUltraTallAspect = isUltraTallAspect,
        isCompactCoverScreen = isCompactCoverScreen,
    )
}

/**
 * Observes current window geometry reactively and returns the corresponding [AdaptivePaneConfig].
 * Automatically updates on screen resize, orientation changes, split-screen mode, and fold/unfold.
 */
@Composable
fun rememberAdaptivePaneConfig(): AdaptivePaneConfig {
    val windowInfo = LocalWindowInfo.current
    val density = LocalDensity.current
    val containerSize = windowInfo.containerSize

    return remember(containerSize, density) {
        val widthDp = if (containerSize.width > 0) {
            with(density) { containerSize.width.toDp() }
        } else {
            AdaptiveBreakpointTokens.FALLBACK_CONTAINER_WIDTH
        }
        val heightDp = if (containerSize.height > 0) {
            with(density) { containerSize.height.toDp() }
        } else {
            AdaptiveBreakpointTokens.FALLBACK_CONTAINER_HEIGHT
        }
        calculateAdaptivePaneConfig(screenWidthDp = widthDp, screenHeightDp = heightDp)
    }
}

/**
 * Design tokens specific to multi-pane and adaptive layouts.
 */
object AdaptivePaneTokens {
    val minPaneWidth: Dp = 320.dp
    val dividerThickness: Dp = Spacing.hairline
    val paneGutter: Dp = Spacing.md
    const val DEFAULT_PRIMARY_PANE_RATIO: Float = 0.50f
    const val MASTER_DETAIL_PRIMARY_RATIO: Float = 0.40f
    const val TABLETOP_UPPER_RATIO: Float = 0.55f
}
