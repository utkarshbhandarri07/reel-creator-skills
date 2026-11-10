# Sources and adaptations

Original user inputs, preserved in `C:/Users/utkarsh/Desktop/Development/Reel`:

- `SKILL.md`, SHA-256 `2ac0bf5f2ab7a689b3751050df664920d7763392a9287b0ce8d7254ea4cfc2ed`
- `cartoon-short-kit.zip`, SHA-256 `784c07e36df5e91ddf93c78a1dde6b98b3aa3e3c37cadff03c5603d3971ce788`

The user-supplied kit has no independent license file. Preserve its attribution and do not claim it has a blanket MIT license. Its third-party components have separate MIT notices:

- `kit/vendor/toon.ts`: mromidev/claude-animated-shorts, commit `e3b817b6afc6cd413466d43f11ba31209e034bbf`; notice `toon-LICENSE`.
- `kit/vendor/three.module.js`: mrdoob/three.js, r160 (0.160.0); notice `three-LICENSE`.

`kit/vendor/sources.json` records exact URLs and SHA-256 checksums. Setup verifies these files before copying. Runtime dependencies are pinned in setup and requirements; generated projects retain an npm lockfile. No automatic source updates.

The adapted copy adds Windows-compatible project setup, a constant-gain mixer, script-first checked timing, a local-only checked renderer, stem-only sample audio and a linear-gain encoding/QA helper. The original Bash setup and finishing helpers are omitted to avoid invoking contradictory workflows. The original source inputs and Open Film remain unchanged.
