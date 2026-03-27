import type { Track } from "@/types";
import { Loader2 } from "lucide-react";

interface CurrentTrackProps {
  track: Track;
}

const CurrentTrack = ({ track }: CurrentTrackProps) => {
  if (!track.id) return null;

  return (
    <div className="flex items-center gap-4 rounded-xl border border-primary/20 bg-primary/5 p-3">
      <div className="relative h-14 w-14 flex-shrink-0 overflow-hidden rounded-lg">
        <img
          src={track.thumbnail}
          alt={track.title}
          className="h-full w-full object-cover"
        />
        <div className="absolute inset-0 flex items-center justify-center bg-background/40">
          <Loader2 className="h-5 w-5 animate-spin text-primary" />
        </div>
      </div>
      <div className="min-w-0 flex-1">
        <p className="text-xs font-medium uppercase tracking-wider text-primary">
          Baixando agora
        </p>
        <p className="truncate text-sm font-semibold text-foreground">
          {track.title}
        </p>
      </div>
    </div>
  );
};

export default CurrentTrack;
