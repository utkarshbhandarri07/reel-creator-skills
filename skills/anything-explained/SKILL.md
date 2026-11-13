---
name: anything-explained
description: Create vertical explainer animations in a dark UI style with glassmorphic cards, status pills, kinetic typography, and spring transitions. Use for tech reels, system design explainers, or other topics explicitly requested in this visual style.
---

# Anything Explained

Turn a topic, script, or timestamped narration into a 9:16 explainer using the dark UI visual language below. This skill is an animation design and production workflow; it does not bundle a rendering engine or TTS service.

## Production workflow

- Use the supplied topic, language, script, narration, and branding. If narration exists, derive scene timing from it. Otherwise draft a concise script and scene timings appropriate to the requested duration.
- Prefer the project's existing animation stack. For a new code-driven project, use Remotion (React) or HTML/CSS with GSAP and an available capture/export pipeline. Choose one implementation rather than generating parallel versions.
- Map the explanation into a hook, visual demonstration or comparison, and takeaway. Build scenes around the meaning of the script; use only the primitives that help communicate it. Do not force interview dialogue, a rejection stamp, or a day grid into unrelated topics.
- Use the user's creator handle and series title in a persistent monospace HUD when supplied. Do not copy the reference video's creator identity or invent a series/day number.
- Drive animation from deterministic frame or timeline positions. In Remotion, use frame-based springs and interpolation; in HTML/GSAP, use a controllable timeline for repeatable capture. Wait for fonts and assets before capturing frames.
- Preview representative frames and transitions at phone size. Check text fit, contrast, subtitle clearance, audio sync, and the final exported video's dimensions, duration, frame rate, and playback. If rendering tools are unavailable, deliver the source/storyboard and identify what remains unrendered.

## Canvas and global layout

- **Resolution:** 1080×1920 (9:16 vertical video), 60 FPS by default; preserve a requested or existing project frame rate.
- **Safe zones:** Top HUD at `top: 60px`, `padding: 0 48px`. Main visual stage between `y: 250px` and `y: 1350px`. Reserve `y: 1350px` to `1600px` for burned-in subtitles. Check platform overlays and adjust where needed.
- **Background:** Base `#070709`. Subtle perspective floor grid in the bottom 35% (`rgba(255,255,255,0.04)` lines with `perspective(600px) rotateX(65deg)`).
- **Center glow:** A radial gradient of roughly `600px` radius behind the focal element, transitioning with scene meaning:
  - Alert, hook, or series branding: crimson `rgba(229,25,43,0.22)`.
  - Value reveal: amber `rgba(245,183,0,0.20)`.
  - Neutral technical UI: blue `rgba(59,130,246,0.15)`.

## Typography

- **Impact headings:** Anton, Bebas Neue, or Inter Black; heavy uppercase, tight tracking around `-0.03em`.
- **UI body and cards:** Inter or Plus Jakarta Sans, weight 600/700.
- **Labels, badges, and URLs:** JetBrains Mono or Fira Code; uppercase badges with `0.12em` tracking.
- Use fonts available in the project or properly licensed assets; verify glyph coverage for the chosen language.

## Component primitives

### StatusPill

Rounded pill: `border-radius: 9999px`, `padding: 10px 24px`, monospace, `font-size: 20px`. Add a status dot when useful.

| Variant | Background | 1px border | Text |
| --- | --- | --- | --- |
| Danger | `rgba(239,68,68,0.12)` | `rgba(239,68,68,0.45)` | `#F87171` |
| Success | `rgba(34,197,94,0.12)` | `rgba(34,197,94,0.45)` | `#4ADE80` |
| Warning | `rgba(234,179,8,0.12)` | `rgba(234,179,8,0.45)` | `#FACC15` |
| Info | `rgba(59,130,246,0.12)` | `rgba(59,130,246,0.45)` | `#60A5FA` |

### DialogueCard

Dark glassmorphic container: `background: rgba(20,22,29,0.88)`, `border: 1px solid rgba(255,255,255,0.1)`, `border-radius: 24px`, `padding: 28px 32px`. Pair with a `56×56px` circular avatar and uppercase monospace role label where the script uses dialogue. Reveal text character by character in sync with narration, leaving enough time to read it.

### StampOverlay

Heavy rectangular stamp: `border: 4px solid #EF4444`, `color: #EF4444`, `border-radius: 12px`, `padding: 12px 36px`. Animate from `scale(2.2)` to `scale(1)` with rotation around `-4deg` and background dim `rgba(0,0,0,0.65)`. Use a label supported by the explanation.

### DeviceMockupCard

Phone shell: `border-radius: 44px`, `border: 2px solid rgba(255,255,255,0.12)`, `background: #0D0E12`, `padding: 36px`. Separate internal sections with dashed dividers; use monospace code blocks for strings or URLs and status pills for actual metrics. Compute displayed counts from the example data.

### ProgressGrid

For a series or progression, use a grid with `grid-template-columns: repeat(10,1fr)` and `gap: 12px`, adapting columns to content and legibility. Inactive cells: `#14151A`, `1px solid rgba(255,255,255,0.08)`, muted numbers. Active cell: `#E5192B`, red outer glow, bold white number.

## Motion and pacing

- Use snappy springs for cards and badges: starting values `stiffness: 220`, `damping: 18`, `mass: 0.9`. Avoid linear entrance motion for these elements.
- Stagger child entrances by approximately `0.1–0.16s` (6–10 frames at 60 FPS): top badge fades/slides from `translateY(-20px)`; headline/card scales from `0.92` to `1`; comparisons or grid cells populate; bottom callout appears last.
- Aim for a meaningful visual state change every `1.5–2.5s` and scene cuts around `3–5s`, while allowing sufficient reading and comprehension time. Derive frame counts from the actual project FPS.
- Use word-by-word highlighted captions when requested or when narration benefits from them. Match the supplied language; Hinglish is an option, not a requirement.

## Sound

When audio is part of the deliverable, keep narration clear above other tracks. Use subtle keyboard ticks/pops for text, a low impact for a stamp, crisp whooshes or UI clicks for pills, and an optional quiet synth pulse beneath the sequence. Use supplied or licensed audio; avoid constant effects that obscure the explanation.
