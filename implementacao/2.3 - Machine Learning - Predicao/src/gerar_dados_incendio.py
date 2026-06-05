import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Seed para reprodutibilidade
np.random.seed(42)

# Parâmetros da Amazônia
n_samples = 1000

# Definir ranges realistas para a Amazônia
# Temperatura: 20-35°C (típico da região tropical)
# Umidade: 30-95% (varia bastante entre estações)

dados = {
    'temperatura_celsius': [],
    'umidade_percentual': [],
    'risco_incendio': []
}

# Gerar dados com distribuições realistas
# A Amazônia tem períodos secos (risco maior) e períodos chuvosos (risco menor)

for i in range(n_samples):
    # 30% de chance de estar em período seco (maior risco)
    if np.random.random() < 0.3:
        # Período seco: temperatura alta, umidade baixa
        temp = np.random.normal(loc=32, scale=2.5)  # Média 32°C
        umidade = np.random.uniform(25, 50)  # Umidade baixa
    else:
        # Período chuvoso: distribuição mais variada
        temp = np.random.normal(loc=27, scale=3)  # Média 27°C
        umidade = np.random.uniform(50, 95)  # Umidade alta
    
    # Adicionar variação aleatória natural
    temp += np.random.normal(0, 0.5)
    
    # Limitar aos ranges realistas
    temp = np.clip(temp, 18, 38)
    umidade = np.clip(umidade, 25, 95)
    
    dados['temperatura_celsius'].append(round(temp, 2))
    dados['umidade_percentual'].append(round(umidade, 2))
    
    # Lógica de classificação de risco
    # Baseado em estudos de incêndios na Amazônia
    risco = 0  # Sem risco
    
    # Fatores de risco:
    # 1. Temperatura alta (>30°C) + Umidade baixa (<50%)
    # 2. Temperatura muito alta (>32°C) + Umidade baixa (<60%)
    # 3. Temperatura acima de 34°C (risco elevado mesmo com umidade moderada)
    
    if temp > 34:
        if umidade < 70:
            risco = 1  # Alto risco
        elif umidade < 80:
            risco = 1  # Médio-alto, classificar como risco
    elif temp > 32:
        if umidade < 45:
            risco = 1  # Alto risco
        elif umidade < 55:
            risco = 1  # Risco moderado-alto
    elif temp > 30:
        if umidade < 40:
            risco = 1  # Risco
        elif umidade < 45:
            # Risco moderado
            risco = 1 if np.random.random() < 0.6 else 0
    elif temp > 28:
        if umidade < 35:
            risco = 1  # Risco
        elif umidade < 40:
            risco = 1 if np.random.random() < 0.3 else 0
    else:
        # Temperatura baixa, risco muito reduzido
        if umidade < 30:
            risco = 1 if np.random.random() < 0.1 else 0
    
    dados['risco_incendio'].append(risco)

# Criar DataFrame
df = pd.DataFrame(dados)

# Estatísticas
print("=" * 60)
print("DATASET DE RISCO DE INCÊNDIO - AMAZÔNIA")
print("=" * 60)
print(f"\nTotal de amostras: {len(df)}")
print(f"\nDistribuição de Risco:")
print(f"  - Sem risco (0): {(df['risco_incendio'] == 0).sum()} amostras ({(df['risco_incendio'] == 0).sum()/len(df)*100:.1f}%)")
print(f"  - Com risco (1): {(df['risco_incendio'] == 1).sum()} amostras ({(df['risco_incendio'] == 1).sum()/len(df)*100:.1f}%)")

print(f"\nEstatísticas de Temperatura (°C):")
print(f"  - Mínima: {df['temperatura_celsius'].min():.2f}")
print(f"  - Máxima: {df['temperatura_celsius'].max():.2f}")
print(f"  - Média: {df['temperatura_celsius'].mean():.2f}")
print(f"  - Desvio Padrão: {df['temperatura_celsius'].std():.2f}")

print(f"\nEstatísticas de Umidade (%):")
print(f"  - Mínima: {df['umidade_percentual'].min():.2f}")
print(f"  - Máxima: {df['umidade_percentual'].max():.2f}")
print(f"  - Média: {df['umidade_percentual'].mean():.2f}")
print(f"  - Desvio Padrão: {df['umidade_percentual'].std():.2f}")

print(f"\nMatriz de Correlação Temperatura x Risco:")
corr_temp_risco = df['temperatura_celsius'].corr(df['risco_incendio'])
print(f"  - Correlação: {corr_temp_risco:.4f}")

print(f"\nMatriz de Correlação Umidade x Risco:")
corr_umid_risco = df['umidade_percentual'].corr(df['risco_incendio'])
print(f"  - Correlação: {corr_umid_risco:.4f}")

# Salvar em diferentes formatos
# CSV
csv_path = 'dados_incendio_amazonia.csv'
df.to_csv(csv_path, index=False)
print(f"\n✓ Arquivo CSV salvo: {csv_path}")

# JSON
json_path = 'dados_incendio_amazonia.json'
df.to_json(json_path, orient='records', indent=2)
print(f"✓ Arquivo JSON salvo: {json_path}")

# Exibir algumas amostras
print("\n" + "=" * 60)
print("PRIMEIRAS 10 AMOSTRAS:")
print("=" * 60)
print(df.head(10).to_string(index=True))

print("\n" + "=" * 60)
print("AMOSTRAS COM ALTO RISCO:")
print("=" * 60)
print(df[df['risco_incendio'] == 1].head(10).to_string(index=True))

print("\n" + "=" * 60)
print("AMOSTRAS SEM RISCO:")
print("=" * 60)
print(df[df['risco_incendio'] == 0].head(10).to_string(index=True))
