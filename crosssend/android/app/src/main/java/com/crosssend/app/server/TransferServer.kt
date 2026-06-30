package com.crosssend.app.server

import android.content.ContentValues
import android.content.Context
import android.os.Build
import android.os.Environment
import android.provider.MediaStore
import com.crosssend.app.protocol.CompleteResponse
import com.crosssend.app.protocol.DeviceInfoResponse
import com.crosssend.app.protocol.OfferRequest
import com.crosssend.app.protocol.OfferResponse
import com.crosssend.app.protocol.ReceiveSession
import com.crosssend.app.protocol.TransferSession
import com.crosssend.app.protocol.UploadResponse
import io.ktor.http.HttpStatusCode
import io.ktor.serialization.kotlinx.json.json
import io.ktor.server.application.call
import io.ktor.server.application.install
import io.ktor.server.engine.embeddedServer
import io.ktor.server.netty.Netty
import io.ktor.server.plugins.contentnegotiation.ContentNegotiation
import io.ktor.server.request.receive
import io.ktor.server.response.respond
import io.ktor.server.routing.get
import io.ktor.server.routing.post
import io.ktor.server.routing.put
import io.ktor.server.routing.routing
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.serialization.json.Json
import java.io.File
import java.io.FileOutputStream
import java.util.Base64
import java.util.UUID
import java.util.concurrent.ConcurrentHashMap

