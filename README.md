# Reel Creator Skills

Personal Codex skills for producing animated videos and publishing approved videos through connected Chrome.

| Skill | Purpose |
| --- | --- |
| `$cartoon-audio-short` — Reel Cartoons | Develop ideas/scripts or render voiceover-led cartoons locally. Finished videos use portrait 9:16, 1080×1920 at 30 fps, H.264/AAC, with captions, quiet background audio, a matching cover and posting caption by default. |
| `$stickman-animation` | Create programmatic 2D stickman stories and explainers, including scene manifests, rendering pipelines, narration, and synchronized captions. |
| `$upload-youtube` — Upload YouTube | Upload existing videos to YouTube Studio, add metadata and covers, and save or schedule a requested release. |
| `$upload-reel` — Upload Reel | Upload or resume an Instagram Reel with portrait framing, a matching cover, caption and hashtags; publish or schedule as requested. |

## Install

Clone this private repository using your own GitHub access. Copy the desired folders from `skills/` into your Codex skills directory, normally `~/.codex/skills/` or `$CODEX_HOME/skills/` if configured. Do not overwrite existing installations without reviewing differences.

For example, in PowerShell from this repository root:

```powershell
$skillsHome = Join-Path $env:USERPROFILE '.codex\skills'
New-Item -ItemType Directory -Path $skillsHome -Force | Out-Null
foreach ($skillName in @('cartoon-audio-short', 'stickman-animation', 'upload-youtube', 'upload-reel')) {
    $targetPath = Join-Path $skillsHome $skillName
    if (Test-Path -LiteralPath $targetPath) { throw "Review existing skill before replacing: $targetPath" }
    Copy-Item -LiteralPath (Join-Path '.\skills' $skillName) -Destination $targetPath -Recurse
}
```

Confirm the skills appear in a subsequent Codex turn's skill catalog. Explicit invocation uses the names shown above; automatic selection is enabled by default.

## Prerequisites and use

- **Reel Cartoons:** native Python 3.12+, Node with `module.stripTypeScriptTypes` (Node 24 recommended), npm, FFmpeg and FFprobe. Project setup installs pinned Python dependencies and Playwright/Chromium locally; setup downloads require network access. Create production projects outside the installed skill. Read its production reference before running the kit.
- **Stickman animation:** the skill describes a data-driven workflow; rendering tools, audio assets and any selected TTS provider must be supplied for each project.
- **Cover generation:** the cartoon skill uses the host's image-generation skill/tool when available. Image generation is not bundled with this repository. Rendering the cartoon engine itself needs no AI video provider.
- **Uploading:** a working connected Chrome session signed into the intended account. Browser permissions, account verification, available scheduling controls and upload limits can require user action. No credentials or browser sessions are included.
- **Defaults:** upload skills target Dinke4Leetcode on YouTube and `@dinke4leetcode` on Instagram, and use IST for requested schedules. Verify the account in the live UI. User instructions override defaults; the skills do not grant standing permission to publish.
- **Paths:** these are copies of the installed Windows skills and retain personal example paths under `C:/Users/utkarsh/`, the local Reels output convention and original-kit provenance paths. Adapt those defaults for another machine. Runtime resources resolve relative to each skill; the original Reel folder is provenance, not a dependency to copy.
- **Timestamps:** upload skills skip manual chapter/timecode mapping and subtitle alignment. The production skill still uses audio timing internally and generates captions/SRT as part of its normal rendering workflow.

Example requests:

```text
Use $cartoon-audio-short to explain insertion sort using my narration and transcript.
Use $upload-youtube to upload the approved video and cover, then schedule its release in IST.
Use $upload-reel to finish my prepared Instagram reel with its caption and hashtags.
```

## Contents and provenance

The skill directories preserve the installed files, including the cartoon engine, technical example, references, vendor sources and license notices. The bundled soldier story is a technical demonstration, not verified history. See `skills/cartoon-audio-short/references/sources.md` and `kit/vendor/` inside that skill for provenance, pinned source versions, hashes and third-party license terms.

Generated reels, narration recordings, upload screenshots, the original kit ZIP, local environments, credentials and unrelated skills are excluded. No new repository-wide license is assigned to third-party code; retain and follow the bundled notices.
