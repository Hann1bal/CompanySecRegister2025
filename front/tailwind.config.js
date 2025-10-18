// const flowbite = require('flowbite-react/tailwinds');

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './src/**/*.{js,jsx,ts,tsx}',
    './node_modules/flowbite-react/**/*.{js,jsx,ts,tsx}',
    // flowbite.content(),
  ],
  theme: {
    extend: {
      gridTemplateColumns: {
      // Simple 16 row grid
      '16': 'repeat(auto-fit, minmax(400px, 1fr))',

      // Complex site-specific row configuration
      'layout': '200px minmax(200px, 1fr) 100px',
    }},
  },
  plugins: [
    // ...
    require('flowbite/plugin'),
    // flowbite.plugin(),
  ],
};