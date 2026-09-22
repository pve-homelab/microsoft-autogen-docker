import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// In production the frontend is served by the FastAPI backend from the same
// origin, so API calls use the relative "/api" path. During local `vite dev`
// we proxy /api (REST + WebSocket) to the backend on port 3000.
export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 5173,
    proxy: {
      "/api": {
        target: "http://localhost:3000",
        changeOrigin: true,
        ws: true,
      },
    },
  },
});
