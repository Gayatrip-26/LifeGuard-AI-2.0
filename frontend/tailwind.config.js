/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          500: "#22d3ee",
          600: "#0891b2"
        }
      }
    }
  },
  plugins: []
};
