import cv2
from core.ocr_plates import PlateReader

imagem = cv2.imread("Dados/teste_carro.png") 

if imagem is None:
    print("[ERRO] Imagem 'teste_carro.png' não encontrada na pasta Dados!")
else:
    
    leitor = PlateReader()
    textos_encontrados = leitor.extract_text(imagem)
    
    print("\n" + "="*40)
    print(" MATRÍCULAS/TEXTOS DETETADOS:")
    for t in textos_encontrados:
        print(f" -> {t}")
    print("="*40 + "\n")