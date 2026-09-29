# Third-party notices

This project's own source is licensed GPL-3.0-or-later — see `LICENSE`.
Some components this project uses or plans to use carry their own,
separate licensing/attribution terms, independent of this project's own
license choice. This file exists so those obligations aren't lost; see
`docs/architecture.md` and `decisions/` for the full reasoning behind each.

## Chess piece artwork ("cburnett" set, bundled with `python-chess`'s `chess.svg`)

**Not yet vendored into this repository** — no rendering code exists yet
(tracked in `planning/ROADMAP.md`). This entry is added proactively now,
alongside the GPL relicensing work in `decisions/0010`, so the obligation
below isn't lost once rendering code does land.

The default chess piece SVG set used by `python-chess`'s `chess.svg`
rendering module ("cburnett") was created by Colin M. L. Burnett and is
offered under a choice of licenses: GFDL v1.2+, CC BY-SA 3.0 Unported,
BSD-3-clause, or GPL v2+ (confirmed on the artist's own Wikimedia Commons
file page — see `decisions/0004-board-rendering-approach.md` and
`docs/research/board-rendering-options.md`).

This project exercises the **BSD-3-clause option**:

> Copyright (c) 2006, Colin M.L. Burnett
> All rights reserved.
>
> Redistribution and use of this chess piece artwork, with or without
> modification, is permitted provided that the copyright notice above and
> this attribution are retained.

**This choice is independent of this project's own GPL-3.0-or-later
license.** Relicensing this project's own source to GPL does not remove or
change this attribution obligation — it exists because of the artwork's
own, separate copyright, not because of any relationship to this project's
license. The BSD option remains the simplest available choice (attribution
only, no share-alike) regardless of what license this project's own code
carries.

## Chess rules, notation, and board rendering: `python-chess`

`python-chess` (PyPI: `chess`) is licensed GPL-3.0-or-later, the same as
this project — see `decisions/0010-gpl-relicensing-and-dependency-simplification.md`.
No separate attribution beyond normal dependency disclosure (e.g. in a
`pyproject.toml`/lockfile, once one exists) is required, since this
project's own license is now compatible with using it directly.

## Data: Lichess puzzle, game, and evaluation exports

Sourced under CC0 1.0 (public domain dedication) — see
`decisions/0006-tactical-puzzle-sourcing-and-validation.md`. No attribution
is legally required, but this project credits Lichess (https://lichess.org)
as the source of puzzle and game data, as a matter of provenance and good
practice, not legal obligation.

## Development tool: CodeCompass

CodeCompass (`codecompass-context`) is licensed GPL-3.0-or-later and is
used only as a development-time tool, never a runtime dependency of this
project — see `CLAUDE.md` §8 and `docs/architecture.md`. No attribution
obligation arises from a development-tool-only relationship, but it is
noted here for completeness.
