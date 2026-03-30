import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';

// Exportando a configuração básica sem os plugins manuais do Vite
export default defineConfig({
  integrations: [react(), tailwind()],
});