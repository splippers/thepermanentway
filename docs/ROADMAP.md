# The Permanent Way — Roadmap

This is the working plan. It replaces the scattered "planned, not yet written"
list in `REPO_STRUCTURE.md`. The rule is simple: one corridor, finished
properly, before the next one.

## The loop

**Survey → acquire → engineer → operate.**

A corridor is five to ten named problems tied to real assets, not a line
between two dots. The player walks the lost line, inspects what survives,
decides what to keep, buys or takes the land, builds over weeks, opens the
line, and lives with the bill.

The first corridor is Essex: Witham–Maldon–South Woodham Ferrers. Mission 1
already contains the survey. The next jobs are the structure decisions, the
land, and the opening.

## Mandates, not difficulty levels

Difficulty changes what the player is asked to decide, not the size of the
numbers. Each corridor can be played under three mandates.

| | **Restorationist** | **Engineer** | **Surveyor** |
|---|---|---|---|
| Alignment | Historical, locked | Historical + surveyed variants | Bypasses drawn on real terrain |
| Structures | Auto-repaired, costed | Inspect + restore/replace/divert | Condition uncertainty, load ratings |
| Land | Assumed CPO, no gameplay | 3–5 parcels, negotiate/buy/CPO | Parcel-level, fragmented owners |
| Consent | None | Four dials, light events | EIA, inquiry, planning conditions |
| Failure | None | A dial hits zero | Dials, legal challenge, inquiry |
| Time | Untimed, or one budget | Weekly drain | Seasons + consultation clocks |
| Map | Stylised | Corridor map with structures | LIDAR/historic/OSM planning canvas |
| Score | Weeks, cost, structures saved | Benefit-cost, consent, heritage | BCR, ecology, network benefit |

**Restorationist is not easy mode.** Consequences are hidden, not removed.
The player forces the line through, opens it quickly, and then the epilogue
presents the bill: the garden taken, the reserve cut, the listed parapet
lost, the inquiry that will arrive later. It is the "come what may" fantasy
with a conscience, and it gives the careful player a reason to replay.

The mandates are a content-depth setting, not a separate mission. One
decision graph, three cuts: Restorationist auto-resolves, Engineer sees the
structure and land choices, Surveyor sees everything plus the alignment
question and the paperwork.

## Structures are the core verb

`data/alignments/wsw_structures.csv` already lists eleven real structures
with chainages, NGRs and survey descriptions. Turn each into a decision:

- **Bridge 839, St Stephens Road, Cold Norton** — iron girder, blue brick
  parapet, ground raised 3.5 m to make a front lawn. Buy the garden and
  restore; replace and lose the parapet; or divert around it.
- **Bridge 833, Woodham Road** — three blue-brick arches, cutting below.
- **Bridge 836, Church Lane, Stow Maries** — three segmental arches, beside
  the nature reserve.
- **Bridge 840, Latchingdon Road** — three 25.5 ft arches, dentilled.
- **Bridge 852, Chelmer viaduct** — 75 ft bowstring, span demolished 1965.
- **Maldon West tunnel** — 66 yards, blocked, under the bypass roundabout.

Each structure shows condition, designation, ownership and three options.
The options move capex, gradient, heritage, consent and delay. No invented
content is needed: the survey is the design document.

## The real map

**Google is for inspection, not for planning.**

Google Maps Platform terms prohibit tracing or digitising from satellite
imagery and prohibit mixing Google and non-Google maps on the same screen
(outside the EEA). A draw-your-own-alignment canvas over Google satellite is
not a licences-clear use. Dynamic Maps are also billed per load after 10,000
a month, and a static GitHub Pages build cannot hide a key.

What we do instead:

1. **Field check (now).** Every structure gets coordinates, an "Open in
   Google Maps" link and a Street View link. No key, no overlay, no terms
   problem. The player can stand in the road and look at the garden on top
   of bridge 839 before deciding.
