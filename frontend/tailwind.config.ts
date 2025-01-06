import type { Config } from "tailwindcss";
import typography from "@tailwindcss/typography";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class", // Enables dark mode switching with class
  theme: {
    extend: {
      colors: {
        light: {
          primary: "#fefcf5", 
          secondary: "#f6f4eb", 
          accent: "#e8e6df",
          text: "#1c1c1c",
        },
        dark: {
          primary: "#0a0a0a",
          secondary: "#111111",
          accent: "#2c3e50", // Slightly lighter for hover contrast
          text: "#ffffff",
        },
        gray: {
          50: "#fafafa",
          100: "#f5f5f5",
          200: "#e5e5e5",
          700: "#374151",
          750: "#2d2d2d", // Custom mid-tone gray
          800: "#1e293b",
          900: "#111827",
        },
        green: {
          500: "#2ecc71",
        },
        ring: {
          DEFAULT: "#3b3b3b",  // Darker focus ring for accessibility
        },
      },
      fontFamily: {
        sans: ["Montserrat", "Inter", "sans-serif"],
      },
    },
  },
  plugins: [typography],
};

export default config;
