import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        dark: {
          900: "#0d1117",
          800: "#161b22",
          700: "#1a1f2e",
          600: "#21262d",
          500: "#2d333b",
        },
        cyan: {
          400: "#22d3ee",
          500: "#06b6d4",
          600: "#0891b2",
        },
      },
    },
  },
  plugins: [],
};

export default config;
