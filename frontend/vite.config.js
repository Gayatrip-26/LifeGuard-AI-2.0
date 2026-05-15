import path from "node:path";
import { fileURLToPath } from "node:url";
import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, path.resolve(__dirname, ".."), "");
  const proxyBackend = env.VITE_PROXY_BACKEND || "http://localhost:8000";
  const proxyIngestion =
    env.VITE_PROXY_INGESTION || "http://localhost:8101";
  const proxyPrediction =
    env.VITE_PROXY_PREDICTION || "http://localhost:8102";

  return {
    plugins: [react()],
    envDir: path.resolve(__dirname, ".."),
    server: {
      host: "0.0.0.0",
      port: 5173,
      proxy: {
        "/ingest": {
          target: proxyIngestion,
          changeOrigin: true,
        },
        "/auth": { target: proxyBackend, changeOrigin: true },
        "/users": { target: proxyBackend, changeOrigin: true },
        "/dashboard": { target: proxyBackend, changeOrigin: true },
        "/prediction": { target: proxyBackend, changeOrigin: true },
        "/alert": { target: proxyBackend, changeOrigin: true },
        "/ai": { target: proxyBackend, changeOrigin: true },
        "/health": { target: proxyBackend, changeOrigin: true },
        "/prediction-service": {
          target: proxyPrediction,
          changeOrigin: true,
          rewrite: (p) => p.replace(/^\/prediction-service/, ""),
        },
      },
    },
  };
});
