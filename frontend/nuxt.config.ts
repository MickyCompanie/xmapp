// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  app: {
    head: {
      title: 'xmapp',
      htmlAttrs: {
        'lang': 'fr',
        'data-theme': 'christmas' 
      }
    }
  },
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  modules: [
    '@nuxtjs/tailwindcss'
  ],
  vite: {
    server: {
      watch: {
        usePolling: true,
        interval: 100, // Vérifie les changements toutes les 100ms
      },
    },
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000',
      prefix: process.env.PREFIX,
      version: process.env.VERSION,
    }
  }
})