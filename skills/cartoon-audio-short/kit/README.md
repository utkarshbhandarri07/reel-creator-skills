# cartoon-short-kit
Audio in, finished vertical cartoon short out. 2D bean-head cards in an inked, painted 3D world
(three.js in headless Chromium, no Remotion and no GPU needed), with a synthesized music bed and SFX.

- `engine/` renderer: world helpers, cards, ink pass, lens blur, grade (`main.js`), painted textures (`paint.js`),
  cast drawing (`roman.js` on top of the bundled Pen library from mromidev/claude-animated-shorts),
  motion helpers (`motion.js`).
- `example/soldier/` the worked example "The Soldier Who Never Left" (story.js shot plan + audio.py cue table).
- `tools/` setup.py (isolated project), timing.py (approximate timing), render.mjs (frames), sheet.py (contact sheets), mix.py (constant audio levels), finish.py (encode + QA).

Adapted quick start: `python tools/setup.py <new-project-folder>`, then use the project-local Python environment for `timing.py voice.wav script.txt --out work`. See the skill's production reference for complete checked commands.
Built on github.com/mromidev/claude-animated-shorts (MIT): toon.ts, look values and readability rules.
