package com.deardhruv.hackathon.ui.components

import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.defaultMinSize
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Clear
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.composed
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.deardhruv.hackathon.ui.theme.Spacing
import kotlinx.datetime.Clock

/**
 * Wraps content in an adaptive centered container with an optional max-width clamp.
 * Crucial for Desktop & Web widescreen monitors to prevent layouts from stretching across 4K displays.
 */
@Composable
fun AdaptiveContainer(
    modifier: Modifier = Modifier,
    maxContentWidth: Dp = 1200.dp,
    contentAlignment: Alignment = Alignment.TopCenter,
    content: @Composable () -> Unit
) {
    Box(
        modifier = modifier.fillMaxSize(),
        contentAlignment = contentAlignment
    ) {
        Box(
            modifier = Modifier
                .widthIn(max = maxContentWidth)
                .fillMaxSize()
        ) {
            content()
        }
    }
}

/**
 * Production-ready Empty State card rendered when lists or search queries return zero items.
 * Adheres to Dhruv's capsule styling invariant (INV-UI-01).
 */
@Composable
fun EmptyStateCard(
    title: String,
    description: String,
    modifier: Modifier = Modifier,
    icon: ImageVector = Icons.Default.Info,
    actionLabel: String? = null,
    onActionClick: (() -> Unit)? = null
) {
    Card(
        modifier = modifier
            .fillMaxWidth()
            .padding(Spacing.m),
        shape = RoundedCornerShape(Spacing.cardCornerRadius),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.4f)
        )
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(Spacing.xl),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Surface(
                shape = CircleShape,
                color = MaterialTheme.colorScheme.primaryContainer,
                modifier = Modifier.size(56.dp)
            ) {
                Box(contentAlignment = Alignment.Center) {
                    Icon(
                        imageVector = icon,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.primary,
                        modifier = Modifier.size(28.dp)
                    )
                }
            }

            Spacer(modifier = Modifier.height(Spacing.m))

            Text(
                text = title,
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onSurface,
                textAlign = TextAlign.Center,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )

            Spacer(modifier = Modifier.height(Spacing.xs))

            Text(
                text = description,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                textAlign = TextAlign.Center,
                maxLines = 3,
                overflow = TextOverflow.Ellipsis
            )

            if (actionLabel != null && onActionClick != null) {
                Spacer(modifier = Modifier.height(Spacing.l))
                Button(
                    onClick = onActionClick,
                    shape = CircleShape,
                    modifier = Modifier.defaultMinSize(minHeight = Spacing.minTouchTarget)
                ) {
                    Text(text = actionLabel)
                }
            }
        }
    }
}

/**
 * Resilient Error State view with explicit retry callback.
 * Guarantees that app failures display actionable feedback rather than crashing or freezing.
 */
@Composable
fun ErrorStateCard(
    errorMessage: String,
    onRetry: () -> Unit,
    modifier: Modifier = Modifier,
    title: String = "Something went wrong",
    icon: ImageVector = Icons.Default.Warning
) {
    Card(
        modifier = modifier
            .fillMaxWidth()
            .padding(Spacing.m),
        shape = RoundedCornerShape(Spacing.cardCornerRadius),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.errorContainer.copy(alpha = 0.5f)
        )
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(Spacing.xl),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Surface(
                shape = CircleShape,
                color = MaterialTheme.colorScheme.error,
                modifier = Modifier.size(48.dp)
            ) {
                Box(contentAlignment = Alignment.Center) {
                    Icon(
                        imageVector = icon,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onError,
                        modifier = Modifier.size(24.dp)
                    )
                }
            }

            Spacer(modifier = Modifier.height(Spacing.m))

            Text(
                text = title,
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onErrorContainer,
                textAlign = TextAlign.Center
            )

            Spacer(modifier = Modifier.height(Spacing.xs))

            Text(
                text = errorMessage,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onErrorContainer.copy(alpha = 0.8f),
                textAlign = TextAlign.Center,
                maxLines = 3,
                overflow = TextOverflow.Ellipsis
            )

            Spacer(modifier = Modifier.height(Spacing.l))

            OutlinedButton(
                onClick = onRetry,
                shape = CircleShape,
                modifier = Modifier.defaultMinSize(minHeight = Spacing.minTouchTarget),
                colors = ButtonDefaults.outlinedButtonColors(
                    contentColor = MaterialTheme.colorScheme.onErrorContainer
                )
            ) {
                Icon(
                    imageVector = Icons.Default.Refresh,
                    contentDescription = null,
                    modifier = Modifier.size(18.dp)
                )
                Spacer(modifier = Modifier.size(Spacing.xs))
                Text(text = "Try Again")
            }
        }
    }
}

