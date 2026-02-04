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
- `resources/spadinner/` — spadinner overlay assets
- `resources/spadinner_sounds/` — spadinner audio stingers

## Default Media Paths

- `resources/intro.mp4` — intro clip (optional)
- `resources/outro.mp4` — outro clip (optional)

## Clip and Sound Controls

- `min_clip_duration` / `max_clip_duration` — range for randomized clip durations.
- `effects_per_clip` — max effect passes per clip.
- `reverse_direction` — force reverse playback direction.
- `sound_frequency` — probability of sound overlay placement.
- `preserve_original_audio` — keep original audio under overlays.
- `cut_audio` — remove original audio entirely.
- `sound_sync_mode` — align sound overlays to cuts for sync humor.
- `temp_number` — suffix index for temp render batches.
- `recall_number` — post-render recall iterations (placeholder).
- `remixes_number` — remix pass count (placeholder).
- `autoytp_number` — automatic YTP pass count (placeholder).
- `ytp_effects_name` — label for the active effect preset.

## Related Config File

The sample configuration values are stored in `App.config` and align with the defaults above.
