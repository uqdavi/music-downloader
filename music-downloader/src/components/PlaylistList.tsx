import type { Track } from "@/types";
import PlaylistItem from "./PlaylistItem";
import { ScrollArea } from "@/components/ui/scroll-area";

interface PlaylistListProps {
  playlist: Track[];
  currentId: string;
}

const PlaylistList = ({ playlist, currentId }: PlaylistListProps) => {
  if (playlist.length === 0) return null;

  return (
    <div className="space-y-2">
      <h3 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
        Playlist ({playlist.filter((t) => t.status === "done").length}/{playlist.length})
      </h3>
      <ScrollArea className="h-[280px] rounded-xl border border-border bg-secondary/30 p-2">
        <div className="space-y-1">
          {playlist.map((track) => (
            <PlaylistItem
              key={track.id}
              track={track}
              isActive={track.id === currentId}
            />
          ))}
        </div>
      </ScrollArea>
    </div>
  );
};

export default PlaylistList;
