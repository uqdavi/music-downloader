import type { Track } from "@/types";
import { Check, Loader2, AlertCircle } from "lucide-react";

interface PlaylistItemProps {
  track: Track;
  isActive: boolean;
}

const PlaylistItem = ({ track, isActive }: PlaylistItemProps) => {
  return (
    <div
      className={`flex items-center gap-3 rounded-xl p-2.5 transition-all duration-300 ${
        isActive
          ? "bg-primary/15 ring-1 ring-primary/30"
          : track.status === "skipped"
          ? "opacity-50"
          : "hover:bg-secondary/60"
      }`}
    >
      <div className="relative h-10 w-10 flex-shrink-0 overflow-hidden rounded-lg">
        <img
          src={track.thumbnail}
          alt={track.title}
          className="h-full w-full object-cover"
          loading="lazy"
        />
        {track.status === "downloading" && (
          <div className="absolute inset-0 flex items-center justify-center bg-background/60">
            <Loader2 className="h-4 w-4 animate-spin text-primary" />
          </div>
        )}
        {track.status === "done" && (
          <div className="absolute inset-0 flex items-center justify-center bg-background/50">
            <Check className="h-4 w-4 text-green-400" />
          </div>
        )}
        {track.status === "skipped" && (
          <div className="absolute inset-0 flex items-center justify-center bg-background/60">
            <AlertCircle className="h-4 w-4 text-orange-400" />
          </div>
        )}
      </div>

      <span className={`min-w-0 flex-1 truncate text-sm font-medium ${
        track.status === "skipped" ? "text-muted-foreground line-through" : "text-foreground"
      }`}>
        {track.title}
      </span>

      <span
        className={`flex-shrink-0 text-xs font-medium ${
          track.status === "done"
            ? "text-green-400"
            : track.status === "downloading"
            ? "text-primary"
            : track.status === "skipped"
            ? "text-orange-400"
            : "text-muted-foreground"
        }`}
      >
        {track.status === "done"
          ? "Concluído"
          : track.status === "downloading"
          ? "Baixando"
          : track.status === "skipped"
          ? "Pulado"
          : "Pendente"}
      </span>
    </div>
  );
};

export default PlaylistItem;
