# Paytech One - Visão Computacional

Este repositório contém a pipeline de processamento de vídeo e os modelos de Machine Learning desenvolvidos para a **Prova de Conceito 4 (PoC 4)** da parceria entre o Hub de IA e a Paytech One. 

O objetivo principal desta fase é validar a viabilidade técnica de algoritmos de visão computacional aplicados a gravações reais de estações de serviço. O sistema visa mapear temporalmente os abastecimentos e identificar ativos para auditoria e prevenção de fraudes.

---

## Objetivos do Projeto (Níveis de Maturidade)

O desenvolvimento está dividido em três níveis incrementais de entrega:

* **Nível 1: Auditoria e Mapeamento Temporal (Essencial)**
    * Detectar automaticamente os marcos de **início** e **fim** do evento de abastecimento (ex: movimentação do bocal/mangueira).
    * Sincronizar esses timestamps com o banco de dados de transações financeiras.
* **Nível 2: Identificação de Ativos (Intermediário)**
    * Localizar e isolar a região da placa do veículo na pista de abastecimento.
    * Aplicar técnicas de OCR para extrair o texto da placa.
* **Nível 3: Identificação de Fraudes (Avançado)**
    * Análise comportamental na pista para detectar anomalias operacionais.

---

## Arquitetura da Solução Atual (Implementação)

Para responder aos Níveis 1 e 2, o pipeline atual foi desenhado com foco em eficiência e redução de falsos positivos, dividindo-se em três camadas principais:

1. **Módulo de Visão (YOLOv8):** Um modelo de IA treinado especificamente para reconhecer 5 classes em ambiente de posto: `bico`, `pessoa`, `veiculo`, `toten` e `placa`. O modelo atingiu uma precisão média (mAP50) superior a 98%.
2. **Máquina de Estados (Lógica Antifraude):** Algoritmo que cruza as deteções da IA. O evento de "Abastecimento" só inicia quando a *bounding box* do `bico` sobrepõe a do `veiculo`.
3. **Módulo de Auditoria (OCR Cirúrgico):** Durante o abastecimento, a IA recorta apenas a área exata da placa, enviando essa imagem minimizada para o motor OCR, otimizando o processamento e salvando os dados em ficheiro CSV local.

---

## Equipe de Residentes

* **Aryel Medeiros** * **Adilson Cabaca:** (Nível 1 e Integração de IA)
* **Amer** ---

## Estrutura de Diretórios

Para que o pipeline funcione corretamente, a máquina local deve respeitar a seguinte hierarquia. *(Aviso: Vídeos e pesos do modelo `.pt` não são versionados no Git devido ao tamanho).*

```text
paytech-poc4-visao/
├── Dados/                  # Pasta local para vídeos brutos (Ignorada no Git)
│   └── videos/             # Coloque os vídeos (.mp4, .avi) aqui
├── output/                 # Relatórios CSV gerados automaticamente
├── runs/
│   └── detect/
│       └── train-10/
│           └── weights/
│               └── best.pt # O modelo treinado do YOLOv8 deve estar aqui
├── src/                    # Código-fonte principal
│   ├── core/               # Módulos de detecção e auditoria (ocr_plates.py, etc)
│   ├── pipeline.py         # Orquestrador do fluxo completo (Visão + Estados)
│   └── dashboard.py        # Script de geração de métricas de negócio
├── .gitignore              # Filtros de segurança
└── README.md               # Documentação

# Pré-requisitos e Execução

As bibliotecas principais do projeto podem ser instaladas através do terminal com o seguinte comando:

```bash
pip install ultralytics opencv-python pandas matplotlib
```

## 1. Iniciar o Pipeline de Auditoria em Lote

O sistema foi concebido para processar vídeos em lote (*batch processing*).

Coloque os vídeos de teste na pasta:

```text
Dados/videos
```

Em seguida, execute:

```bash
python src/pipeline.py
```

### O que acontece?

- O sistema processa todos os vídeos encontrados na pasta `Dados/videos`;
- Uma interface será aberta reproduzindo o vídeo com as detecções da IA em tempo real;
- Pressione **`q ou Ctrl+c`** para interromper a execução de forma segura.

---

## 2. Gerar o Dashboard de Negócios

Após a análise, o sistema gera automaticamente o arquivo:

```text
output/auditoria_abastecimentos.csv
```

Para extrair os principais KPIs (Taxa de Sucesso do OCR, Contagem de Veículos, entre outros) e gerar o dashboard, execute:

```bash
python src/dashboard.py
```

### Saída

Será criada a imagem:

```text
dashboard_negocio.png
```

Esta imagem é formatada para utilização em apresentações e relatórios.

---

## Fluxo Completo

```text
Instalar Dependências
        │
        ▼
pip install ultralytics opencv-python pandas matplotlib
        │
        ▼
Adicionar vídeos em
Dados/videos/
        │
        ▼
python src/pipeline.py
        │
        ▼
Gera:
output/auditoria_abastecimentos.csv
        │
        ▼
python src/dashboard.py
        │
        ▼
Gera:
dashboard_negocio.png
```
