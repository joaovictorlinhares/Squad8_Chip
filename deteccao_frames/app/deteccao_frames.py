import os
import time
import cv2
import threading
import requests
import base64
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ultralytics import YOLO

# Configurações de Caminhos
CAMINHO_BASE = os.path.join('/app')
CAMINHO_VOLUME_FRAME = os.path.join(CAMINHO_BASE, 'volumeFrame')
CAMINHO_VOLUME_FRAME_TEMP = os.path.join(CAMINHO_VOLUME_FRAME, 'temp')
CAMINHO_VOLUME_FRAME_TREINAMENTO = os.path.join(CAMINHO_BASE, 'volumeFrameTreinamento')
CAMINHO_VOLUME_YOLO = os.path.join(CAMINHO_BASE, 'volumeYolo')

# Configurações de Ambiente
ALTA_PRECISAO = float(os.getenv('ALTA_PRECISAO', 0.75))
BAIXA_PRECISAO = float(os.getenv('BAIXA_PRECISAO', 0.5))
LARGURA_IMAGEM = float(os.getenv('LARGURA_IMAGEM', 1280))
ALTURA_IMAGEM = float(os.getenv('ALTURA_IMAGEM', 720))
URL_ENVIO_IMAGEM_API = os.getenv('URL_ENVIO_IMAGEM_API', 'http://127.0.0.1:5000/upload')
ID_CLASSE_DETECTAR = int(os.getenv('ID_CLASSE_DETECTAR', 0))
TEMPO_ATUALIZAR_MODELO = int(os.getenv('TEMPO_ATUALIZAR_MODELO', 3600))
TEMPO_INSERIR_TEMP = int(os.getenv('TEMPO_INSERIR_TEMP', 2))

# Função para obter o modelo mais recente
def obter_melhor_modelo():
    return max([os.path.join(CAMINHO_VOLUME_YOLO, f) for f in os.listdir(CAMINHO_VOLUME_YOLO)], key=os.path.getctime)

# Inicializa o modelo YOLO
def inicializar_modelo():
    caminho_modelo_recente = obter_melhor_modelo()
    print(f"Carregando o modelo: {caminho_modelo_recente}")
    return YOLO(caminho_modelo_recente)

# Inicialização do modelo
MODELO = inicializar_modelo()

# Funções Utilitárias
def verificar_diretorio(diretorio):
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

verificar_diretorio(CAMINHO_VOLUME_FRAME)
verificar_diretorio(CAMINHO_VOLUME_FRAME_TEMP)
verificar_diretorio(CAMINHO_VOLUME_FRAME_TREINAMENTO)

# Classe de Representação de Imagem
class Imagem:
    def __init__(self, nome, imagem, tipo_precisao, precisao):
        self.nome = nome
        self.imagem = imagem
        tipos_validos = ['media', 'alta']
        self.tipo = tipo_precisao if tipo_precisao in tipos_validos else 'baixa'
        self.precisao = precisao

# Funções de Manipulação de Imagem
def mover_imagens_para_temp(limite=10):
    contagem = 0
    for nome_arquivo in os.listdir(CAMINHO_VOLUME_FRAME):
        if nome_arquivo.endswith('.jpg'):
            caminho_origem = os.path.join(CAMINHO_VOLUME_FRAME, nome_arquivo)
            caminho_destino = os.path.join(CAMINHO_VOLUME_FRAME_TEMP, nome_arquivo)
            
            shutil.move(caminho_origem, caminho_destino)
            print(f"Imagem movida para temp: {caminho_destino}")
            
            contagem += 1
            if contagem >= limite:
                break

def enviar_imagem_para_api(dados_imagem, nome_arquivo, precisao):
    _, buffer = cv2.imencode('.jpg', dados_imagem)
    imagem_base64 = base64.b64encode(buffer).decode('utf-8')
    payload = {
        "file_name": nome_arquivo,
        "image": imagem_base64,
        "precision": precisao,
    }
    try:
        requests.post(URL_ENVIO_IMAGEM_API, json=payload)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar imagem: {nome_arquivo} / Erro: {e}")

def salvar_imagem_para_treinamento(dados_imagem, nome_arquivo):
    cv2.imwrite(os.path.join(CAMINHO_VOLUME_FRAME_TREINAMENTO, nome_arquivo), dados_imagem)

def deletar_temp(caminho_temp):
    if os.path.exists(caminho_temp):
        shutil.rmtree(caminho_temp)
    verificar_diretorio(caminho_temp)

# Processamento de Imagens
def processar_imagens():
    global MODELO  # Garantir que o modelo seja atualizado dentro desta função
    print(obter_melhor_modelo())
    mover_imagens_para_temp()
    imagens = MODELO(os.path.join(CAMINHO_VOLUME_FRAME_TEMP, '*.jpg'))

    for resultado in imagens:
        caixas = resultado.boxes
        caminho_arquivo = resultado.path
        nome_arquivo = os.path.basename(caminho_arquivo)
        imagem_original = resultado.orig_img

        if caixas:
            for caixa in caixas:
                id_classe = caixa.cls.item()
                if id_classe == ID_CLASSE_DETECTAR:
                    precisao = caixa.conf.item() if caixa.conf.nelement() > 0 else 0
                    if precisao >= ALTA_PRECISAO:
                        imagem_formatada = resultado.plot()
                        imagem = Imagem(nome_arquivo, imagem_formatada, 'alta', precisao)
                        threading.Thread(target=enviar_imagem_para_api, args=(imagem.imagem, imagem.nome, imagem.precisao)).start()
                    elif BAIXA_PRECISAO <= precisao < ALTA_PRECISAO:
                        threading.Thread(target=salvar_imagem_para_treinamento, args=(imagem_original, nome_arquivo)).start()

    deletar_temp(CAMINHO_VOLUME_FRAME_TEMP)

# Monitoramento de Alterações na Pasta YOLO
class ManipuladorVolumeYolo(FileSystemEventHandler):
    def on_created(self, event):
        global MODELO
        if event.src_path.endswith(".pt"):
            time.sleep(TEMPO_ATUALIZAR_MODELO)
            MODELO = inicializar_modelo() 

    def on_modified(self, event):
        global MODELO
        if event.src_path.endswith(".pt"):  
            time.sleep(TEMPO_ATUALIZAR_MODELO)  
            MODELO = inicializar_modelo() 

# Configuração do Observador de Arquivos
manipulador_volume_yolo = ManipuladorVolumeYolo()
observador = Observer()
observador.schedule(manipulador_volume_yolo, path=CAMINHO_VOLUME_YOLO, recursive=False)
observador.start()

# Execução do Processamento de Imagens em Loop
try:
    while True:
        if any(arquivo.endswith('.jpg') for arquivo in os.listdir(CAMINHO_VOLUME_FRAME)):
            processar_imagens()
        time.sleep(TEMPO_INSERIR_TEMP)
except KeyboardInterrupt:
    observador.stop()
observador.join()