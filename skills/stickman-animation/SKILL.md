---
name: stickman-animation
description: Create programmatic 2D stickman story or explainer animations, including scene manifests, rendering pipelines, voiceover, and synchronized captions. Use for stickman videos built with Canvas, Remotion, or Python, not generic animation or ordinary video editing.
---

# Stickman animation

Build the deliverable the user requests: a story, scene manifest, rendering pipeline, or finished video. Adapt the genre, format, duration, visual style, and technology to the request. For the detailed visual and pipeline specification, read [references/source-brief.md](references/source-brief.md).

Keep story data in a scene manifest separate from a reusable renderer. Describe scene timing, camera, environment, actors, poses, narration, and sound cues in the manifest; make the renderer interpret those values rather than hardcoding a particular story. Use deterministic vector primitives, reusable character rigs, and seeded procedural effects for consistent output. Support appropriate camera, backgrounds, character expressions and movement, HUDs, chapter cards, and atmospheric effects as needed by the story.

For narrated video, use actual speech alignment timestamps to synchronize word-by-word captions and relevant actions. ElevenLabs timestamped TTS and sound generation are options when requested or available; local audio and other providers are acceptable when suited to the user's constraints. Do not invent timestamps or claim generated audio or video exists when it does not. Handle credentials via environment variables, never embed secrets, and avoid paid API calls without authorization. Use local assets or explain any remaining dependency when necessary.

For a complete video pipeline, make frame rate, dimensions, and output configurable (default 1920x1080 and 30 fps unless the user specifies otherwise); render and mix audio with ffmpeg to an H.264/AAC MP4 when feasible. Verify the manifest and code, and inspect or play representative output when the environment permits. Report any missing dependencies or unrendered components clearly.
