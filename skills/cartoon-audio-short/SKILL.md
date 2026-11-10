---
name: cartoon-audio-short
description: >-
  Develop ideas and scripts or render voiceover-led vertical cartoons using the bundled Reel Cartoons engine: flat 2D characters in an inked, painted 3D world. Use for narrated cartoon reels in this style or explicit Reel Cartoons requests, rather than generic animation, realistic AI video, or ordinary video edits.
---

# Reel Cartoons

Create original narrated cartoon shorts with the bundled local Three.js engine. The default look is flat bean-head characters with plum outlines in colourful painted 3D environments, with moving cameras, music and SFX. Final output is a portrait 9:16 MP4 for YouTube Shorts and Instagram Reels: 1080x1920 at 30 fps, H.264 video (yuv420p) and AAC audio, within one frame of the supplied narration duration. Compose natively for the vertical frame; keep faces, essential actions and captions away from the edges and platform control areas. Verify these export properties before delivery. No AI video provider is required.

## Choose the starting stage

Reuse supplied materials instead of repeating intake. If the starting point is unclear, ask whether the user has narration, a script, or needs ideas. Default length is 20–30 seconds; respect a requested duration. A request for ideas or a script stays in that text stage.

- **Ideas:** read [story-development.md](references/story-development.md). Default to ten ideas, then develop the selected idea.
- **Script:** use the same reference. Deliver narration, word count, estimated duration, a short visual plan and recording guidance. When voiceover is needed, request the final recording and script text; do not claim a video is ready.
- **Voiceover supplied / actual cartoon requested:** read [production.md](references/production.md) and [animation-engine.md](references/animation-engine.md). Build a new project from `kit/`; treat the installed kit as read-only. Enter at timing when the script and recording are available. Read [delivery.md](references/delivery.md) for captions, cover and the final package.

## Preserve the material

- Keep narration wording and timing unchanged. Picture follows the actual recording; estimated script length is not a reason to stretch the audio. Approximate alignment needs a timing check and must not be described as exact word timestamps.
- Preserve the user's approved story, character, style, and shot decisions. The bundled soldier story is only a technical example, not verified history or a template to copy into every project.
- Make original stories and designs. Do not reproduce another creator's shots. The default format avoids living named people, brand mascots/logos, graphic content and political stories; treat these as this kit's editorial defaults rather than general restrictions on unrelated work.
- Completed video requests include burned-in captions and an SRT by default, using the supplied transcript. Explicit requests such as “no captions” override this. Visible signs or carved text must be legible and correctly oriented.
- For covers, follow [thumbnail-style.md](references/thumbnail-style.md): use the bundled approved Selection Sort cover as the primary visual reference and preserve its layout, typography, palette and teacher across topics. Save each cover beside its video and in the central Covers folder; user-requested styles override this default.
- Use `mix.py`: default music is 25% of narration gated RMS (about -12.04 dB), SFX are at or below that level, and SFX peaks are capped at 35% of narration peak. These are half the previous defaults. User-specified levels override defaults; “no music” disables music, “no background” disables music and SFX. Finishing applies one shared linear gain and reports peak-constrained loudness; no ducking, time stretching or narration compression.

## Execute and deliver honestly

Use checked commands and the project-local Python environment and Node packages. Show and inspect a stills contact sheet before a long render; fix framing, characters, text and action readability first. Monitor renders in the current task and resume complete frames after interruption. Do not schedule an automation to watch a render.

If the actual recording differs from the requested duration by more than one frame, report the mismatch before rendering and follow the supplied recording without stretching it.

Run technical QA, inspect the output and distinguish automated checks from full playback review. Do not claim aesthetic acceptance or a complete watched film from a contact sheet alone. For each completed video, deliver the latest MP4, a matching portrait cover, SRT, and a concise posting caption with relevant hashtags. Save extras alongside the video. Provide clickable local links and exact absolute paths; identify the latest version and disclose any missing deliverable or unperformed review. See [delivery.md](references/delivery.md). “Video only” omits the cover, SRT and posting-caption deliverables, but preserves burned-in captions unless the user also says “no captions.”

Setup may need network access for pinned runtime dependencies; media rendering then runs locally. Do not download optional ASR models, create voices, spend credits, upload recordings, publish, or change accounts merely because this skill was invoked. If a tool or dependency is unavailable, identify the specific gap and continue only work that can be completed honestly.

The bundled vendor licenses and hashes are in `kit/vendor/`; [sources.md](references/sources.md) describes provenance and adaptations. Open Film can inform a specifically requested screenplay or directing task, but is not a runtime dependency of this skill.
