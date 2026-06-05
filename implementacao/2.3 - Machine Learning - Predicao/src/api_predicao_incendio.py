from flask import Flask, request, jsonify
import pickle
import os
import numpy as np
from influxdb_client import InfluxDBClient

app = Flask(__name__)

# Variáveis globais para armazenar o modelo e scaler
modelo = None
scaler = None
modelo_carregado = False

# Configurações do InfluxDB
INFLUX_URL = "http://192.168.68.119:8086"
INFLUX_TOKEN = "wnXf_GR-av5Erye0BLlWoir8pvLd6elVsgLu7HuDewZOJUD7vx0Bm84LMOmIfNZ92Pwse9q8SeYG_rnKEqMuDw=="
INFLUX_ORG = "fiap"
INFLUX_BUCKET = "dados-area"
INFLUX_MEASUREMENT = "amazonas"

def carregar_modelo():
    """Carrega o modelo e scaler do arquivo pickle"""
    global modelo, scaler, modelo_carregado
    
    try:
        with open('modelo_incendio.pkl', 'rb') as f:
            dados = pickle.load(f)
            modelo = dados['modelo']
            scaler = dados['scaler']
        modelo_carregado = True
        print("✓ Modelo carregado com sucesso!")
        return True
    except FileNotFoundError:
        print("✗ Erro: Arquivo 'modelo_incendio.pkl' não encontrado!")
        print("  Execute 'python3 treinar_modelo_incendio.py' primeiro")
        return False
    except Exception as e:
        print(f"✗ Erro ao carregar modelo: {str(e)}")
        return False


@app.route('/dados-sensor', methods=['GET'])
def dados_sensor():
    """
    Lê dados do InfluxDB - measurement 'amazonas' (temperatura e umidade)

    Query param opcional:
    - intervalo: duração Flux, ex: 1h, 30m, 24h (padrão: 1h)

    Exemplo:
    GET /dados-sensor
    GET /dados-sensor?intervalo=30m
    """
    intervalo = request.args.get('intervalo', '1h')

    query = f'''
from(bucket: "{INFLUX_BUCKET}")
  |> range(start: -{intervalo})
  |> filter(fn: (r) => r._measurement == "{INFLUX_MEASUREMENT}")
  |> filter(fn: (r) => r._field == "temperatura" or r._field == "umidade")
  |> sort(columns: ["_time"], desc: true)
'''

    try:
        with InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG) as client:
            tabelas = client.query_api().query(query)

        registros = []
        for tabela in tabelas:
            for linha in tabela.records:
                registros.append({
                    'timestamp': linha.get_time().isoformat(),
                    'campo': linha.get_field(),
                    'valor': linha.get_value(),
                    'measurement': linha.get_measurement(),
                })

        return jsonify({
            'sucesso': True,
            'bucket': INFLUX_BUCKET,
            'measurement': INFLUX_MEASUREMENT,
            'intervalo': intervalo,
            'total_registros': len(registros),
            'dados': registros,
        }), 200

    except Exception as e:
        return jsonify({
            'erro': 'Erro ao consultar InfluxDB',
            'mensagem': str(e),
        }), 500


