"""Parse all CSV txt files in the csv/ folder and output csv_people_data.py."""
import csv
import io
import os
import re

CSV_DIR = os.path.join(os.path.dirname(__file__), "csv")
OUT_FILE = os.path.join(os.path.dirname(__file__), "csv_people_data.py")

def clean_value(s):
    """Strip surrounding quotes and whitespace."""
    return s.strip().strip('"').strip()

def normalize_header(h):
    """Strip markdown bold markers and whitespace from header names."""
    return re.sub(r'\*+', '', h).strip().strip('"').strip()

def parse_file(path):
    entries = []
    with open(path, encoding="utf-8", errors="replace") as f:
        raw = f.read()

    # Drop lines that are code fences or prose preamble
    lines = []
    for line in raw.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            continue
        if stripped.lower().startswith("here is"):
            continue
        lines.append(line)

    content = "\n".join(lines)

    reader = csv.reader(io.StringIO(content), skipinitialspace=True)
    rows = list(reader)
    if not rows:
        return entries

    # Find the header row (first row that contains "name")
    header_idx = None
    headers = []
    for i, row in enumerate(rows):
        normalized = [normalize_header(c) for c in row]
        # Handle case where entire header is one quoted string e.g. "**name,profession,bio,known_for**"
        if len(normalized) == 1 and "," in normalized[0]:
            split = [normalize_header(h) for h in normalized[0].split(",")]
            if any(h.lower() == "name" for h in split):
                header_idx = i
                headers = [h.lower() for h in split]
                break
        if any(h.lower() == "name" for h in normalized):
            header_idx = i
            headers = [h.lower() for h in normalized]
            break
    if header_idx is None:
        return entries

    # Map column indices
    def idx(name):
        for i, h in enumerate(headers):
            if h == name:
                return i
        return None

    ni = idx("name")
    pi = idx("profession")
    bi = idx("bio")
    ki = idx("known_for")

    if None in (ni, pi, bi, ki):
        print(f"WARNING: missing columns in {os.path.basename(path)}: {headers}")
        return entries

    for row in rows[header_idx + 1:]:
        if len(row) < max(ni, pi, bi, ki) + 1:
            continue
        name = row[ni].strip()
        if not name:
            continue
        # Handle malformed row where profession is duplicated (e.g. Chris Evans line)
        profession = row[pi].strip()
        bio = row[bi].strip()
        known_for = row[ki].strip()

        # If bio looks like a profession (very short, no period), swap bio with next field
        if len(bio) < 30 and "." not in bio and len(row) > max(ni, pi, bi, ki) + 1:
            # The real bio is in the next column
            bio = row[bi + 1].strip()
            known_for = row[ki + 1].strip() if ki + 1 < len(row) else known_for

        entries.append({
            "name": name,
            "profession": profession,
            "bio": bio,
            "known_for": known_for,
        })

    return entries

def main():
    all_entries = {}
    skipped_dupes = 0

    for fname in sorted(os.listdir(CSV_DIR)):
        if not fname.endswith(".txt"):
            continue
        path = os.path.join(CSV_DIR, fname)
        entries = parse_file(path)
        print(f"{fname}: {len(entries)} entries")
        for e in entries:
            name = e["name"]
            if name in all_entries:
                skipped_dupes += 1
            else:
                all_entries[name] = e

    print(f"\nTotal unique entries: {len(all_entries)}")
    print(f"Skipped duplicates: {skipped_dupes}")

    lines = [
        "# Auto-generated from retardguesser/csv/*.txt — do not edit manually\n",
        "\n",
        "CSV_PEOPLE = {\n",
    ]
    for name, e in all_entries.items():
        # Escape backslashes and quotes for Python string literals
        def esc(s):
            return s.replace("\\", "\\\\").replace('"', '\\"')

        lines.append(f'    "{esc(name)}": {{\n')
        lines.append(f'        "name": "{esc(e["name"])}",\n')
        lines.append(f'        "profession": "{esc(e["profession"])}",\n')
        lines.append(f'        "bio": "{esc(e["bio"])}",\n')
        lines.append(f'        "known_for": "{esc(e["known_for"])}",\n')
        lines.append(f'    }},\n')

    lines.append("}\n")

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"Written to {OUT_FILE}")

if __name__ == "__main__":
    main()
