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
        if enabled("random_clip_shuffle"):
            notes.append("Remix shuffle enabled for render v2.")
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
        if enabled("random_cuts"):
            notes.append("Random cuts enabled.")
        if enabled("recall_post_render"):
            notes.append("Recall post-render effect placeholder.")
        if enabled("get_down"):
            notes.append("Get down effect preset enabled.")
        if enabled("temporal_scramble"):
            notes.append("Temporal scramble effect enabled.")
        if enabled("high_harmony"):
            audio_filters.append("asetrate=48000*1.15,atempo=1/1.15")
        if enabled("low_harmony"):
            audio_filters.append("asetrate=48000*0.85,atempo=1/0.85")
        if enabled("fearful"):
            video_filters.append("eq=contrast=1.2:brightness=-0.1")
            audio_filters.append("tremolo=f=6")
        if enabled("half_reversed"):
            notes.append("Half-reversed effect placeholder.")
        if enabled("pitch_shift"):
            notes.append("Pitch shift effect placeholder.")
        if enabled("mirror_symmetry"):
            notes.append("Mirror symmetry effect placeholder.")
        if enabled("hue_rotate"):
            video_filters.append("hue=h=90")
        if enabled("spadinner"):
            overlays.append("spadinner_assets")
        if enabled("confusion"):
            notes.append("Confusion effect placeholder.")
        if enabled("overlay_plus_three"):
            overlays.append("overlay_plus_three")
        if enabled("ytpmv_auto"):
            notes.append("YTPMV automatic effect placeholder.")
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

        return EffectResult(
            audio_filters=audio_filters,
            video_filters=video_filters,
            overlays=overlays,
            notes=notes,
        )
