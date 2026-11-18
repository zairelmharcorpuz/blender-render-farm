# blender-render-farm

Render Blender frames on **GitHub's public Actions runners** — free and unlimited on public repos.

## How it works

1. **plan** — splits `frame_start..frame_end` into `workers` chunks
2. **render** — one runner per chunk (parallel VMs): downloads Blender 4.2 LTS (cached between runs), renders its frames with **Cycles CPU**
3. **collect** — verifies every expected frame arrived, zips them, and assembles an MP4 with ffmpeg

## Quick start

```bash
# render the built-in demo scene, frames 1-48 on 4 parallel workers
gh workflow run render.yml -f frame_start=1 -f frame_end=48 -f workers=4

# watch progress, then pull the results
gh run watch
gh run download   # saves all-frames.zip + render.mp4
```

## Inputs

| Input | Default | Description |
|---|---|---|
| `blend_path` | *(empty)* | Path to a `.blend` file in the repo. Empty = generate a demo scene |
| `frame_start` | `1` | First frame |
| `frame_end` | `48` | Last frame |
| `workers` | `4` | Parallel render jobs (each gets its own runner) |
| `samples` | `32` | Cycles samples per frame |
| `resolution_x` | `640` | Output width |
| `resolution_y` | `360` | Output height |
| `fps` | `24` | FPS for the assembled video |
| `assemble_video` | `true` | Also produce `render.mp4` |

## Rendering your own scene

Commit a `.blend` file, then point `blend_path` at it:

```bash
gh workflow run render.yml \
  -f blend_path=scenes/my-scene.blend \
  -f frame_start=100 -f frame_end=200 \
  -f workers=8 -f samples=128 -f resolution_x=1920 -f resolution_y=1080
```

Notes:

- Rendering always uses **Cycles on CPU** (runners have no GPU). `scripts/apply_settings.py`
  applies samples/resolution/PNG from the inputs on top of your scene; adjust it if you need
  more control (denoising is disabled by default for speed).
- Files over 100 MB must go through **Git LFS**.
- Each chunk runs on its own 4-vCPU runner, so `workers=8` gives you 8 VMs working at once.

## Outputs

Artifacts (kept 7 days):

- `all-frames` — every PNG as a zip
- `render-video` — the assembled MP4 (if `assemble_video=true`)
- per-chunk `frames-N` — individual chunks

## Files

```
.github/workflows/render.yml   # plan → render (matrix) → collect pipeline
scripts/setup_demo.py          # generates the demo scene when no blend_path given
scripts/apply_settings.py      # applies samples/resolution/engine to the scene
```
