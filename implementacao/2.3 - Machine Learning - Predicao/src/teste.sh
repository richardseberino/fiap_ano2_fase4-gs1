#!/bin/bash

# Variáveis
TEMP=32
UMID=35
URL="http://localhost:5000/prever?temperatura=${TEMP}&umidade=${UMID}"

# Fazer requisição
RESPOSTA=$(curl -s "$URL")

# Extrair resultado
RISCO=$(echo "$RESPOSTA" | grep -o '"risco":"[^"]*"' | cut -d'"' -f4)
CONFIANCA=$(echo "$RESPOSTA" | grep -o '"confianca_percentual":[0-9.]*' | cut -d':' -f2)

echo "Risco: $RISCO (Confiança: $CONFIANCA%)"