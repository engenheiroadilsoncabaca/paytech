import math

class AdvancedDetector:
    def __init__(self, yolo_model):
        self.model = yolo_model
        
    def calcular_distancia(self, box1, box2):
        """Calcula a distância entre o centro de dois objetos."""
        centro_x1 = (box1[0] + box1[2]) / 2
        centro_y1 = (box1[1] + box1[3]) / 2
        centro_x2 = (box2[0] + box2[2]) / 2
        centro_y2 = (box2[1] + box2[3]) / 2
        return math.sqrt((centro_x2 - centro_x1)**2 + (centro_y2 - centro_y1)**2)

    def analisar_cena(self, frame):
        """
        Roda o YOLO e devolve um dicionário com o que encontrou na imagem.
        Classes esperadas do YOLO: 'veiculo', 'placa_traseira', 'placa_porta', 'pistola', 'boca_tanque', 'pessoa'
        """
        resultados = self.model(frame, verbose=False)[0]
        cena = {
            "veiculo_box": None,
            "placas": [], # Pode ter traseira ou porta
            "pistola_box": None,
            "tanque_box": None,
            "pessoa_na_frente": False
        }
        
        for box in resultados.boxes:
            classe_id = int(box.cls[0])
            nome_classe = self.model.names[classe_id]
            coords = box.xyxy[0].tolist() # [x1, y1, x2, y2]
            
            if nome_classe in ['veiculo']:
                cena["veiculo_box"] = coords
            elif nome_classe in ['placa_traseira', 'placa_porta']:
                cena["placas"].append({"tipo": nome_classe, "box": coords})
            elif nome_classe == 'pistola':
                cena["pistola_box"] = coords
            elif nome_classe == 'boca_tanque':
                cena["tanque_box"] = coords
            elif nome_classe == 'pessoa':
                cena["pessoa_na_frente"] = True
                
        return cena

    def is_abastecendo(self, cena, limite_distancia=50):
        """
        A regra de ouro: Só está a abastecer se a pistola e o tanque estiverem visíveis 
        E próximos um do outro (interseção ou quase).
        """
        if cena["pistola_box"] and cena["tanque_box"]:
            dist = self.calcular_distancia(cena["pistola_box"], cena["tanque_box"])
            if dist < limite_distancia:
                return True
        return False