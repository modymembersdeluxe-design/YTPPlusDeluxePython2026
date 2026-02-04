# YTP+ Deluxe Paths and Directory Layout

This document summarizes the default folder layout and path-oriented settings used by the Python/Tkinter scaffold.

## Default Tool Paths

- `ffmpeg` (FFmpeg binary)
- `ffprobe` (FFprobe binary)
- `magick` (ImageMagick binary)
- `ffplay` (FFplay binary for preview)

## Default Project Directories

- `sources/` — primary source video clips
- `temp/` — temporary render workspace
- `sounds/` — audio effect clips
- `music/` — music beds or longer audio tracks
- `resources/` — shared assets and nested folders listed below

## Default Resource Subfolders

These folders live under `resources/` and are auto-created by the app:

- `resources/images/` — image montage/injection sources
- `resources/memes/` — meme images for overlays
- `resources/meme_sounds/` — meme audio stingers
- `resources/sounds/` — supplemental sound effects
- `resources/overlay_videos/` — overlay video clips
- `resources/adverts/` — advert overlay clips
- `resources/errors/` — glitch/error overlays

## Default Media Paths

- `resources/intro.mp4` — intro clip (optional)
- `resources/outro.mp4` — outro clip (optional)

## Related Config File

The sample configuration values are stored in `App.config` and align with the defaults above.
