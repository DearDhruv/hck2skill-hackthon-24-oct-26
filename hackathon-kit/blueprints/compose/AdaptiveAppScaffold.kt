package com.deardhruv.hackathon.ui.navigation

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.material3.adaptive.navigationsuite.NavigationSuiteScaffold
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp
import com.deardhruv.hackathon.ui.components.AdaptiveContainer

/**
 * Top-level destinations for the hackathon application.
 */
enum class AppDestination(
    val title: String,
    val icon: ImageVector,
    val description: String
) {
    HOME("Home", Icons.Default.Home, "Overview and primary actions"),
    EXPLORE("Explore", Icons.Default.Info, "Discover insights and deep dives"),
    SETTINGS("Settings", Icons.Default.Settings, "Preferences and offline toggle")
}

/**
 * Production-ready Adaptive Navigation Shell for Compose Multiplatform.
 * Automatically renders:
 * - Bottom Navigation on Compact screens (Mobile Phones < 600dp)
 * - Navigation Rail on Medium screens (Tablets & Foldables 600dp - 840dp)
 * - Navigation Drawer on Expanded screens (Desktop & Web Wasm > 840dp)
 * - Built-in AdaptiveContainer clamping maximum content width to 1200dp on ultra-wide desktop monitors.
 */
@Composable
fun AdaptiveAppScaffold(
    selectedDestination: AppDestination = AppDestination.HOME,
    onDestinationChanged: (AppDestination) -> Unit = {},
    content: @Composable (AppDestination) -> Unit
) {
    NavigationSuiteScaffold(
        navigationSuiteItems = {
            AppDestination.entries.forEach { destination ->
                item(
                    selected = selectedDestination == destination,
                    onClick = { onDestinationChanged(destination) },
                    icon = {
                        Icon(
                            imageVector = destination.icon,
                            contentDescription = destination.description
                        )
                    },
                    label = {
                        Text(text = destination.title)
                    }
                )
            }
        }
    ) {
        AdaptiveContainer(maxContentWidth = 1200.dp) {
            content(selectedDestination)
        }
    }
}