/**
 * Shimmer Loading Skeleton item to display during initial data fetches or latency simulation.
 */
@Composable
fun LoadingSkeletonCard(
    modifier: Modifier = Modifier,
    height: Dp = 96.dp
) {
    val shimmerColors = listOf(
        MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.6f),
        MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.2f),
        MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.6f)
    )

    val transition = rememberInfiniteTransition()
    val translateAnim by transition.animateFloat(
        initialValue = 0f,
        targetValue = 1000f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 1200, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Restart
        )
    )

    val brush = Brush.linearGradient(
        colors = shimmerColors,
        start = Offset.Zero,
        end = Offset(x = translateAnim, y = translateAnim)
    )

    Box(
        modifier = modifier
            .fillMaxWidth()
            .height(height)
            .clip(RoundedCornerShape(Spacing.cardCornerRadius))
            .background(brush)
    )
}

/**
 * Debounced clickable modifier that prevents rapid double-taps and concurrent duplicate submissions.
 * Pure Kotlin Multiplatform (uses kotlinx.datetime.Clock), retains ripple indication,
 * and respects enabled state and accessibility roles.
 */
fun Modifier.debouncedClickable(
    debounceMs: Long = 500L,
    enabled: Boolean = true,
    onClickLabel: String? = null,
    role: Role? = null,
    onClick: () -> Unit
): Modifier = composed {
    val currentOnClick by rememberUpdatedState(onClick)
    var lastClickTime by remember { mutableStateOf(0L) }

    this.clickable(
        enabled = enabled,
        onClickLabel = onClickLabel,
        role = role
    ) {
        val currentTime = Clock.System.now().toEpochMilliseconds()
        if (currentTime - lastClickTime >= debounceMs) {
            lastClickTime = currentTime
            currentOnClick()
        }
    }
}

/**
 * Keyboard-aware, scrollable form container.
 * Automatically applies imePadding and vertical scrolling so on-screen keyboards
 * never obscure input fields or submit buttons on mobile devices (INV-EDGE-01, INSTINCT-005).
 */
@Composable
fun AdaptiveFormLayout(
    modifier: Modifier = Modifier,
    contentAlignment: Alignment.Horizontal = Alignment.CenterHorizontally,
    content: @Composable ColumnScope.() -> Unit
) {
    Column(
        modifier = modifier
            .fillMaxWidth()
            .imePadding()
            .verticalScroll(rememberScrollState())
            .padding(Spacing.m),
        horizontalAlignment = contentAlignment
    ) {
        content()
    }
}

/**
 * Production-ready validated text field with label, character counter, error message,
 * clear trailing icon, and IME action handling.
 */
