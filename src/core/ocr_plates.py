import cv2
import easyocr
from ultralytics import YOLO

class PlateReader:
    def __init__(self):
        """Inicializa o YOLO (Deteção) e o EasyOCR (Leitura)"""
        print("[INFO] A carregar o modelo YOLOv8 (Recorte de Veículos)...")
        self.yolo = YOLO('yolov8n.pt') 
        
        print("[INFO] A carregar o EasyOCR (Leitura de Matrículas)...")
        self.reader = easyocr.Reader(['pt', 'en'], gpu=False)

    def find_and_read_plate(self, frame):
        resultados_yolo = self.yolo(frame, classes=[2, 3, 5, 7], verbose=False)
        
        textos_encontrados = []
        
        for resultado in resultados_yolo:
            for caixa in resultado.boxes:
                # Obtendo as coordenadas do veículo detetado
                x1, y1, x2, y2 = map(int, caixa.xyxy[0])
                
                recorte_carro = frame[y1:y2, x1:x2]
                
                if recorte_carro.size > 0:
                    rgb_carro = cv2.cvtColor(recorte_carro, cv2.COLOR_BGR2RGB)
                    textos = self.reader.readtext(rgb_carro, detail=0)
                    
                    for texto in textos:
                        texto_limpo = texto.upper().replace(" ", "").replace("-", "")
                        if len(texto_limpo) >= 6 and len(texto_limpo) <= 8:
                            textos_encontrados.append(texto_limpo)
                            
        return textos_encontrados