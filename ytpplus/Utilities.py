from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class EffectConfig:
    name: str
    enabled: bool = True
    probability: float = 0.5
    max_level: int = 1
    description: str = ""


@dataclass
class SourceLibrary:
    videos: List[Path] = field(default_factory=list)
    images: List[Path] = field(default_factory=list)
    gifs: List[Path] = field(default_factory=list)
    audio: List[Path] = field(default_factory=list)
    transitions: List[Path] = field(default_factory=list)
    urls: List[str] = field(default_factory=list)


@dataclass
class ToolPaths:
    ffmpeg: str = "ffmpeg"
    ffprobe: str = "ffprobe"
    magick: str = "magick"
    ffplay: str = "ffplay"


@dataclass
class ProjectSettings:
    clip_count: int = 20
    width: int = 640
    height: int = 480
    min_stream_duration: float = 0.2
    max_stream_duration: float = 0.4
    min_clip_duration: float = 0.5
    max_clip_duration: float = 2.5
    effects_per_clip: int = 1
    reverse_direction: bool = False
    sound_frequency: float = 0.5
    preserve_original_audio: bool = True
    cut_audio: bool = False
    sound_sync_mode: bool = False
    temp_number: int = 1
    recall_number: int = 0
    remixes_number: int = 0
    autoytp_number: int = 0
    ytp_effects_name: str = "default"
    insert_transitions: bool = True
    insert_intro: bool = False
    insert_outro: bool = False
    plugin_test: bool = False
    intro_path: str = "resources/intro.mp4"
    outro_path: str = "resources/outro.mp4"
    source_dir: str = "sources"
    temp_dir: str = "temp"
    sounds_dir: str = "sounds"
    music_dir: str = "music"
    resources_dir: str = "resources"
    theme: str = "Dark"
    project_type: str = "Generic"


