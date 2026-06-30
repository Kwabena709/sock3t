package com.crosssend.app.receive

import android.graphics.Bitmap
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Stop
import androidx.compose.material.icons.filled.Wifi
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilledTonalButton
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedCard
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.crosssend.app.server.DiscoveryManager

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ReceiveScreen(viewModel: ReceiveViewModel = viewModel()) {
    val state = viewModel.uiState

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("CrossSend") },
            )
        },
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(horizontal = 20.dp)
                .verticalScroll(rememberScrollState()),
            verticalArrangement = Arrangement.spacedBy(16.dp),
        ) {
            Text(
                text = if (state.isActive) "Ready to receive" else "Receive from iPhone",
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold,
            )
            Text(
                text = state.statusMessage,
                style = MaterialTheme.typography.bodyLarge,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )

            if (!state.isActive) {
                InfoCard(
                    title = "How it works",
                    body = "1. Connect both phones to the same Wi‑Fi\n" +
                        "2. Tap Start receiving on this phone\n" +
                        "3. Scan the QR code from the iPhone CrossSend app",
                )
                Button(
                    onClick = viewModel::startReceiving,
                    modifier = Modifier.fillMaxWidth(),
                ) {
                    Icon(Icons.Default.Wifi, contentDescription = null)
                    Text("Start receiving", modifier = Modifier.padding(start = 8.dp))
                }
            } else {
                ActiveReceiveCard(state)
                FilledTonalButton(
                    onClick = viewModel::stopReceiving,
                    modifier = Modifier.fillMaxWidth(),
                ) {
                    Icon(Icons.Default.Stop, contentDescription = null)
                    Text("Stop", modifier = Modifier.padding(start = 8.dp))
                }
            }

            state.lastTransferSummary?.let { summary ->
                InfoCard(title = "Last transfer", body = summary)
            }

            if (state.filesReceived.isNotEmpty()) {
                InfoCard(
                    title = "Received files",
                    body = state.filesReceived.joinToString("\n") { "• $it" },
                )
            }

            Spacer(modifier = Modifier.height(24.dp))
        }
    }
}

@Composable
private fun ActiveReceiveCard(state: ReceiveUiState) {
    OutlinedCard(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.outlinedCardColors(),
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(20.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            state.qrBitmap?.let { bitmap ->
                QrImage(bitmap)
            }

            Text(
                text = state.deviceName,
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.SemiBold,
            )

            Row(
                horizontalArrangement = Arrangement.spacedBy(24.dp),
            ) {
                MetaColumn(label = "PIN", value = state.pin)
                MetaColumn(label = "Address", value = "${state.host}:${state.port}")
            }

            Text(
                text = "Scan this QR code from the iPhone app",
                style = MaterialTheme.typography.bodyMedium,
                textAlign = TextAlign.Center,
            )
        }
    }
}

@Composable
private fun QrImage(bitmap: Bitmap) {
    Image(
        bitmap = bitmap.asImageBitmap(),
        contentDescription = "Pairing QR code",
        modifier = Modifier.size(220.dp),
    )
}

@Composable
private fun MetaColumn(label: String, value: String) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(label, style = MaterialTheme.typography.labelMedium)
        Text(
            value,
            style = MaterialTheme.typography.titleLarge,
            fontFamily = FontFamily.Monospace,
            fontWeight = FontWeight.Bold,
        )
    }
}

@Composable
private fun InfoCard(title: String, body: String) {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
            Spacer(modifier = Modifier.height(8.dp))
            Text(body, style = MaterialTheme.typography.bodyMedium)
        }
    }
}
