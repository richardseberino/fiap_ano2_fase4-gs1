# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# 🎓 Graduação ON em Inteligência Artificial  
## 📚 Repositório Oficial de Projetos e Trabalhos Acadêmicos
## Fase 4 - GS1

---
## Grupo DRELL

## 👨‍🎓 Integrantes:
- <a href="https://www.linkedin.com/in/richard-marques-26b3a14/">Richard</a>
- <a href="https://www.linkedin.com/in/luis-fernando-dos-santos-costa-b69894365/">Luis</a>

## 👩🏻‍💻 Sobre este Repositório

Este repositório term como objetivo documentar nossa Prova de Conceito (PoC) aplicando **os principais conceitos aprendidos na fase 3 e 4** do segundo ano de graduação de Inteligencia Artificial na FIAP 

Aqui você vai encontrar todos os detalhes, esplicações, diagrams, código e documentação do nosso projeto:

- Introdução com o propósito da nossa Prova de Conceito
- Arquitetura da solução
- Código gerado nos diferentes componentes (ESP32, APIs em Python, Interfaces em Reactive, etec)
- Video da apreserntação do projeto

Este repositório funciona como um **portfólio técnico estruturado**, evidenciando domínio progressivo das competências exigidas na formação.

---

## 1 Objetivo

Nossa prova de conceito consiste em monitorar regiões remotas com coleta de dados locais, integrada a um serviço em núvem que recebe violações de thresholds comuns nestas coletas e combina com análise de um modelo de Machine Learning treinado com dados da região para identificar possíveis riscos. Uma aplicação móvel vai alertas os responsáveis em tempo real sobre riscos que necessitam de alguma intervenção.

## 2 Arquitetura

### 2.1 Diagrama geral da solução

Visite o [Documento de Requisitos](./implementacao/2.1%20-%20Requisitos/READM.md) para maiores informações sobre os requisitos e passo a passo para colocar essa solução para rodar no seu computador simulando todas as peças e componentes. 

![Diagrama](./assets/arquitetura.png)


### 2.2 Coleta e pre-processamento (IoT e FogComputing)

Vamos usar um dispositivo IoT conectado a internet via Wi-fi com sensores de umidade e temperatura para identificar desvio nos thresholds padrões para o ambiente monitorado. Uma vez que esses thresholds sejam violados os dados da coleta serão enviados para um tópico em um broker MQTT. 
Uma instancia local no NodeRed coleta os dados do broker MQTT e envia para uma base de dados InfluxDB em um provedor de Cloud (vamos simular com uma instancia de container rodando o influxDB)

<img src="./assets/diagram-esp32.png" alt="Coleta ESP32" width="500"> 

Visite o [Documento de Definição](./implementacao/2.2%20-%20Esp32%20-%20RedNode/README.md) para ver os detalhes do código que implementamos para fazer a coleta e o envio de dados

### 2.3 Analise de desvios (Cloud Comnputing e Machine Learning)

O Serviço hospedado em cloud conectado a esta base InfluxDB le cada registro que é armazenado nela para analisar os dados sobre possíveis desvios na telemetria (umidade e temperatura) do ambiente monitorado. 

Este Serviço possui um modelo de machine learning treinado para avaliar riscos climáticos na região. O modelo foi treinado de forma supervisionada (dados etiquetados) com informações da região sobre os últimos anos. 

Este Serviço possui uma API que analisa a última coleta enviada, e retorna a análise de risco .

Consulte o [Documento](./implementacao/2.3%20-%20Machine%20Learning%20-%20Predicao/README.md) para ver como o modelo de Machine Learning foi treinado e também sobre a API em Python que consome os dados, submete ao modelo para predição e retorna o resultado via API Rest.

### 2.4 Aplicação Móvel (Desenvolvimento Mobile em Android)

Aqui os responsáveis pela área monitorada usam um apliativo em seu telefone celular onde é recebem os avisos via notificação PUSH dos alertas de riscos confirmados por dados e um modelo de Machine Learning. Com essa informação em tempo real eles conseguem reagir de forma mais tempestiva para conter o problema.

O aplicativo consulta a API do serviço de análise e quando identifica algum risco avisa o usuário com os detalhes da análise. 

<img src="./assets/android-detalhe-alerta.png" alt="Detalhe do alerta" width="300"> 

Consulte o [Documento](./implementacao/2.4%20-%20Aplicacao%20Movel/README.md) para maiores detalhes sobre a implementação da aplicação Móvel em Android. 

---

## 🧠 Estrutura Macro do Repositório

```bash
📂 FIAP-GRAD-ON-IA
│
├── 📂 implementacao
│   ├── 📂 2.1 - Requisitos
│   │   ├── 📂 imagens
│   │   ├── README.md
│   ├── 📂 2.2 - Esp32 - NodeRed
│   │   ├── 📂 imagens
│   │   ├── 📂 src
│   │   ├── README.md
│   ├── 📂 2.3 - Machine Learning - Predicao
│   │   ├── 📂 imagens
│   │   ├── 📂 src
│   │   ├── README.md
│   ├── 📂 2.4 - Aplicacao Movel
│   │   ├── 📂 imagens
│   │   ├── 📂 src
│   │   ├── README.md
└── README.md
```

---

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/SabrinaOtoni/TEMPLATE-FIAP-GRAD-ON-IA">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">FIAP</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
