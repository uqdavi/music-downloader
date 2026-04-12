import type { Format } from "@/types";

interface FormatSelectorProps {
  value: Format;
  onChange: (value: Format) => void;
  disabled?: boolean;
}

const formats: { value: Format; label: string; icon: string }[] = [
  { value: "mp3", label: "MP3", icon: "🎵" },
  { value: "mp4", label: "MP4", icon: "🎬" },
];

const FormatSelector = ({ value, onChange, disabled }: FormatSelectorProps) => {
  return (
    <div className="flex gap-3">
      {formats.map((f) => (
        <button
          key={f.value}
          onClick={() => onChange(f.value)}
          disabled={disabled}
          className={`flex-1 rounded-xl px-4 py-3 text-sm font-medium transition-all duration-200 ${
            value === f.value
              ? "bg-brand-accent text-white shadow-lg shadow-brand-accent/30"
              : "bg-brand-surface text-muted-foreground border border-brand-border hover:border-brand-accent/50"
          } disabled:opacity-50 disabled:cursor-not-allowed`}
        >
          <span className="mr-2">{f.icon}</span>
          {f.label}
        </button>
      ))}
    </div>
  );
};

export default FormatSelector;
