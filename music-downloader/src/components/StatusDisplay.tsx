import type { DownloadStatus } from "@/types";

interface StatusDisplayProps {
  status: DownloadStatus;
  error: string | null;
}

const statusMap: Record<DownloadStatus, { label: string; color: string }> = {
  idle: { label: "Pronto para baixar", color: "text-muted-foreground" },
  starting: { label: "Iniciando...", color: "text-yellow-400" },
  downloading: { label: "Baixando...", color: "text-brand-accent" },
  processing: { label: "Processando...", color: "text-orange-400" },
  done: { label: "Concluído!", color: "text-green-400" },
};

const StatusDisplay = ({ status, error }: StatusDisplayProps) => {
  if (error) {
    return (
      <div className="rounded-xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-400">
        {error}
      </div>
    );
  }

  const info = statusMap[status];

  return (
    <div className={`text-sm font-medium ${info.color} transition-colors duration-300`}>
      {info.label}
    </div>
  );
};

export default StatusDisplay;