@Composable
fun ValidatedInputField(
    value: String,
    onValueChange: (String) -> Unit,
    label: String,
    modifier: Modifier = Modifier,
    placeholder: String? = null,
    errorMessage: String? = null,
    leadingIcon: ImageVector? = null,
    maxLength: Int? = null,
    singleLine: Boolean = true,
    keyboardType: KeyboardType = KeyboardType.Text,
    imeAction: ImeAction = ImeAction.Next,
    onImeAction: (() -> Unit)? = null
) {
    Column(modifier = modifier.fillMaxWidth()) {
        OutlinedTextField(
            value = value,
            onValueChange = { input ->
                if (maxLength == null || input.length <= maxLength) {
                    onValueChange(input)
                }
            },
            label = { Text(text = label) },
            placeholder = placeholder?.let { { Text(text = it) } },
            isError = errorMessage != null,
            singleLine = singleLine,
            shape = RoundedCornerShape(16.dp),
            modifier = Modifier
                .fillMaxWidth()
                .defaultMinSize(minHeight = Spacing.minTouchTarget),
            leadingIcon = leadingIcon?.let {
                { Icon(imageVector = it, contentDescription = null) }
            },
            trailingIcon = {
                if (value.isNotEmpty()) {
                    IconButton(onClick = { onValueChange("") }) {
                        Icon(imageVector = Icons.Default.Clear, contentDescription = "Clear text")
                    }
                }
            },
            supportingText = {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text(
                        text = errorMessage ?: "",
                        color = MaterialTheme.colorScheme.error,
                        style = MaterialTheme.typography.bodySmall,
                        modifier = Modifier.weight(1f)
                    )
                    if (maxLength != null) {
                        Text(
                            text = "${value.length}/$maxLength",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            },
            keyboardOptions = KeyboardOptions(
                keyboardType = keyboardType,
                imeAction = imeAction
            ),
            keyboardActions = KeyboardActions(
                onAny = { onImeAction?.invoke() }
            )
        )
    }
}

/**
 * Prominent banner for live stage judging. Displays whether the application is running
 * against the Zero-Flake Offline Mock Engine or Live API, with an instant toggle button.
 * (INV-MOCK-01, INSTINCT-004).
 */
@Composable
fun DemoModeBanner(
    isMockMode: Boolean,
    onToggle: () -> Unit,
    modifier: Modifier = Modifier
) {
    Surface(
        modifier = modifier.fillMaxWidth(),
        color = if (isMockMode) MaterialTheme.colorScheme.tertiaryContainer else MaterialTheme.colorScheme.primaryContainer,
        shape = RoundedCornerShape(Spacing.cardCornerRadius / 2)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = Spacing.m, vertical = Spacing.s),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.weight(1f)
            ) {
                Icon(
                    imageVector = if (isMockMode) Icons.Default.Info else Icons.Default.CheckCircle,
                    contentDescription = null,
                    tint = if (isMockMode) MaterialTheme.colorScheme.tertiary else MaterialTheme.colorScheme.primary,
                    modifier = Modifier.size(20.dp)
                )
                Spacer(modifier = Modifier.size(Spacing.s))
                Column {
                    Text(
                        text = if (isMockMode) "⚡ Offline Demo Engine Active" else "🌐 Live API Connected",
                        style = MaterialTheme.typography.labelLarge,
                        fontWeight = FontWeight.Bold,
                        color = if (isMockMode) MaterialTheme.colorScheme.onTertiaryContainer else MaterialTheme.colorScheme.onPrimaryContainer
                    )
                    Text(
                        text = if (isMockMode) "Zero network dependency (Wi-Fi safe)" else "Syncing with cloud endpoints",
                        style = MaterialTheme.typography.bodySmall,
                        color = if (isMockMode) MaterialTheme.colorScheme.onTertiaryContainer.copy(alpha = 0.8f) else MaterialTheme.colorScheme.onPrimaryContainer.copy(alpha = 0.8f)
                    )
                }
            }

            Button(
                onClick = onToggle,
                shape = CircleShape,
                modifier = Modifier.defaultMinSize(minHeight = 36.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = if (isMockMode) MaterialTheme.colorScheme.tertiary else MaterialTheme.colorScheme.primary
                )
            ) {
                Text(
                    text = if (isMockMode) "Go Live" else "Go Offline",
                    style = MaterialTheme.typography.labelMedium
                )
            }
        }
    }
}

/**
 * Safe image fallback placeholder for offline mode or network image load failures.
 * Prevents blank spaces or image loading crashes during offline live demos.
 */
@Composable
fun SafeAsyncImagePlaceholder(
    modifier: Modifier = Modifier,
    label: String = "No Image",
    icon: ImageVector = Icons.Default.Info
) {
    Surface(
        modifier = modifier,
        shape = RoundedCornerShape(Spacing.s),
        color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
    ) {
        Column(
            modifier = Modifier.fillMaxSize(),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Icon(
                imageVector = icon,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.6f),
                modifier = Modifier.size(28.dp)
            )
            Spacer(modifier = Modifier.height(Spacing.xs))
            Text(
                text = label,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.7f),
                textAlign = TextAlign.Center,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        }
    }
}
