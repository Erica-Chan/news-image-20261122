# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Erica-Chan/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Erica-Chan/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One image summing up the world's news of Sunday, 22 November 2026: 42 stories across 8 regions. Top story: COP31 collapses in Antalya with no climate deal. Six illustrated leads: Iran's strikes on US bases in Bahrain, suspected Ukrainian sea drones hitting the Russian warship Merkury off Benghazi, Russia's drone and missile strikes near Kyiv and on Kryvyi Rih, the capture of 'El Chapo Isidro' in Sinaloa, Iran's plan to send 14 tankers past the US blockade in the Gulf, and BepiColombo reaching Mercury orbit — plus a world map with story dots, a by-the-numbers strip and a date check. The day's other stories run as one-line briefs under region headers: Europe, Middle East, Asia & Pacific, Africa, Americas, Oceania & Sport, Markets & Tech, Culture & Science.

The poster is drawn by `compose_poster.py` (PIL; crisp text over text-free AI illustrations kept as `hero.png` / `hero2.png`) and shipped as `entry.png`. `main.ts` (Node 22, standard library only) copies it to `/output/entry.png`, so two runs write identical bytes with no network.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=96p1ekwa&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
