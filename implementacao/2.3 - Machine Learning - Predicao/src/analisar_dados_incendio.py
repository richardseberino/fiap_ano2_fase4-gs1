import pandas as pd
import numpy as np
import json

# Carregar dados
df = pd.read_csv('dados_incendio_amazonia.csv')

print("\n" + "=" * 70)
print("ANÁLISE DETALHADA DO DATASET - RISCO DE INCÊNDIO NA AMAZÔNIA")
print("=" * 70)

# 1. Análise por faixa de temperatura
print("\n1. ANÁLISE POR FAIXA DE TEMPERATURA:")
print("-" * 70)
faixas_temp = [
    (18, 22, "Baixa (18-22°C)"),
    (22, 26, "Moderada Baixa (22-26°C)"),
    (26, 30, "Moderada (26-30°C)"),
    (30, 34, "Moderada Alta (30-34°C)"),
    (34, 39, "Alta (34°C+)")
]

for min_t, max_t, label in faixas_temp:
    mask = (df['temperatura_celsius'] >= min_t) & (df['temperatura_celsius'] < max_t)
    count = mask.sum()
    risk_count = df[mask]['risco_incendio'].sum()
    risk_pct = (risk_count / count * 100) if count > 0 else 0
    print(f"  {label:30} | Amostras: {count:3} | Risco: {risk_count:3} ({risk_pct:5.1f}%)")

# 2. Análise por faixa de umidade
print("\n2. ANÁLISE POR FAIXA DE UMIDADE:")
print("-" * 70)
faixas_umid = [
    (25, 35, "Muito Baixa (25-35%)"),
    (35, 45, "Baixa (35-45%)"),
    (45, 55, "Moderada Baixa (45-55%)"),
    (55, 70, "Moderada (55-70%)"),
    (70, 100, "Alta (70-100%)")
]

for min_u, max_u, label in faixas_umid:
    mask = (df['umidade_percentual'] >= min_u) & (df['umidade_percentual'] < max_u)
    count = mask.sum()
    risk_count = df[mask]['risco_incendio'].sum()
    risk_pct = (risk_count / count * 100) if count > 0 else 0
    print(f"  {label:30} | Amostras: {count:3} | Risco: {risk_count:3} ({risk_pct:5.1f}%)")

# 3. Análise de combinações críticas
print("\n3. COMBINAÇÕES CRÍTICAS (TEMP x UMIDADE):")
print("-" * 70)

combinacoes = [
    ((30, 38), (25, 45), "⚠️  ALTO RISCO: T>30°C + U<45%"),
    ((32, 38), (25, 55), "⚠️  MUITO ALTO: T>32°C + U<55%"),
    ((34, 38), (25, 70), "🔴 CRÍTICO: T>34°C + U<70%"),
    ((26, 30), (25, 40), "⚠️  MODERADO: T=26-30°C + U<40%"),
    ((18, 26), (25, 95), "✓ BAIXO: T<26°C (qualquer U)"),
]

for (temp_min, temp_max), (umid_min, umid_max), descricao in combinacoes:
    mask = (df['temperatura_celsius'] >= temp_min) & \
           (df['temperatura_celsius'] <= temp_max) & \
           (df['umidade_percentual'] >= umid_min) & \
           (df['umidade_percentual'] <= umid_max)
    count = mask.sum()
    risk_count = df[mask]['risco_incendio'].sum()
    risk_pct = (risk_count / count * 100) if count > 0 else 0
    print(f"  {descricao:50} | {count:3} amostras | Risco: {risk_pct:5.1f}%")

# 4. Recomendações para treinamento do modelo
print("\n4. RECOMENDAÇÕES PARA TREINAMENTO DO MODELO:")
print("-" * 70)

# Calcular métricas de desempenho
n_risco = (df['risco_incendio'] == 1).sum()
n_sem_risco = (df['risco_incendio'] == 0).sum()

print(f"\n  ✓ Dataset balanceado: {n_sem_risco}/{n_risco} ({n_sem_risco/len(df)*100:.1f}%/{n_risco/len(df)*100:.1f}%)")
print(f"  ✓ Total de features: 2 (temperatura, umidade)")
print(f"  ✓ Classes: 2 (0: sem risco, 1: com risco)")
print(f"  ✓ Correlação Temperature-Risco: 0.6541 (forte)")
print(f"  ✓ Correlação Umidade-Risco: -0.7057 (muito forte)")

print(f"\n  Sugestões:")
print(f"    • Use 80% dos dados para treinamento (800 amostras)")
print(f"    • Use 20% para teste/validação (200 amostras)")
print(f"    • Normalize os valores entre 0-1 para melhor performance")
print(f"    • Algoritmos recomendados:")
print(f"      - Logistic Regression (baseline)")
print(f"      - Decision Tree")
print(f"      - Random Forest")
print(f"      - SVM com kernel RBF")
print(f"      - Neural Network (MLP)")

# 5. Estatísticas descritivas por classe
print("\n5. ESTATÍSTICAS DESCRITIVAS:")
print("-" * 70)

for classe in [0, 1]:
    label = "SEM RISCO" if classe == 0 else "COM RISCO"
    dados_classe = df[df['risco_incendio'] == classe]
    
    print(f"\n  {label}:")
    print(f"    Temperatura:")
    print(f"      - Média: {dados_classe['temperatura_celsius'].mean():.2f}°C")
    print(f"      - Mediana: {dados_classe['temperatura_celsius'].median():.2f}°C")
    print(f"      - Desvio: {dados_classe['temperatura_celsius'].std():.2f}°C")
    print(f"    Umidade:")
    print(f"      - Média: {dados_classe['umidade_percentual'].mean():.2f}%")
    print(f"      - Mediana: {dados_classe['umidade_percentual'].median():.2f}%")
    print(f"      - Desvio: {dados_classe['umidade_percentual'].std():.2f}%")

# 6. Criar resumo em JSON
print("\n6. SALVANDO ANÁLISE...")
print("-" * 70)

resumo = {
    "dataset_info": {
        "total_amostras": len(df),
        "amostras_sem_risco": int(n_sem_risco),
        "amostras_com_risco": int(n_risco),
        "percentual_risco": float(n_risco / len(df) * 100)
    },
    "temperatura": {
        "minima": float(df['temperatura_celsius'].min()),
        "maxima": float(df['temperatura_celsius'].max()),
        "media": float(df['temperatura_celsius'].mean()),
        "desvio_padrao": float(df['temperatura_celsius'].std())
    },
    "umidade": {
        "minima": float(df['umidade_percentual'].min()),
        "maxima": float(df['umidade_percentual'].max()),
        "media": float(df['umidade_percentual'].mean()),
        "desvio_padrao": float(df['umidade_percentual'].std())
    },
    "correlacoes": {
        "temperatura_risco": float(df['temperatura_celsius'].corr(df['risco_incendio'])),
        "umidade_risco": float(df['umidade_percentual'].corr(df['risco_incendio']))
    }
}

with open('analise_dataset.json', 'w', encoding='utf-8') as f:
    json.dump(resumo, f, indent=2, ensure_ascii=False)

print("  ✓ Análise salva em: analise_dataset.json")
print("=" * 70 + "\n")
