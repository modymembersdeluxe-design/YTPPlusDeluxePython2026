# YTP+ Deluxe Edition V2 (Python) Beta 1

This repository contains a Tkinter-based scaffold for a YTP (YouTube Poop) effects editor on Windows 7/8.1. It acts as a WIP automated video production tool (V2 Beta 1) that uses imported media, user-defined effects, and a variety of parameters to randomly pick and transform clips into a single render that mimics the crude video editing styles popularized by the YTP genre.

## Highlights

- Source browsers for local video/audio/images/gifs, transitions, and spadinner audio/video.
- URL registry for online sources.
- Toggleable audio/video effects with per-effect probability and max level.
- Controls for clip count, min/max stream duration, clip duration, effect layers, direction, and sound placement frequency.
- Create Video action renders `ytp_output.mp4` via FFmpeg concat from the selected sources.
- Insert transitions and spadinner clips can be toggled from the Settings tab.
- V2 work-in-progress scaffolding with major feature placeholders for future expansion.
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