@app.route('/prever-sensor', methods=['GET'])
def prever_sensor():
    """
    Lê os últimos valores de temperatura e umidade do InfluxDB
    e retorna a predição de risco de incêndio.

    Exemplo:
    GET /prever-sensor
    """
    if not modelo_carregado:
        return jsonify({
            'erro': 'Modelo não carregado',
            'mensagem': 'Execute o script de treinamento primeiro'
        }), 503

    query = f'''
from(bucket: "{INFLUX_BUCKET}")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "{INFLUX_MEASUREMENT}")
  |> filter(fn: (r) => r._field == "temperatura" or r._field == "umidade")
  |> last()
'''

    try:
        with InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG) as client:
            tabelas = client.query_api().query(query)

        leituras = {}
        timestamp = None
        for tabela in tabelas:
            for linha in tabela.records:
                leituras[linha.get_field()] = linha.get_value()
                timestamp = linha.get_time().isoformat()

        if 'temperatura' not in leituras or 'umidade' not in leituras:
            campos_faltando = [c for c in ('temperatura', 'umidade') if c not in leituras]
            return jsonify({
                'erro': 'Dados insuficientes no InfluxDB',
                'mensagem': f'Campos não encontrados: {campos_faltando}',
                'leituras_encontradas': leituras,
            }), 422

        temperatura = float(leituras['temperatura'])
        umidade = float(leituras['umidade'])

        entrada_normalizada = scaler.transform([[temperatura, umidade]])
        predicao = modelo.predict(entrada_normalizada)[0]

        if hasattr(modelo, 'predict_proba'):
            probabilidades = modelo.predict_proba(entrada_normalizada)[0]
            confianca = float(max(probabilidades) * 100)
        else:
            confianca = 100.0

        risco = "COM RISCO" if predicao == 1 else "SEM RISCO"

        return jsonify({
            'sucesso': True,
            'fonte': {
                'bucket': INFLUX_BUCKET,
                'measurement': INFLUX_MEASUREMENT,
                'timestamp': timestamp,
            },
            'entrada': {
                'temperatura_celsius': temperatura,
                'umidade_percentual': umidade,
            },
            'predicao': {
                'risco': risco,
                'codigo': int(predicao),
                'confianca_percentual': round(confianca, 2),
            },
            'recomendacoes': gerar_recomendacoes(temperatura, umidade, predicao),
        }), 200

    except Exception as e:
        return jsonify({
            'erro': 'Erro ao processar dados do sensor',
            'mensagem': str(e),
        }), 500


@app.route('/prever', methods=['POST', 'GET'])
def prever():
    """
    Faz predição de risco de incêndio
    
    Parâmetros esperados:
    - temperatura: float (em Celsius, range: 18-38)
    - umidade: float (em %, range: 25-95)
    
    Métodos: POST (JSON) ou GET (query params)
    
    Exemplo GET:
    /prever?temperatura=32&umidade=35
    
    Exemplo POST:
    {
        "temperatura": 32,
        "umidade": 35
    }
    """
    
    if not modelo_carregado:
        return jsonify({
            'erro': 'Modelo não carregado',
            'mensagem': 'Execute o script de treinamento primeiro'
        }), 503
    
    try:
        # Obter parâmetros (GET ou POST)
        if request.method == 'POST':
            dados = request.get_json()
            temperatura = float(dados.get('temperatura'))
            umidade = float(dados.get('umidade'))
        else:  # GET
            temperatura = float(request.args.get('temperatura'))
            umidade = float(request.args.get('umidade'))
        
        # Validar ranges
        if not (10 <= temperatura <= 50):
            return jsonify({
                'erro': 'Temperatura inválida',
                'mensagem': 'Temperatura deve estar entre 10°C e 50°C',
                'valor_recebido': temperatura
            }), 400
        
        if not (0 <= umidade <= 100):
            return jsonify({
                'erro': 'Umidade inválida',
                'mensagem': 'Umidade deve estar entre 0% e 100%',
                'valor_recebido': umidade
            }), 400
        
        # Normalizar dados usando o scaler do treinamento
        entrada_normalizada = scaler.transform([[temperatura, umidade]])
        
        # Fazer predição
        predicao = modelo.predict(entrada_normalizada)[0]
        
        # Obter confiança
        if hasattr(modelo, 'predict_proba'):
            probabilidades = modelo.predict_proba(entrada_normalizada)[0]
            confianca = float(max(probabilidades) * 100)
        else:
            confianca = 100.0
        
        # Classificar risco
        if predicao == 1:
            risco = "COM RISCO"
        else:
            risco = "SEM RISCO"
        
        # Retornar resposta
        resposta = {
            'sucesso': True,
            'entrada': {
                'temperatura_celsius': temperatura,
                'umidade_percentual': umidade
            },
            'predicao': {
                'risco': risco,
                'codigo': int(predicao),
                'confianca_percentual': round(confianca, 2),
            },
            'recomendacoes': gerar_recomendacoes(temperatura, umidade, predicao)
        }
        
        return jsonify(resposta), 200
    
    except ValueError as e:
        return jsonify({
            'erro': 'Parâmetros inválidos',
            'mensagem': f'Erro ao converter parâmetros: {str(e)}',
            'esperado': {
                'temperatura': 'float (10-50)',
                'umidade': 'float (0-100)'
            }
        }), 400
    
    except Exception as e:
        return jsonify({
            'erro': 'Erro ao fazer predição',
            'mensagem': str(e)
        }), 500



