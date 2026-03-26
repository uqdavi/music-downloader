// Importa os hooks useState e useEffect da biblioteca React
// useState: para gerenciar estado (valores que podem mudar)
// useEffect: para executar efeitos colaterais (como chamadas de API)
import { useState, useEffect } from "react";

function App() {
  const [url, setUrl] = useState("");
  const [progress, setProgress] = useState(null);
  const [format, setFormat] = useState("mp4");

  // Função assíncrona que inicia o download
  // async permite usar await para esperar requisições completarem
  async function startDownload() {
    // Realiza uma requisição POST para o servidor backend
    await fetch("http://localhost:5000/download", {
      method: "POST",
      // Define os headers (metadados da requisição)
      headers: {
        // Especifica que estamos enviando JSON
        "Content-Type": "application/json",
      },
      // Converte os dados (url e format) para JSON e envia no corpo da requisição
      body: JSON.stringify({ 
        url,          // URL da playlist a baixar
        format        // Formato desejado (mp4 ou mp3)
      }),
    });
  }

  // Hook que executa código quando o componente é montado (aparece na tela)
  useEffect(() => {
    // Cria um intervalo que executa a cada 1000ms (1 segundo)
    const interval = setInterval(async () => {
      // Faz uma requisição GET para obter o status do progresso do servidor
      const res = await fetch("http://localhost:5000/progress");
      // Converte a resposta de JSON para um objeto JavaScript
      const data = await res.json();

      setProgress(data);
    }, 1000);


    return () => clearInterval(interval);
  }, []); // O array vazio [] significa que executa apenas uma vez


  return (
    <div style={{ padding: 20 }}>
      <h1>Downloader de Playlist</h1>

      <input
        type="text"
        placeholder="Cole a URL da playlist"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        style={{ width: "400px" }}
      />

      <div>
        <label>
          <input
            type="radio"
            value="mp4"
            checked={format === "mp4"}
            onChange={() => setFormat("mp4")}
          />
          MP4
        </label>

        <label style={{ marginLeft: 10 }}>
          <input
            type="radio"
            value="mp3"
            checked={format === "mp3"}
            onChange={() => setFormat("mp3")}
          />
          MP3
        </label>
      </div>

      <button onClick={startDownload}>Baixar</button>

      {progress && (
        <div>
          {/* Exibe o status atual do download */}
          <p>Status: {progress.status}</p>
          {/* Exibe a porcentagem do progresso */}
          <p>Progresso: {progress.percent}</p>
          {/* Exibe qual arquivo está sendo baixado no momento */}
          <p>Arquivo atual: {progress.current}</p>
        </div>
      )}
    </div>
  );
}

export default App;