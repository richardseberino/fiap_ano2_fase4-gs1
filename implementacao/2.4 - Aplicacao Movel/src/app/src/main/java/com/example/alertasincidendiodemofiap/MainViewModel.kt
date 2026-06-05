package com.example.alertasincidendiodemofiap

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class MainViewModel(application: Application) : AndroidViewModel(application) {
    private val _alerts = MutableStateFlow<List<SensorResponse>>(emptyList())
    val alerts: StateFlow<List<SensorResponse>> = _alerts

    init {
        NotificationHelper.createNotificationChannel(application)
        startPolling()
    }

    private fun startPolling() {
        viewModelScope.launch {
            while (true) {
                try {
                    val response = RetrofitClient.instance.getSensorData()
                    if (response.predicao.codigo == 1) {
                        val lastAlert = _alerts.value.firstOrNull()
                        val isDuplicate = lastAlert != null &&
                                lastAlert.entrada.temperaturaCelsius == response.entrada.temperaturaCelsius &&
                                lastAlert.entrada.umidadePercentual == response.entrada.umidadePercentual

                        if (!isDuplicate) {
                            _alerts.value = listOf(response) + _alerts.value
                            NotificationHelper.showNotification(
                                getApplication(),
                                "🔥 Novo Alerta: ${response.fonte.measurement.uppercase()}",
                                response.recomendacoes.firstOrNull() ?: "Risco detectado"
                            )
                        }
                    }
                } catch (e: Exception) {
                    e.printStackTrace()
                }
                delay(10000) // Poll every 10 seconds
            }
        }
    }

    fun removeAlert(alert: SensorResponse) {
        _alerts.value = _alerts.value.filter { it != alert }
    }
}
