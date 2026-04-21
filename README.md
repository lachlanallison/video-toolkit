# Video Toolkit

Local, browser-based video toolkit powered by [ffmpeg.wasm](https://ffmpegwasm.netlify.app/). Shrink, convert, extract, trim, and more — everything runs in your browser. Files never leave your machine.

## Operations

- **Shrink** — hit a specific file size (e.g. Discord's 10 MB limit) via bitrate-targeted re-encode.
- **Convert** — change codec (H.264 / H.265 / VP9), container (`.mp4` / `.mkv` / `.mov` / `.webm`) and quality (CRF).
- **Remux** — change container only, no re-encode. Near-instant.
- **Extract audio** — save the audio track as MP3 / AAC / Ogg / Opus / FLAC / WAV, or stream-copy.
- **Trim** — cut a time range. Stream copy (fast, keyframe-aligned) or re-encode (frame-accurate).
- **Thumbnail grid** — one PNG sprite-sheet of evenly-spaced stills.
- **Make GIF** — palette-generated GIF from a slice of the clip.

## Run locally

```powershell
python -m http.server 8000
# then open http://localhost:8000/video-toolkit.html
```

## Deploy to GitHub Pages

1. Commit the entire `video-toolkit/` folder to a GitHub repo.
2. Repo → **Settings** → **Pages** → Build and deployment → **Deploy from a branch**. Pick `main` + `/ (root)` (or `/docs` if you move the folder).
3. Wait for the Pages build, then open `https://<user>.github.io/<repo>/video-toolkit.html`.

If the repo root contains other files, you can point Pages at the `/video-toolkit` subfolder directly.

### Important files for Pages
- `video-toolkit.html` — the app.
- `coi-serviceworker.js` — installs a service worker that adds `Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Embedder-Policy: require-corp` headers. Without it the page can't use `SharedArrayBuffer`, which means no multi-threaded ffmpeg.
- `vendor/*` — same-origin copies of ffmpeg.wasm core files (`@ffmpeg/core@0.12.10`, `@ffmpeg/ffmpeg@0.12.15`). Avoids cross-origin `importScripts` failures in Firefox/Brave when third-party workers are blocked.
- `vendor/mt/*` — multi-threaded + SIMD core (`@ffmpeg/core-mt@0.12.10`).
- `.nojekyll` — disables GitHub Pages' Jekyll pipeline so nothing filters these assets.

### First-visit behavior
The service worker installs on first load and then reloads the page once so the page comes back cross-origin isolated. Look at the badges near the title:
- `build: MT + SIMD` (green) — multi-threaded build active, optimal performance.
- `build: single-thread` (yellow) — isolation failed; falls back to the slower single-threaded build.

## Browser limitations (expanded inside the app)

- **~2 GB memory cap per tab** — `ffmpeg.wasm` is `wasm32`, 32-bit pointers inside the module. Most browsers cap at 2 GB (some allow 4 GB). Not a 32-bit-browser issue.
- **No hardware acceleration** — no NVENC / Quick Sync / VideoToolbox. Pure CPU through wasm, 10–50× slower than native `ffmpeg`.
- **Firefox hides `performance.memory`** — live memory readouts say "n/a" on Firefox.
- **One runtime per tab** — wasm heap cannot be reclaimed after an abort. Reload between failures.
- **MT build quirks** — 2-pass transition and teardown can abort; the app auto-recovers output and/or suggests 1-pass.

## Performance

Single-threaded vs multi-threaded on a ~39 s 4K clip shrunk to 10 MB @ 720p H.264 veryfast 2-pass:

| Build | Typical wall time | Speed vs native ffmpeg |
|---|---|---|
| Single-thread wasm (no SIMD) | ~13 min | ~20–40× slower |
| MT + SIMD wasm | ~1.5–3 min | ~2–5× slower |
| Native `ffmpeg` (CPU, all cores) | ~30–90 s | baseline |
| Native with NVENC / QuickSync | ~5–20 s | 3–10× faster than native CPU |

Speed tips:
- Use the **1-pass bitrate** quality mode (default) unless you need ~1% size accuracy.
- Use a faster **Encoder preset** (ultrafast / superfast) when quality matters less than speed.
- Downscale aggressively (720p → 480p roughly halves encoding time).
- Stick with H.264; VP9 / H.265 are ~2× slower at comparable quality.
- For container-only changes use **Remux** — 20–100× faster than re-encoding.

## Refreshing vendored ffmpeg files

Re-run these any time you want to pick up a newer pinned version:

```powershell
# single-thread core
Invoke-WebRequest 'https://cdn.jsdelivr.net/npm/@ffmpeg/core@0.12.10/dist/umd/ffmpeg-core.js'  -OutFile .\vendor\ffmpeg-core.js
Invoke-WebRequest 'https://cdn.jsdelivr.net/npm/@ffmpeg/core@0.12.10/dist/umd/ffmpeg-core.wasm' -OutFile .\vendor\ffmpeg-core.wasm
Invoke-WebRequest 'https://cdn.jsdelivr.net/npm/@ffmpeg/ffmpeg@0.12.15/dist/umd/814.ffmpeg.js' -OutFile .\vendor\814.ffmpeg.js
Invoke-WebRequest 'https://cdn.jsdelivr.net/npm/@ffmpeg/ffmpeg@0.12.15/dist/umd/ffmpeg.js'      -OutFile .\vendor\ffmpeg.js
Invoke-WebRequest 'https://cdn.jsdelivr.net/npm/@ffmpeg/util@0.12.2/dist/umd/index.js'          -OutFile .\vendor\ffmpeg-util.js

# multi-thread core
Invoke-WebRequest 'https://cdn.jsdelivr.net/npm/@ffmpeg/core-mt@0.12.10/dist/umd/ffmpeg-core.js'        -OutFile .\vendor\mt\ffmpeg-core.js
Invoke-WebRequest 'https://cdn.jsdelivr.net/npm/@ffmpeg/core-mt@0.12.10/dist/umd/ffmpeg-core.wasm'      -OutFile .\vendor\mt\ffmpeg-core.wasm
Invoke-WebRequest 'https://cdn.jsdelivr.net/npm/@ffmpeg/core-mt@0.12.10/dist/umd/ffmpeg-core.worker.js' -OutFile .\vendor\mt\ffmpeg-core.worker.js

# cross-origin isolation shim
Invoke-WebRequest 'https://cdn.jsdelivr.net/npm/coi-serviceworker@0.1.7/coi-serviceworker.js' -OutFile .\coi-serviceworker.js
```
