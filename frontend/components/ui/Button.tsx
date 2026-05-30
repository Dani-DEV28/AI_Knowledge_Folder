import { ButtonHTMLAttributes } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost";
  size?: "sm" | "md";
}

export default function Button({ variant = "primary", size = "md", className = "", children, ...props }: ButtonProps) {
  const base = "rounded transition-colors font-medium";
  const variants = {
    primary: "bg-cyan-600 hover:bg-cyan-500 text-white",
    secondary: "bg-dark-700 hover:bg-dark-600 border border-dark-500 text-white",
    ghost: "text-gray-400 hover:text-cyan-400",
  };
  const sizes = { sm: "px-2 py-1 text-xs", md: "px-4 py-2 text-sm" };

  return (
    <button className={`${base} ${variants[variant]} ${sizes[size]} ${className}`} {...props}>
      {children}
    </button>
  );
}
