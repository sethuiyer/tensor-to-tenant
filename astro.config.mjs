// @ts-check
import { defineConfig } from 'astro/config';

// Deployment target is selected at build time. Cloudflare Pages serves the
// site at the apex domain root (`base: '/'`); GitHub Pages serves it as a
// project site under `/tensor-to-tenant/`. The GitHub Pages workflow sets
// these via env; any other build (Cloudflare, local preview) uses the root.
const site = process.env.ASTRO_SITE ?? 'https://tensor-to-tenant.pages.dev';
const base = process.env.ASTRO_BASE ?? '/';

// https://astro.build/config
export default defineConfig({
  // Static site output. `dist/` holds the final static website.
  output: 'static',
  site,
  base,
  build: {
    format: 'directory',
  },
  markdown: {
    shikiConfig: {
      theme: 'github-dark',
    },
  },
});
