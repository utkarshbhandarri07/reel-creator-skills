# Local production

## Setup

Resolve `<skill>` from this SKILL.md's location. Use an explicit new project path outside the skill, normally under the user's workspace. Never run a project from inside the installed kit.

```powershell
python "<skill>/kit/tools/setup.py" "<workspace>/shorts/my-short"
```

Requires native Python 3.12+, Node with `module.stripTypeScriptTypes` (Node 24 recommended), npm, FFmpeg and FFprobe. Verify `python` is native Windows Python, rather than an MSYS executable found incidentally on PATH. If necessary use `C:/Users/utkarsh/AppData/Local/Programs/Python/Python312/python.exe`, which was verified during installation. Setup vendors the engine, validates bundled libraries, creates a project `.venv`, installs pinned dependencies locally, and asks Playwright to install its matching Chromium (an existing matching installation is reused). Downloads need normal network permissions. No global npm or pip installs are necessary. `--skip-deps` creates files for inspection only. Existing destinations are refused, including partial setups; repair a partial dependency installation explicitly or choose another project name without deleting user work.

From the new project's working directory, use `.venv/Scripts/python.exe` on Windows (`.venv/bin/python` on POSIX), abbreviated below as `<python>`.

## Vertical delivery

Use portrait 9:16, 1080x1920, 30 fps throughout planning, previews and final rendering for YouTube Shorts and Instagram Reels. Export MP4 with limited-range H.264/yuv420p video and AAC audio; the finishing helper already enforces the dimensions, frame rate and codecs. Compose for portrait instead of cropping a landscape composition afterward. Keep faces, essential action, labels and captions comfortably inset; avoid the right-side control rail and top/bottom interface areas. Inspect this in the contact sheet, and verify the encoded file before delivery. These are composition precautions, not fixed platform safe-area measurements.

## Timing and shots

```text
<python> timing.py voice.wav script.txt --out work
```

The default aligns the final script to detected speech segments. The returned `words.json` and `phrases.json` are approximate and need inspection against the audio. Silence is not speech evidence. A local optional faster-whisper model can be supplied with `--asr-model <existing-folder>`; install the optional ASR package only when requested, and do not download a model automatically. Missing text, silence, empty audio and failed alignment stop with an explicit error.

Use `frames30 = round(actual_narration_seconds * 30)`. Write `work/PLAN.md` before editing animation: frame ranges, spoken text, setting/light, camera, actors/actions and SFX. Place the hook at frame zero; usually allocate a shot per meaningful phrase and merge tiny fragments. Aim reactions zero to three frames before their related word, but do not claim that precision from approximate alignment. Update `web/story.js` TOTAL, shot boundaries, camera and action functions, plus `audio.py` duration and cue table, for the actual story.

## Captions

For completed video requests, run `captions.py work/words.json --duration <actual-seconds> --srt out/Title.srt` before rendering. This creates `web/captions.json`; the renderer burns its cues into previews and full frames automatically. Use the supplied transcript, inspect timing, and label the default script alignment approximate. It is not exact word timing. For “no captions,” skip this step and set `$env:CAPTIONS="none"` for the render. Clear that environment variable for a later captioned render. Never add a second caption overlay to a scene that already draws captions. See delivery.md for layout and overrides.

## Stills, render and audio

```text
node render.mjs stills/check "5,40,120"
<python> sheet.py stills/check stills/contact.jpg
```

Choose valid representative frames for the actual duration, including transitions and key actions. Inspect and show the sheet before the full render. Render original character tests for new cast designs. Confirm the vertical frame does not hide actions or faces, the camera does not pass through geometry, and visible lettering reads normally.

```text
node render.mjs frames "0-<N-1>"
<python> audio.py
<python> mix.py voice.wav music.wav sfx.wav
<python> finish.py out/Title.mp4 --voice voice.wav
```

Set `RESUME=1` to reuse completed frames; never resume stale frames after changing their scene or timing. The renderer is local-only and exits on page errors; monitor its frame log through normal execution sessions, reporting meaningful progress. If interrupted, check frame files and the source revision before resuming.

The supplied `audio.py` is a 592-frame technical example. Rewrite its duration and story-specific cue table before production; do not merely truncate its sounds for a new story. It generates stems only, without reading the narration. `mix.py` decodes narration once to mono 48 kHz without changing timing, aligns stem lengths, and records constant gains and measured ratios in `mix_raw.wav.json`. Channel conversion/resampling and AAC encoding are not bit-identical preservation; narration content and timing are retained. Default mix levels are music/SFX 0.25 of narration gated RMS and SFX peaks at most 0.35 of narration peak. Override with `--music-level`, `--sfx-level`, and `--sfx-peak-ratio`; zero mutes that stem. `--no-music` / `--no-sfx` skip reading the respective stem (the positional filenames remain required and may be placeholders). For narration only use both switches. Do not normalize muted stems back up.

Final finishing uses one common linear gain toward -14 LUFS with headroom for peaks; it can finish quieter rather than compress narration. Its report discloses this and any QA concerns.

`finish.py` requires contiguous frames, refuses an existing output, verifies H.264/AAC, dimensions/frame rate and duration within a frame, scans freezes/black spans, measures loudness, and produces `.qa.jpg` and `.qa.json`. Review flagged spans (a deliberate transition may be valid). Inspect the contact sheet and review full playback with an available media capability before saying it was watched. Otherwise explicitly report that playback review remains unperformed.

## Later background-volume changes

Use `remix.py out/Title.mp4 out/Title-v2.mp4 --voice voice.wav --mix-report mix_raw.wav.json`. Default multipliers are 0.5 for both existing background stems; set `--music-multiplier` / `--sfx-multiplier` to change either. The helper reuses the previous QA common gain, copies the encoded video, and creates a new version. For another revision, use the latest video and its `.mix.json` as the mix report. Never run ordinary finish normalization again for an audio-only adjustment: that would change the retained narration level. Existing outputs are refused; excessive levels fail rather than silently lowering narration.

Finishing converts full-range rendered JPEGs to limited-range yuv420p and verifies the encoded range. Its review sheet samples evenly across the full video, including the first and last frame. Read [delivery.md](delivery.md) to complete the cover, posting caption and final paths.
