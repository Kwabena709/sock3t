package com.crosssend.app.server

import android.content.Context
import android.graphics.Bitmap
import android.graphics.Color
import android.net.nsd.NsdManager
import android.net.nsd.NsdServiceInfo
import android.net.wifi.WifiManager
import com.crosssend.app.protocol.ReceiveSession
import com.google.zxing.BarcodeFormat
import com.google.zxing.qrcode.QRCodeWriter
import java.net.Inet4Address
import java.net.NetworkInterface
import java.util.UUID
import kotlin.random.Random

class DiscoveryManager(
    private val context: Context,
    private val port: Int,
) {
    private val nsdManager = context.getSystemService(NsdManager::class.java)
    private var registrationListener: NsdManager.RegistrationListener? = null
    private var multicastLock: WifiManager.MulticastLock? = null

    fun startAdvertising(deviceName: String, onRegistered: (ReceiveSession) -> Unit) {
        acquireMulticastLock()

        val host = getLocalIpv4() ?: "0.0.0.0"
        val pin = Random.nextInt(0, 1_000_000).toString().padStart(6, '0')
        val session = ReceiveSession(
            pin = pin,
            host = host,
            port = port,
            deviceName = deviceName,
        )

        val serviceInfo = NsdServiceInfo().apply {
            serviceName = "CrossSend-${UUID.randomUUID().toString().take(8)}"
            serviceType = SERVICE_TYPE
            setPort(port)
        }

        val listener = object : NsdManager.RegistrationListener {
            override fun onServiceRegistered(info: NsdServiceInfo) {
                onRegistered(session)
            }

            override fun onRegistrationFailed(serviceInfo: NsdServiceInfo, errorCode: Int) {
                onRegistered(session)
            }

            override fun onServiceUnregistered(serviceInfo: NsdServiceInfo) = Unit

            override fun onUnregistrationFailed(serviceInfo: NsdServiceInfo, errorCode: Int) = Unit
        }

        registrationListener = listener
        nsdManager.registerService(serviceInfo, NsdManager.PROTOCOL_DNS_SD, listener)
    }

    fun stopAdvertising() {
        registrationListener?.let { listener ->
            runCatching { nsdManager.unregisterService(listener) }
        }
        registrationListener = null
        releaseMulticastLock()
    }

    private fun acquireMulticastLock() {
        val wifi = context.applicationContext.getSystemService(WifiManager::class.java)
        multicastLock = wifi.createMulticastLock("crosssend-mdns").apply {
            setReferenceCounted(true)
            acquire()
        }
    }

    private fun releaseMulticastLock() {
        multicastLock?.let {
            if (it.isHeld) it.release()
        }
        multicastLock = null
    }

    companion object {
        const val SERVICE_TYPE = "_crosssend._tcp."
        const val DEFAULT_PORT = 53317

        fun getLocalIpv4(): String? {
            val interfaces = NetworkInterface.getNetworkInterfaces() ?: return null
            for (networkInterface in interfaces) {
                if (!networkInterface.isUp || networkInterface.isLoopback) continue
                for (address in networkInterface.inetAddresses) {
                    if (address is Inet4Address && !address.isLoopbackAddress) {
                        return address.hostAddress
                    }
                }
            }
            return null
        }

        fun createQrBitmap(content: String, size: Int = 512): Bitmap {
            val matrix = QRCodeWriter().encode(content, BarcodeFormat.QR_CODE, size, size)
            val pixels = IntArray(size * size)
            for (y in 0 until size) {
                for (x in 0 until size) {
                    pixels[y * size + x] = if (matrix[x, y]) Color.BLACK else Color.WHITE
                }
            }
            return Bitmap.createBitmap(pixels, size, size, Bitmap.Config.ARGB_8888)
        }
    }
}
