/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/components/**/*.{js,vue,ts}",
    "./app/layouts/**/*.vue",
    "./app/pages/**/*.vue",
    "./app/plugins/**/*.{js,ts}",
    "./app/app.vue",
    "./app/error.vue",
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui')
  ],
  daisyui: {
    themes: [
      {
        christmas: {
          "primary": "#b91c1c",          /* Rouge Père Noël (Boutons principaux, entêtes) */
          "primary-content": "#ffffff",  /* Texte sur fond rouge */
          "secondary": "#15803d",        /* Vert Sapin (Actions secondaires, éléments d'état) */
          "secondary-content": "#ffffff",/* Texte sur fond vert */
          "accent": "#f59e0b",           /* Or Étoile (Badges, mises en avant, notifications) */
          "accent-content": "#78350f",   /* Texte sombre sur fond or */
          "neutral": "#1c1917",          /* Marron Chocolat très sombre (Textes principaux) */
          "neutral-content": "#f5f5f4",  
          "base-100": "#fafaf9",         /* Blanc Neige Écru (Fond de page principal) */
          "base-200": "#f3f4f6",         /* Gris Givré (Cartes et conteneurs) */
          "base-300": "#e5e7eb",         /* Bordures et séparateurs */
          "info": "#0284c7",            /* Bleu Givre (Informations) */
          "success": "#16a34a",         /* Vert Guirlande (Succès) */
          "warning": "#d97706",         /* Orange Pain d'Épices (Avertissements) */
          "error": "#dc2626",           /* Rouge Sucre d'Orge (Erreurs) */
        },
      },
    ],
  },
}