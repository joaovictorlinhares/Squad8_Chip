from datetime import datetime
from time import sleep
import cv2
import os

def inicializar_camera():
    try:
        camera = cv2.VideoCapture(os.getenv("LINK_CAMERA"), cv2.CAP_FFMPEG)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, int(os.getenv("LARGURA_IMAGEM", 1280)))
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, int(os.getenv("ALTURA_IMAGEM", 720)))
        if not camera.isOpened():
            raise ValueError("Não foi possível conectar à câmera.")
        return camera
    except Exception as e:
        print(f"Erro ao inicializar a câmera: {e}")
        return None

def reconectar_camera(tentativas=3):
    for tentativa in range(tentativas):
        camera = inicializar_camera()
        if camera is not None:
            print(f"[{datetime.now()}] Reconectado com sucesso na tentativa {tentativa + 1}.")
            return camera
        sleep(2)
    print(f"Erro: Não foi possível conectar à câmera após {tentativas} tentativas. Encerrando a execução.")
    return None

def extrair_frame():
    camera = inicializar_camera()
    if camera is None:
        print("Erro: Não foi possível conectar à câmera. Encerrando a execução.")
        return
    
    while True:
        try:
            sucesso, frame = camera.read()
            if not sucesso:
                raise ValueError("Falha ao capturar o frame.")
            
            salvar_frame(frame)
        
        except Exception as e:
            print(f"Erro durante a captura do frame: {e}")
            if camera is not None:
                camera.release()
            camera = reconectar_camera()
            if camera is None:
                break

def salvar_frame(frame):
    try:
        data_hora = datetime.now().strftime("%Y%m%d_%H%M%S%f")
        caminho = os.path.join("volumeFrame", f"{data_hora}.jpg")
        cv2.imwrite(caminho, frame)
        sleep(INTERVALO)
    except Exception as e:
        print(f"Erro ao salvar o frame: {e}")

def gerar_intervalo(fotos_por_segundo=1):
    if 1 <= fotos_por_segundo <= 30:
        return round(1 / fotos_por_segundo, 6) - 0.025
    else:
        print("A quantidade de fotos por segundo deve estar entre 1 e 30")
        exit()

INTERVALO = gerar_intervalo(int(os.getenv("FOTOS_POR_SEGUNDO", 5)))

os.makedirs("volumeFrame", exist_ok=True)

extrair_frame()