export default defineNuxtConfig({
  vite: {
    server: {
      allowedHosts: [
        "6c04-2a01-e0a-e4b-7e50-a9d3-1e39-434a-30e8.ngrok-free.app"
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
