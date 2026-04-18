#!/usr/bin/env python3
"""
generate_individual.py — Generate one name-only SVG per person for reprints.

Use this when blank tags are already printed/cut and you only need to print
the name overlay.  Each output SVG is exactly one badge wide/tall, with the
name positioned to match the standard sheet layout.

Usage:
    python3 generate_individual.py <show_config.yaml> [names_csv]

If names_csv is omitted the script looks for extra_names.csv next to the
show config, then falls back to the show's configured names_csv.

Output is written to <output_dir>/individual/<FirstLast.svg>.
"""

import argparse
import csv
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

try:
    import yaml
except ImportError:
    sys.exit("python3-yaml is required: sudo apt install python3-yaml")

# ---------------------------------------------------------------------------
# Shared geometry (must stay in sync with generate_sheets.py)
# ---------------------------------------------------------------------------

SVG_NS   = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"

ET.register_namespace("",      SVG_NS)
ET.register_namespace("xlink", XLINK_NS)


def svgtag(local):
    return f"{{{SVG_NS}}}{local}"


BADGE_W   = 335      # template units (96 DPI px)
BADGE_H   = 239
ART_W     = 252.0    # art-coordinate space
ART_H     = 180.0
ART_SCALE_X = BADGE_W / ART_W   # ≈ 1.3294
ART_SCALE_Y = BADGE_H / ART_H   # ≈ 1.3278

DEFAULTS = {
    "output_dir": "output",
    "name_style": {
        "font_family":   "Sour Gummy",
        "font_color":    "#0194e9",
        "shadow_color":  "#000000",
        "shadow_offset": 1.370,
        "font_weight":   "normal",
        "base_font_size": 24,
        "min_font_size":  10,
        "name_center_x": 126.0,
        "first_name_y":  110.0,
        "last_name_y":   140.0,
        "name_margin":   10.0,
    },
}


def deep_merge(base, override):
    result = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(result.get(k), dict):
            result[k] = deep_merge(result[k], v)
        else:
            result[k] = v
    return result


def load_config(config_path: Path) -> dict:
    with open(config_path) as f:
        user_cfg = yaml.safe_load(f) or {}
    cfg = deep_merge(DEFAULTS, user_cfg)
    cfg["show_dir"] = config_path.parent
    for key in ("front_art", "back_art", "names_csv"):
        if key in cfg:
            p = Path(cfg[key])
            if not p.is_absolute():
                cfg[key] = (config_path.parent / p).resolve()
    cfg["output_dir"] = (config_path.parent / cfg["output_dir"]).resolve()
    return cfg


def load_names(csv_path: Path) -> list[tuple[str, str]]:
    names = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            if not row:
                continue
            full = row[0].strip()
            if not full:
                continue
            parts = full.split(None, 1)
            first = parts[0].upper()
            last  = parts[1].upper() if len(parts) > 1 else ""
            names.append((first, last))
    return names


# ---------------------------------------------------------------------------
# Font-size helper
# ---------------------------------------------------------------------------

def choose_font_size(text: str, base_t: float, min_t: float, avail_t: float) -> float:
    size = base_t
    while size > min_t:
        if size * len(text) * 0.55 <= avail_t:
            break
        size -= 1
    return max(size, min_t)


# ---------------------------------------------------------------------------
# SVG generator for a single badge (name text only, no art background)
# ---------------------------------------------------------------------------

def make_badge_svg(first: str, last: str, style: dict) -> ET.Element:
    """
    Return an SVG element sized to one badge (BADGE_W × BADGE_H template units).
    Contains only the name text elements — no background art.
    """
    root = ET.Element(svgtag("svg"))
    root.set("version",   "1.1")
    root.set("viewBox",   f"0 0 {BADGE_W} {BADGE_H}")
    root.set("width",     f"{BADGE_W / 96:.6f}in")
    root.set("height",    f"{BADGE_H / 96:.6f}in")

    ns = style
    # Art-space → template-space (badge origin is 0,0)
    cx_t      = ns["name_center_x"] * ART_SCALE_X
    first_y_t = ns["first_name_y"]  * ART_SCALE_Y
    last_y_t  = ns["last_name_y"]   * ART_SCALE_Y
    margin_t  = ns["name_margin"]   * ART_SCALE_X
    avail_t   = BADGE_W - 2 * margin_t

    base_t       = ns["base_font_size"] * ART_SCALE_Y
    min_t        = ns["min_font_size"]  * ART_SCALE_Y
    shadow_off_t = ns["shadow_offset"]  * ART_SCALE_X
    family       = ns["font_family"]
    weight       = ns.get("font_weight", "normal")
    main_color   = ns["font_color"]
    shadow_color = ns.get("shadow_color", "#000000")

    def make_text(content, x, y, fill, sz):
        el = ET.Element(svgtag("text"))
        el.set("x",           f"{x:.2f}")
        el.set("y",           f"{y:.2f}")
        el.set("text-anchor", "middle")
        el.set("font-family", family)
        el.set("font-size",   f"{sz:.1f}")
        el.set("font-weight", weight)
        el.set("fill",        fill)
        el.text = content
        return el

    def add_line(content, cx, y):
        sz = choose_font_size(content, base_t, min_t, avail_t)
        root.append(make_text(content, cx + shadow_off_t, y + shadow_off_t, shadow_color, sz))
        root.append(make_text(content, cx,                y,                main_color,   sz))

    if first:
        add_line(first, cx_t, first_y_t)
    if last:
        add_line(last,  cx_t, last_y_t)

    return root


def write_badge_svg(first: str, last: str, style: dict, out_dir: Path) -> Path:
    root = make_badge_svg(first, last, style)
    ET.indent(root, space="  ")
    safe_name = f"{first}_{last}".strip("_").replace(" ", "_")
    out_path  = out_dir / f"{safe_name}.svg"
    tree = ET.ElementTree(root)
    tree.write(out_path, xml_declaration=True, encoding="UTF-8")
    print(f"  Wrote {out_path}")
    return out_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate individual name-only badge SVGs.")
    parser.add_argument("config",     type=Path, help="Show config YAML")
    parser.add_argument("names_csv",  type=Path, nargs="?", help="CSV of names (default: extra_names.csv beside config, or config's names_csv)")
    args = parser.parse_args()

    if not args.config.exists():
        sys.exit(f"Config not found: {args.config}")

    cfg = load_config(args.config)

    # Resolve names CSV
    if args.names_csv:
        names_path = args.names_csv.resolve()
    else:
        # Try extra_names.csv beside the config first
        candidate = args.config.parent / "extra_names.csv"
        if not candidate.exists():
            candidate = args.config.parent.parent.parent / "extra_names.csv"
        names_path = candidate if candidate.exists() else Path(cfg.get("names_csv", ""))

    if not names_path or not names_path.exists():
        sys.exit(f"Names CSV not found: {names_path}")

    print(f"Loading names: {names_path}")
    names = load_names(names_path)
    print(f"  {len(names)} names loaded")

    out_dir = cfg["output_dir"] / "individual"
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output dir: {out_dir}")

    style = cfg["name_style"]
    for first, last in names:
        write_badge_svg(first, last, style, out_dir)

    print(f"\nDone. {len(names)} SVG(s) written to {out_dir}")


if __name__ == "__main__":
    main()
