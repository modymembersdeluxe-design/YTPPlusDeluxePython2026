# YTP+ Deluxe Edition (Python)

This repository contains a Tkinter-based scaffold for a YTP (YouTube Poop) effects editor on Windows 7/8.1. It mirrors a subset of the original YTP+ Deluxe configuration model and exposes toggles for audio/video effects, source management, and export planning.

## Highlights

- Source browsers for local video/audio/images/gifs and transitions.
- URL registry for online sources.
- Toggleable audio/video effects with per-effect probability and max level.
- Preview using FFplay (falls back to FFmpeg if available).
- Export a JSON “plan” that captures settings, sources, and effect flags.

## Quick Start

```bash
python Program.py
```

## Project Layout

- `Main.py` — Tkinter GUI.
- `Program.py` — Entry point.
- `ytpplus/EffectsFactory.py` — Effect flag mapping to FFmpeg filters (scaffold).
- `ytpplus/YTPGenerator.py` — FFmpeg orchestration (scaffold).
- `ytpplus/Utilities.py` — Data models, defaults, and assets.
- `App.config` — Sample config values aligned with defaults.
