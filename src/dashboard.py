import pandas as pd
import matplotlib.pyplot as plt

# 1. Carregar os dados reais gerados pelo teu AuditLogger
CAMINHO_CSV = "output/auditoria_abastecimentos.csv"

try:
    df = pd.read_csv(CAMINHO_CSV)
    
    # Garantir que a coluna de tempo é reconhecida como Data/Hora
    df['Timestamp_Deteccao'] = pd.to_datetime(df['Timestamp_Deteccao'], errors='coerce')
    
    # 2. Métricas de Negócio
    total_abastecimentos = len(df)
    
    # Filtrar matrículas que não foram lidas para contar os veículos únicos
    placas_validas = df[df['Matricula_Provavel'] != 'DESCONHECIDA']['Matricula_Provavel']
    veiculos_unicos = placas_validas.nunique()
    taxa_sucesso_ocr = (len(placas_validas) / total_abastecimentos) * 100 if total_abastecimentos > 0 else 0

    print("="*50)
    print("RESUMO EXECUTIVO PAYTECH ONE - PoC 4")
    print("="*50)
    print(f"Total de Abastecimentos Registados: {total_abastecimentos}")
    print(f" Veículos Únicos (Placas Lidas): {veiculos_unicos}")
    print(f" Taxa de Leitura de Matrículas: {taxa_sucesso_ocr:.1f}%")
    print("="*50)

    # 3. Gerar um Gráfico: "Volume de Abastecimentos por Câmera/Vídeo"
    plt.figure(figsize=(10, 6))
    
    # Contar quantos abastecimentos houve em cada vídeo
    contagem_video = df['Ficheiro_Origem'].value_counts()
    
    # Desenhar o gráfico de barras
    barras = contagem_video.plot(kind='bar', color='#1f77b4', edgecolor='black')
    
    plt.title('Volume de Abastecimentos Auditados por Vídeo', fontsize=14, fontweight='bold')
    plt.xlabel('Câmara / Arquivo de Vídeo', fontsize=12)
    plt.ylabel('Quantidade de Veículos', fontsize=12)
    plt.xticks(rotation=15, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    
    # Adicionar o número em cima de cada barra
    for i, v in enumerate(contagem_video):
        plt.text(i, v + 0.1, str(v), ha='center', fontweight='bold')

    plt.tight_layout()
    
    # Salvar a imagem para arrastares para a apresentação
    plt.savefig('dashboard_negocio.png', dpi=300)
    print("\n Gráfico 'dashboard_negocio.png' gerado com sucesso para a apresentação!")
    
    # Mostrar na tela
    plt.show()

except FileNotFoundError:
    print(f" Erro: O ficheiro '{CAMINHO_CSV}' não foi encontrado.")
except Exception as e:
    print(f" Erro inesperado: {e}")