def gerar_recomendacoes(temperatura, umidade, predicao):
    """Gera recomendações baseadas na predição"""
    recomendacoes = []
    
    if predicao == 1:  # Com risco
        recomendacoes.append("⚠️ ALERTA: Risco elevado de incêndio detectado!")
        
        if temperatura > 34:
            recomendacoes.append(f"🌡️ Temperatura muito alta ({temperatura}°C) - Aumenta drasticamente o risco")
        elif temperatura > 32:
            recomendacoes.append(f"🌡️ Temperatura alta ({temperatura}°C) - Favorece propagação de incêndios")
        
        if umidade < 35:
            recomendacoes.append(f"💧 Umidade muito baixa ({umidade}%) - Condições críticas para incêndio")
        elif umidade < 45:
            recomendacoes.append(f"💧 Umidade baixa ({umidade}%) - Vegetação seca, fácil ignição")
        
        recomendacoes.append("📋 Recomendações:")
        recomendacoes.append("  • Aumentar patrulhas de vigilância")
        recomendacoes.append("  • Manter recursos de combate a incêndio preparados")
        recomendacoes.append("  • Alertar comunidades locais")
        recomendacoes.append("  • Monitorar continuamente as condições meteorológicas")
    
    else:  # Sem risco
        recomendacoes.append("✓ Condições seguras - Baixo risco de incêndio")
        
        if umidade > 70:
            recomendacoes.append(f"💧 Umidade alta ({umidade}%) - Vegetação úmida, menos inflamável")
        
        if temperatura < 26:
            recomendacoes.append(f"🌡️ Temperatura baixa ({temperatura}°C) - Reduz risco significativamente")
        
        recomendacoes.append("📋 Manutenção de rotina:")
        recomendacoes.append("  • Continuar monitoramento normal")
        recomendacoes.append("  • Manter equipamentos de prontidão")
    
    return recomendacoes

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("API DE PREDIÇÃO DE RISCO DE INCÊNDIO NA AMAZÔNIA")
    print("=" * 70)
    
    # Carregar modelo
    print("\n1. Carregando modelo...")
    if not carregar_modelo():
        print("\n✗ Falha ao carregar o modelo. Encerrando...")
        exit(1)
    
    # Iniciar servidor
    print("\n2. Iniciando servidor Flask...")
    print("\n" + "=" * 70)
    print("Endpoints disponíveis:")
    print("  • GET  /health      - Status da API")
    print("  • GET  /info        - Informações e documentação")
    print("  • GET  /exemplo     - Exemplos de predições")
    print("  • POST /prever      - Fazer predição (JSON)")
    print("  • GET  /prever?temperatura=X&umidade=Y - Fazer predição (Query params)")
    print("  • GET  /dados-sensor                   - Lê temperatura/umidade do InfluxDB (último 1h)")
    print("  • GET  /dados-sensor?intervalo=30m      - Lê dados com intervalo personalizado")
    print("  • GET  /prever-sensor                  - Lê sensor do InfluxDB e retorna predição")
    print("\nExemplos:")
    print("  • curl 'http://localhost:5001/prever?temperatura=32&umidade=35'")
    print("  • curl -X POST http://localhost:5001/prever \\")
    print("    -H 'Content-Type: application/json' \\")
    print("    -d '{\"temperatura\": 32, \"umidade\": 35}'")
    print("=" * 70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
