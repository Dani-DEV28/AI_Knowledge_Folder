import { InputHTMLAttributes } from "react";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
}

export default function Input({ label, className = "", ...props }: InputProps) {
  return (
    <div>
      {label && <label className="text-xs text-gray-400 mb-1 block">{label}</label>}
      <input
        className={`w-full bg-dark-700 border border-dark-500 rounded px-3 py-2 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500 ${className}`}
        {...props}
      />
    </div>
  );
}