DEFAULT_EFFECTS: Dict[str, EffectConfig] = {
    "random_sound": EffectConfig(
        name="Random Sound",
        description="Overlay short sound effects on clips.",
    ),
    "reverse": EffectConfig(
        name="Reverse Clip",
        description="Reverse audio and video stream for a clip.",
    ),
    "speed_up": EffectConfig(
        name="Speed Up",
        description="Increase playback speed for a clip.",
    ),
    "slow_down": EffectConfig(
        name="Slow Down",
        description="Decrease playback speed for a clip.",
    ),
    "chorus": EffectConfig(
        name="Chorus Effect",
        description="Approximate chorus via aecho filter.",
    ),
    "vibrato": EffectConfig(
        name="Vibrato/Pitch Bend",
        description="Approximate vibrato using asetrate + atempo.",
    ),
    "stutter": EffectConfig(
        name="Stutter Loop",
        description="Repeat a short slice of the clip.",
    ),
    "recall_post_render": EffectConfig(
        name="Recall Post Render",
        description="Placeholder for post-render recall processing.",
    ),
    "get_down": EffectConfig(
        name="Get Down Effect",
        description="Rhythmic speed/tempo preset.",
    ),
    "temporal_scramble": EffectConfig(
        name="Temporal Scramble",
        description="Scramble clip timing for chaotic edits.",
    ),
    "high_harmony": EffectConfig(
        name="High Harmony",
        description="Pitch-shift audio to a higher harmony.",
    ),
    "low_harmony": EffectConfig(
        name="Low Harmony",
        description="Pitch-shift audio to a lower harmony.",
    ),
    "fearful": EffectConfig(
        name="Fearful Effect",
        description="Apply darkened tone and audio warble.",
    ),
    "half_reversed": EffectConfig(
        name="Half Reversed",
        description="Reverse mid-section of a clip.",
    ),
    "pitch_shift": EffectConfig(
        name="Pitch Shift",
        description="Shift audio pitch without tempo change.",
    ),
    "mirror_symmetry": EffectConfig(
        name="Mirror Symmetry",
        description="Mirror video with a center seam.",
    ),
    "hue_rotate": EffectConfig(
        name="Hue Rotate",
        description="Rotate hue for psychedelic colors.",
    ),
    "spadinner": EffectConfig(
        name="Spadinner Effect",
        description="Overlay spadinner assets and audio.",
    ),
    "confusion": EffectConfig(
        name="Confusion Effect",
        description="Layer audio/video jitter for confusion.",
    ),
    "overlay_plus_three": EffectConfig(
        name="Overlay +3",
        description="Stack three overlay layers.",
    ),
    "ytpmv_auto": EffectConfig(
        name="YTPMV Automatic",
        description="Auto rhythm mapping for YTPMV edits.",
    ),
    "earrape": EffectConfig(
        name="Earrape Mode",
        description="Apply large gain on audio.",
    ),
    "autotune_chaos": EffectConfig(
        name="Auto-Tune Chaos",
        enabled=False,
        description="Placeholder for external autotune tool.",
    ),
    "dance": EffectConfig(
        name="Dance Mode",
        description="Simple video transform preset.",
    ),
    "squidward": EffectConfig(
        name="Squidward Mode",
        description="Video transform using ImageMagick overlay.",
    ),
    "invert": EffectConfig(
        name="Invert Colors",
        description="Invert video colors.",
    ),
    "rainbow": EffectConfig(
        name="Rainbow Overlay",
        description="Overlay a rainbow PNG/GIF on the video.",
    ),
    "mirror": EffectConfig(
        name="Mirror Mode",
        description="Mirror the video horizontally.",
    ),
    "sus": EffectConfig(
        name="Sus Effect",
        description="Random pitch/tempo wobble.",
    ),
    "explosion_spam": EffectConfig(
        name="Explosion Spam",
        description="Repeatedly overlay explosion clips.",
    ),
    "frame_shuffle": EffectConfig(
        name="Frame Shuffle",
        enabled=False,
        description="Placeholder; sample shuffle implementation.",
    ),
    "meme_injection": EffectConfig(
        name="Meme Injection",
        description="Overlay meme images/audio from assets.",
    ),
    "sentence_mix": EffectConfig(
        name="Sentence Mixing",
        description="Reorder short segments for comedic timing.",
    ),
    "random_clip_shuffle": EffectConfig(
        name="Random Clip Shuffle",
        description="Shuffle chosen source clips.",
    ),
    "random_cuts": EffectConfig(
        name="Random Cuts",
        description="Add quick hard cuts between segments.",
    ),
}


ASSET_FOLDERS = {
    "images": "images",
    "memes": "memes",
    "meme_sounds": "meme_sounds",
    "sounds": "sounds",
    "overlay_videos": "overlay_videos",
    "adverts": "adverts",
    "errors": "errors",
    "spadinner": "spadinner",
    "spadinner_sounds": "spadinner_sounds",
}


PROJECT_TYPES = [
    "Generic",
    "YTP Tennis",
    "Collab Entry",
    "YTPMV",
]


def ensure_directories(settings: ProjectSettings) -> None:
    base = Path(settings.resources_dir)
    base.mkdir(parents=True, exist_ok=True)
    Path(settings.temp_dir).mkdir(parents=True, exist_ok=True)
    Path(settings.sounds_dir).mkdir(parents=True, exist_ok=True)
    Path(settings.music_dir).mkdir(parents=True, exist_ok=True)
    Path(settings.source_dir).mkdir(parents=True, exist_ok=True)
    for folder in ASSET_FOLDERS.values():
        (base / folder).mkdir(parents=True, exist_ok=True)


def load_default_settings() -> ProjectSettings:
    return ProjectSettings()


def load_default_effects() -> Dict[str, EffectConfig]:
    return {key: EffectConfig(**vars(value)) for key, value in DEFAULT_EFFECTS.items()}


@dataclass
class RenderJob:
    output_path: Path
    sources: SourceLibrary
    settings: ProjectSettings
    effects: Dict[str, EffectConfig]
    tool_paths: ToolPaths
    notes: Optional[str] = None
