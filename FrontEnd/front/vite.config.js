import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { getCert } from "./cert/createCert.js"; 

export default defineConfig(async () => {
  const { key, cert } = await getCert(); 

  return {
    plugins: [react()],
    server: {
      https: {
        key,
        cert,
        port: 3000
      },
    },
  };
});
