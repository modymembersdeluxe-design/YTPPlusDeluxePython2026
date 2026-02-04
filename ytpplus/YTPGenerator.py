from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Iterable, List

from .EffectsFactory import EffectsFactory
from .Utilities import RenderJob


class YTPGenerator:
    """FFmpeg-based generator scaffold for YTP+ Deluxe."""

    def __init__(self, job: RenderJob) -> None:
        self.job = job
        self.effects_factory = EffectsFactory(job.effects)

    def _write_concat_file(self, file_list: Iterable[Path], output_file: Path) -> None:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        lines = [f"file '{path.as_posix()}'" for path in file_list]
        output_file.write_text("\n".join(lines), encoding="utf-8")

    def _build_filters(self) -> str:
        effects = self.effects_factory.build()
        filters: List[str] = []
        if effects.video_filters:
            filters.append(",".join(effects.video_filters))
        if effects.audio_filters:
            filters.append(",".join(effects.audio_filters))
        return ";".join(filters)

    def _ffmpeg_cmd(self, input_path: Path, output_path: Path) -> List[str]:
        filters = self._build_filters()
        cmd = [self.job.tool_paths.ffmpeg, "-y", "-i", str(input_path)]
        if filters:
            cmd += ["-filter_complex", filters]
        cmd += [str(output_path)]
        return cmd

    def _concat_cmd(self, concat_file: Path, output_path: Path) -> List[str]:
        filters = self._build_filters()
        cmd = [
            self.job.tool_paths.ffmpeg,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
        ]
        if filters:
            cmd += ["-filter_complex", filters]
        cmd += [str(output_path)]
        return cmd

    def preview(self, input_path: Path) -> None:
        ffplay = shutil.which(self.job.tool_paths.ffplay) or shutil.which("ffplay")
        ffmpeg = shutil.which(self.job.tool_paths.ffmpeg) or shutil.which("ffmpeg")
        if ffplay:
            subprocess.Popen([ffplay, str(input_path)])
        elif ffmpeg:
            subprocess.Popen([ffmpeg, "-i", str(input_path)])
        else:
            raise RuntimeError("FFplay/FFmpeg not found for preview.")

    def generate_plan(self) -> dict:
        """Return a JSON-serializable plan used by the UI for review."""
        effects = self.effects_factory.build()
        plan = {
            "sources": {
                "videos": [str(p) for p in self.job.sources.videos],
                "images": [str(p) for p in self.job.sources.images],
                "gifs": [str(p) for p in self.job.sources.gifs],
                "audio": [str(p) for p in self.job.sources.audio],
                "transitions": [str(p) for p in self.job.sources.transitions],
                "urls": list(self.job.sources.urls),
            },
            "settings": self.job.settings.__dict__,
            "effects": {name: config.__dict__ for name, config in self.job.effects.items()},
            "filters": {
                "audio": effects.audio_filters,
                "video": effects.video_filters,
                "overlays": effects.overlays,
                "notes": effects.notes,
            },
            "spadinner": {
                "audio": [str(p) for p in self.job.sources.spadinner_audio],
                "videos": [str(p) for p in self.job.sources.spadinner_videos],
            },
        }
        return plan

    def export_plan(self, output_path: Path) -> None:
        plan = self.generate_plan()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(plan, indent=2), encoding="utf-8")

    def render(self, input_path: Path, output_path: Path) -> subprocess.CompletedProcess:
        cmd = self._ffmpeg_cmd(input_path, output_path)
        return subprocess.run(cmd, check=False, capture_output=True, text=True)

    def render_concat(self, inputs: Iterable[Path], output_path: Path) -> subprocess.CompletedProcess:
        concat_file = Path(self.job.settings.temp_dir) / "concat.txt"
        self._write_concat_file(inputs, concat_file)
        cmd = self._concat_cmd(concat_file, output_path)
        return subprocess.run(cmd, check=False, capture_output=True, text=True)

    def render_preview(self, input_path: Path, seconds: int = 15) -> subprocess.CompletedProcess:
        output_path = Path(self.job.settings.temp_dir) / "preview.mp4"
        cmd = [
            self.job.tool_paths.ffmpeg,
            "-y",
            "-t",
            str(seconds),
            "-i",
            str(input_path),
            str(output_path),
        ]
        return subprocess.run(cmd, check=False, capture_output=True, text=True)

    def render_v2(self, inputs: Iterable[Path], output_path: Path) -> subprocess.CompletedProcess:
        inputs_list = list(inputs)
        if len(inputs_list) > 1:
            return self.render_concat(inputs_list, output_path)
        if not inputs_list:
            raise ValueError("No inputs provided for render_v2.")
        return self.render(inputs_list[0], output_path)
