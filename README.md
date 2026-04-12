# 🎵 Music Downloader (YouTube Playlist)

Um projeto simples de estudo que permite baixar músicas ou vídeos a
partir de playlists do YouTube.

> ⚠️ Este projeto foi desenvolvido exclusivamente para fins educacionais
> e uso pessoal.

------------------------------------------------------------------------

## 🚀 Sobre o projeto

Este é um projeto base que utiliza:

-   Frontend com React (Vite)
-   Backend com Python (Flask)
-   yt-dlp para download de conteúdo do YouTube
-   FFmpeg para conversão de áudio (MP3)
-   Deno (necessário para resolver desafios do YouTube)

A ideia principal é:

-   Colar a URL de uma playlist do YouTube\
-   Escolher o formato (MP3 ou MP4)\
-   Baixar automaticamente todos os itens da playlist

------------------------------------------------------------------------

## ⚠️ Aviso importante

-   Este projeto é para uso pessoal e aprendizado\
-   Não deve ser utilizado para violar direitos autorais\
-   Você é responsável pelo uso da ferramenta

------------------------------------------------------------------------

## 🧠 Status do projeto

🚧 Em desenvolvimento

Este projeto é uma base inicial e continuará evoluindo com novas
funcionalidades.

------------------------------------------------------------------------

## 🛠️ Tecnologias utilizadas

### Frontend

-   React
-   Vite
-   TypeScript

### Backend

-   Python
-   Flask
-   yt-dlp

### Ferramentas

-   FFmpeg (obrigatório para MP3)
-   Deno (obrigatório para funcionamento do yt-dlp)

------------------------------------------------------------------------

## ⚙️ Pré-requisitos

Antes de rodar o projeto, você precisa ter instalado:

-   Node.js
-   Python (3.10+ recomendado)
-   FFmpeg
-   Deno

------------------------------------------------------------------------

## 📥 Instalando o Deno (Windows - PowerShell)

Execute o comando abaixo no PowerShell:

``` powershell
irm https://deno.land/install.ps1 | iex
```

Depois, feche e abra o terminal novamente e verifique:

``` bash
deno --version
```

------------------------------------------------------------------------

## 📥 Instalando o FFmpeg

Baixe em: https://ffmpeg.org/download.html

Depois: - Extraia os arquivos - Adicione a pasta `bin` ao PATH do
sistema

Teste com:

``` bash
ffmpeg -version
```

------------------------------------------------------------------------

## 📦 Instalação do Projeto

### 🔧 Backend

``` bash
cd server
pip install flask flask-cors yt-dlp
python server.py
```

------------------------------------------------------------------------

### 💻 Frontend

``` bash
cd music-downloader
npm install
npm run dev
```

------------------------------------------------------------------------

## 🎯 Funcionalidades

-   Download de playlists do YouTube\
-   Suporte a MP3 e MP4\
-   Barra de progresso em tempo real\
-   Exibição de nome e thumbnail das músicas\
-   Conversão automática de links do YouTube Music

------------------------------------------------------------------------

## 🧠 Observações técnicas

-   Links do YouTube Music são automaticamente convertidos para YouTube
    padrão\
-   O yt-dlp requer um runtime JavaScript (Deno) para funcionar
    corretamente\
-   O progresso é calculado manualmente usando bytes baixados

------------------------------------------------------------------------

## 📌 Autor

Davi Silva
