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
CORS(app, resources={r"/*": {"origins": "*"}})

# ===== HANDLER PARA OPTIONS (CORS PREFLIGHT) =====
@app.route('/download', methods=['OPTIONS'])
@app.route('/progress', methods=['OPTIONS'])
def handle_options():
    return '', 200

# ===== ERROR HANDLER =====
@app.errorhandler(Exception)
def handle_error(error):
    import traceback
    print(f"\n{'='*60}")
    print(f"❌ ERRO GLOBAL: {error}")
    print(f"{'='*60}")
    traceback.print_exc()
    return jsonify({"error": str(error)}), 500

# ===== VARIÁVEL GLOBAL PARA RASTREAR O PROGRESSO =====
progress_data = {
    "status": "idle",  
    "percent": "0%",  
    "current": {},  # Informações da música que está sendo baixada agora
    "playlist": []  # Lista de todas as músicas da playlist
}

# ===== FUNÇÃO PARA BAIXAR A PLAYLIST =====
def download_playlist(url, format_type):
    # 'global' significa que vamos usar a variável progress_data que foi criada lá em cima
    global progress_data

    # ETAPA 1: Extrair informações da playlist rapidamente (modo flat)
    print("\n" + "="*60)
    print("🔍 ETAPA 1: Extraindo informações da playlist...")
    print("="*60)
    progress_data['status'] = 'extracting'
    
    # Modo flat extrai apenas IDs e URLs (muito mais rápido que modo completo)
    with yt_dlp.YoutubeDL({'extract_flat': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        entries = info.get('entries', [])
        playlist = []
        print(f"\n📋 Playlist encontrada: {info.get('title', 'Desconhecida')}")
        print(f"📊 Total de músicas: {len([e for e in entries if e])}")
        for i, video in enumerate(entries, 1):
            if video:
                # Usar ID do vídeo ou URL como fallback
                video_id = video.get("id", video.get("url", f"video_{i}"))
                # Título pode vir incompleto no modo flat, mas é melhor que nada
                title = video.get("title")
                if not title:
                    title = f"Música {i}"
                # Gerar thumbnail a partir do ID (padrão YouTube)
                thumbnail = video.get("thumbnail", "")
                if not thumbnail and video_id:
                    thumbnail = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
                playlist.append({
                    "id": video_id,
                    "title": title,
                    "thumbnail": thumbnail,
                    "status": "pending"
                })
                print(f"   {i}. {title[:60]}{'...' if len(title) > 60 else ''}")
        progress_data['playlist'] = playlist
        print(f"\n✅ Extração concluída! {len(playlist)} músicas encontradas.\n")

    # ETAPA 2: Fazer o download de cada vídeo
    print("="*60)
    print("⬇️  ETAPA 2: Iniciando downloads...")
    print("="*60 + "\n")

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
            thumbnail = info.get('thumbnail') or f"https://i.ytimg.com/vi/{current_id}/hqdefault.jpg"
            progress_data['current'] = {
                "id": current_id,
                "title": info.get('title'),
                "thumbnail": thumbnail
            }

            # Atualizar status do vídeo na playlist (e garantir thumbnail)
            for item in progress_data['playlist']:
                if item['id'] == current_id:
                    item['status'] = 'downloading'
                    if not item.get('thumbnail'):
                        item['thumbnail'] = thumbnail
                    break

        # Verificar se terminou de baixar um vídeo
        elif d['status'] == 'finished':
            info = d.get('info_dict', {})
            current_id = info.get('id')
            title = info.get('title', 'Desconhecido')

            progress_data['status'] = 'processing'
            print(f"\n✅ Download concluído: {title[:60]}{'...' if len(title) > 60 else ''}")

            # Procurar este vídeo na playlist e marcar como concluído
            for item in progress_data['playlist']:
                if item['id'] == current_id:
                    item['status'] = 'done'
                    break

    # Esta função cria as configurações corretas baseado no formato escolhido
    def get_ydl_opts():
        if format_type == 'mp3':
            print(f"🎵 Formato selecionado: MP3 (192kbps)")
            return {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(DOWNLOAD_DIR, '%(playlist_title)s/%(title)s.%(ext)s'),
                'progress_hooks': [progress_hook],
                'ignore_errors': True,  # Pular vídeos com erro e continuar
                'no_warnings': False,   # Mostrar avisos sobre vídeos pulados
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:
            print(f"🎬 Formato selecionado: MP4 (melhor qualidade)")
            return {
                'format': 'best',
                'outtmpl': os.path.join(DOWNLOAD_DIR, '%(playlist_title)s/%(title)s.%(ext)s'),
                'progress_hooks': [progress_hook],
                'ignore_errors': True,  # Pular vídeos com erro e continuar
                'no_warnings': False,
            }

    ydl_opts = get_ydl_opts()

    print(f"\n🚀 Iniciando download da playlist...\n")
    
    # Extrair URLs individuais de cada vídeo + nome da playlist
    print(f"📋 Preparando downloads individuais...")
    with yt_dlp.YoutubeDL({'extract_flat': True, 'quiet': True}) as ydl_flat:
        playlist_info = ydl_flat.extract_info(url, download=False)
        playlist_title = playlist_info.get('title', 'Playlist')
        entries = playlist_info.get('entries', [])
        videos = []
        for i, video in enumerate(entries, 1):
            if video:
                video_id = video.get('id')
                video_url = video.get('url') or f"https://www.youtube.com/watch?v={video_id}"
                videos.append({'id': video_id, 'url': video_url, 'index': i})
        
        total = len(videos)
        print(f"📋 Playlist: {playlist_title}")
        print(f"📊 {total} vídeos para baixar\n")

    # Criar pasta da playlist
    playlist_folder = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in playlist_title)
    playlist_path = os.path.join(DOWNLOAD_DIR, playlist_folder)
    os.makedirs(playlist_path, exist_ok=True)

    # Atualizar outtmpl para usar a pasta correta
    if format_type == 'mp3':
        ydl_opts['postprocessors'][0]['key'] = 'FFmpegExtractAudio'
    
    # Baixar cada vídeo individualmente com tratamento de erro
    success_count = 0
    error_count = 0
    
    for video in videos:
        video_id = video['id']
        video_url = video['url']
        video_index = video['index']
        
        # Encontrar título na playlist
        title = f"Vídeo {video_index}"
        for item in progress_data['playlist']:
            if item['id'] == video_id:
                title = item['title']
                break
        
        print(f"\n{'='*60}")
        print(f"⬇️  [{video_index}/{total}] {title[:60]}")
        print(f"{'='*60}")
        
        try:
            # Criar opções de download para este vídeo com caminho correto
            video_opts = ydl_opts.copy()
            video_opts['outtmpl'] = os.path.join(playlist_path, '%(title)s.%(ext)s')
            
            with yt_dlp.YoutubeDL(video_opts) as ydl:
                ydl.download([video_url])
            
            success_count += 1
            print(f"✅ Concluído: {title[:50]}")
            
        except Exception as e:
            error_msg = str(e)
            if 'unavailable' in error_msg.lower() or 'not available' in error_msg.lower():
                print(f"⚠️  Vídeo indisponível, pulando: {title[:50]}")
            else:
                print(f"⚠️  Erro ao baixar, pulando: {title[:50]}")
            
            error_count += 1
            
            # Marcar como skipped na playlist
            for item in progress_data['playlist']:
                if item['id'] == video_id:
                    item['status'] = 'skipped'
                    break

    print(f"\n{'='*60}")
    print(f"🎉 Download concluído!")
    print(f"✅ Sucesso: {success_count} vídeos")
    print(f"⚠️  Erros: {error_count} vídeos")
    print(f"{'='*60}\n")
    
    progress_data['status'] = 'done'
    progress_data['percent'] = '100%'

# ===== ROTA 1: RECEBER SOLICITAÇÃO DE DOWNLOAD =====
@app.route('/download', methods=['POST'])
def download():
    global progress_data

    try:
        data = request.json
        # Extrair a URL da playlist (exemplo: 'https://www.youtube.com/playlist?list=...')
        url = data.get('url')
        format_type = data.get('format', 'mp4')

        print(f"\n{'='*60}")
        print(f"📥 Nova requisição de download recebida!")
        print(f"🔗 URL: {url}")
        print(f"🎵 Formato: {format_type}")
        print(f"{'='*60}\n")

        # Reinicializar progress_data com status inicial (sem esperar extração da playlist)
        progress_data = {
            "status": "extracting",  # Novo status: extraindo informações
            "percent": "0%",
            "current": {},
            "playlist": []  # Lista será preenchida gradualmente
        }

        # ===== EXECUTAR DOWNLOAD EM PARALELO =====
        # Criar uma "thread" (processo paralelo) para não travar o servidor
        thread = threading.Thread(
            target=download_playlist,  # Função que vai executar
            args=(url, format_type)  # Parâmetros: url e formato
        )
        thread.daemon = True  # Thread morre quando o programa principal sai
        thread.start()

        # Responder ao cliente INSTANTANEAMENTE que o download começou
        return jsonify({"message": "Download iniciado", "status": "extracting"}), 202
    
    except Exception as e:
        print(f"\n❌ Erro ao processar requisição de download: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# ===== ROTA 2: CONSULTAR PROGRESSO DO DOWNLOAD =====
@app.route('/progress', methods=['GET'])
def progress():
    # Devolver o progress_data atual em formato JSON
    return jsonify(progress_data)


# ===== INICIAR O SERVIDOR =====
if __name__ == '__main__':
    # debug=False e threaded=False para evitar problemas com Python 3.14
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=False)