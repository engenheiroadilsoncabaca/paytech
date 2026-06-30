# import cv2
# import os
# import glob
# import time
# from core.detector import SupplyEventDetector
# from core.ocr_plates import PlateReader
# from core.auditor import AuditLogger  # Importação do módulo de auditoria

# def process_batch_videos(data_folder):
  
#     video_extensions = ['*.mp4', '*.avi', '*.mkv']
#     video_files = []
#     for ext in video_extensions:
#         video_files.extend(glob.glob(os.path.join(data_folder, ext)))
    
#     if not video_files:
#         print(f"[ERRO] Nenhum vídeo encontrado na pasta '{data_folder}'.")
#         return

#     print(f"Encontrados {len(video_files)} arquivos de vídeo para processamento.\n")

#     detector = SupplyEventDetector(roi_coords=[106, 243, 327, 587])
    
#     leitor_ocr = PlateReader()
    
#     auditor = AuditLogger()
    
#     ultimo_ocr_tempo = 0 

#     for video_path in sorted(video_files):
#         print(f"\nIniciando processamento do arquivo: {os.path.basename(video_path)}")
        
#         cap = cv2.VideoCapture(video_path)
        
#         fps = cap.get(cv2.CAP_PROP_FPS)
#         frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
#         if fps > 0:
#             duration_min = (frame_count / fps) / 60
#             print(f"Duração: {duration_min:.2f} minutos | FPS: {fps:.2f}")

#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 break 

#             is_moving = detector.detect_motion_in_roi(frame)
            
#             if is_moving:
#                 cv2.putText(frame, "Movimento na Bomba: ATIVO", (50, 50), 
#                             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
#                 tempo_atual = time.time()
#                 if (tempo_atual - ultimo_ocr_tempo) > 5.0:
#                     print("[OCR] Abastecimento detetado! A procurar veículo na imagem...")
                    
#                     matriculas = leitor_ocr.find_and_read_plate(frame)
                    
#                     if matriculas:
#                         print(f"SUCESSO! MATRÍCULA LIDA: {matriculas}")
                        
#                         auditor.log_evento(os.path.basename(video_path), matriculas)
#                     ultimo_ocr_tempo = tempo_atual 
            
#             cv2.imshow("Monitoramento Paytech One", frame)
            
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 print("\n[INFO] Processo interrompido pelo utilizador.")
#                 cap.release()
#                 cv2.destroyAllWindows()
#                 return  

#         cap.release()
        
#     cv2.destroyAllWindows()
#     print("\nProcessamento em lote concluído com sucesso!")

# # AQUI ESTÁ A ALTERAÇÃO PARA TIRAR O ERRO DO CTRL+C
# if __name__ == "__main__":
#     DATA_DIR = "Dados"
#     try:
#         process_batch_videos(DATA_DIR)
#     except KeyboardInterrupt:
#         print("\n[INFO] O utilizador forçou a paragem do sistema (Ctrl+C). A encerrar em segurança...")

import cv2
import os
import glob
import time
from datetime import datetime
from ultralytics import YOLO
from core.ocr_plates import PlateReader
from core.auditor import AuditLogger  


def bico_tocou_veiculo(caixa_bico, caixa_veiculo):
   
    bx1, by1, bx2, by2 = caixa_bico
    vx1, vy1, vx2, vy2 = caixa_veiculo
    
    sobrepoe_x = bx1 < vx2 and bx2 > vx1
    sobrepoe_y = by1 < vy2 and by2 > vy1
    
    return sobrepoe_x and sobrepoe_y


