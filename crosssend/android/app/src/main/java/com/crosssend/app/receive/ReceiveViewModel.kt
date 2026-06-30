package com.crosssend.app.receive

import android.app.Application
import android.graphics.Bitmap
import android.os.Build
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.crosssend.app.protocol.ReceiveSession
import com.crosssend.app.server.DiscoveryManager
import com.crosssend.app.server.TransferForegroundService
import com.crosssend.app.server.TransferServer
import kotlinx.coroutines.launch

data class ReceiveUiState(
    val isActive: Boolean = false,
    val deviceName: String = "",
    val host: String = "",
    val port: Int = DiscoveryManager.DEFAULT_PORT,
    val pin: String = "",
    val pairingUrl: String = "",
    val qrBitmap: Bitmap? = null,
    val statusMessage: String = "Tap Start to receive files from iPhone",
    val filesReceived: List<String> = emptyList(),
    val lastTransferSummary: String? = null,
)

class ReceiveViewModel(application: Application) : AndroidViewModel(application) {
    var uiState by mutableStateOf(ReceiveUiState())
        private set

    private var discoveryManager: DiscoveryManager? = null
    private var transferServer: TransferServer? = null
    private var activeSession: ReceiveSession? = null

    fun startReceiving() {
        if (uiState.isActive) return

        val context = getApplication<Application>()
        val deviceName = Build.MODEL.ifBlank { "Android device" }
        val port = DiscoveryManager.DEFAULT_PORT

        TransferForegroundService.start(context)

        transferServer = TransferServer(
            context = context,
            deviceName = deviceName,
            activeSessionProvider = { activeSession },
            onTransferStarted = { session ->
                viewModelScope.launch {
                    val names = session.files.joinToString { it.name }
                    uiState = uiState.copy(statusMessage = "Receiving: $names")
                    TransferForegroundService.update(
                        context,
                        "Receiving from iPhone",
                        names,
                    )
                }
            },
            onFileReceived = { name, size ->
                viewModelScope.launch {
                    val kb = size / 1024
                    uiState = uiState.copy(
                        filesReceived = uiState.filesReceived + name,
                        statusMessage = "Saved $name (${kb} KB)",
                    )
                    TransferForegroundService.update(
                        context,
                        "Received $name",
                        "${kb} KB saved to device",
                    )
                }
            },
            onTransferComplete = { count ->
                viewModelScope.launch {
                    uiState = uiState.copy(
                        lastTransferSummary = "$count file(s) received successfully",
                        statusMessage = "Ready for next transfer",
                    )
                    TransferForegroundService.update(
                        context,
                        "Transfer complete",
                        "$count file(s) saved",
                    )
                }
            },
        ).also { it.start(port) }

        discoveryManager = DiscoveryManager(context, port).also { manager ->
            manager.startAdvertising(deviceName) { session ->
                viewModelScope.launch {
                    activeSession = session
                    val qrBitmap = DiscoveryManager.createQrBitmap(session.pairingUrl())
                    uiState = uiState.copy(
                        isActive = true,
                        deviceName = deviceName,
                        host = session.host,
                        port = session.port,
                        pin = session.pin,
                        pairingUrl = session.pairingUrl(),
                        qrBitmap = qrBitmap,
                        statusMessage = "Waiting for iPhone to connect…",
                        filesReceived = emptyList(),
                        lastTransferSummary = null,
                    )
                }
            }
        }
    }

    fun stopReceiving() {
        discoveryManager?.stopAdvertising()
        discoveryManager = null
        transferServer?.stop()
        transferServer = null
        activeSession = null
        TransferForegroundService.stop(getApplication())

        uiState = uiState.copy(
            isActive = false,
            qrBitmap = null,
            pin = "",
            pairingUrl = "",
            statusMessage = "Receive mode stopped",
        )
    }

    override fun onCleared() {
        stopReceiving()
        super.onCleared()
    }
}
