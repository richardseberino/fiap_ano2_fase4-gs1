package com.example.alertasincidendiodemofiap

import android.Manifest
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.core.content.ContextCompat
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.alertasincidendiodemofiap.ui.theme.AlertasIncidendioDemoFiapTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            AlertasIncidendioDemoFiapTheme {
                NotificationPermissionHandler()
                
                var selectedAlert by remember { mutableStateOf<SensorResponse?>(null) }
                
                if (selectedAlert == null) {
                    Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                        AlertListScreen(
                            modifier = Modifier.padding(innerPadding),
                            onAlertClick = { selectedAlert = it }
                        )
                    }
                } else {
                    val viewModel: MainViewModel = viewModel()
                    AlertDetailScreen(
                        alert = selectedAlert!!,
                        onBack = { selectedAlert = null },
                        onValidate = {
                            viewModel.removeAlert(selectedAlert!!)
                            selectedAlert = null
                        }
                    )
                }
            }
        }
    }
}

@Composable
fun NotificationPermissionHandler() {
    val context = LocalContext.current
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
        val launcher = rememberLauncherForActivityResult(
            contract = ActivityResultContracts.RequestPermission()
        ) { _ -> }

        LaunchedEffect(Unit) {
            if (ContextCompat.checkSelfPermission(
                    context,
                    Manifest.permission.POST_NOTIFICATIONS
                ) != PackageManager.PERMISSION_GRANTED
            ) {
                launcher.launch(Manifest.permission.POST_NOTIFICATIONS)
            }
        }
    }
}

@Composable
fun AlertListScreen(
    modifier: Modifier = Modifier,
    viewModel: MainViewModel = viewModel(),
    onAlertClick: (SensorResponse) -> Unit
) {
    val alerts by viewModel.alerts.collectAsState()

    Column(modifier = modifier.padding(16.dp)) {
        Text(
            text = "Alertas de Incêndio",
            style = MaterialTheme.typography.headlineMedium,
            modifier = Modifier.padding(bottom = 16.dp)
        )

        if (alerts.isEmpty()) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text(text = "Nenhum alerta detectado até o momento.", style = MaterialTheme.typography.bodyLarge)
            }
        } else {
            LazyColumn {
                items(alerts) { alert ->
                    AlertItem(alert = alert) {
                        onAlertClick(alert)
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                }
            }
        }
    }
}

@Composable
fun AlertItem(alert: SensorResponse, onClick: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() },
        elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = alert.fonte.measurement.uppercase(),
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.primary
            )
            Text(
                text = alert.recomendacoes.firstOrNull() ?: "Sem recomendação",
                style = MaterialTheme.typography.bodyMedium
            )
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AlertDetailScreen(alert: SensorResponse, onBack: () -> Unit, onValidate: () -> Unit) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Detalhes do Alerta") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(imageVector = Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Voltar")
                    }
                }
            )
        }
    ) { innerPadding ->
        Surface(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding),
            color = MaterialTheme.colorScheme.background
        ) {
            LazyColumn(modifier = Modifier.padding(16.dp)) {
                item {
                    Text(
                        text = alert.fonte.measurement.uppercase(),
                        style = MaterialTheme.typography.headlineMedium,
                        color = MaterialTheme.colorScheme.error
                    )
                    HorizontalDivider(modifier = Modifier.padding(vertical = 12.dp))
                    
                    DetailRow(label = "Bucket de Origem", value = alert.fonte.bucket)
                    DetailRow(label = "Timestamp da Ocorrência", value = alert.fonte.timestamp)
                    
                    Spacer(modifier = Modifier.height(24.dp))
                    Text(text = "Dados do Sensor", style = MaterialTheme.typography.titleLarge)
                    Card(
                        modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp),
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            DetailRow(label = "Temperatura Detectada", value = "${alert.entrada.temperaturaCelsius}°C")
                            DetailRow(label = "Umidade do Ar", value = "${alert.entrada.umidadePercentual}%")
                        }
                    }
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(text = "Resultado da Predição", style = MaterialTheme.typography.titleLarge)
                    Card(
                        modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp),
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.errorContainer)
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            DetailRow(label = "Nível de Risco", value = alert.predicao.risco)
                            DetailRow(label = "Grau de Confiança", value = "${alert.predicao.confiancaPercentual}%")
                            DetailRow(label = "Código do Evento", value = alert.predicao.codigo.toString())
                        }
                    }
                    
                    Spacer(modifier = Modifier.height(24.dp))
                    Text(text = "Plano de Ação e Recomendações", style = MaterialTheme.typography.titleLarge)
                    Spacer(modifier = Modifier.height(8.dp))
                    alert.recomendacoes.forEach { recomendacao ->
                        Card(
                            modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp),
                            elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
                        ) {
                            Text(
                                text = recomendacao,
                                style = MaterialTheme.typography.bodyMedium,
                                modifier = Modifier.padding(12.dp)
                            )
                        }
                    }
                    
                    Spacer(modifier = Modifier.height(32.dp))
                    Button(
                        onClick = onValidate,
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text("Validar e Fechar")
                    }
                    Spacer(modifier = Modifier.height(16.dp))
                }
            }
        }
    }
}

@Composable
fun DetailRow(label: String, value: String) {
    Column(modifier = Modifier.padding(vertical = 6.dp)) {
        Text(text = label, style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.secondary)
        Text(text = value, style = MaterialTheme.typography.bodyLarge)
    }
}
