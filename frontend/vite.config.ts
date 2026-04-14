import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // Proxy all /api requests to the FastAPI backend
      '/api': {
        target: 'http://localhost:8002',
        changeOrigin: true,
        secure: false,
      },
      // Proxy avatar image requests too
      '/avatars': {
        target: 'http://localhost:8002',
        changeOrigin: true,
        secure: false,
      },
    },
  },
})
