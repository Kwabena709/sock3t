package com.crosssend.app.protocol

import kotlinx.serialization.Serializable

@Serializable
data class DeviceInfoResponse(
    val name: String,
    val version: String,
    val protocol: Int,
)

@Serializable
data class FileOfferItem(
    val name: String,
    val size: Long,
    val mime: String,
)

@Serializable
data class OfferRequest(
    val pin: String,
    val files: List<FileOfferItem>,
)

@Serializable
data class OfferResponse(
    val sessionId: String,
    val accepted: Boolean,
)

@Serializable
data class UploadResponse(
    val received: Long,
    val savedAs: String,
)

@Serializable
data class CompleteResponse(
    val ok: Boolean,
    val filesReceived: Int,
)

data class ReceiveSession(
    val pin: String,
    val host: String,
    val port: Int,
    val deviceName: String,
) {
    fun pairingUrl(): String {
        val encodedName = java.net.URLEncoder.encode(deviceName, Charsets.UTF_8.name())
        return "crosssend://v1?h=$host&p=$port&pin=$pin&n=$encodedName"
    }
}

data class TransferSession(
    val sessionId: String,
    val files: List<FileOfferItem>,
    val receivedFiles: MutableList<String> = mutableListOf(),
)
