// Prefix an internal absolute path (e.g. `/curriculum/`) with the configured
// `base` (`/tensor-to-tenant`), so links and assets resolve under the GitHub
// Pages project sub-path. Use for every internal href/src; leave external
// URLs untouched.
export const url = (path: string): string => {
  const base = import.meta.env.BASE_URL.replace(/\/$/, ''); // e.g. '/tensor-to-tenant'
  const clean = path.replace(/^\/+/, ''); // strip leading slashes, keep trailing
  return `${base}/${clean}`;
};

export const SITE = {
  name: 'Tensor-to-Tenant',
  short: 'tensor-to-tenant',
  tagline:
    'A production-oriented learning path that turns you into an AI / software engineer who can build, evaluate, deploy, and operate ML and LLM systems — and pass the interviews that get you hired to do it.',
  description:
    '108-week AI engineering apprenticeship covering mathematics, algorithms, ML systems, LLM inference, production AI platforms, and interview readiness.',
  url: 'https://sethuiyer.github.io/tensor-to-tenant',
  consolidator: 'https://sethuiyer.github.io/',
  github: 'https://github.com/sethuiyer/tensor-to-tenant',
  darbar: 'https://aninokuma.codeberg.page/leetcode-darbar/',
  cookiecutter: 'https://github.com/sethuiyer/tensor-to-tenant/tree/main/cookiecutter',
  duration: '108 weeks · 10–15 hrs/week',
  programs: ['Foundations (W1–30)', 'Engineering + Systems (W31–69)', 'LLM Platform (W70–108)', 'Recommender'],
};
