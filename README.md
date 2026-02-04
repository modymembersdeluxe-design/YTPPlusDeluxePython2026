# YTP+ Deluxe Edition (Python)

This repository contains a Tkinter-based scaffold for a YTP (YouTube Poop) effects editor on Windows 7/8.1. It acts as an automated video production tool that uses imported media, user-defined effects, and a variety of parameters to randomly pick and transform clips into a single render that mimics the crude video editing styles popularized by the YTP genre.

## Highlights

- Source browsers for local video/audio/images/gifs and transitions.
- URL registry for online sources.
- Toggleable audio/video effects with per-effect probability and max level.
- Controls for clip duration, effects-per-clip, direction, and sound placement frequency.
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
- `YTPPLUS_PATHS.md` — Default tool and directory layout reference.
- `App.config` — Sample config values aligned with defaults.
