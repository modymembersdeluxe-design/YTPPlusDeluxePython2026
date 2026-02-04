from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .Utilities import EffectConfig


@dataclass
class EffectResult:
    audio_filters: List[str]
    video_filters: List[str]
    overlays: List[str]
    notes: List[str]


class EffectsFactory:
    """Translate effect toggles into ffmpeg filter chains.

    This is a scaffold. Each method returns filter fragments that can be
    stitched together by the generator.
    """

    def __init__(self, effects: Dict[str, EffectConfig]) -> None:
        self.effects = effects

    def build(self) -> EffectResult:
        audio_filters: List[str] = []
        video_filters: List[str] = []
        overlays: List[str] = []
        notes: List[str] = []

        def enabled(key: str) -> bool:
            return self.effects.get(key, EffectConfig(key)).enabled

        if enabled("random_sound"):
            notes.append("Random sound overlay enabled; will mix from assets.")
        if enabled("reverse"):
            audio_filters.append("areverse")
            video_filters.append("reverse")
        if enabled("speed_up"):
            audio_filters.append("atempo=1.25")
            video_filters.append("setpts=PTS/1.25")
        if enabled("slow_down"):
            audio_filters.append("atempo=0.8")
            video_filters.append("setpts=PTS/0.8")
        if enabled("chorus"):
            audio_filters.append("aecho=0.8:0.9:1000:0.3")
        if enabled("vibrato"):
            audio_filters.append("asetrate=48000*1.02,atempo=1/1.02")
        if enabled("stutter"):
            notes.append("Stutter effect selected; will loop short slices.")
        if enabled("earrape"):
            audio_filters.append("volume=10")
        if enabled("autotune_chaos"):
            notes.append("Auto-tune requires external tool; placeholder only.")
        if enabled("dance"):
            video_filters.append("hue=s=1")
        if enabled("squidward"):
            notes.append("Squidward effect uses ImageMagick overlay assets.")
        if enabled("invert"):
            video_filters.append("negate")
        if enabled("rainbow"):
            overlays.append("rainbow_overlay")
        if enabled("mirror"):
            video_filters.append("hflip")
        if enabled("sus"):
            notes.append("Sus effect uses random pitch/tempo wobble.")
        if enabled("explosion_spam"):
            overlays.append("explosion_overlays")
        if enabled("frame_shuffle"):
            notes.append("Frame shuffle placeholder; sample implementation.")
        if enabled("meme_injection"):
            overlays.append("meme_injection")
        if enabled("sentence_mix"):
            notes.append("Sentence mixing enabled; reorder segments.")
        if enabled("random_clip_shuffle"):
            notes.append("Random clip shuffle enabled.")
        if enabled("random_cuts"):
            notes.append("Random cuts enabled.")

        return EffectResult(
            audio_filters=audio_filters,
            video_filters=video_filters,
            overlays=overlays,
            notes=notes,
        )
