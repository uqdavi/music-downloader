import { Loader2, Download } from "lucide-react";

interface DownloadButtonProps {
  onClick: () => void;
  loading: boolean;
  disabled?: boolean;
}

const DownloadButton = ({ onClick, loading, disabled }: DownloadButtonProps) => {
  return (
    <button
      onClick={onClick}
      disabled={loading || disabled}
      className="w-full rounded-xl bg-brand-accent px-6 py-3.5 text-sm font-semibold text-white transition-all duration-200 hover:brightness-110 hover:shadow-lg hover:shadow-brand-accent/30 active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
    >
      {loading ? (
        <>
          <Loader2 className="h-4 w-4 animate-spin" />
          Processando...
        </>
      ) : (
        <>
          <Download className="h-4 w-4" />
          Baixar
        </>
      )}
    </button>
  );
};

export default DownloadButton;
