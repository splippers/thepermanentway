# Repository Structure

What exists today, and what is planned.

## Exists

```
├── README.md
├── LORE.md                  Premise, HS2 breach, resurrection, mission
├── GAMEPLAY_OVERVIEW.md     Core loop and pillars
├── FILM_PITCH.md            Logline, tone, set pieces (casting is a joke, not a plan)
├── REPO_STRUCTURE.md
├── docs/narrative/
│   ├── character_bios.md
│   ├── loveinterestarc.md
│   ├── mary_brunel.md
│   ├── modernloveinterest.md
│   └── romantic_themes.md
├── index.html               Redirects to game/index.html
├── game.html                Redirects to game/game.html
├── tools/
│   ├── build_map.py         Builds game/map-data.js from Natural Earth geography
│   └── fetch_wsw_images.py  Fetches Mission 1 photos and credits from Wikimedia Commons
└── game/
    ├── index.html           Game hub
    ├── game.html            The game
    ├── map-data.js          Generated: real coastlines, city and station positions
    ├── mission-wsw.js       Mission 1: guided survey of the Witham-Maldon-SWF line
    ├── wsw-images.js        Generated: photo credits for Mission 1
    ├── img/wsw/             Mission 1 photos (CC BY-SA / public domain)
    ├── credits.html         Full attributions and sources
    ├── record.html          Voice Studio
    └── portraits.html       Portrait Studio
```

## Planned (not yet written)

- `docs/narrative/`: `story_arc.md`, `under_infrastructure_metaphysics.md`
- `docs/gameplay/`: `core_loop.md`, `mission_design.md`, `ui_ux.md`
- `docs/engineering/`: `simulation_model.md`, `track_geometry.md`, `hs2_incident_analysis.md`
- `docs/film/`: `screenplay_outline.md`, `set_piece_design.md`
- `concept_art/`, `prototypes/`, `data/` (maps, lidar, historical, alignments), `tools/` (route planner, cost model)
