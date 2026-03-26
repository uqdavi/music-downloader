# Importa Flask (um framework para criar servidores web) e funções úteis
# Flask = ferramenta para criar o servidor
# request = para receber dados que o cliente envia
# jsonify = para converter dados em formato JSON (formato que o navegador entende)
from flask import Flask, request, jsonify

# Importa CORS (permite que sites diferentes se comuniquem com nosso servidor)
from flask_cors import CORS

import yt_dlp

# Importa threading (permite executar múltiplas coisas ao mesmo tempo)
import threading

import os

# ============================================================================
# CONFIGURAÇÃO DE PASTAS - Definindo onde os arquivos vão ser salvos
# ============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Resultado: /server
ROOT_DIR = os.path.dirname(BASE_DIR)  # Resultado: /music-downloader
# Define o caminho completo para a pasta onde os arquivos serão salvos
DOWNLOAD_DIR = os.path.join(ROOT_DIR, "downloads")  # Resultado: /music-downloader/downloads

# Cria a pasta de downloads se ela não existir
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ============================================================================
# CONFIGURAÇÃO DO SERVIDOR
# ============================================================================

# Cria a aplicação Flask (nosso servidor web)
app = Flask(__name__)
CORS(app)

progress_data = {
    "status": "idle",  # Estado inicial: sem fazer nada
    "percent": "0%",   # Começa em 0%
    "current": ""      # Sem arquivo sendo processado
}


# ============================================================================
# FUNÇÃO DE DOWNLOAD - Faz o download da playlist
# ============================================================================
def download_playlist(url, format_type):
    # Sem essa linha, Python criaria uma nova variável local ao invés de usar a global
    global progress_data
    
    # Esta função é chamada a cada update do progresso do download
    # Recebe um dicionário 'd' com informações sobre o download
    def progress_hook(d):
        if d['status'] == 'downloading':
            progress_data['status'] = 'downloading'
            
            # Pega o percentual de download e coloca em progress_data
            progress_data['percent'] = d.get('_percent_str', '0%')
            # Pega o nome do arquivo que está sendo baixado no momento
            progress_data['current'] = d.get('filename', '')

        elif d['status'] == 'finished':
            progress_data['status'] = 'processing'

    
    # Esta função retorna as configurações corretas dependendo do formato escolhido
    def get_ydl_opts():
        if format_type == 'mp3':
            return {
                # 'bestaudio/best' = pega o melhor áudio disponível
                'format': 'bestaudio/best',
                
                # Define o caminho e o nome dos arquivos baixados
                # %(playlist_title)s = nome da playlist
                # %(title)s = título do vídeo
                # %(ext)s = extensão do arquivo (mp3, mp4, etc)
                'outtmpl': os.path.join(DOWNLOAD_DIR, '%(playlist_title)s/%(title)s.%(ext)s'),
                
                # Define nossa função progress_hook como a função que acompanha progresso
                'progress_hooks': [progress_hook],
                
                # Configurações de pós-processamento (conversão para MP3)
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',  # Ferramente que extrai áudio
                    'preferredcodec': 'mp3',      # Converte para MP3
                    'preferredquality': '192',    # Qualidade do áudio (192 kbps)
                }],
            }

        else:  # mp4
            return {
                'format': 'best',
                'outtmpl': 'downloads/%(playlist_title)s/%(title)s.%(ext)s',
                'progress_hooks': [progress_hook],
            }

    ydl_opts = get_ydl_opts()



    # ========================================================================
    # INÍCIO DO DOWNLOAD
    # ========================================================================  
    # "with" = palavra-chave que garante que a sessão será fechada corretamente quando terminar
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


    # ========================================================================
    # FINALIZAÇÃO
    # ========================================================================
    progress_data['status'] = 'done'
    progress_data['percent'] = '100%'



# ============================================================================
# ROTA 1 - ENDPOINT DE DOWNLOAD (/download)
# ============================================================================

# Decorator que define esta função como uma ROTA (um endereço web)
# @app.route = cria um endereço web para this servidor
@app.route('/download', methods=['POST'])
def download():
    global progress_data

    # Recebe os dados enviados pelo cliente (em formato JSON)
    data = request.json

    url = data.get('url')
    
    format_type = data.get('format', 'mp4')  # default mp4

    progress_data = {
        "status": "starting",  # Status: iniciando
        "percent": "0%",       # 0% de progresso
        "current": ""          # Sem arquivo no momento
    }

    # ========================================================================
    # EXECUÇÃO EM THREAD (executar em paralelo)
    # ========================================================================
    # Cria uma nova thread (linha de execução) separada
    # threading.Thread = cria um processo que rodará em paralelo
    # target = qual função executar (download_playlist)
    # args = parâmetros para passar à função (url e format_type)
    thread = threading.Thread(
        target=download_playlist,
        args=(url, format_type)
    )
    
    # Inicia a thread (começa a executar o download em background)
    thread.start()

    # Retorna uma mensagem JSON para o cliente (o navegador)
    # jsonify() = converte um dicionário em JSON
    return jsonify({"message": "Download iniciado"})


# ============================================================================
# ROTA 2 - ENDPOINT DE PROGRESSO (/progress)
# ============================================================================
@app.route('/progress', methods=['GET'])
def progress():
    # Retorna os dados de progresso em formato JSON
    # O cliente (navegador) pode consultar isto para saber o progresso
    return jsonify(progress_data)


# ============================================================================
# EXECUTAR O SERVIDOR
# ============================================================================
# __name__ == '__main__' = significa que este é o arquivo principal
if __name__ == '__main__':
    # Inicia o servidor Flask
    # debug=True = modo de desenvolvimento (mostra erros detalhados, recarrega automaticamente)
    app.run(debug=True)