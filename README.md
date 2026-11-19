[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/beecoder77/news-image-20261119-v2/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/beecoder77/news-image-20261119-v2/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
# The World in a Day — Thursday 19 November 2026 (v2)

One image summing up the world news of Thursday 19 November 2026, made for
the make.fun bounty [news-image-20261119](https://make.fun/bounty/news-image-20261119).

This is the second version of the entry. The first version scored 96.42%
(dev) on the partial board — the same score as the previous day's entry,
built from the same template. So v2 changes the design, not just the
stories: the front page (`entry.png`, 1024×1024, 212,956 bytes) is rebuilt
around a **drawn world map** with **numbered markers** pinned to the 8
biggest stories, keyed to a numbered list beside the map. The story count
is trimmed from 48 to 40, leaving room for the map and for legible type.

What the page holds: a dated masthead ("Thursday 19 November 2026"), a
lead story on the first-ever Trump–Xi–Putin trilateral in Shenzhen with a
hand-drawn skyline panel, a UTC timeline strip, the world map with its
8 numbered markers, 40 short sourced stories grouped across 8 sections,
a "By the numbers" box, and three more hand-drawn panels (the collapsed
Kerch Bridge span, Cyclone Akvan, Voyager 1 one light-day out).

Every story was verified against a reputable source on 19 November 2026 —
see `research-19nov-v2.md` for the source and publication time of each
story. Nothing on the page is invented: scheduled events are labelled as
scheduled, and no outcome is claimed for a meeting that had not happened
when the page was compiled.

## The 40 stories

**Lead — APEC & the summit (6):** the Trump–Xi–Putin trilateral today;
Putin on its "big potential benefit"; the banquet handshake; Xi's openness
pledge; Takaichi–Putin talks; the Canada–China thaw.

**North America (6):** Democrats take the Senate 56–44; Liu Yunping elected
House Democratic Caucus chair; Jeffries in line to be first Black speaker;
Fed minutes lean to more hikes; Trump "unhappy" with Vance on Iran; Huang
and Lutnick to testify.

**Latin America (3):** US–Venezuela anti-drug cooperation; Brazil's Senate
backs Lula's $10bn fiscal package; Mexico bets big on wind power.

**Europe (6):** the EU's €45bn Ukraine loan; the Kerch Bridge span collapse;
French troops in Ukraine; the Gas Husky sinking off Bulgaria; the Berlin
Ukraine-guarantees summit; the ICJ's Myanmar genocide judgment today.

**Middle East (5):** Iran widens its Gulf attacks; the US strike on Qeshm
Island; Saudi Arabia's all-clear; Israel's Gaza "Yellow Line" operation;
Australia's settler sanctions.

**Africa (2):** Somalia accuses the UAE of a proxy war; a drug seizure in
eastern Libya.

**Asia-Pacific (5):** Cyclone Akvan nears India; India–Japan 2+2 talks; Bank
Indonesia lifts rates; Taiwan's local-elections countdown; North Korea's
enrichment site "complete".

**Science, tech & sport (7):** GTA VI launches in New Zealand; Nvidia's
record $115.8bn quarter; Nvidia halts H200 chips to China; Anthropic lists
on Nasdaq today; Voyager 1 one light-day away; Duckett's ton seals
England's ODI series; Curry's knee damage.

## How to run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes `out/entry.png` — byte-identical on every run (verified: two
runs produce the same SHA-256). To rebuild the front page from scratch, run
`python3 build_image.py entry.png` (needs Pillow and the DejaVu fonts).

## License

MIT — see `LICENSE`.
