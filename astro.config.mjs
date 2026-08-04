// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  // Static site output. `dist/` holds the final static website.
  output: 'static',
  site: 'https://tensor-to-tenant.dev',
  build: {
    format: 'directory',
  },
  markdown: {
    shikiConfig: {
      theme: 'github-dark',
    },
  },
});
