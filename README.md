# Paytech One - Visão Computacional (Sprint 4)

![Python](https://img.shields.io/badge/Python-3.13+-blue?style=for-the-badge&logo=python)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![YOLO](https://img.shields.io/badge/YOLO-Ultralytics-111827?style=for-the-badge)
![Ultralytics](https://img.shields.io/badge/Ultralytics-6248FF?style=for-the-badge)
![EasyOCR](https://img.shields.io/badge/EasyOCR-00A98F?style=for-the-badge)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![CVAT](https://img.shields.io/badge/CVAT-Computer%20Vision%20Annotation%20Tool-1E88E5?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

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
```

## 🛠️ Instalação do Conda (Pré-requisito)

Este projeto utiliza o gerenciador de pacotes e ambientes **Conda** (via Miniconda) para garantir a consistência do ambiente de execução. Se você ainda não o possui, siga as instruções abaixo:

### 1. Baixar o Miniconda

Recomendamos o **Miniconda** por ser uma instalação mínima e rápida.

1.  Acesse a página oficial de downloads do Miniconda: [Miniconda Installer](https://docs.conda.io/en/latest/miniconda_install.html).
2.  Baixe o instalador mais recente para o seu sistema operacional (Windows, macOS ou Linux).

### 2. Execução do Instalador

#### 💻 Windows

* Localize o arquivo `.exe` baixado e execute-o (duplo clique).
* Siga as instruções na tela, aceitando os termos de licença e optando pela instalação **"Just Me"** (Apenas para mim) e confirmando o diretório de instalação padrão.

#### 🐧 macOS e Linux

* Abra o Terminal.
* Navegue até o diretório onde você baixou o arquivo `.sh` (ex: `cd ~/Downloads`).
* Execute o instalador:
    ```bash
    bash Miniconda3-latest-Linux-x86_64.sh  # (Ajuste o nome do arquivo, se necessário)
    ```
* Siga as instruções, pressionando `ENTER` para aceitar a licença. **Quando perguntado sobre inicializar o Conda (`conda init`), digite `yes` para configurar automaticamente o ambiente `(base)`**.

### 3. Verificar a Instalação

Após a instalação e o reinício do seu terminal (ou abertura do `Anaconda Prompt` no Windows), execute:

```bash
conda --version
```
## Importar o ambeinte de Desenvolviento com todas as bibliotecas e pacotes necessários

```bash
conda env create -f environment.yml
``` 

## Ativar o ambiente importado

```bash
conda activate paytech
```


# Anotação dos dados
Fez parte do desenvolvimento do projeto da Sprint 4 a anotação dos frames dos videos enviados pela empresa, os vídeos são as gravações de abastecimento de um posto expecifico. 

Por se tratar de dados sensiveis, foi adotada a estrategia de anotação em uma ferramenta executada localmente, a escolhida foi a `CVAT (Computer Vision Anotation Tool)`.

Ter os dados devidamente anotados é uma etapa crucial para o sucesso do restante do proejto. 

### Instalação do CVAT

O CVAT é utilizado neste projeto para a anotação das imagens empregadas no treinamento do modelo YOLO.

#### Pré-requisitos

- Docker Desktop (Windows/macOS) ou Docker Engine (Linux)
- Docker Compose (já incluso nas versões recentes do Docker Desktop)

#### 1. Clone o repositório oficial

```bash
git clone https://github.com/cvat-ai/cvat.git
cd cvat
```

#### 2. Inicie os containers

```bash
docker compose up -d
```

Na primeira execução, o download das imagens pode levar alguns minutos.

#### 3. Crie um usuário administrador

Após os containers iniciarem, execute:

```bash
docker exec -it cvat_server bash -ic 'python3 ~/manage.py createsuperuser'
```

Informe:

- Username
- E-mail
- Senha

### 4. Acesse o CVAT

Abra o navegador e acesse:

```
http://localhost:8080
```

Faça login com o usuário criado anteriormente.

### 5. Encerrar o CVAT

```bash
docker compose down
```

Para remover também os volumes:

```bash
docker compose down -v
```
# Treino do modelo YOLO

Neste repositorio existem **2 experimentos** de treino do modelo `YOLO 8 nano`. Para reprodução do treino desses modelos é necessario que os dados anotados já estejam dentro dos devidos repositorios.

- O primeiro é um treino simples, executado direto no terminal através do script `treino.py`

- O segundo treino, com mais hiperparametros, apresentado no `Jupyter Notebook` `yolo.ipynb`

**OBS**: O segundo experimento foi ajustado para ser executado em uma maquina com outro processador, ele ainda pode ser reproduzido em outras maquinas mas é necessário o ajuste do parametro (detalhado no notebook). 

# Utilização do Modelo

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