#!/usr/bin/env python3
"""
download_images.py — populate images/ for FruitGuesser.

Fetches the top 15 image results per fruit via DuckDuckGo Images
(same sources as Google Images; no API key or scraping blocks).

Usage:
    cd fruitguesser
    python download_images.py           # all fruits
    python download_images.py 10        # first N fruits only

Images are saved to:
    images/<Fruit Name>/img-001.jpg
    images/<Fruit Name>/img-002.jpg
    ...

Re-runnable: folders with >= SKIP_THRESHOLD images are skipped.
After the run, browse images/<Fruit Name>/ and delete any bad photos.
"""

import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

# ── Paths ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
IMAGES_DIR = SCRIPT_DIR / "images"

# ── Fruit list ─────────────────────────────────────────────────────────────────
FRUITS = [
    # Apples
    "Apple", "Fuji Apple", "Honeycrisp Apple", "Granny Smith Apple",
    "Gala Apple", "Braeburn Apple", "Pink Lady Apple", "McIntosh Apple",
    # Pears
    "Pear", "Bartlett Pear", "Asian Pear", "Bosc Pear",
    # Citrus
    "Orange", "Blood Orange", "Clementine", "Tangerine", "Mandarin",
    "Grapefruit", "Pomelo", "Lemon", "Lime", "Meyer Lemon", "Kumquat",
    "Yuzu", "Bergamot", "Cara Cara Orange", "Satsuma", "Ugli Fruit",
    # Berries
    "Strawberry", "Raspberry", "Blueberry", "Blackberry", "Cranberry",
    "Gooseberry", "Boysenberry", "Elderberry", "Mulberry", "Huckleberry",
    "Lingonberry", "Cloudberry", "Acai",
    # Stone Fruits
    "Peach", "Nectarine", "Plum", "Cherry", "Apricot", "Damson Plum",
    # Tropical (common)
    "Banana", "Plantain", "Pineapple", "Mango", "Papaya", "Coconut",
    "Guava", "Passion Fruit", "Dragon Fruit", "Lychee", "Longan",
    "Rambutan", "Jackfruit", "Durian", "Mangosteen", "Starfruit",
    # Tropical (less common but recognizable)
    "Soursop", "Cherimoya", "Feijoa", "Tamarind", "Breadfruit",
    "Ackee", "Sapodilla", "Sugar Apple", "Mamey Sapote", "Jabuticaba",
    # Melons
    "Watermelon", "Cantaloupe", "Honeydew Melon", "Canary Melon",
    "Galia Melon", "Crenshaw Melon",
    # Grapes
    "Grape", "Concord Grape", "Moondrop Grape", "Cotton Candy Grape",
    "Muscat Grape",
    # Other common
    "Kiwi", "Golden Kiwi", "Fig", "Date", "Pomegranate", "Avocado",
    "Persimmon", "Quince", "Loquat", "Currant", "Olive", "Noni",
    "Finger Lime",
]

# ── Config ─────────────────────────────────────────────────────────────────────
IMAGES_PER_FRUIT = 15
SKIP_THRESHOLD = 5        # skip folder if already has >= this many images
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
DELAY_BETWEEN_FRUITS = 2  # seconds between fruits
DOWNLOAD_WORKERS = 8       # parallel image downloads per fruit
DOWNLOAD_TIMEOUT = 20      # seconds per image download

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def existing_count(folder: Path) -> int:
    if not folder.is_dir():
        return 0
    return sum(1 for p in folder.iterdir() if p.suffix.lower() in IMAGE_EXTS)


_ddgs = None  # single shared session to avoid rate limits


def _get_ddgs():
    global _ddgs
    if _ddgs is None:
        try:
            from ddgs import DDGS
        except ImportError:
            from duckduckgo_search import DDGS  # fallback
        _ddgs = DDGS()
    return _ddgs


