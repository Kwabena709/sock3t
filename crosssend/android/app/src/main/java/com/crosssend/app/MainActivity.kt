package com.crosssend.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.crosssend.app.receive.ReceiveScreen
import com.crosssend.app.ui.theme.CrossSendTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            CrossSendTheme {
                ReceiveScreen()
            }
        }
    }
}
