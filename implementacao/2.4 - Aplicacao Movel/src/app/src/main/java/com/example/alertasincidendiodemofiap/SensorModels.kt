package com.example.alertasincidendiodemofiap

import com.google.gson.annotations.SerializedName

data class SensorResponse(
    val entrada: Entrada,
    val fonte: Fonte,
    val predicao: Predicao,
    val recomendacoes: List<String>,
    val sucesso: Boolean
)

data class Entrada(
    @SerializedName("temperatura_celsius") val temperaturaCelsius: Double,
    @SerializedName("umidade_percentual") val umidadePercentual: Double
)

data class Fonte(
    val bucket: String,
    val measurement: String,
    val timestamp: String
)

data class Predicao(
    val codigo: Int,
    @SerializedName("confianca_percentual") val confiancaPercentual: Double,
    val risco: String
)
