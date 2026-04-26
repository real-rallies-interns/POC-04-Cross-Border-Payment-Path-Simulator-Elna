/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        obsidian: "#030712",
        navy: "#0B1117",
        slate800: "#1F2937",
        cyan: {
          DEFAULT: "#38BDF8",
          400: "#38BDF8",
        },
        indigo: {
          DEFAULT: "#818CF8",
          400: "#818CF8",
        },
      },
      fontFamily: {
        sans: ["Inter", "Geist Sans", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};