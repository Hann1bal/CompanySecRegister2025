import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  server: { http: true }, // Not needed for Vite 5+

  plugins: [react()],
})
