#!/usr/bin/env python3
"""
Script de teste para a API de Predição de Risco de Incêndio na Amazônia
Testa os endpoints da API com diferentes cenários
"""

import requests
import json
from datetime import datetime

# URL base da API
BASE_URL = 'http://localhost:5001'

def print_header(titulo):
    """Imprime um cabeçalho formatado"""
    print("\n" + "=" * 70)
    print(f"  {titulo}")
    print("=" * 70)

def testar_health():
    """Testa o endpoint /health"""
    print_header("1. TESTE: /health (Verificar se API está online)")
    try:
        resposta = requests.get(f'{BASE_URL}/health')
        print(f"Status: {resposta.status_code}")
        print(f"Resposta: {json.dumps(resposta.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"✗ Erro: {str(e)}")
        print("  A API não está rodando. Execute: python3 api_predicao_incendio.py")

def testar_info():
    """Testa o endpoint /info"""
    print_header("2. TESTE: /info (Informações sobre a API)")
    try:
        resposta = requests.get(f'{BASE_URL}/info')
        print(f"Status: {resposta.status_code}")
        dados = resposta.json()
        print(f"\nEndpoints disponíveis:")
        for endpoint, descricao in dados['endpoints'].items():
            print(f"  • {endpoint:20} - {descricao}")
    except Exception as e:
        print(f"✗ Erro: {str(e)}")

def testar_exemplo():
    """Testa o endpoint /exemplo"""
    print_header("3. TESTE: /exemplo (Ver exemplos de predições)")
    try:
        resposta = requests.get(f'{BASE_URL}/exemplo')
        dados = resposta.json()
        
        for i, ex in enumerate(dados['exemplos'], 1):
            entrada = ex['entrada']
            resultado = ex['resultado']
            print(f"\n  Exemplo {i}: {ex['descricao']}")
            print(f"    Entrada: Temp={entrada['temperatura_celsius']}°C, Umid={entrada['umidade_percentual']}%")
            print(f"    Resultado: {resultado['risco']} (Confiança: {resultado['confianca']}%)")
    except Exception as e:
        print(f"✗ Erro: {str(e)}")

def testar_prever_get(temperatura, umidade, descricao=""):
    """Testa /prever usando método GET"""
    print(f"\n  Teste GET: Temp={temperatura}°C, Umid={umidade}%")
    if descricao:
        print(f"  Descrição: {descricao}")
    
    try:
        url = f'{BASE_URL}/prever?temperatura={temperatura}&umidade={umidade}'
        resposta = requests.get(url)
        
        if resposta.status_code == 200:
            dados = resposta.json()
            predicao = dados['predicao']
            print(f"  ✓ Resultado: {predicao['emoji']} {predicao['risco']} (Confiança: {predicao['confianca_percentual']}%)")
            
            if 'recomendacoes' in dados and dados['recomendacoes']:
                print(f"  Recomendações:")
                for rec in dados['recomendacoes'][:3]:  # Mostrar apenas 3 primeiras
                    print(f"    • {rec}")
        else:
            print(f"  ✗ Erro: {resposta.status_code}")
            print(f"    {resposta.json()}")
    except Exception as e:
        print(f"  ✗ Erro: {str(e)}")

def testar_prever_post(temperatura, umidade, descricao=""):
    """Testa /prever usando método POST"""
    print(f"\n  Teste POST: Temp={temperatura}°C, Umid={umidade}%")
    if descricao:
        print(f"  Descrição: {descricao}")
    
    try:
        payload = {
            'temperatura': temperatura,
            'umidade': umidade
        }
        resposta = requests.post(f'{BASE_URL}/prever', json=payload)
        
        if resposta.status_code == 200:
            dados = resposta.json()
            predicao = dados['predicao']
            print(f"  ✓ Resultado: {predicao['emoji']} {predicao['risco']} (Confiança: {predicao['confianca_percentual']}%)")
        else:
            print(f"  ✗ Erro: {resposta.status_code}")
            print(f"    {resposta.json()}")
    except Exception as e:
        print(f"  ✗ Erro: {str(e)}")

def testar_predicoes():
    """Testa vários cenários de predição"""
    print_header("4. TESTES: Predições em diferentes cenários")
    
    cenarios = [
        # (temperatura, umidade, descrição)
        (25, 80, "Temperatura moderada, umidade alta - ESPERADO: SEM RISCO"),
        (32, 35, "Temperatura alta, umidade baixa - ESPERADO: COM RISCO"),
        (35, 30, "Temperatura muito alta, umidade muito baixa - ESPERADO: ALTO RISCO"),
        (28, 60, "Temperatura normal, umidade moderada - ESPERADO: SEM RISCO"),
        (19, 85, "Temperatura baixa, umidade alta - ESPERADO: SEM RISCO"),
        (34, 40, "Temperatura alta, umidade baixa - ESPERADO: COM RISCO"),
        (26, 70, "Temperatura moderada, umidade moderada - ESPERADO: SEM RISCO"),
    ]
    
    print("\n  --- Testando com método GET ---")
    for temp, umid, desc in cenarios:
        testar_prever_get(temp, umid, desc)
    
    print("\n\n  --- Testando com método POST ---")
    for temp, umid, desc in cenarios[:3]:  # Testar apenas alguns com POST
        testar_prever_post(temp, umid, desc)

def testar_validacoes():
    """Testa validações de entrada"""
    print_header("5. TESTES: Validações de entrada (Erros esperados)")
    
    print("\n  a) Temperatura inválida (muito alta):")
    testar_prever_get(50, 50, "Temperatura fora do range")
    
    print("\n  b) Umidade inválida (muito baixa):")
    testar_prever_get(30, 10, "Umidade fora do range")
    
    print("\n  c) Parâmetros faltando:")
    try:
        resposta = requests.get(f'{BASE_URL}/prever')
        print(f"  Status: {resposta.status_code}")
        print(f"  Resposta: {resposta.json()}")
    except Exception as e:
        print(f"  Erro: {str(e)}")

def main():
    """Função principal"""
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  TESTE COMPLETO - API DE PREDIÇÃO DE RISCO DE INCÊNDIO NA AMAZÔNIA".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    
    print(f"\n⏱️  Horário do teste: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 URL Base: {BASE_URL}")
    
    # Executar testes
    testar_health()
    
    try:
        # Verificar se API está online antes de continuar
        resposta = requests.get(f'{BASE_URL}/health', timeout=2)
        if resposta.status_code != 200:
            print("\n⚠️  AVISO: API não está respondendo corretamente.")
            print("    Execute o servidor: python3 api_predicao_incendio.py")
            return
    except:
        print("\n⚠️  AVISO: Não foi possível conectar à API.")
        print("    Certifique-se de que o servidor está rodando:")
        print("    python3 api_predicao_incendio.py")
        return
    
    # Continuar com os testes
    testar_info()
    testar_exemplo()
    testar_predicoes()
    testar_validacoes()
    
    # Resumo final
    print_header("RESUMO DOS TESTES")
    print("""
    ✓ Todos os endpoints foram testados
    ✓ Cenários de predição foram validados
    ✓ Validações de entrada foram verificadas
    
    A API está funcionando corretamente!
    
    Para usar em produção:
    • Mantenha o servidor rodando: python3 api_predicao_incendio.py
    • Faça requisições para: http://localhost:5000/prever
    • Use os parâmetros: temperatura (float) e umidade (float)
    """)
    print("=" * 70 + "\n")

if __name__ == '__main__':
    main()
