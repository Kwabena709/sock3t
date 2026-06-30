package com.crosssend.app.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val BluePrimary = Color(0xFF1B6EF3)
private val BlueDark = Color(0xFF0F4EB5)

private val LightColors = lightColorScheme(
    primary = BluePrimary,
    onPrimary = Color.White,
    secondary = BlueDark,
    background = Color(0xFFF5F7FB),
    surface = Color.White,
)

private val DarkColors = darkColorScheme(
    primary = Color(0xFF6BA6FF),
    onPrimary = Color(0xFF001B44),
    secondary = BluePrimary,
    background = Color(0xFF0D1117),
    surface = Color(0xFF161B22),
)

@Composable
fun CrossSendTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = LightColors,
        content = content,
    )
}
