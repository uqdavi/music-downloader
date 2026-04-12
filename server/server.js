const express = require('express');
const cors = require('cors');
const { exec } = require('child_process');
const path = require('path');

const app = express();
const PORT = 5000;

// Middleware
app.use(cors());
app.use(express.json());

const DOWNLOAD_DIR = path.join(__dirname, '..', 'downloads');

// Estado global
let progressData = {
    status: 'idle',
    percent: '0%',
    current: {},
    playlist: []
};

app.post('/download', (req, res) => {
    const { url, format } = req.body;

    console.log('\n' + '='.repeat(60));
    console.log('📥 Nova requisição de download!');
    console.log(`🔗 URL: ${url}`);
    console.log(`🎵 Formato: ${format}`);
    console.log('='.repeat(60) + '\n');

    // Reset progress
    progressData = {
        status: 'extracting',
        percent: '0%',
        current: {},
        playlist: []
    };

    // Comando yt-dlp
    const formatFlag = format === 'mp3' ? '-x --audio-format mp3 --audio-quality 192' : '-f best';
    const outputTemplate = `"${path.join(DOWNLOAD_DIR, '%(playlist_title)s', '%(title)s.%(ext)s')}"`;
    
    const command = `yt-dlp ${formatFlag} -o ${outputTemplate} --progress --newline "${url}"`;

    console.log(`🚀 Executando: ${command}\n`);

    const child = exec(command, { cwd: DOWNLOAD_DIR }, (error, stdout, stderr) => {
        if (error) {
            console.error(`❌ Erro: ${error.message}`);
            progressData.status = 'error';
            return;
        }
        progressData.status = 'done';
        progressData.percent = '100%';
        console.log('\n🎉 Download concluído!');
    });

    res.status(202).json({ message: 'Download iniciado', status: 'extracting' });
});

app.get('/progress', (req, res) => {
    res.json(progressData);
});

app.listen(PORT, () => {
    console.log(`\n🚀 Servidor rodando em http://localhost:${PORT}\n`);
});
