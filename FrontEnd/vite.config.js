import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig(async () => {

  return {
    plugins: [react()],
    server: {
      https: {
        port: 3000
      },
    },
  };
});
