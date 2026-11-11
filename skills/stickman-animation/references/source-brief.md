Generate complete programmatic 2D stickman animation videos, scripts, and JSON scene manifests across any story genre or topic (thriller, sci-fi, comedy, educational, historical, mystery, adventure, or survival). Use when the user asks to create a stickman animation, build a programmatic 2D story video via Codex or Claude, or generate HTML5 Canvas, Remotion, or Python video pipelines with ElevenLabs TTS and word-by-word captions.
Generate complete, production-ready code, scripts, and structured scene manifests for programmatic 2D stickman animations across any genre, featuring modular puppet rigs, parametric camera views, dynamic UI/HUD overlays, and word-synchronized subtitles.
- The user wants to create a 2D stickman animated story or explainer video in any genre (sci-fi, comedy, thriller, educational, adventure, drama, or survival).
- The user asks for a programmatic animation pipeline for OpenAI Codex, Claude Code, Remotion, HTML5 Canvas, or Python (pycairo + ffmpeg).
- The user wants to turn a story prompt or concept into a structured scene manifest with ElevenLabs voiceover, sound effects, and automated 2D rendering.
Adapt the tone, visual palette, and UI overlays to match the user's chosen genre while keeping the deterministic data-driven structure:
- Theme Config (theme_config):
  - genre: "thriller" | "scifi" | "comedy" | "educational" | "historical" | "custom"
  - palette: Define primary background tones, accent colors, and stroke width (default 4px #111111 with rounded caps).
  - hud_style: "telemetry_badge" (day/time/status tracker), "minimal_chapter" (clean title banner), "news_ticker", or "none".
  - lighting_mode: "flat_vibrant" (bright comedy/explainer), "cinematic_vignette" (drama/mystery), "flashlight_cone" (thriller/dark), or "neon_glow" (sci-fi).
- Scene Array (scenes): Break the script into sequential beats where each scene defines:
  - scene_id and optional chapter_card (title, subtitle, transition_style such as "label_maker", "typewriter", or "clean_slide")
  - hud_state: Dynamic key-value pairs for the corner overlay (e.g., primary_label, secondary_label, status_text, indicator_color)
  - camera: preset ("closeup_insert", "wide_stage", "one_point_corridor", "top_down_crowd", "isometric_diagram", "split_screen") and motion ("static", "slow_zoom_in", "slow_zoom_out", "pan_horizontal", "camera_shake")
  - environment: Background template, props list (id, x, y, scale, label), and particles ("none", "rain", "snow", "dust_motes", "sparks", "confetti")
  - actors: List of stickman characters with id, x, y, scale, pose ("idle", "walk", "run", "point", "sit", "action_loop"), expression ("neutral", "happy", "shock", "angry", "sad", "focused"), and costume (hat, hair, shirt color, held prop, lanyard/accessory)
  - voiceover: speaker, voice_id, and text
  - sfx_cues: Timed sound effect triggers and visual ring/ripple emitters (x, y, color)
Generate a self-contained rendering engine (HTML5 Canvas for browser preview/capture, Remotion, or Python pycairo + ffmpeg for CLI rendering) with these parametric building blocks:
- Universal Stickman Puppet Rig: 
  - Head: Circle (radius: 28px) with customizable skin/fill tone (#F0EAE1 default) and 4px #111111 outline.
  - Facial Expressions: Swap eye and mouth primitives dynamically based on expression (dot eyes for neutral/happy, wide white circles with pinpoint pupils for shock/fear, angled brows for anger, curved arcs for smiles/frowns).
  - Torso & Wardrobe: Rounded rectangle torso with modular layered accessories (caps, glasses, ties, aprons, backpacks, helmets, or held props) so every character has an unmistakable silhouette.
  - Procedural Limb Kinematics: Use 2-segment line limbs (5px stroke) driven by sine-wave walk/run cycles (Math.sin(t * speed) * amplitude) and target-point inverse kinematics for reaching, pointing, typing, or knocking.
- Parametric Environment & Camera Presets: 
  - One-Point Perspective Corridor/Hallway/Aisle: Converging vanishing-point geometry with modular side walls/shelves and customizable hanging signs.
  - Wide 2D Stage: Layered parallax background, midground props, and foreground silhouettes.
  - Top-Down Tactical / Crowd Map: Bird's-eye layout for showing movement trajectories, group formations, or architectural blueprints with animated path dots.
  - Cutaway Infographic Card: Clean dark or blueprint slate with 3D/isometric vector diagrams and bold accent callout text for explaining facts, rules, or mechanics.
- Atmospheric & Particle Layers: 
  - Support toggleable post-processing passes: radial vignettes, directional spotlight cones, screen shake on impact, expanding visual sound-wave rings, and procedural particle emitters.
- Configurable Corner HUD: Render the selected hud_style in the top-left corner to ground the viewer in time, location, or story state.
- Transition Cards: Between major narrative acts, render stylized full-screen chapter cards synced to a crisp transition sound effect.
- Word-by-Word Center-Bottom Subtitles: Display the active spoken word at (width / 2, height * 0.86) in bold uppercase sans-serif (54px, thick black stroke + drop shadow). Automatically highlight numbers, proper nouns, or emphasis tokens in the theme's accent color (#F5C542 default).
Provide a clean automation script (Python or Node.js) that:
1. Calls the ElevenLabs /v1/text-to-speech/{voice_id}/with-timestamps endpoint for each voiceover line to obtain both the audio file and character/word alignment timestamps.
2. Calls the ElevenLabs Sound Effects API (/v1/sound-generation) or loads local SFX assets for every entry in sfx_cues.
3. Steps the 2D renderer frame-by-frame at 30 or 60 FPS, using the exact timestamp array to drive character actions, camera shakes, and single-word captions.
4. Pipes the rendered frames and mixed audio tracks into ffmpeg (-c:v libx264 -pix_fmt yuv420p -c:a aac) to produce the final 1920x1080 MP4.
- Keep Visuals Deterministic: Use clean vector primitives and reusable parametric rigs rather than generative raster images so characters and rooms stay 100% consistent across ratusan of shots.
- Use Word Alignment Data for Captions: Always drive the single-word pop-up subtitles from actual TTS word timestamps rather than linear character-count interpolation so pauses and punchlines land naturally.
- Separate Story Data from Render Code: Keep the rendering engine completely generic so producing a new episode or switching genres only requires swapping out story_manifest.json.