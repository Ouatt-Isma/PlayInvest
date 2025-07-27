export default defineNuxtConfig({
  runtimeConfig:{public: {
    apiBase: process.env.API_BASE_URL || 'http://localhost:8000'
  }},
  vite: {
    server: {
      allowedHosts: [
        "7112-2a01-e0a-e4b-7e50-d9f6-80fa-1000-64c3.ngrok-free.app"
      ]
    }
  },
  css: ['@/assets/css/tailwind.css'],
  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },
  modules: ['nuxt-keen-slider'],
  app: {
    head: {
      link: [
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap',
        },
      ],
    },
  },
})
