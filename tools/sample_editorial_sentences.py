"""Print a repeatable reservoir sample of prose from the built Astro site.

The sampler reads rendered HTML instead of TypeScript source. It keeps actual
copy blocks and skips navigation, code, scripts, styles, and footer text. The
sample is for human review, not automated scoring.

Usage::

    npm run build
    python3 tools/sample_editorial_sentences.py --count 100 --seed 20260324
"""
from __future__ import annotations

import argparse
import random
import re
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SITE = ROOT / "dist"
VOID_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}


class ProseBlocks(HTMLParser):
    """Collect text from prose elements while ignoring site chrome."""

    ignored_tags = {"code", "footer", "nav", "pre", "script", "style"}
    prose_tags = {"blockquote", "dd", "dt", "li", "p", "summary"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ignored_depth = 0
        self.current: list[str] | None = None
        self.blocks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if self.ignored_depth:
            if tag not in VOID_TAGS:
                self.ignored_depth += 1
            return
        if tag in self.ignored_tags or "data-pagefind-ignore" in attributes:
            self.ignored_depth = 1
        elif tag in self.prose_tags:
            self.current = []

    def handle_endtag(self, tag: str) -> None:
        if self.ignored_depth:
            if tag not in VOID_TAGS:
                self.ignored_depth -= 1
            return
        if tag in self.prose_tags and self.current is not None:
            text = re.sub(r"\s+", " ", " ".join(self.current)).strip()
            if text:
                self.blocks.append(text)
            self.current = None

    def handle_data(self, data: str) -> None:
        if not self.ignored_depth and self.current is not None:
            self.current.append(data)


def sentences(site: Path) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    files = sorted(site.rglob("*.html"))
    for path in files:
        parser = ProseBlocks()
        parser.feed(path.read_text(encoding="utf-8"))
        for block in parser.blocks:
            for sentence in re.split(r"(?<=[.!?])\s+", block):
                sentence = sentence.strip(" \u00a0")
                if 45 <= len(sentence) <= 420 and re.search(r"[A-Za-z]{3}", sentence):
                    rows.append((path.relative_to(site).as_posix(), sentence))
    return rows


def reservoir_sample(rows: list[tuple[str, str]], count: int, seed: int) -> list[tuple[str, str]]:
    rng = random.Random(seed)
    sample: list[tuple[str, str]] = []
    for index, row in enumerate(rows):
        if index < count:
            sample.append(row)
            continue
        replacement = rng.randrange(index + 1)
        if replacement < count:
            sample[replacement] = row
    return sample


def balanced_sample(rows: list[tuple[str, str]], count: int, seed: int) -> list[tuple[str, str]]:
    """Sample across pages so large pages do not swallow the review."""
    grouped: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row[0]].append(row)
    paths = sorted(grouped)
    quotas = {path: 0 for path in paths}
    remaining = min(count, len(rows))
    while remaining:
        progressed = False
        for path in paths:
            if quotas[path] < len(grouped[path]):
                quotas[path] += 1
                remaining -= 1
                progressed = True
                if not remaining:
                    break
        if not progressed:
            break

    result: list[tuple[str, str]] = []
    for index, path in enumerate(paths):
        result.extend(reservoir_sample(grouped[path], quotas[path], seed + index))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, default=DEFAULT_SITE, help="built Astro site directory")
    parser.add_argument("--count", type=int, default=100, help="number of sentences to sample")
    parser.add_argument("--seed", type=int, default=20260324, help="random seed for repeatable review")
    parser.add_argument(
        "--balanced",
        action="store_true",
        help="sample evenly across rendered pages instead of sampling globally",
    )
    args = parser.parse_args()
    site = args.site if args.site.is_absolute() else ROOT / args.site
    if args.count < 1:
        parser.error("--count must be positive")
    if not site.exists():
        parser.error(f"site directory does not exist: {site}; run npm run build first")

    rows = sentences(site)
    sample_count = min(args.count, len(rows))
    if args.balanced:
        sample = balanced_sample(rows, sample_count, args.seed)
        mode = "page-balanced"
    else:
        sample = reservoir_sample(rows, sample_count, args.seed)
        mode = "global reservoir"
    print(f"Population: {len(rows)} prose sentences")
    print(f"Sample: {len(sample)} sentences, {mode}, seed {args.seed}\n")
    for index, (path, sentence) in enumerate(sorted(sample), 1):
        print(f"{index:03d}. [{path}] {sentence}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
