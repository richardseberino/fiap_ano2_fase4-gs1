import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import (classification_report, confusion_matrix, 
                             accuracy_score, precision_score, recall_score, 
                             f1_score, roc_auc_score, roc_curve)
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar dados
df = pd.read_csv('dados_incendio_amazonia.csv')

print("=" * 70)
print("TREINAMENTO DE MODELOS - PREVISÃO DE RISCO DE INCÊNDIO NA AMAZÔNIA")
print("=" * 70)

# Preparar dados
X = df[['temperatura_celsius', 'umidade_percentual']]
y = df['risco_incendio']

# Dividir em treino e teste (80-20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\n1. DIVISÃO DO DATASET:")
print(f"   - Treino: {len(X_train)} amostras ({len(X_train)/len(df)*100:.1f}%)")
print(f"   - Teste: {len(X_test)} amostras ({len(X_test)/len(df)*100:.1f}%)")

# Normalizar dados
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"\n2. NORMALIZAÇÃO:")
print(f"   ✓ Dados normalizados usando StandardScaler")
print(f"   ✓ Média após normalização: [{X_train_scaled.mean(axis=0)[0]:.4f}, {X_train_scaled.mean(axis=0)[1]:.4f}]")
print(f"   ✓ Desvio padrão após normalização: [{X_train_scaled.std(axis=0)[0]:.4f}, {X_train_scaled.std(axis=0)[1]:.4f}]")

# Definir modelos para testar
modelos = {
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
    'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=5),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5),
    'SVM (RBF)': SVC(kernel='rbf', probability=True, random_state=42),
}

print(f"\n3. TREINAMENTO DE MODELOS:")
print("=" * 70)

resultados = {}

for nome_modelo, modelo in modelos.items():
    print(f"\n   {nome_modelo}:")
    print("   " + "-" * 66)
    
    # Treinar
    modelo.fit(X_train_scaled, y_train)
    
    # Prever
    y_train_pred = modelo.predict(X_train_scaled)
    y_test_pred = modelo.predict(X_test_scaled)
    
    # Calcular métricas
    train_acc = accuracy_score(y_train, y_train_pred)
    test_acc = accuracy_score(y_test, y_test_pred)
    precision = precision_score(y_test, y_test_pred)
    recall = recall_score(y_test, y_test_pred)
    f1 = f1_score(y_test, y_test_pred)
    
    # Tentar calcular ROC-AUC
    try:
        if hasattr(modelo, 'predict_proba'):
            y_test_pred_proba = modelo.predict_proba(X_test_scaled)[:, 1]
        else:
            y_test_pred_proba = modelo.decision_function(X_test_scaled)
        roc_auc = roc_auc_score(y_test, y_test_pred_proba)
    except:
        roc_auc = None
    
    resultados[nome_modelo] = {
        'modelo': modelo,
        'train_acc': train_acc,
        'test_acc': test_acc,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'roc_auc': roc_auc
    }
    
    print(f"    Acurácia no Treino: {train_acc:.4f}")
    print(f"    Acurácia no Teste:  {test_acc:.4f}")
    print(f"    Precisão:           {precision:.4f}")
    print(f"    Recall:             {recall:.4f}")
    print(f"    F1-Score:           {f1:.4f}")
    if roc_auc is not None:
        print(f"    ROC-AUC:            {roc_auc:.4f}")
    
    # Matriz de confusão
    cm = confusion_matrix(y_test, y_test_pred)
    print(f"\n    Matriz de Confusão:")
    print(f"    Verdadeiros Negativos:  {cm[0,0]:3} | Falsos Positivos: {cm[0,1]:3}")
    print(f"    Falsos Negativos:       {cm[1,0]:3} | Verdadeiros Positivos: {cm[1,1]:3}")

# Comparação entre modelos
print(f"\n\n4. COMPARAÇÃO ENTRE MODELOS:")
print("=" * 70)
print(f"{'Modelo':<25} {'Treino':<10} {'Teste':<10} {'Precisão':<10} {'Recall':<10} {'F1':<10}")
print("-" * 70)

for nome, resultado in resultados.items():
    print(f"{nome:<25} {resultado['train_acc']:.4f}    {resultado['test_acc']:.4f}    "
          f"{resultado['precision']:.4f}     {resultado['recall']:.4f}    {resultado['f1']:.4f}")

# Encontrar melhor modelo
melhor_modelo_nome = max(resultados, key=lambda x: resultados[x]['f1'])
melhor_modelo = resultados[melhor_modelo_nome]['modelo']

print(f"\n✓ MELHOR MODELO: {melhor_modelo_nome} (F1-Score: {resultados[melhor_modelo_nome]['f1']:.4f})")

# Fazer predições com o melhor modelo para exemplos realistas
print(f"\n5. EXEMPLOS DE PREDIÇÃO (Melhor Modelo - {melhor_modelo_nome}):")
print("=" * 70)

exemplos = [
    {'temp': 25, 'umid': 80, 'desc': 'Temperatura moderada, umidade alta'},
    {'temp': 32, 'umid': 35, 'desc': 'Temperatura alta, umidade baixa'},
    {'temp': 35, 'umid': 30, 'desc': 'Temperatura muito alta, umidade muito baixa'},
    {'temp': 28, 'umid': 60, 'desc': 'Temperatura normal, umidade moderada'},
    {'temp': 19, 'umid': 85, 'desc': 'Temperatura baixa, umidade muito alta'},
]

for ex in exemplos:
    entrada = scaler.transform([[ex['temp'], ex['umid']]])
    pred = melhor_modelo.predict(entrada)[0]
    
    if hasattr(melhor_modelo, 'predict_proba'):
        proba = melhor_modelo.predict_proba(entrada)[0]
        conf = proba[1] * 100 if pred == 1 else proba[0] * 100
    else:
        conf = 100
    
    risco = "🔴 RISCO" if pred == 1 else "✓ SEM RISCO"
    print(f"   Temp: {ex['temp']:2}°C | Umid: {ex['umid']:2}% | {risco:15} (Confiança: {conf:.1f}%)")
    print(f"   └─ {ex['desc']}\n")

# Relatório de classificação
print(f"6. RELATÓRIO DE CLASSIFICAÇÃO (Melhor Modelo):")
print("=" * 70)
y_test_pred_final = melhor_modelo.predict(X_test_scaled)
print(classification_report(y_test, y_test_pred_final, 
                           target_names=['Sem Risco', 'Com Risco']))

# Salvar modelo
modelo_path = 'modelo_incendio.pkl'
with open(modelo_path, 'wb') as f:
    pickle.dump({'modelo': melhor_modelo, 'scaler': scaler}, f)
print(f"\n✓ Modelo salvo em: {os.path.abspath(modelo_path)}")

print("=" * 70)
print("\n✓ Análise de modelos concluída com sucesso!\n")
