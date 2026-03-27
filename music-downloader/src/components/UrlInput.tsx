interface UrlInputProps {
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

const UrlInput = ({ value, onChange, disabled }: UrlInputProps) => {
  return (
    <div className="w-full">
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        placeholder="Cole a URL da playlist do YouTube"
        className="w-full rounded-xl border border-brand-border bg-brand-surface px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground outline-none transition-all duration-200 focus:border-brand-accent focus:ring-2 focus:ring-brand-accent/30 disabled:opacity-50"
      />
    </div>
  );
};

export default UrlInput;
