import { useState, useEffect, useRef, useCallback } from "react";
import { startDownload, getProgress } from "@/services/api";
import type { DownloadStatus, Format, ProgressResponse, Track } from "@/types";
import { toast } from "sonner";

const emptyTrack: Track = { id: "", title: "", thumbnail: "", status: "pending" };

const initialProgress: ProgressResponse = {
  status: "idle",
  percent: "0",
  current: emptyTrack,
  playlist: [],
};

export function useDownload() {
  const [url, setUrl] = useState("");
  const [format, setFormat] = useState<Format>("mp3");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [progress, setProgress] = useState<ProgressResponse>(initialProgress);

  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const stopPolling = useCallback(() => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  }, []);

  const startPolling = useCallback(() => {
    stopPolling();
    intervalRef.current = setInterval(async () => {
      try {
        const { data } = await getProgress();
        setProgress(data);
        if (data.status === "done") {
          stopPolling();
          setLoading(false);
          toast.success("Download concluído com sucesso!");
        } else if (data.status === "error") {
          stopPolling();
          setLoading(false);
          toast.error("Erro durante o download");
        }
      } catch {
        // silently ignore polling errors
      }
    }, 1000);
  }, [stopPolling]);

  const handleDownload = useCallback(async () => {
    if (!url.trim()) {
      setError("Por favor, insira uma URL válida.");
      return;
    }
    setError(null);
    setLoading(true);
    // Resetar progresso imediatamente para mostrar "extracting"
    setProgress({ ...initialProgress, status: "extracting" });

    try {
      await startDownload({ url, format });
      startPolling();
    } catch (err: unknown) {
      setLoading(false);
      const message =
        err instanceof Error ? err.message : "Erro ao iniciar o download.";
      setError(message);
      toast.error("Falha ao iniciar download");
    }
  }, [url, format, startPolling]);

  useEffect(() => {
    return stopPolling;
  }, [stopPolling]);

  return { url, setUrl, format, setFormat, loading, error, progress, handleDownload };
}
