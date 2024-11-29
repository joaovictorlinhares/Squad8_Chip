## Projeto de Detecção de Colisão

### Descrição do Projeto
Um projeto desenvolvido pelo Squad 8 para a Chip, proposto pela Chip em parceria com o Porto Digital e a Universidade Tiradentes.

---

### Passos de Instalação e Execução

#### 1. Pré-requisitos
Certifique-se de ter o Docker Desktop instalado no seu sistema. Ele é necessário para gerenciar os contêineres e volumes utilizados pelo projeto. Você pode baixá-lo através do link oficial:  
[Baixar Docker Desktop](https://www.docker.com/products/docker-desktop/)

#### 2. Clonando o Repositório
Clone o repositório para o seu ambiente local com o comando:
```bash
git clone https://github.com/joaovictorlinhares/Squad8_Chip.git
```
Em seguida, entre na pasta clonada:
```bash
cd <NOME_DA_PASTA_CLONADA>
```

#### 3. Configurando Variáveis de Ambiente
As variáveis de ambiente permitem ajustar o comportamento de cada serviço conforme necessário. Antes de criar os contêineres, você pode personalizá-las no arquivo `docker-compose.yml`.

Exemplo de variáveis configuráveis:
- URL da câmera (`LINK_CAMERA`) para captura de frames.
- Dimensões das imagens processadas (`LARGURA_IMAGEM` e `ALTURA_IMAGEM`).
- Limiares de precisão para detecção de objetos (`ALTA_PRECISAO` e `BAIXA_PRECISAO`).

Veja a seção [Variáveis de Ambiente](#variáveis-de-ambiente) para mais detalhes sobre todas as configurações disponíveis.

#### 4. Subindo os Contêineres
Após ajustar as configurações, use o Docker Compose para construir e iniciar os serviços. Execute o comando:
```bash
docker-compose up --build
```

---

### Visão Geral dos Componentes

#### Geração de Frame
Conecta-se a uma câmera para capturar frames conforme configurado nas variáveis de ambiente. Os frames são armazenados no volume compartilhado `volumeFrame`.

#### Detecção de Imagens
Processa os frames armazenados em `volumeFrame` usando o modelo YOLO:
- **Alta precisão**: Envia as imagens para uma API configurada.
- **Baixa precisão**: Salva as imagens em `volumeFrameTreinamento` para treinamento futuro.
- Atualiza automaticamente o modelo YOLO ao detectar mudanças em `volumeYolo`.

#### Treinamento do Modelo
Treina o modelo YOLO utilizando imagens de `volumeTreinamento` e salva a versão mais recente (`best.pt`) em `volumeYolo`.

---

### Estrutura de Volumes e Integração

1. **`volumeFrame`**: Frames capturados pelo **Geração de Frame**.
2. **`volumeFrameTreinamento`**: Imagens para treinamento, geradas pelo **Detecção de Imagens**.
3. **`volumeYolo`**: Modelo YOLO treinado, utilizado e atualizado automaticamente pelo **Detecção de Imagens**.

Fluxo de Integração:
1. **Geração de Frame** salva frames em `volumeFrame`.
2. **Detecção de Imagens** processa os frames e salva imagens de baixa precisão em `volumeFrameTreinamento` ou envia as de alta precisão para a API.
3. **Treinamento do Modelo** consome imagens de `volumeTreinamento`, treina um novo modelo, e salva a versão mais recente em `volumeYolo`.

---

### Variáveis de Ambiente
As variáveis de ambiente podem ser ajustadas conforme necessário para personalizar o comportamento dos serviços:

#### **Geração de Frame**
- `PYTHONUNBUFFERED`: Garante saída imediata do Python.
- `LINK_CAMERA`: URL da câmera.
- `LARGURA_IMAGEM` e `ALTURA_IMAGEM`: Dimensões dos frames.
- `FOTOS_SEGUNDO`: Frames por segundo.

#### **Detecção de Imagens**
- `PYTHONUNBUFFERED`: Garante saída imediata do Python.
- `ALTA_PRECISAO` e `BAIXA_PRECISAO`: Limites de precisão.
- `LARGURA_IMAGEM` e `ALTURA_IMAGEM`: Dimensões das imagens.
- `URL_ENVIO_IMAGEM_API`: URL da API para envio de imagens.
- `ID_CLASSE_DETECTAR`: Classe alvo para detecção.

---

### Composição do Squad8:
- **Bruno Souza Lima**
- **Felliphe Soares dos Santos**
- **Jairo Williams Guedes Lopes Neto**
- **João Victor Melo Fontes Linhares**
- **Jorge Célio do Prado Nascimento Júnior**
- **Jorge Vitor Silva Gois**

---

### Responsáveis pelo Código
- **João Victor Melo Fontes Linhares**: [Gerador de Frames](https://github.com/joaovictorlinhares/Squad8_Chip_Gerador_de_Frames).
- **Jairo Williams Guedes Lopes Neto**: [Detecção de Imagens](https://github.com/JairoNetoDev/Squad8_Chip_Deteccao_De_Imagens).
- **Jorge Vitor Silva Gois**: [Treinamento do Modelo](https://github.com/jorge159753/Squad8_Chip_Train_model).

---

### Contate-nos
Se você tiver dúvidas ou precisar de suporte, entre em contato com os membros do Squad8 através das informações a seguir:

| Nome                              | Contato                                                                                                   |
|-----------------------------------|-----------------------------------------------------------------------------------------------------------|
| **Bruno Souza Lima**              | [![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?logo=linkedin&style=flat)](https://www.linkedin.com/in/bruno-souza-lima-387a96275) [![GitHub](https://img.shields.io/badge/GitHub-gray?logo=github&style=flat)](https://github.com/brunoSL) |
| **Felliphe Soares dos Santos**    | [![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?logo=linkedin&style=flat)](https://www.linkedin.com/in/felliphe-soares-dos-santos-ba816626b/) [![GitHub](https://img.shields.io/badge/GitHub-gray?logo=github&style=flat)](https://github.com/fellipheS) |
| **Jairo Williams Guedes Lopes Neto** | [![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?logo=linkedin&style=flat)](https://www.linkedin.com/in/jaironetodev/) [![GitHub](https://img.shields.io/badge/GitHub-gray?logo=github&style=flat)](https://github.com/JairoNetoDev) |
| **João Victor Melo Fontes Linhares** | [![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?logo=linkedin&style=flat)](https://linkedin.com/in/joaovictorlinhares) [![GitHub](https://img.shields.io/badge/GitHub-gray?logo=github&style=flat)](https://github.com/joaovictorlinhares) |
| **Jorge Célio do Prado Nascimento Júnior** | [![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?logo=linkedin&style=flat)](https://linkedin.com/in/jorge-celio) [![GitHub](https://img.shields.io/badge/GitHub-gray?logo=github&style=flat)](https://github.com/jorgecelio) |
| **Jorge Vitor Silva Gois**        | [![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?logo=linkedin&style=flat)](https://www.linkedin.com/in/jorge-vitor-091814248/) [![GitHub](https://img.shields.io/badge/GitHub-gray?logo=github&style=flat)](https://github.com/jorge159753) |
