package com.crosssend.app.server

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.os.Build
import android.os.IBinder
import androidx.core.app.NotificationCompat
import com.crosssend.app.MainActivity
import com.crosssend.app.R

class TransferForegroundService : Service() {
    override fun onBind(intent: Intent?): IBinder? = null

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        when (intent?.action) {
            ACTION_START -> {
                val title = intent.getStringExtra(EXTRA_TITLE) ?: getString(R.string.notification_receiving)
                startForeground(NOTIFICATION_ID, buildNotification(title, "Waiting for iPhone…"))
            }
            ACTION_UPDATE -> {
                val title = intent.getStringExtra(EXTRA_TITLE) ?: getString(R.string.notification_receiving)
                val body = intent.getStringExtra(EXTRA_BODY) ?: ""
                val manager = getSystemService(NotificationManager::class.java)
                manager.notify(NOTIFICATION_ID, buildNotification(title, body))
            }
            ACTION_STOP -> {
                stopForeground(STOP_FOREGROUND_REMOVE)
                stopSelf()
            }
        }
        return START_STICKY
    }

    private fun buildNotification(title: String, body: String): Notification {
        createChannel()

        val launchIntent = PendingIntent.getActivity(
            this,
            0,
            Intent(this, MainActivity::class.java),
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE,
        )

        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setSmallIcon(android.R.drawable.stat_sys_download_done)
            .setContentTitle(title)
            .setContentText(body)
            .setContentIntent(launchIntent)
            .setOngoing(true)
            .build()
    }

    private fun createChannel() {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.O) return
        val manager = getSystemService(NotificationManager::class.java)
        val channel = NotificationChannel(
            CHANNEL_ID,
            getString(R.string.notification_channel_name),
            NotificationManager.IMPORTANCE_LOW,
        ).apply {
            description = getString(R.string.notification_channel_desc)
        }
        manager.createNotificationChannel(channel)
    }

    companion object {
        private const val CHANNEL_ID = "crosssend_transfer"
        private const val NOTIFICATION_ID = 1001

        const val ACTION_START = "com.crosssend.app.action.START"
        const val ACTION_UPDATE = "com.crosssend.app.action.UPDATE"
        const val ACTION_STOP = "com.crosssend.app.action.STOP"
        const val EXTRA_TITLE = "extra_title"
        const val EXTRA_BODY = "extra_body"

        fun start(context: Context) {
            val intent = Intent(context, TransferForegroundService::class.java).apply {
                action = ACTION_START
            }
            context.startForegroundService(intent)
        }

        fun update(context: Context, title: String, body: String) {
            val intent = Intent(context, TransferForegroundService::class.java).apply {
                action = ACTION_UPDATE
                putExtra(EXTRA_TITLE, title)
                putExtra(EXTRA_BODY, body)
            }
            context.startService(intent)
        }

        fun stop(context: Context) {
            val intent = Intent(context, TransferForegroundService::class.java).apply {
                action = ACTION_STOP
            }
            context.startService(intent)
        }
    }
}
