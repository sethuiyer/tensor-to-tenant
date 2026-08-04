/**
 * Theme handling for the site.
 * - Reads a saved preference from localStorage.
 * - Falls back to the system color-scheme preference.
 * - Toggle button swaps between dark and light.
 */

type Theme = 'dark' | 'light';

const STORAGE_KEY = 't3-theme';

function getInitialTheme(): Theme {
  if (typeof localStorage !== 'undefined') {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved === 'dark' || saved === 'light') return saved;
  }
  if (typeof window !== 'undefined' && window.matchMedia) {
    return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  }
  return 'dark';
}

function applyTheme(theme: Theme) {
  document.documentElement.setAttribute('data-theme', theme);
  const btn = document.querySelector<HTMLButtonElement>('.theme-toggle');
  if (btn) {
    btn.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`);
    btn.textContent = theme === 'dark' ? '☀' : '☾';
  }
}

export function initTheme() {
  applyTheme(getInitialTheme());
}

export function toggleTheme() {
  const current = (document.documentElement.getAttribute('data-theme') as Theme) || 'dark';
  const next: Theme = current === 'dark' ? 'light' : 'dark';
  localStorage.setItem(STORAGE_KEY, next);
  applyTheme(next);
}

// Run immediately when the module loads (Astro <script is:inline> in head calls initTheme directly).
initTheme();