def process_batch_videos(data_folder):
  
    video_extensions = ['*.mp4', '*.avi', '*.mkv']
    video_files = []
    for ext in video_extensions:
        video_files.extend(glob.glob(os.path.join(data_folder, ext)))
    
    if not video_files:
        print(f"[ERRO] Nenhum vídeo encontrado na pasta '{data_folder}'.")
        return

    print(f"Encontrados {len(video_files)} arquivos de vídeo para processamento.\n")

    print("[INFO] A carregar o modelo YOLOv8 treinado...")
    model = YOLO('runs/detect/train-10/weights/best.pt')  
    
    leitor_ocr = PlateReader()
    auditor = AuditLogger()
    
    ultimo_ocr_tempo = 0 

    for video_path in sorted(video_files):
        print(f"\nIniciando processamento do arquivo: {os.path.basename(video_path)}")
        cap = cv2.VideoCapture(video_path)
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        if fps > 0:
            duration_min = (frame_count / fps) / 60
            print(f"Duração: {duration_min:.2f} minutos | FPS: {fps:.2f}")

        # Variáveis da Máquina de Estados
        estado_abastecendo = False
        hora_inicio = None
        matricula_atual = "DESCONHECIDA"

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break 

            resultados = model(frame, verbose=False)
            
            caixa_do_bico = None
            caixa_do_veiculo = None
            caixa_da_placa = None
            
            # Extrair as coordenadas das coisas que nos interessam
            for box in resultados[0].boxes:
                classe_id = int(box.cls[0].item())
                coordenadas = box.xyxy[0].tolist() # [x1, y1, x2, y2]
                
                if classe_id == 0:   # 0 é o bico
                    caixa_do_bico = coordenadas
                elif classe_id == 2: # 2 é o veiculo
                    caixa_do_veiculo = coordenadas
                elif classe_id == 4: # 4 é a placa
                    caixa_da_placa = coordenadas
                    
            # MÁQUINA DE ESTADOS: Lógica de negócio
           
            if caixa_do_bico and caixa_do_veiculo:
                if bico_tocou_veiculo(caixa_do_bico, caixa_do_veiculo):
                    if not estado_abastecendo:
                        # Começou o abastecimento!
                        estado_abastecendo = True
                        hora_inicio = time.time()
                        print("\n[INÍCIO] Abastecimento detetado pela IA!")
                        matricula_atual = "DESCONHECIDA" #
                else:
                    if estado_abastecendo:
                        # Terminou o abastecimento!
                        estado_abastecendo = False
                        duracao = time.time() - hora_inicio
                        print(f"[FIM] Abastecimento concluído. Duração: {duracao:.2f}s")
                        
                        # Grava no Log o fim do evento com a matrícula lida
                        auditor.log_evento(os.path.basename(video_path), matricula_atual)

    
            if caixa_da_placa and estado_abastecendo:
                tempo_atual = time.time()
                
                if (tempo_atual - ultimo_ocr_tempo) > 5.0 and matricula_atual == "DESCONHECIDA":
                    print("[OCR] Placa encontrada pelo YOLO! A ler caracteres...")
                    
                    x1, y1, x2, y2 = map(int, caixa_da_placa)
                    crop_placa = frame[y1:y2, x1:x2]
                    
                    matriculas = leitor_ocr.find_and_read_plate(crop_placa)
                    
                    if matriculas:
                        print(f"SUCESSO! MATRÍCULA LIDA: {matriculas}")
                        matricula_atual = matriculas
                        
                    ultimo_ocr_tempo = tempo_atual 
            
            # D. VISUALIZAÇÃO
        
            frame_anotado = resultados[0].plot()
            
            texto_estado = "ABASTECENDO" if estado_abastecendo else "LIVRE"
            cor_estado = (0, 255, 0) if estado_abastecendo else (0, 0, 255)
            cv2.putText(frame_anotado, f"Estado: {texto_estado}", (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, cor_estado, 2)
            cv2.putText(frame_anotado, f"Placa: {matricula_atual}", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            
            cv2.imshow("Monitoramento Paytech One (Com IA)", frame_anotado)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\n[INFO] Processo interrompido pelo utilizador.")
                cap.release()
                cv2.destroyAllWindows()
                return  

        cap.release()
        
        if estado_abastecendo:
            auditor.log_evento(os.path.basename(video_path), matricula_atual)

    cv2.destroyAllWindows()
    print("\nProcessamento em lote concluído com sucesso!")


if __name__ == "__main__":
    DATA_DIR = "Dados"  
    try:
        process_batch_videos(DATA_DIR)
    except KeyboardInterrupt:
        print("\n[INFO] O utilizador forçou a paragem do sistema (Ctrl+C). A encerrar em segurança...")