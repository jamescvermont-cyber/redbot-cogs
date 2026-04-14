#!/usr/bin/env python3
"""
create_stages.py — generate progressive reveal stages for BrandGuesser.

For each processed image images/{brand}/img-NNN.jpg, generates 7 blur stages:
  images/{brand}/stages/img-NNN_s1.jpg   ← most blurred  (shown at t=0s)
  images/{brand}/stages/img-NNN_s2.jpg                   (shown at t=10s)
  ...
  images/{brand}/stages/img-NNN_s7.jpg   ← nearly clear  (shown at t=60s)
  images/{brand}/stages/img-NNN_s8.jpg   ← fully clear   (shown at t=70s)

Three styles, randomly assigned per image so every round feels different:

  pixel — hard block pixelation (downscale + NEAREST upscale)
           Classic retro/Minecraft look. Hard color edges.

  blur  — smooth Gaussian blur
           "Out of focus" look. Soft color gradients.

  blob  — soft pixelation (downscale + LANCZOS upscale)
           Watercolor / impressionist look. Large smooth color clouds.

Usage:
    python create_stages.py                  # all brands, assign styles randomly
    python create_stages.py "Toyota"         # single brand (substring match)
    python create_stages.py --regen          # regenerate even if stages exist
    python create_stages.py --test           # all 3 styles on first available image
    python create_stages.py --test "Toyota"  # all 3 styles on Toyota img-001
"""

import os
import sys
import random
from pathlib import Path
from PIL import Image, ImageFilter

# ── Paths & config ─────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
IMAGES_DIR  = Path(os.environ.get("IMAGES_DIR", str(SCRIPT_DIR / "images")))

DISPLAY_SIZE = (400, 400)   # all stage images standardized to this
IMAGE_EXTS   = {".jpg", ".jpeg", ".png", ".webp"}
STYLES       = ["pixel", "blur", "blob"]

# ── Style parameters ───────────────────────────────────────────────────────────

# Pixelation: size of the intermediate downscale image.
# Geometric ~1.7× progression: 8→14→24→42→72→120→200.
# At 8×8 a 400×400 image becomes 50px hard blocks — extremely abstract.
# At 200×200 it's 2px blocks — nearly indistinguishable from original.
PIXEL_SIZES = [8, 14, 24, 42, 72, 120, 200]

# Gaussian blur radii (pixels). Large radius = very soft/spread.
# At radius 80 on a 400×400 image the whole thing is a smear of color.
BLUR_RADII = [80, 55, 38, 26, 17, 9, 3]


# ── Stage generators ───────────────────────────────────────────────────────────

def stage_pixel(img: Image.Image, small_size: int) -> Image.Image:
    """Hard pixelation: downscale with BOX (average), upscale with NEAREST (hard edges)."""
    small = img.resize((small_size, small_size), Image.BOX)
    return small.resize(DISPLAY_SIZE, Image.NEAREST)


def stage_blur(img: Image.Image, radius: float) -> Image.Image:
    """Smooth Gaussian blur."""
    return img.filter(ImageFilter.GaussianBlur(radius=radius))


def stage_blob(img: Image.Image, small_size: int) -> Image.Image:
    """Soft pixelation: downscale with BOX, upscale with LANCZOS.
    Produces large smooth color clouds — watercolor / impressionist look."""
    small = img.resize((small_size, small_size), Image.BOX)
    return small.resize(DISPLAY_SIZE, Image.LANCZOS)


def _make_stage(img: Image.Image, style: str, stage_num: int) -> Image.Image:
    """stage_num is 1-based (1 = most blurred, 7 = nearly clear)."""
    idx = stage_num - 1
    if style == "pixel":
        return stage_pixel(img, PIXEL_SIZES[idx])
    elif style == "blur":
        return stage_blur(img, BLUR_RADII[idx])
    elif style == "blob":
        return stage_blob(img, PIXEL_SIZES[idx])
    else:
        raise ValueError(f"Unknown style: {style!r}")


# ── Core: process one image ────────────────────────────────────────────────────

def generate_stages_for_image(
    img_path: Path,
    style: str,
    regen: bool = False,
) -> bool:
    """
    Generate 7 blur stages + 1 clear stage for a single processed image.
    Returns True if stages were written, False if skipped (already exist).
    """
    stages_dir = img_path.parent / "stages"
    stem = img_path.stem  # e.g. "img-001"

    if not regen:
        existing = list(stages_dir.glob(f"{stem}_s*.jpg"))
        if len(existing) >= 8:
            return False

    stages_dir.mkdir(exist_ok=True)

    img = Image.open(img_path).convert("RGB")
    img = img.resize(DISPLAY_SIZE, Image.LANCZOS)

    # Stages 1–7: progressively clearer
    for stage_num in range(1, 8):
        out = stages_dir / f"{stem}_s{stage_num}.jpg"
        _make_stage(img, style, stage_num).save(out, "JPEG", quality=90)

    # Stage 8: fully clear (standardized size copy of the original)
    (stages_dir / f"{stem}_s8.jpg").parent.mkdir(exist_ok=True)
    img.save(stages_dir / f"{stem}_s8.jpg", "JPEG", quality=93)

    return True


