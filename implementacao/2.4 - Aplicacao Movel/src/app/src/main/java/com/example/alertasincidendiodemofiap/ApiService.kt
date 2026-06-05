package com.example.alertasincidendiodemofiap

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET

interface ApiService {
    @GET("prever-sensor")
    suspend fun getSensorData(): SensorResponse
}

object RetrofitClient {
    private const val BASE_URL = "http://10.0.2.2:5001/"

    val instance: ApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiService::class.java)
    }
}