def search_images(fruit: str, count: int) -> list[str]:
    """Return up to *count* image URLs for *fruit* via DuckDuckGo Images."""
    # Append 'fruit' to disambiguate (e.g. 'kiwi' → 'kiwi fruit', not the bird)
    query = fruit if "fruit" in fruit.lower() else f"{fruit} fruit"
    for attempt in range(3):
        try:
            ddgs = _get_ddgs()
            results = list(ddgs.images(
                query,
                max_results=count * 2,  # fetch extra in case some fail
            ))
            return [r["image"] for r in results if r.get("image")][:count * 2]
        except Exception as exc:
            wait = (attempt + 1) * 5
            print(f"\n      [Search error attempt {attempt+1}] {fruit}: {exc} — retrying in {wait}s")
            time.sleep(wait)
    return []


def download_image(url: str, dest: Path) -> bool:
    """Download *url* to *dest*. Returns True on success."""
    if dest.exists():
        return True
    try:
        r = requests.get(url, headers=HEADERS, timeout=DOWNLOAD_TIMEOUT, stream=True)
        if r.status_code == 200:
            content_type = r.headers.get("content-type", "")
            if "image" not in content_type and "octet" not in content_type:
                return False
            data = r.content
            if len(data) > 5_000:  # skip suspiciously tiny responses
                dest.write_bytes(data)
                return True
    except Exception:
        pass
    return False


def ext_from_url(url: str) -> str:
    """Derive a file extension from a URL."""
    from urllib.parse import urlparse
    import posixpath
    path = urlparse(url).path
    _, ext = posixpath.splitext(path)
    ext = ext.lower().split("?")[0]
    if ext in (".jpeg", ".jpg"):
        return ".jpg"
    if ext in (".png", ".gif", ".webp"):
        return ext
    return ".jpg"  # default


def process_fruit(fruit: str, idx: int, total: int) -> int:
    """Download images for one fruit. Returns number of images saved."""
    folder = IMAGES_DIR / fruit
    count = existing_count(folder)

    if count >= SKIP_THRESHOLD:
        print(f"[{idx:3d}/{total}] {fruit:<32} skip ({count} images present)")
        return count

    folder.mkdir(parents=True, exist_ok=True)
    print(f"[{idx:3d}/{total}] {fruit:<32} searching...", end="", flush=True)

    urls = search_images(fruit, IMAGES_PER_FRUIT)
    if not urls:
        print(f" no results")
        return 0

    print(f" found {len(urls)} URLs, downloading...", end="", flush=True)

    # Download images in parallel, capping at IMAGES_PER_FRUIT successes
    import threading
    save_lock = threading.Lock()
    saved_paths = []

    def try_download(url):
        """Download url; return saved Path on success or None."""
        ext = ext_from_url(url)
        with save_lock:
            if len(saved_paths) >= IMAGES_PER_FRUIT:
                return None
            slot = len(saved_paths) + 1
            dest = folder / f"img-{slot:03d}{ext}"
            saved_paths.append(dest)  # reserve the slot
        ok = download_image(url, dest)
        if not ok:
            with save_lock:
                if dest in saved_paths:
                    saved_paths.remove(dest)
            try:
                dest.unlink(missing_ok=True)
            except Exception:
                pass
        return dest if ok else None

    with ThreadPoolExecutor(max_workers=DOWNLOAD_WORKERS) as pool:
        list(pool.map(try_download, urls))

    saved = sum(1 for p in saved_paths if p.exists())

    note = "  *** NO IMAGES ***" if saved == 0 else ""
    print(f" {saved} saved{note}")
    return saved


def main() -> None:
    IMAGES_DIR.mkdir(exist_ok=True)

    limit = int(sys.argv[1]) if len(sys.argv) > 1 else len(FRUITS)
    fruits = FRUITS[:limit]

    print("FruitGuesser — image downloader (DuckDuckGo Images)")
    print(f"  Fruits    : {len(fruits)} (of {len(FRUITS)} total)")
    print(f"  Output    : {IMAGES_DIR}")
    print(f"  Per fruit : {IMAGES_PER_FRUIT} images")
    print(f"  Skip if   : >= {SKIP_THRESHOLD} images already present")
    print("-" * 60)

    for idx, fruit in enumerate(fruits, 1):
        process_fruit(fruit, idx, len(fruits))
        if idx < len(fruits):
            time.sleep(DELAY_BETWEEN_FRUITS)

    print("\nDone! Review images/<Fruit>/ and delete any bad photos.")
    print("Then rsync/scp the images/ folder to your Redbot server.")


if __name__ == "__main__":
    main()
