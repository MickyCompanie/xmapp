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
          "primary": "#b91c1c",
          "primary-content": "#ffffff",
          "secondary": "#15803d",
          "secondary-content": "#ffffff",
          "accent": "#f59e0b",
          "accent-content": "#78350f",
          "neutral": "#1c1917",
          "neutral-content": "#f5f5f4",
          "base-100": "#fafaf9",
          "base-200": "#f3f4f6",
          "base-300": "#e5e7eb",
          "info": "#0284c7",
          "success": "#16a34a",
          "warning": "#d97706",
          "error": "#dc2626",
        },
      },
    ],
  },
}