from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from ytpplus.Utilities import (
    ASSET_FOLDERS,
    DEFAULT_EFFECTS,
    PROJECT_TYPES,
    ProjectSettings,
    RenderJob,
    SourceLibrary,
    ToolPaths,
    ensure_directories,
    load_default_effects,
)
from ytpplus.YTPGenerator import YTPGenerator


class YTPPlusDeluxeApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("YTP+ Deluxe Edition (Python)")
        self.geometry("1200x780")

        self.settings = ProjectSettings()
        self.effects = load_default_effects()
        self.sources = SourceLibrary()
        self.tools = ToolPaths()

        ensure_directories(self.settings)
        self._build_ui()

    def _build_ui(self) -> None:
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True)

        self.sources_frame = ttk.Frame(notebook)
        self.effects_frame = ttk.Frame(notebook)
        self.settings_frame = ttk.Frame(notebook)
        self.render_frame = ttk.Frame(notebook)

        notebook.add(self.sources_frame, text="Sources")
        notebook.add(self.effects_frame, text="Effects")
        notebook.add(self.settings_frame, text="Settings")
        notebook.add(self.render_frame, text="Render")

        self._build_sources_tab()
        self._build_effects_tab()
        self._build_settings_tab()
        self._build_render_tab()

    def _build_sources_tab(self) -> None:
        left = ttk.Frame(self.sources_frame)
        right = ttk.Frame(self.sources_frame)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._add_source_group(left, "Videos", "videos", ("Video Files", "*.mp4 *.wmv *.avi *.mkv"))
        self._add_source_group(left, "Images", "images", ("Image Files", "*.png *.jpg *.jpeg *.webp"))
        self._add_source_group(left, "GIFs", "gifs", ("GIF Files", "*.gif"))
        self._add_source_group(left, "Audio", "audio", ("Audio Files", "*.mp3 *.wav *.ogg"))
        self._add_source_group(left, "Transitions", "transitions", ("Video Files", "*.mp4 *.wmv *.avi *.mkv"))

        url_label = ttk.Label(right, text="Online URLs (YouTube/Facebook/etc.)")
        url_label.pack(anchor="w")
        self.url_list = tk.Listbox(right, height=10)
        self.url_list.pack(fill=tk.BOTH, expand=False)

        url_entry_frame = ttk.Frame(right)
        url_entry_frame.pack(fill=tk.X, pady=5)
        self.url_entry = ttk.Entry(url_entry_frame)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(url_entry_frame, text="Add URL", command=self._add_url).pack(side=tk.LEFT, padx=4)
        ttk.Button(url_entry_frame, text="Remove Selected", command=self._remove_url).pack(side=tk.LEFT)

        assets_label = ttk.Label(right, text="Asset Folders")
        assets_label.pack(anchor="w", pady=(10, 0))
        self.assets_box = tk.Text(right, height=8)
        self.assets_box.pack(fill=tk.BOTH, expand=True)
        self._refresh_assets_box()

    def _add_source_group(self, parent: ttk.Frame, label: str, attr: str, filetypes) -> None:
        group = ttk.Labelframe(parent, text=label)
        group.pack(fill=tk.BOTH, expand=True, pady=5)

        listbox = tk.Listbox(group, height=6)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        setattr(self, f"{attr}_listbox", listbox)

        button_frame = ttk.Frame(group)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)
        ttk.Button(button_frame, text="Add", command=lambda: self._add_files(attr, filetypes)).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="Remove", command=lambda: self._remove_selected(attr)).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="Clear", command=lambda: self._clear_all(attr)).pack(fill=tk.X, pady=2)

    def _add_files(self, attr: str, filetypes) -> None:
        paths = filedialog.askopenfilenames(filetypes=[filetypes])
        if not paths:
            return
        storage = getattr(self.sources, attr)
        listbox = getattr(self, f"{attr}_listbox")
        for path in paths:
            storage.append(Path(path))
            listbox.insert(tk.END, path)

    def _remove_selected(self, attr: str) -> None:
        listbox = getattr(self, f"{attr}_listbox")
        storage = getattr(self.sources, attr)
        selected = listbox.curselection()
        for index in reversed(selected):
            listbox.delete(index)
            storage.pop(index)

    def _clear_all(self, attr: str) -> None:
        listbox = getattr(self, f"{attr}_listbox")
        listbox.delete(0, tk.END)
        storage = getattr(self.sources, attr)
        storage.clear()

    def _add_url(self) -> None:
        url = self.url_entry.get().strip()
        if not url:
            return
        self.sources.urls.append(url)
        self.url_list.insert(tk.END, url)
        self.url_entry.delete(0, tk.END)

    def _remove_url(self) -> None:
        selected = self.url_list.curselection()
        for index in reversed(selected):
            self.url_list.delete(index)
            self.sources.urls.pop(index)

    def _refresh_assets_box(self) -> None:
        self.assets_box.delete("1.0", tk.END)
        for key, value in ASSET_FOLDERS.items():
            self.assets_box.insert(tk.END, f"{key}: {Path(self.settings.resources_dir) / value}\n")

    def _build_effects_tab(self) -> None:
        canvas = tk.Canvas(self.effects_frame)
        scrollbar = ttk.Scrollbar(self.effects_frame, orient=tk.VERTICAL, command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.effect_vars = {}
        self.effect_prob_vars = {}
        self.effect_level_vars = {}

        for key, config in self.effects.items():
            row = ttk.Frame(scroll_frame)
            row.pack(fill=tk.X, pady=2)

            enabled_var = tk.BooleanVar(value=config.enabled)
            prob_var = tk.DoubleVar(value=config.probability)
            level_var = tk.IntVar(value=config.max_level)

            self.effect_vars[key] = enabled_var
            self.effect_prob_vars[key] = prob_var
            self.effect_level_vars[key] = level_var

            ttk.Checkbutton(row, text=config.name, variable=enabled_var).pack(side=tk.LEFT, padx=4)
            ttk.Label(row, text=config.description).pack(side=tk.LEFT, padx=4)
            ttk.Label(row, text="Prob:").pack(side=tk.LEFT, padx=(20, 2))
            ttk.Spinbox(row, from_=0.0, to=1.0, increment=0.05, textvariable=prob_var, width=5).pack(side=tk.LEFT)
            ttk.Label(row, text="Max Level:").pack(side=tk.LEFT, padx=(10, 2))
            ttk.Spinbox(row, from_=1, to=10, increment=1, textvariable=level_var, width=4).pack(side=tk.LEFT)

    def _build_settings_tab(self) -> None:
        frame = self.settings_frame

        setting_fields = [
            ("Clip Count", "clip_count"),
            ("Width", "width"),
            ("Height", "height"),
            ("Min Stream Duration", "min_stream_duration"),
            ("Max Stream Duration", "max_stream_duration"),
            ("Min Clip Duration", "min_clip_duration"),
            ("Max Clip Duration", "max_clip_duration"),
            ("Effects Per Clip", "effects_per_clip"),
            ("Sound Frequency", "sound_frequency"),
            ("Temp Number", "temp_number"),
            ("Recall Number", "recall_number"),
            ("Remixes Number", "remixes_number"),
            ("AutoYTP Number", "autoytp_number"),
        ]
        self.setting_vars = {}
        for label, attr in setting_fields:
            row = ttk.Frame(frame)
            row.pack(fill=tk.X, padx=10, pady=5)
            ttk.Label(row, text=label, width=22).pack(side=tk.LEFT)
            var = tk.DoubleVar(value=getattr(self.settings, attr))
            if attr in {
                "clip_count",
                "width",
                "height",
                "effects_per_clip",
                "temp_number",
                "recall_number",
                "remixes_number",
                "autoytp_number",
            }:
                var = tk.IntVar(value=getattr(self.settings, attr))
            self.setting_vars[attr] = var
            ttk.Entry(row, textvariable=var, width=20).pack(side=tk.LEFT)

        effects_name_row = ttk.Frame(frame)
        effects_name_row.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(effects_name_row, text="YTP Effects Name", width=22).pack(side=tk.LEFT)
        self.ytp_effects_name_var = tk.StringVar(value=self.settings.ytp_effects_name)
        ttk.Entry(effects_name_row, textvariable=self.ytp_effects_name_var, width=30).pack(side=tk.LEFT)

        toggle_frame = ttk.Frame(frame)
        toggle_frame.pack(fill=tk.X, padx=10, pady=5)
        self.insert_transitions_var = tk.BooleanVar(value=self.settings.insert_transitions)
        self.insert_intro_var = tk.BooleanVar(value=self.settings.insert_intro)
        self.insert_outro_var = tk.BooleanVar(value=self.settings.insert_outro)
        self.plugin_test_var = tk.BooleanVar(value=self.settings.plugin_test)
        self.reverse_direction_var = tk.BooleanVar(value=self.settings.reverse_direction)
        self.preserve_audio_var = tk.BooleanVar(value=self.settings.preserve_original_audio)
        self.cut_audio_var = tk.BooleanVar(value=self.settings.cut_audio)
        self.sound_sync_var = tk.BooleanVar(value=self.settings.sound_sync_mode)
        ttk.Checkbutton(toggle_frame, text="Insert Transitions", variable=self.insert_transitions_var).pack(side=tk.LEFT)
        ttk.Checkbutton(toggle_frame, text="Insert Intro", variable=self.insert_intro_var).pack(side=tk.LEFT)
        ttk.Checkbutton(toggle_frame, text="Insert Outro", variable=self.insert_outro_var).pack(side=tk.LEFT)
        ttk.Checkbutton(toggle_frame, text="Plugin Test", variable=self.plugin_test_var).pack(side=tk.LEFT)
        ttk.Checkbutton(toggle_frame, text="Reverse Direction", variable=self.reverse_direction_var).pack(side=tk.LEFT)
        ttk.Checkbutton(toggle_frame, text="Preserve Audio", variable=self.preserve_audio_var).pack(side=tk.LEFT)
        ttk.Checkbutton(toggle_frame, text="Cut Audio", variable=self.cut_audio_var).pack(side=tk.LEFT)
        ttk.Checkbutton(toggle_frame, text="Sound Sync Mode", variable=self.sound_sync_var).pack(side=tk.LEFT)

        intro_row = ttk.Frame(frame)
        intro_row.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(intro_row, text="Intro Path", width=22).pack(side=tk.LEFT)
        self.intro_var = tk.StringVar(value=self.settings.intro_path)
        ttk.Entry(intro_row, textvariable=self.intro_var, width=60).pack(side=tk.LEFT)
        ttk.Button(intro_row, text="Browse", command=self._browse_intro).pack(side=tk.LEFT, padx=4)

        outro_row = ttk.Frame(frame)
        outro_row.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(outro_row, text="Outro Path", width=22).pack(side=tk.LEFT)
        self.outro_var = tk.StringVar(value=self.settings.outro_path)
        ttk.Entry(outro_row, textvariable=self.outro_var, width=60).pack(side=tk.LEFT)
        ttk.Button(outro_row, text="Browse", command=self._browse_outro).pack(side=tk.LEFT, padx=4)

        path_fields = [
            ("Sources Dir", "source_dir"),
            ("Temp Dir", "temp_dir"),
            ("Sounds Dir", "sounds_dir"),
            ("Music Dir", "music_dir"),
            ("Resources Dir", "resources_dir"),
        ]
        self.path_vars = {}
        for label, attr in path_fields:
            row = ttk.Frame(frame)
            row.pack(fill=tk.X, padx=10, pady=5)
            ttk.Label(row, text=label, width=22).pack(side=tk.LEFT)
            var = tk.StringVar(value=getattr(self.settings, attr))
            self.path_vars[attr] = var
            ttk.Entry(row, textvariable=var, width=60).pack(side=tk.LEFT)
            ttk.Button(row, text="Browse", command=lambda a=attr: self._browse_dir(a)).pack(side=tk.LEFT, padx=4)

        tools_row = ttk.LabelFrame(frame, text="Tool Paths")
        tools_row.pack(fill=tk.X, padx=10, pady=10)
        self.tool_vars = {}
        for label, attr in [
            ("FFmpeg", "ffmpeg"),
            ("FFprobe", "ffprobe"),
            ("Magick", "magick"),
            ("FFplay", "ffplay"),
        ]:
            row = ttk.Frame(tools_row)
            row.pack(fill=tk.X, pady=2)
            ttk.Label(row, text=label, width=12).pack(side=tk.LEFT)
            var = tk.StringVar(value=getattr(self.tools, attr))
            self.tool_vars[attr] = var
            ttk.Entry(row, textvariable=var, width=50).pack(side=tk.LEFT)

        project_row = ttk.Frame(frame)
        project_row.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(project_row, text="Project Type", width=22).pack(side=tk.LEFT)
        self.project_type_var = tk.StringVar(value=self.settings.project_type)
        ttk.Combobox(project_row, values=PROJECT_TYPES, textvariable=self.project_type_var, width=20).pack(side=tk.LEFT)

        ttk.Button(frame, text="Reset to Defaults", command=self._reset_defaults).pack(pady=10)

    def _build_render_tab(self) -> None:
        frame = self.render_frame
        overview = (
            "YTP+ Deluxe Edition V2 (Python) is an automated YTP editor scaffold for Windows 7/8.1.\n"
            "Import media, tune effect parameters, and let the generator remix clips into a single render.\n"
            "This is a WIP V2 build with major feature placeholders. Export plans or render via FFmpeg.\n"
            "Preview uses FFplay when available, otherwise FFmpeg."
        )
        ttk.Label(frame, text=overview, justify=tk.LEFT).pack(anchor="w", padx=10, pady=10)

        self.render_log = tk.Text(frame, height=18)
        self.render_log.pack(fill=tk.BOTH, expand=True, padx=10)

        action_frame = ttk.Frame(frame)
        action_frame.pack(fill=tk.X, pady=10)
        ttk.Button(action_frame, text="Preview First Video", command=self._preview_first).pack(side=tk.LEFT, padx=4)
        ttk.Button(action_frame, text="Export Plan JSON", command=self._export_plan).pack(side=tk.LEFT, padx=4)
        ttk.Button(action_frame, text="Render (Stub)", command=self._render_stub).pack(side=tk.LEFT, padx=4)
        ttk.Button(action_frame, text="Create Video", command=self._create_video).pack(side=tk.LEFT, padx=4)

    def _browse_intro(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.wmv *.avi *.mkv")])
        if path:
            self.intro_var.set(path)

    def _browse_outro(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.wmv *.avi *.mkv")])
        if path:
            self.outro_var.set(path)

    def _browse_dir(self, attr: str) -> None:
        path = filedialog.askdirectory()
        if path:
            self.path_vars[attr].set(path)
            if attr == "resources_dir":
                self._refresh_assets_box()

    def _reset_defaults(self) -> None:
        self.settings = ProjectSettings()
        self.effects = load_default_effects()
        self.sources = SourceLibrary()
        self.tools = ToolPaths()

        for attr, var in self.setting_vars.items():
            var.set(getattr(self.settings, attr))
        self.insert_transitions_var.set(self.settings.insert_transitions)
        self.insert_intro_var.set(self.settings.insert_intro)
        self.insert_outro_var.set(self.settings.insert_outro)
        self.plugin_test_var.set(self.settings.plugin_test)
        self.reverse_direction_var.set(self.settings.reverse_direction)
        self.preserve_audio_var.set(self.settings.preserve_original_audio)
        self.cut_audio_var.set(self.settings.cut_audio)
        self.sound_sync_var.set(self.settings.sound_sync_mode)
        self.ytp_effects_name_var.set(self.settings.ytp_effects_name)
        self.intro_var.set(self.settings.intro_path)
        self.outro_var.set(self.settings.outro_path)
        for attr, var in self.path_vars.items():
            var.set(getattr(self.settings, attr))
        for attr, var in self.tool_vars.items():
            var.set(getattr(self.tools, attr))
        self.project_type_var.set(self.settings.project_type)
        self._refresh_assets_box()
        for key, config in DEFAULT_EFFECTS.items():
            self.effect_vars[key].set(config.enabled)
            self.effect_prob_vars[key].set(config.probability)
            self.effect_level_vars[key].set(config.max_level)

        for attr in ["videos", "images", "gifs", "audio", "transitions"]:
            getattr(self, f"{attr}_listbox").delete(0, tk.END)
        self.url_list.delete(0, tk.END)

    def _sync_models(self) -> None:
        for attr, var in self.setting_vars.items():
            setattr(self.settings, attr, var.get())
        self.settings.insert_transitions = self.insert_transitions_var.get()
        self.settings.insert_intro = self.insert_intro_var.get()
        self.settings.insert_outro = self.insert_outro_var.get()
        self.settings.plugin_test = self.plugin_test_var.get()
        self.settings.reverse_direction = self.reverse_direction_var.get()
        self.settings.preserve_original_audio = self.preserve_audio_var.get()
        self.settings.cut_audio = self.cut_audio_var.get()
        self.settings.sound_sync_mode = self.sound_sync_var.get()
        self.settings.ytp_effects_name = self.ytp_effects_name_var.get()
        self.settings.intro_path = self.intro_var.get()
        self.settings.outro_path = self.outro_var.get()
        self.settings.project_type = self.project_type_var.get()

        for attr, var in self.path_vars.items():
            setattr(self.settings, attr, var.get())

        for attr, var in self.tool_vars.items():
            setattr(self.tools, attr, var.get())

        for key, config in self.effects.items():
            config.enabled = self.effect_vars[key].get()
            config.probability = float(self.effect_prob_vars[key].get())
            config.max_level = int(self.effect_level_vars[key].get())

    def _build_job(self) -> RenderJob:
        self._sync_models()
        ensure_directories(self.settings)
        return RenderJob(
            output_path=Path(self.settings.temp_dir) / "tempoutput.mp4",
            sources=self.sources,
            settings=self.settings,
            effects=self.effects,
            tool_paths=self.tools,
            notes="Generated via Tkinter GUI",
        )

    def _preview_first(self) -> None:
        if not self.sources.videos:
            messagebox.showwarning("Preview", "Add at least one video source to preview.")
            return
        job = self._build_job()
        generator = YTPGenerator(job)
        try:
            generator.preview(self.sources.videos[0])
            self._log("Preview launched for first video source.")
        except Exception as exc:
            messagebox.showerror("Preview Error", str(exc))
            self._log(f"Preview failed: {exc}")

    def _export_plan(self) -> None:
        job = self._build_job()
        generator = YTPGenerator(job)
        output_path = Path(self.settings.temp_dir) / "ytp_plan.json"
        generator.export_plan(output_path)
        self._log(f"Plan exported to {output_path}")

    def _render_stub(self) -> None:
        job = self._build_job()
        generator = YTPGenerator(job)
        if not self.sources.videos:
            messagebox.showwarning("Render", "Add at least one video source to render.")
            return
        if len(self.sources.videos) > 1:
            result = generator.render_concat(self.sources.videos, job.output_path)
        else:
            result = generator.render(self.sources.videos[0], job.output_path)
        self._log(f"FFmpeg exit code: {result.returncode}")
        if result.stdout:
            self._log(result.stdout)
        if result.stderr:
            self._log(result.stderr)

    def _create_video(self) -> None:
        job = self._build_job()
        generator = YTPGenerator(job)
        if not self.sources.videos:
            messagebox.showwarning("Create Video", "Add at least one video source to render.")
            return
        output_path = Path(self.settings.temp_dir) / "ytp_output.mp4"
        if len(self.sources.videos) > 1:
            result = generator.render_concat(self.sources.videos, output_path)
        else:
            result = generator.render(self.sources.videos[0], output_path)
        self._log(f"Create video exit code: {result.returncode}")
        self._log(f"Output: {output_path}")
        if result.stdout:
            self._log(result.stdout)
        if result.stderr:
            self._log(result.stderr)

    def _log(self, message: str) -> None:
        self.render_log.insert(tk.END, f"{message}\n")
        self.render_log.see(tk.END)


if __name__ == "__main__":
    app = YTPPlusDeluxeApp()
    app.mainloop()
