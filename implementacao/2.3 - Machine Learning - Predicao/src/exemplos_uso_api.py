#!/usr/bin/env python3
"""
Exemplos de como usar a API de Predição de Risco de Incêndio
Execute: python3 exemplos_uso_api.py
"""

import requests
import json

BASE_URL = 'http://localhost:5001'

def exemplo_1_verificar_status():
    """Exemplo 1: Verificar status da API"""
    print("\n" + "="*70)
    print("EXEMPLO 1: Verificar Status da API")
    print("="*70)
    
    print("\nCódigo Python:")
    print("""
import requests

response = requests.get('http://localhost:5000/health')
print(response.json())
""")
    
    print("\nComando curl:")
    print("curl http://localhost:5000/health")
    
    print("\nExecutando...")
    try:
        response = requests.get(f'{BASE_URL}/health')
        print(f"\nResposta ({response.status_code}):")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Erro: {e}")

def exemplo_2_predicao_get():
    """Exemplo 2: Fazer predição usando GET"""
    print("\n" + "="*70)
    print("EXEMPLO 2: Fazer Predição (Método GET)")
    print("="*70)
    
    temperatura = 32
    umidade = 35
    
    print(f"\nCódigo Python:")
    print(f"""
import requests

response = requests.get(
    'http://localhost:5000/prever',
    params={{
        'temperatura': {temperatura},
        'umidade': {umidade}
    }}
)
print(response.json())
""")
    
    print(f"\nComando curl:")
    print(f"curl 'http://localhost:5000/prever?temperatura={temperatura}&umidade={umidade}'")
    
    print(f"\nExecutando (Temp={temperatura}°C, Umid={umidade}%)...")
    try:
        response = requests.get(f'{BASE_URL}/prever', params={
            'temperatura': temperatura,
            'umidade': umidade
        })
        print(f"\nResposta ({response.status_code}):")
        dados = response.json()
        print(json.dumps(dados, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Erro: {e}")

def exemplo_3_predicao_post():
    """Exemplo 3: Fazer predição usando POST"""
    print("\n" + "="*70)
    print("EXEMPLO 3: Fazer Predição (Método POST)")
    print("="*70)
    
    temperatura = 25
    umidade = 80
    
    print(f"\nCódigo Python:")
    print(f"""
import requests

payload = {{
    'temperatura': {temperatura},
    'umidade': {umidade}
}}

response = requests.post(
    'http://localhost:5000/prever',
    json=payload
)
print(response.json())
""")
    
    print(f"\nComando curl:")
    print(f"""curl -X POST http://localhost:5000/prever \\
  -H 'Content-Type: application/json' \\
  -d '{{"temperatura": {temperatura}, "umidade": {umidade}}}'
""")
    
    print(f"\nExecutando (Temp={temperatura}°C, Umid={umidade}%)...")
    try:
        payload = {'temperatura': temperatura, 'umidade': umidade}
        response = requests.post(f'{BASE_URL}/prever', json=payload)
        print(f"\nResposta ({response.status_code}):")
        dados = response.json()
        print(json.dumps(dados, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Erro: {e}")

def exemplo_4_processar_resposta():
    """Exemplo 4: Processar resposta e extrair dados úteis"""
    print("\n" + "="*70)
    print("EXEMPLO 4: Processar Resposta")
    print("="*70)
    
    print("\nCódigo Python:")
    codigo = """
import requests

response = requests.get('http://localhost:5000/prever', params={
    'temperatura': 32,
    'umidade': 35
})

if response.status_code == 200:
    dados = response.json()
    
    # Extrair informações
    entrada = dados['entrada']
    predicao = dados['predicao']
    recomendacoes = dados['recomendacoes']
    
    # Imprimir de forma amigável
    print(f"Temperatura: {entrada['temperatura_celsius']}°C")
    print(f"Umidade: {entrada['umidade_percentual']}%")
    print(f"Risco: {predicao['risco']}")
    print(f"Confiança: {predicao['confianca_percentual']}%")
    print("\\nRecomendações:")
    for rec in recomendacoes:
        print(f"  • {rec}")
else:
    print(f"Erro: {response.status_code}")
    print(response.json())
"""
    print(codigo)
    
    print("\nExecutando...")
    try:
        response = requests.get(f'{BASE_URL}/prever', params={
            'temperatura': 32,
            'umidade': 35
        })
        
        if response.status_code == 200:
            dados = response.json()
            entrada = dados['entrada']
            predicao = dados['predicao']
            recomendacoes = dados['recomendacoes']
            
            print(f"\nResultado:")
            print(f"Temperatura: {entrada['temperatura_celsius']}°C")
            print(f"Umidade: {entrada['umidade_percentual']}%")
            print(f"Risco: {predicao['risco']}")
            print(f"Confiança: {predicao['confianca_percentual']}%")
            print(f"\nPrimeiras 3 recomendações:")
            for rec in recomendacoes[:3]:
                print(f"  • {rec}")
        else:
            print(f"Erro: {response.status_code}")
    except Exception as e:
        print(f"Erro: {e}")

def exemplo_5_lote():
    """Exemplo 5: Processar múltiplas predições em lote"""
    print("\n" + "="*70)
    print("EXEMPLO 5: Processar Lote de Predições")
    print("="*70)
    
    print("\nCódigo Python:")
    codigo = """
import requests

# Lista de cenários para prever
cenarios = [
    {'temp': 25, 'umid': 80, 'local': 'Región A'},
    {'temp': 32, 'umid': 35, 'local': 'Región B'},
    {'temp': 35, 'umid': 30, 'local': 'Región C'},
    {'temp': 28, 'umid': 60, 'local': 'Región D'},
    {'temp': 19, 'umid': 85, 'local': 'Región E'},
]

print("Processando predições...")
for cenario in cenarios:
    response = requests.get('http://localhost:5000/prever', params={
        'temperatura': cenario['temp'],
        'umidade': cenario['umid']
    })
    
    if response.status_code == 200:
        dados = response.json()
        predicao = dados['predicao']
        print(f"{cenario['local']:15} | "
              f"T={cenario['temp']:2}°C U={cenario['umid']:2}% | "
              f"{predicao['emoji']} {predicao['risco']:15} | "
              f"Conf: {predicao['confianca_percentual']:5.1f}%")
"""
    print(codigo)
    
    print("\nExecutando...")
    try:
        cenarios = [
            {'temp': 25, 'umid': 80, 'local': 'Región A'},
            {'temp': 32, 'umid': 35, 'local': 'Región B'},
            {'temp': 35, 'umid': 30, 'local': 'Región C'},
            {'temp': 28, 'umid': 60, 'local': 'Región D'},
            {'temp': 19, 'umid': 85, 'local': 'Región E'},
        ]
        
        print(f"\nResultados:")
        print("-" * 85)
        for cenario in cenarios:
            response = requests.get(f'{BASE_URL}/prever', params={
                'temperatura': cenario['temp'],
                'umidade': cenario['umid']
            })
            
            if response.status_code == 200:
                dados = response.json()
                predicao = dados['predicao']
                print(f"{cenario['local']:15} | "
                      f"T={cenario['temp']:2}°C U={cenario['umid']:2}% | "
                      f"{predicao['emoji']} {predicao['risco']:15} | "
                      f"Conf: {predicao['confianca_percentual']:5.1f}%")
    except Exception as e:
        print(f"Erro: {e}")

def exemplo_6_tratamento_erros():
    """Exemplo 6: Tratamento de erros"""
    print("\n" + "="*70)
    print("EXEMPLO 6: Tratamento de Erros")
    print("="*70)
    
    print("\nCódigo Python:")
    codigo = """
import requests

def fazer_predicao(temperatura, umidade):
    try:
        response = requests.get('http://localhost:5000/prever', 
            params={'temperatura': temperatura, 'umidade': umidade},
            timeout=5)
        
        if response.status_code == 200:
            return response.json()
        
        elif response.status_code == 400:
            erro = response.json()
            print(f"Erro de validação: {erro['mensagem']}")
            return None
        
        elif response.status_code == 503:
            print("API indisponível. Modelo não carregado.")
            return None
        
        else:
            print(f"Erro {response.status_code}: {response.text}")
            return None
    
    except requests.exceptions.Timeout:
        print("Timeout: A API não respondeu a tempo")
        return None
    
    except requests.exceptions.ConnectionError:
        print("Erro de conexão: A API não está rodando")
        return None
    
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

# Testar com valores inválidos
resultado = fazer_predicao(50, 50)  # Temperatura inválida
resultado = fazer_predicao(30, 10)  # Umidade inválida
resultado = fazer_predicao(25, 80)  # Valores válidos
"""
    print(codigo)
    
    print("\nExecutando testes de erro...")
    
    def fazer_predicao(temperatura, umidade):
        try:
            response = requests.get(f'{BASE_URL}/prever', 
                params={'temperatura': temperatura, 'umidade': umidade},
                timeout=5)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 400:
                erro = response.json()
                print(f"  ✗ Erro: {erro['mensagem']}")
                return None
            else:
                print(f"  ✗ Erro {response.status_code}")
                return None
        except requests.exceptions.ConnectionError:
            print(f"  ✗ Erro de conexão: A API não está rodando")
            return None
        except Exception as e:
            print(f"  ✗ Erro: {e}")
            return None
    
    print(f"\nTeste 1: Temperatura inválida (50°C)")
    fazer_predicao(50, 50)
    
    print(f"Teste 2: Umidade inválida (10%)")
    fazer_predicao(30, 10)
    
    print(f"Teste 3: Valores válidos (25°C, 80%)")
    resultado = fazer_predicao(25, 80)
    if resultado:
        print(f"  ✓ Sucesso: {resultado['predicao']['risco']}")

def main():
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + "EXEMPLOS DE USO - API DE PREDIÇÃO DE INCÊNDIO".center(68) + "║")
    print("╚" + "="*68 + "╝")
    
    print("\n⚠️  IMPORTANTE: Certifique-se de que a API está rodando!")
    print("   Em outro terminal, execute: python3 api_predicao_incendio.py")
    
    exemplo_1_verificar_status()
    exemplo_2_predicao_get()
    exemplo_3_predicao_post()
    exemplo_4_processar_resposta()
    exemplo_5_lote()
    exemplo_6_tratamento_erros()
    
    print("\n" + "="*70)
    print("EXEMPLOS CONCLUÍDOS")
    print("="*70)
    print("\nPara mais informações, veja: README_API.md\n")

if __name__ == '__main__':
    main()
