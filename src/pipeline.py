import cv2
import os
import glob
import time
from core.detector import SupplyEventDetector
from core.ocr_plates import PlateReader
from core.auditor import AuditLogger  # Importação do módulo de auditoria

def process_batch_videos(data_folder):
  
    video_extensions = ['*.mp4', '*.avi', '*.mkv']
    video_files = []
    for ext in video_extensions:
        video_files.extend(glob.glob(os.path.join(data_folder, ext)))
    
    if not video_files:
        print(f"[ERRO] Nenhum vídeo encontrado na pasta '{data_folder}'.")
        return

    print(f"Encontrados {len(video_files)} arquivos de vídeo para processamento.\n")

    detector = SupplyEventDetector(roi_coords=[106, 243, 327, 587])
    
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

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break 

            is_moving = detector.detect_motion_in_roi(frame)
            
            if is_moving:
                cv2.putText(frame, "Movimento na Bomba: ATIVO", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
                tempo_atual = time.time()
                if (tempo_atual - ultimo_ocr_tempo) > 5.0:
                    print("[OCR] Abastecimento detetado! A procurar veículo na imagem...")
                    
                    matriculas = leitor_ocr.find_and_read_plate(frame)
                    
                    if matriculas:
                        print(f"SUCESSO! MATRÍCULA LIDA: {matriculas}")
                        
                        auditor.log_evento(os.path.basename(video_path), matriculas)
                    ultimo_ocr_tempo = tempo_atual 
            
            cv2.imshow("Monitoramento Paytech One", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\n[INFO] Processo interrompido pelo utilizador.")
                cap.release()
                cv2.destroyAllWindows()
                return  

        cap.release()
        
    cv2.destroyAllWindows()
    print("\nProcessamento em lote concluído com sucesso!")

if __name__ == "__main__":
    DATA_DIR = "Dados"
    process_batch_videos(DATA_DIR)