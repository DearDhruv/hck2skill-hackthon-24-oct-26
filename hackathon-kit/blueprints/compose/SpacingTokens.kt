package com.deardhruv.hackathon.ui.theme

import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp

/**
 * Dhruv's canonical Design Tokens for Spacing, Radiuses, and Touch Targets.
 * Enforces visual balance, zero text congestion, and consistent touch bounds.
 */
object Spacing {
    val hairline: Dp = 1.dp
    val xxs: Dp = 2.dp
    val xs: Dp = 4.dp
    val s: Dp = 8.dp
    val sm: Dp = 8.dp
    val m: Dp = 16.dp
    val md: Dp = 16.dp
    val l: Dp = 24.dp
    val lg: Dp = 24.dp
    val xl: Dp = 32.dp
    val xxl: Dp = 48.dp

    // Invariant Dimensions
    val minTouchTarget: Dp = 48.dp
    val cardCornerRadius: Dp = 24.dp
    val buttonCornerRadius: Dp = 100.dp // Enforces capsule shape styling
    val elevationLow: Dp = 2.dp
    val elevationMedium: Dp = 6.dp
}

/**
 * Shape tokens enforcing the Capsule Invariant for buttons and rounded cards.
 */
object AppShapes {
    val capsule = CircleShape
    val buttonShape = RoundedCornerShape(Spacing.buttonCornerRadius)
    val cardShape = RoundedCornerShape(Spacing.cardCornerRadius)
    val sheetShape = RoundedCornerShape(topStart = Spacing.cardCornerRadius, topEnd = Spacing.cardCornerRadius)
}

// Brand Colors: Android Slate, Kotlin Violet, Compose Blue-Green
val SlateDark = Color(0xFF0F172A)
val SlateMedium = Color(0xFF1E293B)
val SlateLight = Color(0xFFF8FAFC)
val KotlinViolet = Color(0xFF7F52FF)
val ComposeTeal = Color(0xFF00D2B4)
val AccentOrange = Color(0xFFFF7A00)

private val DarkColorScheme = darkColorScheme(
    primary = KotlinViolet,
    onPrimary = Color.White,
    primaryContainer = Color(0xFF3B1E8C),
    secondary = ComposeTeal,
    onSecondary = Color.Black,
    background = Color(0xFF0B0F17),
    surface = SlateMedium,
    onSurface = Color.White,
    surfaceVariant = Color(0xFF283548),
    onSurfaceVariant = Color(0xFFCBD5E1)
)

private val LightColorScheme = lightColorScheme(
    primary = KotlinViolet,
    onPrimary = Color.White,
    primaryContainer = Color(0xFFEADBFF),
    secondary = Color(0xFF0D9488),
    onSecondary = Color.White,
    background = SlateLight,
    surface = Color.White,
    onSurface = Color(0xFF0F172A),
    surfaceVariant = Color(0xFFE2E8F0),
    onSurfaceVariant = Color(0xFF475569)
)

@Composable
fun HackathonTheme(
    darkTheme: Boolean = true, // Default to dark mode for impressive developer aesthetic
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme

    MaterialTheme(
        colorScheme = colorScheme,
        content = content
    )
}
