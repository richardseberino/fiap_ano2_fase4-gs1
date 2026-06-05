#!/bin/bash

# GUIA RÁPIDO - INICIAR E TESTAR A API
# =====================================

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║   GUIA RÁPIDO - API DE PREDIÇÃO DE RISCO DE INCÊNDIO NA AMAZÔNIA   ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}PASSO 1: Verificando arquivos...${NC}"
echo ""

ARQUIVOS=(
    "treinar_modelo_incendio.py"
    "api_predicao_incendio.py"
    "testar_api.py"
    "exemplos_uso_api.py"
)

for arquivo in "${ARQUIVOS[@]}"; do
    if [ -f "$arquivo" ]; then
        echo -e "${GREEN}✓${NC} $arquivo"
    else
        echo -e "✗ $arquivo (NÃO ENCONTRADO)"
    fi
done

echo ""

if [ ! -f "modelo_incendio.pkl" ]; then
    echo -e "${YELLOW}⚠️  AVISO: modelo_incendio.pkl não encontrado${NC}"
    echo -e "${BLUE}PASSO 2: Treinando o modelo...${NC}"
    echo ""
    python3 treinar_modelo_incendio.py
    echo ""
else
    echo -e "${GREEN}✓${NC} modelo_incendio.pkl já existe"
    echo ""
fi

echo -e "${BLUE}PASSO 3: Iniciando servidor...${NC}"
echo ""
echo "Comando: python3 api_predicao_incendio.py"
echo ""
echo "Opções:"
echo "  1) Terminal 1: python3 api_predicao_incendio.py"
echo "  2) Terminal 2: python3 testar_api.py"
echo "  3) Terminal 2: python3 exemplos_uso_api.py"
echo "  4) Terminal 2: curl 'http://localhost:5000/prever?temperatura=32&umidade=35'"
echo ""
echo -e "${YELLOW}PRÓXIMO PASSO:${NC}"
echo "  1) Abra um novo terminal"
echo "  2) Navegue até este diretório"
echo "  3) Execute: python3 api_predicao_incendio.py"
echo ""
echo -e "${BLUE}Testando status...${NC}"
echo ""

# Verificar se Flask está instalado
python3 -c "import flask" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Flask instalado"
else
    echo -e "${YELLOW}⚠️  Flask não instalado${NC}"
    echo "   Instale com: pip install flask scikit-learn pandas numpy"
fi

# Verificar se scikit-learn está instalado
python3 -c "import sklearn" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} scikit-learn instalado"
else
    echo -e "${YELLOW}⚠️  scikit-learn não instalado${NC}"
    echo "   Instale com: pip install scikit-learn"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════"
echo ""
echo -e "${GREEN}Tudo pronto! Para iniciar a API:${NC}"
echo ""
echo "  python3 api_predicao_incendio.py"
echo ""
echo "A API estará disponível em: http://localhost:5000"
echo ""
echo "Endpoints:"
echo "  • GET  /health                  - Verificar status"
echo "  • GET  /info                    - Informações da API"
echo "  • GET  /exemplo                 - Exemplos de predições"
echo "  • GET  /prever?temperatura=X&umidade=Y"
echo "  • POST /prever (JSON body)"
echo ""
echo "Exemplo:"
echo "  curl 'http://localhost:5000/prever?temperatura=32&umidade=35'"
echo ""
