/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./**/*.py",
    "./**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
    fontFamily: {
      signature: ["Dancing Script"]
    },
  },
  plugins: [],
}