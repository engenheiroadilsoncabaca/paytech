# Paytech One - Visão Computacional (PoC 4)

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

##  Equipe de Residentes

* **Aryel Medeiros:** 
* **Adilson Cabaca:** (Nível 1).
* **Amer:** 

---

## 📁 Estrutura de Diretórios

```text
paytech-poc4-visao/
├── Dados/                  # Pasta local para vídeos brutos (Ignorada no Git)
├── src/                    # Código-fonte principal
│   ├── core/               # Módulos de detecção (event_detector.py, etc)
│   └── pipeline.py         # Orquestrador do fluxo completo
├── .gitignore              # Filtros de segurança
├── requirements.txt        # Dependências do projeto
└── README.md               # Documentação principal