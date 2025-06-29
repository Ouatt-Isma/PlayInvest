
/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./components/**/*.{vue,js}",
    "./layouts/**/*.{vue,js}",
    "./pages/**/*.{vue,js}",
    "./app.vue",
    "./plugins/**/*.{js,ts}",
    "./nuxt.config.{js,ts}"
  ],
  theme: {
    extend: {
      colors: {
        primary: '#0B4E5C', // ← your hex or rgb here
      },
    },
  },
  plugins: [],
  fontFamily: {
  sans: ['Poppins', 'sans-serif'],
}, 
}

