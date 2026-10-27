import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Dev: semua request /api diteruskan ke backend FinSky.
// Ganti target lewat env: VITE_API_TARGET=http://host:port npm run dev
const target = process.env.VITE_API_TARGET || 'http://localhost:8000'

export default defineConfig({
  plugins: [react()],
  server: { port: 5173, proxy: { '/api': { target, changeOrigin: true } } },
})
