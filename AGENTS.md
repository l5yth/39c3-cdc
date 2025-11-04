# Repository Guidelines

## Project Structure & Module Organization
- `39C3-Design-Package/39C3-Colors` holds theme palettes (`39C3-Variables.json`) consumed by tooling.
- `39C3-Design-Package/39C3-DrawbotScripts` contains DrawBot Python helpers for poster and interpolation workflows; treat configuration blocks at the top of each script as the single source of truth.
- `39C3-Design-Package/39C3-Fonts` provides variable and static font exports under `Desktop/` and `Web/`; keep new faces grouped the same way.
- `39C3-Design-Package/39C3-Logo`, `39C3-Style-Guide`, and `39C3-Visuals` store vector assets and packaged guidelines—update source files first, then regenerate archives such as `39c3-styleguide-full-v1.zip`.
- Repository root keeps lightweight docs (`README.md`, `fonts.cdc.html`); avoid placing large binaries here.

## Build, Test, and Development Commands
- `python3 39C3-Design-Package/39C3-DrawbotScripts/39C3-Script-PosterSetter-FitFormat-V01.py` renders a layout proof; adjust `FONT_PATH` to the local font before running.
- `python3 39C3-Design-Package/39C3-DrawbotScripts/39C3-Script-Interpolation-V01.py` previews weight/width transitions. Run inside DrawBot if UI inspection is required.
- `open 39C3-Design-Package/fonts.index.html` (macOS) or serve with `python3 -m http.server` to browse font specimens in a browser.

## Coding Style & Naming Conventions
- Follow Python 3.10+ idioms: four-space indents, descriptive function names, and inline comments only for non-obvious math or typography rules.
- Preserve the `39C3-*` prefix for directories and assets; new exports should mirror existing casing and spacing for quick discovery.
- Keep configuration constants grouped at the top of scripts and document required units (pt, font units, RGB).

## Testing Guidelines
- No automated tests exist; validate script changes by generating both A3 and A4 outputs and checking console debug output for sane width/height values.
- When updating palettes or fonts, refresh dependent assets (e.g., rerun DrawBot scripts) and compare resulting PDFs/SVGs against prior versions.
- Record manual verification notes in the PR when assets or binaries change.

## Commit & Pull Request Guidelines
- Use concise, present-tense commit messages (e.g., `update upstream style guide`); group unrelated asset updates into separate commits to aid diffing.
- PRs should include: summary of affected assets, before/after previews or paths to generated files, referenced issue or design brief, and any follow-up tasks.
- Large binaries should be linked via release artifacts when possible; if checked in, explain why and mention file sizes to ease reviewer expectations.

## Asset Management Tips
- Preserve original source formats (AI, SVG, DrawBot) alongside exports; never overwrite without keeping the editable master.
- Before merging, ensure fonts and binaries retain executable bit settings where required and that archives open cleanly on macOS and Linux.
