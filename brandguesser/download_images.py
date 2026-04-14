#!/usr/bin/env python3
"""
download_images.py — download logos and generate stages for BrandGuesser.

For each brand:
  1. Search DuckDuckGo images for "{search_term}".
  2. Download the first 3 successful results.
  3. Save originals as images/{brand}/img-001.jpg, img-002.jpg, img-003.jpg.
  4. Generate 5 reveal stages per image:
       img-001 → pixel   stages/img-001_s1.jpg … img-001_s5.jpg
       img-002 → shuffle stages/img-002_s1.jpg … img-002_s5.jpg
       img-003 → blur    stages/img-003_s1.jpg … img-003_s5.jpg

Usage:
    python download_images.py              # all brands
    python download_images.py 10           # first N brands
    python download_images.py "McDonald"   # single brand (substring match)
"""

import io
import os
import sys
import time
import random
from pathlib import Path

import requests
from PIL import Image, ImageFilter

# ── Paths ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
IMAGES_DIR = Path(os.environ.get("IMAGES_DIR", str(SCRIPT_DIR / "images")))

# ── Config ─────────────────────────────────────────────────────────────────────
DELAY_MIN        = 3
DELAY_MAX        = 8
DDG_TIMEOUT      = 25
DOWNLOAD_TIMEOUT = 20
CANDIDATE_URLS   = 15   # fetch this many URLs; take first 3 that download OK

DISPLAY_SIZE = (400, 400)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# ── Stage parameters (from create_stages.py) ───────────────────────────────────
PIXEL_SIZES           = [8, 14, 24, 42, 72]
BLUR_RADII            = [45, 30, 20, 13, 5]
SHUFFLE_FIX_FRACTIONS = [0.0, 0.30, 0.55, 0.72, 0.85]
SHUFFLE_BLOCK_SIZE    = 40


# ── Stage generators ───────────────────────────────────────────────────────────
def stage_pixel(img, small_size):
    return img.resize((small_size, small_size), Image.BOX).resize(DISPLAY_SIZE, Image.NEAREST)


def stage_blur(img, radius):
    return img.filter(ImageFilter.GaussianBlur(radius=radius))


def stage_shuffle(img, fix_fraction, seed):
    bs   = SHUFFLE_BLOCK_SIZE
    cols = DISPLAY_SIZE[0] // bs
    rows = DISPLAY_SIZE[1] // bs
    n    = cols * rows

    blocks = []
    for r in range(rows):
        for c in range(cols):
            blocks.append(img.crop((c*bs, r*bs, (c+1)*bs, (r+1)*bs)))

    rng_shuffle = random.Random(seed)
    shuffled = list(range(n))
    rng_shuffle.shuffle(shuffled)

    n_fix = int(n * fix_fraction)
    rng_fix = random.Random(seed + 99991)
    fix_order = list(range(n))
    rng_fix.shuffle(fix_order)
    fixed_slots = set(fix_order[:n_fix])

    result = img.copy()
    for i in range(n):
        src = i if i in fixed_slots else shuffled[i]
        r, c = divmod(i, cols)
        result.paste(blocks[src], (c*bs, r*bs))
    return result


def generate_stages(img_path: Path, style: str):
    stages_dir = img_path.parent / "stages"
    stages_dir.mkdir(exist_ok=True)
    stem = img_path.stem
    seed = int(stem.split("-")[1]) if "-" in stem else 1

    img = Image.open(img_path).convert("RGB").resize(DISPLAY_SIZE, Image.LANCZOS)

    for i in range(5):
        if style == "pixel":
            out = stage_pixel(img, PIXEL_SIZES[i])
        elif style == "shuffle":
            out = stage_shuffle(img, SHUFFLE_FIX_FRACTIONS[i], seed)
        else:  # blur
            out = stage_blur(img, BLUR_RADII[i])
        out.save(stages_dir / f"{stem}_s{i+1}.jpg", "JPEG", quality=90)


# ── DDG search ────────────────────────────────────────────────────────────────
def search_images(query: str, n: int) -> list:
    try:
        from ddgs import DDGS
    except ImportError:
        from duckduckgo_search import DDGS
    for attempt in range(3):
        try:
            results = list(DDGS(timeout=DDG_TIMEOUT).images(query, max_results=n))
            return [r["image"] for r in results if r.get("image")]
        except Exception as exc:
            wait = (attempt + 1) * 5
            print(f"\n  [DDG error #{attempt+1}] {exc!r} — retrying in {wait}s", flush=True)
            time.sleep(wait)
    return []


# ── Download one image ────────────────────────────────────────────────────────
def fetch_image(url: str):
    """Download URL and return a PIL Image (RGB), or None on failure."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=DOWNLOAD_TIMEOUT)
        if r.status_code != 200 or "image" not in r.headers.get("content-type", ""):
            return None
        img = Image.open(io.BytesIO(r.content))
        if img.mode == "RGBA":
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[3])
            return bg
        return img.convert("RGB")
    except Exception:
        return None


# ── Process one brand ─────────────────────────────────────────────────────────
STYLES = ["pixel", "shuffle", "blur"]   # img-001, img-002, img-003

def process_brand(name: str, search_term: str, idx: int, total: int):
    folder = IMAGES_DIR / name

    # Skip if all 3 images already exist
    if all((folder / f"img-{n:03d}.jpg").exists() for n in [1, 2, 3]):
        print(f"[{idx:3d}/{total}] {name:<42} skip")
        return

    folder.mkdir(parents=True, exist_ok=True)
    (folder / "stages").mkdir(exist_ok=True)

    print(f"[{idx:3d}/{total}] {name:<42}", end="", flush=True)

    urls = search_images(search_term, CANDIDATE_URLS)
    saved = 0
    for url in urls:
        if saved >= 3:
            break
        img = fetch_image(url)
        if img is None:
            continue
        slot = saved + 1
        dest = folder / f"img-{slot:03d}.jpg"
        img.save(dest, "JPEG", quality=92)
        generate_stages(dest, STYLES[saved])
        print(f" img-{slot:03d}[{STYLES[saved][:2]}]", end="", flush=True)
        saved += 1

    if saved == 0:
        print(" *** no images ***", flush=True)
    else:
        print(f"  ({saved}/3)", flush=True)


# ── Main ──────────────────────────────────────────────────────────────────────
def load_brands():
    try:
        from brands import BRANDS
    except ImportError:
        sys.path.insert(0, str(SCRIPT_DIR))
        from brands import BRANDS
    return [(name, data.get("search_term") or f"{name} logo") for name, data in BRANDS.items()]


def main():
    args = sys.argv[1:]
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    all_brands = load_brands()

    if args:
        arg = args[0]
        if arg.isdigit():
            brands = all_brands[:int(arg)]
        else:
            needle = arg.lower()
            brands = [(n, s) for n, s in all_brands if needle in n.lower()]
            if not brands:
                print(f"No brand matching '{arg}' found.")
                sys.exit(1)
    else:
        brands = all_brands

    print(f"BrandGuesser pipeline — {len(brands)} brands")
    print(f"  img-001=pixel  img-002=shuffle  img-003=blur")
    print(f"  Output: {IMAGES_DIR}")
    print("-" * 60)

    for i, (name, term) in enumerate(brands, 1):
        process_brand(name, term, i, len(brands))
        if i < len(brands):
            time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

    print("\nDone.")


if __name__ == "__main__":
    main()
