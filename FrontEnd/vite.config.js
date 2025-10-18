import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig(async () => {

  return {
    plugins: [react()],
    server: {
      http: {
        port: 3000
      },
    },
  };
});
