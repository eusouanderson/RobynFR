// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  ssr: true,

  // 🔹 Configuração para chamadas de API via proxy do Nginx
  runtimeConfig: {
    public: {
      apiBase: '/api', // sempre chama /api, o Nginx redireciona para o backend
    },
  },

  // quando ativar SSR, inlineStyles e devLogs precisam ser desabilitados
  features: {
    inlineStyles: false,
    devLogs: false,
  },

  build: {
    transpile: ['vuetify'],
  },

  vite: {
    ssr: {
      noExternal: ['vuetify'],
    },
  },

  css: [],

  modules: ['@nuxt/fonts', 'vuetify-nuxt-module', '@nuxt/eslint'],

  vuetify: {
    moduleOptions: {
      // https://nuxt.vuetifyjs.com/guide/server-side-rendering.html
      ssrClientHints: {
        reloadOnFirstRequest: false,
        viewportSize: true,
        prefersColorScheme: false,

        prefersColorSchemeOptions: {
          useBrowserThemeOnly: false,
        },
      },

      // se quiser customizar variáveis globais (scss)
      styles: {
        configFile: 'assets/settings.scss',
      },
    },
  },
});