2. **Planning canvas (next).** OpenStreetMap data, the Environment Agency
   1 m LIDAR already in `maldon3d/`, and the 1897 OS plans already in
   `game/img/wsw/`. This is legally clean, works offline, and is better for
   the game: Google shows today, LIDAR and the 1897 map show the alignment.
3. **Optional Google layer (later, if ever).** Keep the map component
   provider-agnostic so a licensed Google canvas can be swapped in without
   rewriting the game. Do not make saves or geometry depend on it.

## The Under-Infrastructure

Keep it as consequence, not a second map. Each corridor carries a **memory**
value. The longer a line stays shut, the more local detail decays: a pub
drops off the map, a station name is forgotten, an event refers to a village
nobody can quite place. Reopening restores it. Restorationist play hides the
decay until the epilogue.

## Tone

> Britain is real. The engineering is real. The bureaucracy is real. Brunel is
> the only cartoon.

The comedy comes from the gap between 1848 and a planning condition. Keep the
history straight and the sources attached. The vape and the chest hair can
stay, but they are garnish, not the meal.

## Content plan

Cut the route list to what can be made specific. Four corridors, not fifteen:

1. **Essex** — Witham–Maldon–South Woodham Ferrers. The tutorial and the
   vertical slice.
2. **Somerset & Dorset** — the emotional sequel. Beeching's cruellest cut.
3. **Cambrian** — heritage, volunteers, narrow gauge, the Welsh mountains.
4. **A national scheme** — Woodhead or the Great Central. The late game.

Each corridor needs station-level research to the standard of Mission 1, a
structure list, and at least three authored alignment variants for Surveyor
play.

## Phases

### Phase 0 — Stabilise

- GitHub Pages and a play link in the README.
- Save/resume to `localStorage`; seeded RNG for reproducible events.
- Fix the map listener leak in `renderMap()`: it re-adds document and panel
  handlers on every restore.
- Split `game.html`'s inline script into `state.js`, `map.js`, `sim.js`,
  `ui.js`. No build step required.
- Code licence; keep the existing photo credits.

### Phase 1 — The Essex vertical slice

- Mandates on the Mission 1 briefing. **Done:** picker, three modes, hidden
  debt epilogue.
- Bridge 839 in three depths. **Done:** inspect, restore/replace/divert,
  Google Maps and Street View field checks.
- Corridor map with the real centreline and all eleven structures pinned.
- Three land parcels: farmer, developer, council.
- Construction over four to six weeks with events keyed to the player's
  choices.
- Opening ledger and the next corridor unlocked.

### Phase 2 — The model

- A small cost/gradient model sampled from LIDAR. No physics engine.
- Replace instant restoration with phased works.
- Operating ledger: demand × service quality, maintenance, one fares slider.
- Dials become outputs of the model, not inputs to it.

### Phase 3 — Content and presentation

- Mission 2 (Somerset & Dorset) in the same schema.
- Voice and portrait studios wired into engineer unlocks.
- The 3D viewer used as an inspection reward, reachable from a structure.
- Story arc around the corridors.

### Phase 4 — Reach

- Keyboard and screen-reader pass on the map and dossier.
- Vendor fonts and three.js, or accept the offline breakage explicitly.
- Playwright smoke test: start → mission → restore → save → reload.
- Node tests for the cost and gradient functions.

## What not to build

- A train-operating sim. Trains are the reward, not the interface.
- A factions/combat layer. The Treasury, the councils and the landowners are
  already the antagonists.
- Fifteen routes with one line and one random event each.
- A literal HS∞ level. It is funnier as a consultation room you never reach.
- Google Maps as the planning canvas.

## Source data

- `data/alignments/wsw_structures.csv` — eleven surveyed structures.
- `data/alignments/wsw_centreline.csv` / `.geojson` — LIDAR-traced alignment.
- `data/alignments/wsw_profile.png` — the gradient profile.
- `maldon3d/` — LIDAR terrain, 1897 plans, as-built and 1980s eras.
- `tools/alignment/` — the tracing pipeline and its caveats.
- `game/mission-wsw.js` — the survey content, sources and photo credits.
