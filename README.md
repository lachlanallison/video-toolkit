# Video Toolkit

**Live app:** [https://lachlanallison.github.io/video-toolkit/](https://lachlanallison.github.io/video-toolkit/)

Fast, browser-based video tools powered by [ffmpeg.wasm](https://ffmpegwasm.netlify.app/). Files stay on your machine.

## Recent WebCodecs updates

- Faster bailout for slow `<video> + rVFC` fallback paths, so jobs do not stall for minutes.
- Smarter routing: try primary WebCodecs first, then selective fallback, then reliable ffmpeg.
- Clearer runtime logs when WebCodecs is skipped and ffmpeg is used.

## What it does

- Shrink to target size
- Convert codecs and containers
- Remux (no re-encode)
- Extract audio
- Trim clips
- Generate thumbnail grids and GIFs

## Run locally

```powershell
python -m http.server 8000
# open http://localhost:8000/
```

## GitHub Pages

1. Push this repo to GitHub.
2. Repo Settings -> Pages -> Deploy from branch.
3. Select `main` and `/ (root)`.
4. Open [https://lachlanallison.github.io/video-toolkit/](https://lachlanallison.github.io/video-toolkit/).

## Notes

- Hardware acceleration is attempted via WebCodecs where supported.
- `ffmpeg.wasm` remains the reliable fallback when codec/profile/browser support does not line up.
- Cross-origin isolation is enabled via `coi-serviceworker.js` for MT + SIMD builds.
