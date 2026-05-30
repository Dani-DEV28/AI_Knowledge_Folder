interface ToggleProps {
  enabled: boolean;
  onToggle: () => void;
  label?: string;
}

export default function Toggle({ enabled, onToggle, label }: ToggleProps) {
  return (
    <button onClick={onToggle} className="flex items-center gap-2 text-sm" type="button">
      <span className={`w-8 h-4 rounded-full relative transition-colors ${enabled ? "bg-cyan-600" : "bg-dark-500"}`}>
        <span className={`absolute top-0.5 w-3 h-3 rounded-full bg-white transition-transform ${enabled ? "left-4" : "left-0.5"}`} />
      </span>
      {label && <span className="text-gray-400">{label}</span>}
    </button>
  );
}
