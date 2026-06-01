import os
import csv
from datetime import datetime

class AuditLogger:
    def __init__(self, output_file="output/auditoria_abastecimentos.csv"):
       
        self.output_file = output_file
        
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        if not os.path.exists(self.output_file):
            with open(self.output_file, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Ficheiro_Origem", "Timestamp_Deteccao", "Matricula_Provavel", "Variacoes_Lidas"])
                
    def log_evento(self, video_nome, lista_matriculas):
        
        if not lista_matriculas:
            matricula_provavel = "DESCONHECIDO"
        else:
            matricula_provavel = max(lista_matriculas, key=len)
            
        timestamp_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        variacoes = " | ".join(lista_matriculas) if lista_matriculas else "N/A"
        
        with open(self.output_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([video_nome, timestamp_atual, matricula_provavel, variacoes])
            
        print(f"[AUDITOR] Evento registado no banco de dados! ({matricula_provavel})")