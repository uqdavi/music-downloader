interface ProgressBarProps {
  percent: string;
  current: string;
}

const ProgressBar = ({ percent, current }: ProgressBarProps) => {
  const numericPercent = parseFloat(percent) || 0;

  return (
    <div className="w-full space-y-2">
      <div className="flex items-center justify-between text-xs text-muted-foreground">
        <span className="truncate max-w-[70%]">{current || "Aguardando..."}</span>
        <span className="font-mono font-medium text-brand-accent">{numericPercent.toFixed(0)}%</span>
      </div>
      <div className="h-2 w-full overflow-hidden rounded-full bg-brand-surface">
        <div
          className="h-full rounded-full bg-gradient-to-r from-brand-accent to-brand-glow transition-all duration-500 ease-out"
          style={{ width: `${Math.min(numericPercent, 100)}%` }}
        />
      </div>
    </div>
  );
};

export default ProgressBar;
