import cv2
import glob
import os

def calibrar_camera():
    print("[INFO] A procurar vídeos na pasta 'Dados'...")
   
    videos = glob.glob("../Dados/*.mp4") + glob.glob("../Dados/*.avi")
    
    if not videos:
        videos = glob.glob("Dados/*.mp4") + glob.glob("Dados/*.avi")

    if not videos:
        print("[ERRO] Nenhum vídeo encontrado na pasta 'Dados'.")
        return

    video_path = sorted(videos)[0]
    print(f"[INFO] A usar o ficheiro {os.path.basename(video_path)} para calibração.")

    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("[ERRO] Não foi possível ler a imagem do vídeo.")
        return

    print("\n" + "="*60)
    print(" INSTRUÇÕES DE CALIBRAÇÃO:")
    print(" 1. Vai abrir-se uma janela com a imagem do posto.")
    print(" 2. Clica e arrasta o rato para desenhar um quadrado APENAS à volta da bomba/mangueira.")
    print(" 3. Quando o quadrado estiver perfeito, pressiona a tecla 'ENTER' ou 'ESPAÇO'.")
    print(" 4. Se te enganares, desenha de novo antes de pressionar ENTER.")
    print("="*60 + "\n")

    roi = cv2.selectROI("Calibracao Paytech - Seleciona a Bomba e prime ENTER", frame, showCrosshair=True, fromCenter=False)
    cv2.destroyAllWindows()

    x, y, w, h = roi
    
    if w > 0 and h > 0:
        y1, y2, x1, x2 = int(y), int(y+h), int(x), int(x+w)
        print("\n" + ""*15)
        print(" SUCESSO! CÓPIA AS COORDENADAS ABAIXO:")
        print(f" roi_coords=[{y1}, {y2}, {x1}, {x2}]")
        print(""*15 + "\n")
        print("-> Agora abre o teu ficheiro 'src/pipeline.py' e substitui os números antigos por estes!")
    else:
        print("\n[AVISO] Calibração cancelada. Nenhum quadrado foi desenhado.")

if __name__ == "__main__":
    calibrar_camera()