class TransferServer(
    private val context: Context,
    private val deviceName: String,
    private val activeSessionProvider: () -> ReceiveSession?,
    private val onTransferStarted: (TransferSession) -> Unit,
    private val onFileReceived: (String, Long) -> Unit,
    private val onTransferComplete: (Int) -> Unit,
) {
    private val sessions = ConcurrentHashMap<String, TransferSession>()
    private var server: io.ktor.server.engine.ApplicationEngine? = null

    fun start(port: Int = DiscoveryManager.DEFAULT_PORT) {
        if (server != null) return

        server = embeddedServer(Netty, port = port) {
            install(ContentNegotiation) {
                json(
                    Json {
                        ignoreUnknownKeys = true
                        encodeDefaults = true
                    },
                )
            }

            routing {
                get("/v1/info") {
                    call.respond(
                        DeviceInfoResponse(
                            name = deviceName,
                            version = "1.0.0",
                            protocol = 1,
                        ),
                    )
                }

                post("/v1/offer") {
                    val receiveSession = activeSessionProvider()
                        ?: return@post call.respond(HttpStatusCode.ServiceUnavailable, "Receive mode is not active")

                    val offer = call.receive<OfferRequest>()
                    if (offer.pin != receiveSession.pin) {
                        return@post call.respond(
                            HttpStatusCode.Forbidden,
                            OfferResponse(sessionId = "", accepted = false),
                        )
                    }

                    val sessionId = UUID.randomUUID().toString()
                    val transferSession = TransferSession(sessionId = sessionId, files = offer.files)
                    sessions[sessionId] = transferSession
                    onTransferStarted(transferSession)

                    call.respond(OfferResponse(sessionId = sessionId, accepted = true))
                }

                put("/v1/upload/{sessionId}/{fileIndex}") {
                    val sessionId = call.parameters["sessionId"]
                        ?: return@put call.respond(HttpStatusCode.BadRequest, "Missing sessionId")
                    val fileIndex = call.parameters["fileIndex"]?.toIntOrNull()
                        ?: return@put call.respond(HttpStatusCode.BadRequest, "Missing fileIndex")

                    val transferSession = sessions[sessionId]
                        ?: return@put call.respond(HttpStatusCode.NotFound, "Unknown session")

                    val fileMeta = transferSession.files.getOrNull(fileIndex)
                        ?: return@put call.respond(HttpStatusCode.BadRequest, "Invalid file index")

                    val encodedName = call.request.headers["X-File-Name"]
                        ?: return@put call.respond(HttpStatusCode.BadRequest, "Missing X-File-Name")
                    val fileName = String(Base64.getDecoder().decode(encodedName), Charsets.UTF_8)
                    val mimeType = call.request.headers["X-File-Mime"] ?: fileMeta.mime

                    val bytes = withContext(Dispatchers.IO) {
                        call.receive<ByteArray>()
                    }

                    val savedName = withContext(Dispatchers.IO) {
                        saveFile(fileName, mimeType, bytes)
                    }

                    transferSession.receivedFiles.add(savedName)
                    onFileReceived(savedName, bytes.size.toLong())

                    call.respond(
                        UploadResponse(
                            received = bytes.size.toLong(),
                            savedAs = savedName,
                        ),
                    )
                }

                post("/v1/complete/{sessionId}") {
                    val sessionId = call.parameters["sessionId"]
                        ?: return@post call.respond(HttpStatusCode.BadRequest, "Missing sessionId")

                    val transferSession = sessions.remove(sessionId)
                        ?: return@post call.respond(HttpStatusCode.NotFound, "Unknown session")

                    onTransferComplete(transferSession.receivedFiles.size)
                    call.respond(
                        CompleteResponse(
                            ok = true,
                            filesReceived = transferSession.receivedFiles.size,
                        ),
                    )
                }
            }
        }.start(wait = false)
    }

    fun stop() {
        server?.stop(1000, 2000)
        server = null
        sessions.clear()
    }

    private fun saveFile(fileName: String, mimeType: String, bytes: ByteArray): String {
        if (mimeType.startsWith("image/") || mimeType.startsWith("video/")) {
            return saveToMediaStore(fileName, mimeType, bytes)
        }
        return saveToDownloads(fileName, bytes)
    }

    private fun saveToMediaStore(fileName: String, mimeType: String, bytes: ByteArray): String {
        val collection = if (mimeType.startsWith("video/")) {
            MediaStore.Video.Media.EXTERNAL_CONTENT_URI
        } else {
            MediaStore.Images.Media.EXTERNAL_CONTENT_URI
        }

        val values = ContentValues().apply {
            put(MediaStore.MediaColumns.DISPLAY_NAME, fileName)
            put(MediaStore.MediaColumns.MIME_TYPE, mimeType)
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                put(MediaStore.MediaColumns.RELATIVE_PATH, Environment.DIRECTORY_PICTURES + "/CrossSend")
                put(MediaStore.MediaColumns.IS_PENDING, 1)
            }
        }

        val resolver = context.contentResolver
        val uri = resolver.insert(collection, values)
            ?: return saveToDownloads(fileName, bytes)

        resolver.openOutputStream(uri)?.use { it.write(bytes) }

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            values.clear()
            values.put(MediaStore.MediaColumns.IS_PENDING, 0)
            resolver.update(uri, values, null, null)
        }

        return fileName
    }

    private fun saveToDownloads(fileName: String, bytes: ByteArray): String {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            val values = ContentValues().apply {
                put(MediaStore.Downloads.DISPLAY_NAME, fileName)
                put(MediaStore.Downloads.MIME_TYPE, "application/octet-stream")
                put(MediaStore.Downloads.RELATIVE_PATH, Environment.DIRECTORY_DOWNLOADS + "/CrossSend")
                put(MediaStore.Downloads.IS_PENDING, 1)
            }
            val resolver = context.contentResolver
            val uri = resolver.insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, values)
                ?: throw IllegalStateException("Unable to create download entry")

            resolver.openOutputStream(uri)?.use { it.write(bytes) }
            values.clear()
            values.put(MediaStore.Downloads.IS_PENDING, 0)
            resolver.update(uri, values, null, null)
            return fileName
        }

        val dir = File(
            Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS),
            "CrossSend",
        )
        if (!dir.exists()) dir.mkdirs()
        val outFile = File(dir, fileName)
        FileOutputStream(outFile).use { it.write(bytes) }
        return outFile.name
    }
}
