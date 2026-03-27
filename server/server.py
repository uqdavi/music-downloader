# Importações - Trazer bibliotecas (ferramentas) para usar no código
from flask import Flask, request, jsonify  # Flask: framework para criar servidor web, request: receber dados, jsonify: converter para JSON
from flask_cors import CORS  # CORS: permite que o servidor receba requisições de origens diferentes
import yt_dlp  
import threading  # threading: permite executar código em paralelo (simultaneamente)
import os 

# ===== CONFIGURAÇÃO DE PASTAS =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Pegar o caminho absoluto (endereço completo) da pasta onde este arquivo está
ROOT_DIR = os.path.dirname(BASE_DIR) # Pegar a pasta pai (acima) de BASE_DIR
DOWNLOAD_DIR = os.path.join(ROOT_DIR, "downloads") # Criar o caminho completo para a pasta "downloads" dentro de ROOT_DIR

# Criar a pasta "downloads" se ela não existir. exist_ok=True significa: não reclame se já existir
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ===== INICIALIZAR SERVIDOR =====
app = Flask(__name__)
CORS(app)

# ===== VARIÁVEL GLOBAL PARA RASTREAR O PROGRESSO =====
progress_data = {
    "status": "idle",  
    "percent": "0%",  
    "current": {},  # Informações da música que está sendo baixada agora
    "playlist": []  # Lista de todas as músicas da playlist
}

# ===== FUNÇÃO PARA PEGAR INFORMAÇÕES DA PLAYLIST =====
def get_playlist_info(url):
    # Usar a ferramenta yt_dlp com as seguintes configurações:
    with yt_dlp.YoutubeDL({
        'quiet': True,  # quiet=True: não mostrar mensagens desnecessárias
        'js_runtime': 'node',  # usar Node.js para processar JavaScript
        'remote_components': ['ejs:github']  # usar componentes remotos do GitHub
    }) as ydl:
        # extract_info: pegar informações do vídeo/playlist. download=False: NÃO baixar ainda
        info = ydl.extract_info(url, download=False)

        # info.get('entries', []): pegar a lista de vídeos. Se não houver, usar lista vazia []
        entries = info.get('entries', [])
        # Criar uma lista vazia para guardar informações de cada vídeo
        playlist = []

        # Para cada vídeo na playlist:
        for video in entries:
            if video:
                playlist.append({
                    "id": video.get("id"),  
                    "title": video.get("title"),  
                    "thumbnail": video.get("thumbnail"),  
                    "status": "pending"  # Status inicial: "pendente" (aguardando download)
                })
        return playlist


# ===== FUNÇÃO PARA BAIXAR A PLAYLIST =====
def download_playlist(url, format_type):
    # 'global' significa que vamos usar a variável progress_data que foi criada lá em cima
    global progress_data

    # Esta função é chamada automaticamente enquanto o vídeo está sendo baixado
    def progress_hook(d):
        # Verificar se está no status "downloading" (baixando agora)
        if d['status'] == 'downloading':
            # Pegar as informações do vídeo que está sendo baixado
            info = d.get('info_dict', {})
            current_id = info.get('id')

            # Atualizar o status global para "downloading"
            progress_data['status'] = 'downloading'
            # Pegar quantos bytes já foram baixados
            downloaded = d.get('downloaded_bytes', 0)
            # Pegar o total de bytes que precisa baixar
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)

            # Calcular o percentual de progresso (se houver total)
            if total > 0:
                percent = (downloaded / total) * 100
                progress_data['percent'] = f"{percent:.2f}%"
            else:
                progress_data['percent'] = "0%"
            
            # Guardar informações do vídeo em progresso
            progress_data['current'] = {
                "id": current_id,
                "title": info.get('title'),  
                "thumbnail": info.get('thumbnail')  
            }

            # Procurar este vídeo na playlist e atualizar seu status
            for item in progress_data['playlist']:
                # Se o ID bater:
                if item['id'] == current_id:
                    # Marcar que está "downloading" (baixando)
                    item['status'] = 'downloading'

        # Verificar se terminou de baixar um vídeo
        elif d['status'] == 'finished':
            info = d.get('info_dict', {})
            current_id = info.get('id')

            progress_data['status'] = 'processing'

            # Procurar este vídeo na playlist e marcar como concluído
            for item in progress_data['playlist']:
                if item['id'] == current_id:
                    item['status'] = 'done'


    # Esta função cria as configurações corretas baseado no formato escolhido
    def get_ydl_opts():
        if format_type == 'mp3':
            return {
                'format': 'bestaudio/best',  # Baixar o melhor áudio disponível
                'outtmpl': os.path.join(DOWNLOAD_DIR, '%(playlist_title)s/%(title)s.%(ext)s'),  # Onde salvar: pasta_downloads/nome_playlist/nome_música.extensão
                'progress_hooks': [progress_hook],  # Usar a função progress_hook para rastrear progresso
                'js_runtime': 'deno',  # Usar Deno para processar JavaScript
                'remote_components': ['ejs:github'],  # Usar componentes do GitHub
                'postprocessors': [{  # Pós-processadores: o que fazer DEPOIS de baixar
                    'key': 'FFmpegExtractAudio',  # Usar FFmpeg para extrair áudio
                    'preferredcodec': 'mp3',  # Converter para MP3
                    'preferredquality': '192',  # Qualidade de 192 kbps
                }],
            }
        else:
            return {
                'format': 'best',  
                'outtmpl': os.path.join(DOWNLOAD_DIR, '%(playlist_title)s/%(title)s.%(ext)s'),  
                'progress_hooks': [progress_hook], 
                'js_runtime': 'deno',
                'remote_components': ['ejs:github'],
            }

    # Pegar as opções configuradas baseado no formato escolhido
    ydl_opts = get_ydl_opts()

    # Usar yt_dlp com as opções configuradas para fazer o download
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Baixar a playlist inteira
        ydl.download([url])

    # Quando terminar todos os downloads:
    progress_data['status'] = 'done'  # Marcar como "done" (concluído)
    progress_data['percent'] = '100%'  

# ===== ROTA 1: RECEBER SOLICITAÇÃO DE DOWNLOAD =====
@app.route('/download', methods=['POST'])
def download():
    global progress_data

    data = request.json
    # Extrair a URL da playlist (exemplo: 'https://www.youtube.com/playlist?list=...')
    url = data.get('url')
    format_type = data.get('format', 'mp4')

    # Chamar a função get_playlist_info para pegar lista de vídeos sem baixar
    playlist = get_playlist_info(url)

    # Reinicializar progress_data com as novas informações
    progress_data = {
        "status": "starting", 
        "percent": "0%", 
        "current": {}, 
        "playlist": playlist  
    }

    # ===== EXECUTAR DOWNLOAD EM PARALELO =====
    # Criar uma "thread" (processo paralelo) para não travar o servidor
    thread = threading.Thread(
        target=download_playlist,  # Função que vai executar
        args=(url, format_type)  # Parâmetros: url e formato
    )
    thread.start()

    # Responder ao cliente que o download começou (NÃO esperar terminar)
    return jsonify({"message": "Download iniciado"})


# ===== ROTA 2: CONSULTAR PROGRESSO DO DOWNLOAD =====
@app.route('/progress', methods=['GET'])
def progress():
    # Devolver o progress_data atual em formato JSON
    return jsonify(progress_data)


# ===== INICIAR O SERVIDOR =====
if __name__ == '__main__':
    app.run(debug=True) # debug=True significa: reiniciar automaticamente ao detectar mudanças no código