/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // TERNS EXIM brand palette — canonical values from static/css/style.css :root
        // on the marketing site. Keep these two in sync if either changes.
        navy: {
          DEFAULT: "#002147",
          light: "#1B4F8A",
          mid: "#003177",
          deep: "#001535",
        },
        gold: {
          DEFAULT: "#D4AF37",
          light: "#F0D060",
          dark: "#9A7B0A",
        },
      },
    },
  },
  plugins: [],
}
