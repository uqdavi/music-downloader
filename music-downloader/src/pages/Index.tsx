import UrlInput from "@/components/UrlInput";
import FormatSelector from "@/components/FormatSelector";
import DownloadButton from "@/components/DownloadButton";
import ProgressBar from "@/components/ProgressBar";
import StatusDisplay from "@/components/StatusDisplay";
import CurrentTrack from "@/components/CurrentTrack";
import PlaylistList from "@/components/PlaylistList";
import { useDownload } from "@/hooks/useDownload";
import { Music } from "lucide-react";

const Index = () => {
  const { url, setUrl, format, setFormat, loading, error, progress, handleDownload } =
    useDownload();

  const isActive = progress.status !== "idle";
  const hasPlaylist = progress.playlist.length > 0;

  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <div className="w-full max-w-lg space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <div className="inline-flex items-center justify-center h-14 w-14 rounded-2xl bg-primary/15 mb-2">
            <Music className="h-7 w-7 text-primary" />
          </div>
          <h1 className="text-2xl font-bold tracking-tight">Music Downloader</h1>
          <p className="text-sm text-muted-foreground">
            Baixe músicas e vídeos de playlists do YouTube
          </p>
        </div>

        {/* Card */}
        <div className="rounded-2xl border border-border bg-card p-6 space-y-5 shadow-xl shadow-black/20">
          <UrlInput value={url} onChange={setUrl} disabled={loading} />
          <FormatSelector value={format} onChange={setFormat} disabled={loading} />
          <DownloadButton onClick={handleDownload} loading={loading} />

          {isActive && (
            <div className="space-y-4 pt-2 animate-in fade-in slide-in-from-bottom-2 duration-300">
              <ProgressBar percent={progress.percent} current={progress.current.title} />
              <StatusDisplay status={progress.status} error={error} />
              <CurrentTrack track={progress.current} />
              {hasPlaylist && (
                <PlaylistList
                  playlist={progress.playlist}
                  currentId={progress.current.id}
                />
              )}
            </div>
          )}

          {!isActive && error && <StatusDisplay status="idle" error={error} />}
        </div>
      </div>
    </div>
  );
};

export default Index;
