# Editorial style for site copy

The site can use AI to help with research, outlining, and first drafts. The
published version should still sound like a person who has made choices.
Correct grammar is not the same thing as a human voice, and deliberately adding
mistakes is not a fix either.

## House rules

- Prefer short, direct sentences. Keep a long sentence when its rhythm or
  meaning earns the extra length.
- Use ordinary punctuation. Full stops, commas, colons, parentheses, and plain
  hyphens are usually enough. Do not use em dashes in site copy.
- Cut stock transitions and filler: `dive into`, `delve into`, `glimpse into`,
  `seamlessly`, `in conclusion`, and `it is worth noting`.
- Avoid the repeated contrast frame `not just X, but Y`. Say what the thing does
  and give the concrete detail that makes it matter.
- Use lists when they help someone scan a page. Do not turn every paragraph into
  a heading, a list, or a three-part slogan.
- Give the copy a point of view. Say what the course expects, what it leaves
  out, and where a learner may struggle.
- Prefer concrete verbs and evidence over polished claims. “The benchmark took
  22 hours” is stronger than “the workflow is highly efficient.”
- Keep technical labels and number ranges intact. A hyphen in a compound term
  or a range is not the same editorial problem as an em dash used for drama.

## Review pass

Before publishing a generated draft, read it aloud once. Remove repeated
transitions, vary paragraph openings, replace vague praise with an example, and
check that each section says something the previous section did not. The final
pass belongs to a human reviewer, even when the first draft came from a model.

`python3 tools/editorial_lint.py` runs the mechanical checks. The build runs it
as well, so new em dashes and the listed stock phrases do not quietly return.
