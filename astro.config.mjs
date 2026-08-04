// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  // Static site output. `dist/` holds the final static website.
  output: 'static',
  // Deployed as a GitHub Pages project site under the consolidator account.
  site: 'https://sethuiyer.github.io',
  base: '/tensor-to-tenant',
  build: {
    format: 'directory',
  },
  markdown: {
    shikiConfig: {
      theme: 'github-dark',
    },
  },
});
