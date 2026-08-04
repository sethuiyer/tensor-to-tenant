"""Prepare a canonical System Design artifact for Weeks 46-57."""

from __future__ import annotations

import argparse
from pathlib import Path


WEEKS = {
    46: ("Delivery framework, networking, numbers", "Bitly / URL shortener"),
    47: ("API design, data modeling, indexes, contracts", "LeetCode problem service"),
    48: ("Caching, sharding, consistent hashing, CAP", "Rate limiter + distributed cache"),
    49: ("Replication, read/write scaling, contention", "News Feed / Instagram"),
    50: ("Large blobs, CDN, metadata, resumable work", "Dropbox / Google Docs"),
    51: ("Queues, workflows, long-running tasks", "Job Scheduler / Slack job queue"),
    52: ("Schema evolution, real-time updates, coordination", "WhatsApp / notifications"),
    53: ("Search, proximity, crawling, ranking", "Yelp / FB Post Search / crawler"),
    54: ("Messaging and social fan-out", "FB Live Comments / Tinder / Discord"),
    55: ("Scheduling, scarcity, marketplace correctness", "Ticketmaster / Uber / auction"),
    56: ("Streaming, analytics, data infrastructure", "Ad clicks / metrics / Robinhood / Spotify"),
    57: ("Integrated architecture and interview boss", "ChatGPT / payments / Figma"),
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--week", type=int, required=True)
    args = parser.parse_args()
    if args.week not in WEEKS:
        parser.error("week must be between 46 and 57")

    theme, case = WEEKS[args.week]
    destination = Path("09_interview/system_design/weeks") / f"week_{args.week:03d}.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        destination.write_text(
            f"""# System Design — Week {args.week}

**Theme:** {theme}
**Core case/lab:** {case}

## Frame

- Users and use cases:
- Functional requirements:
- SLOs and scale assumptions:
- Privacy, tenant, and cost constraints:

## Shape

- APIs:
- Data model and indexes:
- Partitioning / sharding:
- Cache, queue, and replication choices:

## Stress

- Consistency and contention:
- Idempotency and replay:
- Failure modes and recovery:
- Observability and capacity bottleneck:

## AI extension

- Retrieval, memory, routing, evaluation, safety, or cost connection:

## Interview defense

- Primary recommendation:
- Alternative rejected:
- Trade-off in one sentence:

## Evidence

- Diagram:
- Implementation or simulation:
- Benchmark / capacity result:
- Retrospective:
""",
            encoding="utf-8",
        )
    print(f"Prepared System Design artifact: {destination}")


if __name__ == "__main__":
    main()
