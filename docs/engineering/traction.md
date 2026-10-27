# Traction: classic styling, modern power

The reward for rebuilding a corridor isn't a return to 1889. It's what
the line becomes. Brunel's mission is to restore the network, not freeze
it - the lore already says so ("rebuild the soul of the nation", not
"rebuild the nation exactly as it was"). The traction concept follows
that logic: streamlined, Gresley-era styling - the A4 Pacific (Mallard,
1938, still the fastest steam locomotive ever built, 126 mph) is the
obvious reference - carrying solar and hydrogen propulsion instead of a
firebox.

This is not a driving sim and does not become one. See
`docs/ROADMAP.md`'s "what not to build": trains are the reward, not the
interface. A modern-traction unlock is an end-state image for a
corridor the player actually revived, not a new mechanic.

## Why this isn't just a skin

Both halves of "classic styling, modern power" have real UK precedent,
which matters for a project that keeps its sources attached even in the
Brunel-is-a-cartoon parts:

- **Hydrogen.** HydroFLEX (Birmingham University and Porterbrook,
  2019-20) was the UK's first hydrogen train trial, running on the
  national network. Alstom's Coradia iLint is already in passenger
  service in Germany. A hydrogen A4 is a reasonable extrapolation, not
  a fantasy.
- **Solar.** Riding Sunbeams (Network Rail and 10:10 Climate Action)
  trialled solar power fed directly into railway traction supply near
  Aldershot. Feeding a branch line's third rail or overhead from
  trackside panels is closer to "slightly ahead of 2020s practice" than
  invented technology.

Keep that same discipline here as everywhere else in the project: where
a detail is extrapolated rather than sourced, say so.

## Where it sits in the phases

Per `docs/ROADMAP.md`:

- **Phase 2 (the model)** already plans an operating ledger - demand,
  maintenance, a fares slider. A corridor's traction choice (classic
  steam-styled hydrogen/solar vs a plainer modern unit) is a natural
  output of that ledger, not an input to it: style is something the
  player earns by operating the line well, not a knob they turn.
- **Phase 3 (content and presentation)** is where this actually gets
  built - the 3D viewer is already slated as "an inspection reward,
  reachable from a structure"; a revived corridor's hero traction image
  is the same kind of reward, reachable once the corridor is open.

## Design notes, not commitments

- Livery and shrouding: Gresley A4 proportions (full skirting, raked
  nose) are the clearest visual shorthand for "streamlined British
  express power" and need no invented styling language.
  Corridor-specific liveries (GER blue, S&D black, Cambrian green) give
  each of the four planned corridors its own version rather than one
  generic "green train".
- Sound and smoke are the hard part: an A4 without a chime whistle and
  exhaust beat is a different object emotionally, even if the hydrogen
  version is quieter in reality. Worth deciding deliberately rather than
  defaulting to silent.
- A Brunel line for this, in the house style: "They have given my
  express engine a fuel cell. I withhold judgement until I have seen it
  start a gradient at Talerddig." (placeholder - needs the right
  gradient/location once Cambrian is built out).