# ── Process a brand ────────────────────────────────────────────────────────────

def process_brand(brand_name: str, regen: bool = False) -> int:
    folder = IMAGES_DIR / brand_name
    if not folder.is_dir():
        print(f"  [{brand_name}] folder not found, skipping")
        return 0

    img_files = sorted(
        p for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS and p.stem.startswith("img-")
    )
    if not img_files:
        print(f"  [{brand_name}] no images found, skipping")
        return 0

    done = 0
    for img_path in img_files:
        style = random.choice(STYLES)
        generated = generate_stages_for_image(img_path, style, regen=regen)
        marker = f" {img_path.name}[{style[0]}]" if generated else f" {img_path.name}[skip]"
        print(marker, end="", flush=True)
        if generated:
            done += 1

    print()
    return done


# ── Test mode: all 3 styles on one image side by side ─────────────────────────

def test_mode(brand_hint: str = "") -> None:
    """
    Generate all 3 styles × 7 stages for a single image.
    Output: images/_test_comparison/{style}_s{N}.jpg + original.jpg
    Lets you visually compare all three styles before committing.
    """
    # Find the test image
    test_img = None

    if brand_hint:
        needle = brand_hint.lower()
        for brand_dir in sorted(IMAGES_DIR.iterdir()):
            if needle in brand_dir.name.lower() and brand_dir.is_dir():
                imgs = sorted(
                    p for p in brand_dir.iterdir()
                    if p.is_file() and p.suffix.lower() in IMAGE_EXTS
                    and p.stem.startswith("img-")
                )
                if imgs:
                    test_img = imgs[0]
                    break
    else:
        for brand_dir in sorted(IMAGES_DIR.iterdir()):
            if brand_dir.is_dir() and brand_dir.name != "_test_comparison":
                imgs = sorted(
                    p for p in brand_dir.iterdir()
                    if p.is_file() and p.suffix.lower() in IMAGE_EXTS
                    and p.stem.startswith("img-")
                )
                if imgs:
                    test_img = imgs[0]
                    break

    if not test_img:
        print("ERROR: No images found to test with.")
        print(f"  (looked in {IMAGES_DIR})")
        return

    print(f"Test image : {test_img}")
    out_dir = IMAGES_DIR / "_test_comparison"
    out_dir.mkdir(parents=True, exist_ok=True)

    img = Image.open(test_img).convert("RGB")
    img = img.resize(DISPLAY_SIZE, Image.LANCZOS)

    for style in STYLES:
        for stage_num in range(1, 8):
            out_path = out_dir / f"{style}_s{stage_num}.jpg"
            _make_stage(img, style, stage_num).save(out_path, "JPEG", quality=90)
        print(f"  {style}: s1→s7 written")

    # Original
    orig_path = out_dir / "original.jpg"
    img.save(orig_path, "JPEG", quality=93)
    print(f"  original written")

    total = 3 * 7 + 1
    print(f"\n{total} comparison images → {out_dir}")
    print("\nFile naming:")
    print("  pixel_s1.jpg … pixel_s7.jpg  — hard block pixelation")
    print("  blur_s1.jpg  … blur_s7.jpg   — smooth Gaussian blur")
    print("  blob_s1.jpg  … blob_s7.jpg   — soft/watercolor pixelation")
    print("  original.jpg                  — unmodified source")
    print("\nStage 1 = most blurred (t=0s), Stage 7 = nearly clear (t=60s)")


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    args  = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}

    regen     = "--regen" in flags
    test      = "--test"  in flags

    if test:
        test_mode(brand_hint=args[0] if args else "")
        return

    from brands import BRANDS
    all_brand_names = list(BRANDS.keys())

    if args:
        needle = args[0].lower()
        targets = [n for n in all_brand_names if needle in n.lower()]
        if not targets:
            print(f"No brand matching '{args[0]}' found.")
            sys.exit(1)
    else:
        targets = all_brand_names

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    print(f"BrandGuesser — stage generator")
    print(f"  Brands  : {len(targets)}")
    print(f"  Output  : {IMAGES_DIR}")
    print(f"  Styles  : {', '.join(STYLES)} (randomly assigned per image)")
    print(f"  Regen   : {'yes' if regen else 'no (skip if 8 stages exist)'}")
    print("-" * 60)

    total_done = 0
    for name in targets:
        n = process_brand(name, regen=regen)
        total_done += n

    print(f"\nDone — generated stages for {total_done} images.")


if __name__ == "__main__":
    main()
