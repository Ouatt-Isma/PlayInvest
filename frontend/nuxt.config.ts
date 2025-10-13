export default defineNuxtConfig({
  runtimeConfig:{
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:80000'
    }
  },
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
      title: 'PlayInvest',
      meta: [
        { name: 'apple-mobile-web-app-title', content: 'PlayInvest-HD' }
      ],
      link: [
        // Favicon PNG
        { rel: 'icon', type: 'image/png', href: '/favicon-96x96.png', sizes: '96x96' },

        // Favicon SVG
        { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' },

        // Favicon classique (.ico)
        { rel: 'shortcut icon', href: '/favicon.ico' },

        // Apple icon (iPhone / iPad)
        { rel: 'apple-touch-icon', sizes: '180x180', href: '/apple-touch-icon.png' },

        // Web manifest (PWA)
        { rel: 'manifest', href: '/site.webmanifest' }
      ]
    },
  },
})
