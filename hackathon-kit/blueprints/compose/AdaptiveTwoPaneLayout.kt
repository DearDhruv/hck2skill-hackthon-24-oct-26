package com.deardhruv.hackathon.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.width
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import com.deardhruv.hackathon.ui.theme.AdaptivePaneConfig
import com.deardhruv.hackathon.ui.theme.AdaptivePaneTokens
import com.deardhruv.hackathon.ui.theme.calculateAdaptivePaneConfig

/**
 * Sleek, reactive two-pane layout container supporting phones (compact), foldables (book posture),
 * flips (tabletop flex mode), tablets (dual pane landscape/portrait), and multi-screen environments.
 *
 * Automatically adapts between single-pane, horizontal dual-pane, and vertical tabletop split
 * based on [AdaptivePaneConfig] or custom overrides.
 *
 * @param primaryPane The primary content pane (e.g. List, Dashboard, Input).
 * @param secondaryPane Optional secondary/supporting pane (e.g. Details, Preview, Analytics).
 *                      When null or when single pane mode is active, only [primaryPane] occupies the screen.
 * @param modifier Root layout modifier.
 * @param paneConfig Optional adaptive layout configuration; when null, dynamically resolves from local container constraints.
 * @param primaryPaneRatio The proportional width (0.0 to 1.0) given to [primaryPane] in horizontal dual-pane mode.
 * @param tabletopUpperRatio The proportional height (0.0 to 1.0) given to [primaryPane] in tabletop vertical mode.
 * @param showDivider Whether to render a visual separation line between the primary and secondary panes.
 * @param customDivider Optional custom composable divider to override the default hairline divider.
 */
@Composable
fun AdaptiveTwoPaneLayout(
    primaryPane: @Composable () -> Unit,
    modifier: Modifier = Modifier,
    secondaryPane: (@Composable () -> Unit)? = null,
    paneConfig: AdaptivePaneConfig? = null,
    primaryPaneRatio: Float = AdaptivePaneTokens.DEFAULT_PRIMARY_PANE_RATIO,
    tabletopUpperRatio: Float = AdaptivePaneTokens.TABLETOP_UPPER_RATIO,
    showDivider: Boolean = true,
    customDivider: (@Composable () -> Unit)? = null,
) {
    BoxWithConstraints(modifier = modifier.fillMaxSize()) {
        val effectiveConfig = paneConfig ?: calculateAdaptivePaneConfig(
            screenWidthDp = maxWidth,
            screenHeightDp = maxHeight,
        )
        val secondary = secondaryPane
        val isDualPaneActive = secondary != null && effectiveConfig.isDualPanePreferred
        val isTabletopActive = secondary != null && effectiveConfig.isTabletopMode && !effectiveConfig.isDualPanePreferred

        if (secondary != null && isDualPaneActive) {
            HorizontalTwoPaneLayout(
                primaryPane = primaryPane,
                secondaryPane = secondary,
                primaryRatio = primaryPaneRatio.coerceIn(0.2f, 0.8f),
                showDivider = showDivider,
                customDivider = customDivider,
                modifier = Modifier.fillMaxSize(),
            )
        } else if (secondary != null && isTabletopActive) {
            VerticalTwoPaneLayout(
                primaryPane = primaryPane,
                secondaryPane = secondary,
                upperRatio = tabletopUpperRatio.coerceIn(0.2f, 0.8f),
                showDivider = showDivider,
                customDivider = customDivider,
                modifier = Modifier.fillMaxSize(),
            )
        } else {
            // Single-pane mode for phones portrait, small devices, or when secondary pane is absent
            Box(modifier = Modifier.fillMaxSize()) {
                primaryPane()
            }
        }
    }
}

@Composable
private fun HorizontalTwoPaneLayout(
    primaryPane: @Composable () -> Unit,
    secondaryPane: @Composable () -> Unit,
    primaryRatio: Float,
    showDivider: Boolean,
    customDivider: (@Composable () -> Unit)?,
    modifier: Modifier = Modifier,
) {
    Row(modifier = modifier) {
        Box(
            modifier = Modifier
                .weight(primaryRatio)
                .fillMaxHeight(),
        ) {
            primaryPane()
        }

        if (showDivider) {
            if (customDivider != null) {
                customDivider()
            } else {
                Box(
                    modifier = Modifier
                        .width(AdaptivePaneTokens.dividerThickness)
                        .fillMaxHeight()
                        .background(MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f)),
                )
            }
        }

        Box(
            modifier = Modifier
                .weight(1f - primaryRatio)
                .fillMaxHeight(),
        ) {
            secondaryPane()
        }
    }
}

@Composable
private fun VerticalTwoPaneLayout(
    primaryPane: @Composable () -> Unit,
    secondaryPane: @Composable () -> Unit,
    upperRatio: Float,
    showDivider: Boolean,
    customDivider: (@Composable () -> Unit)?,
    modifier: Modifier = Modifier,
) {
    Column(modifier = modifier) {
        Box(
            modifier = Modifier
                .weight(upperRatio)
                .fillMaxWidth(),
        ) {
            primaryPane()
        }

        if (showDivider) {
            if (customDivider != null) {
                customDivider()
            } else {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(AdaptivePaneTokens.dividerThickness)
                        .background(MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f)),
                )
            }
        }

        Box(
            modifier = Modifier
                .weight(1f - upperRatio)
                .fillMaxWidth(),
        ) {
            secondaryPane()
        }
    }
}
