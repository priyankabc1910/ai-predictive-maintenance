import type { Config } from "tailwindcss";

// Design tokens for the Predictive Maintenance platform.
// Near-black navy surfaces with a technical blue accent, plus
// the three status colors used across health/risk indicators.
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        base: {
          950: "#080B10", // page background
          900: "#0D1117", // sidebar / topbar background
          850: "#111722", // panel background
          800: "#161D2B", // raised panel / card background
          700: "#1E2733", // borders, dividers
          600: "#2A3441", // hover borders
        },
        text: {
          primary: "#E6E9EE",
          secondary: "#9AA5B4",
          tertiary: "#5C6773",
        },
        accent: {
          DEFAULT: "#3B82F6",
          dim: "#1D4E8F",
          soft: "#173250",
        },
        status: {
          healthy: "#2FA85A",
          "healthy-soft": "#13301F",
          warning: "#D99A2B",
          "warning-soft": "#3A2E12",
          critical: "#D64545",
          "critical-soft": "#3A1717",
        },
      },
      fontFamily: {
        sans: [
          "Inter",
          "-apple-system",
          "BlinkMacSystemFont",
          "Segoe UI",
          "sans-serif",
        ],
        mono: ["IBM Plex Mono", "ui-monospace", "SFMono-Regular", "monospace"],
      },
      boxShadow: {
        panel: "0 1px 2px 0 rgba(0, 0, 0, 0.4)",
      },
    },
  },
  plugins: [],
} satisfies Config;
