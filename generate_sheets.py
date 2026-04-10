#!/usr/bin/env python3
"""
generate_sheets.py — Build printable badge sheets for Running Dog Productions.

Produces sheet_front.svg plus sheetN_back.svg (25 names per sheet), and
optionally converts each to PDF if inkscape or rsvg-convert is available.

Usage:
    python3 generate_sheets.py <show_config.yaml>
    python3 generate_sheets.py shows/2026_The_Sound_of_Music/config.yaml
"""

import argparse
import csv
import os
import shutil
import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

try:
    import yaml
except ImportError:
    sys.exit("python3-yaml is required: sudo apt install python3-yaml")


# ---------------------------------------------------------------------------
# SVG namespace helpers
# ---------------------------------------------------------------------------

SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"

ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", XLINK_NS)


def svgtag(local):
    return f"{{{SVG_NS}}}{local}"


# ---------------------------------------------------------------------------
# Badge grid geometry
#
# Template: template_5x5_3.5x2.5_landscape.svg
#   Sheet viewBox: 0 0 1712.0001 1224.8  (96 DPI units, ~17.83" × 12.76")
#   Each badge outer rect: 335 × 239 units  (3.49" × 2.49" ≈ 3.5" × 2.5")
#
# Columns (left edge x of outer badge rect):
#   Col 1: x=19   Col 2: x=354  Col 3: x=689  Col 4: x=1024  Col 5: x=1359
#
# Rows (top edge y of outer badge rect):
#   Row 1: y=15.4  Row 2: y=254.4  Row 3: y=493.4  Row 4: y=732.4  Row 5: y=971.4
#
# Slots are numbered left-to-right, top-to-bottom: 0..24
# ---------------------------------------------------------------------------

LANDSCAPE_COLS = [19, 354, 689, 1024, 1359]
LANDSCAPE_ROWS = [15.4, 254.4, 493.4, 732.4, 971.4]
BADGE_W = 335   # outer width in template units
BADGE_H = 239   # outer height in template units

# Art coordinate space for all landscape badge art
ART_W = 252.0
ART_H = 180.0

# Scale factors from art space to template space
ART_SCALE_X = BADGE_W / ART_W   # 335/252 ≈ 1.329
ART_SCALE_Y = BADGE_H / ART_H   # 239/180 ≈ 1.328

# Name placement defaults in art-coordinate space (0 0 252 180).
# The Running Dog Productions logo+text occupies approximately y=23-80.
# Names go below that, centered horizontally across the badge.
# These defaults can be overridden in config.yaml under name_style.
DEFAULT_NAME_CENTER_X = 126.0   # badge center (252/2)
DEFAULT_FIRST_NAME_Y  = 110.0   # baseline for first name line
DEFAULT_LAST_NAME_Y   = 140.0   # baseline for last name line
DEFAULT_NAME_MARGIN   = 10.0    # min horizontal margin from edge (art units)


def badge_slots():
    """Yield (slot_index, x, y) for all 25 badge positions (template units)."""
    idx = 0
    for row_y in LANDSCAPE_ROWS:
        for col_x in LANDSCAPE_COLS:
            yield idx, col_x, row_y
            idx += 1


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------

DEFAULTS = {
    "orientation": "landscape",
    "output_dir": "output",
    "name_style": {
        "font_family": "Georgia, serif",
        "font_color": "#0194e9",
        "shadow_color": "#000000",
        # Shadow offset in art-space units (measured from designer sample: dx=dy=1.370).
        # The shadow is rendered first in shadow_color at this diagonal offset, then
        # the main text is drawn on top in font_color.
        "shadow_offset": 1.370,
        "base_font_size": 20,
        "min_font_size": 10,
        "font_weight": "bold",
        # Art-space coordinates for name placement (0 0 252 180).
        # Adjust these if names land in the wrong spot for a specific badge design.
        "name_center_x": DEFAULT_NAME_CENTER_X,
        "first_name_y":  DEFAULT_FIRST_NAME_Y,
        "last_name_y":   DEFAULT_LAST_NAME_Y,
        "name_margin":   DEFAULT_NAME_MARGIN,
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

    show_dir = config_path.parent
    cfg["show_dir"] = show_dir

    # Resolve relative paths against the show directory
    for key in ("front_art", "back_art", "names_csv"):
        if key in cfg:
            p = Path(cfg[key])
            if not p.is_absolute():
                cfg[key] = (show_dir / p).resolve()

    cfg["output_dir"] = (show_dir / cfg["output_dir"]).resolve()
    return cfg


# ---------------------------------------------------------------------------
# Names loading
# ---------------------------------------------------------------------------

def load_names(csv_path: Path) -> list[tuple[str, str]]:
    """
    Returns list of (first_name, last_name) tuples.
    CSV has a header row; each data row is a full name.
    Names with only one token are stored as (name, "").
    """
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
            first = parts[0]
            last = parts[1] if len(parts) > 1 else ""
            names.append((first, last))
    return names


# ---------------------------------------------------------------------------
# SVG building utilities
# ---------------------------------------------------------------------------

def make_sheet_svg() -> ET.Element:
    """Create a blank sheet SVG with the landscape template dimensions."""
    root = ET.Element(svgtag("svg"))
    root.set("version", "1.1")
    root.set("viewBox", "0 0 1712.0001 1224.8")
    root.set("width", "17.833334in")
    root.set("height", "12.758334in")
    return root


def registration_marks() -> ET.Element:
    """
    Return the Print-Cut Guides group (two crosses) from the landscape template.
    Coordinates match template_5x5_3.5x2.5_landscape.svg exactly.
    """
    g = ET.Element(svgtag("g"))
    g.set("id", "Print-Cut_Guides")

    # Upper-left cross
    ul = ET.SubElement(g, svgtag("g"))
    ul.set("id", "Upper-left_Point")
    h = ET.SubElement(ul, svgtag("line"))
    h.set("stroke", "#f26522"); h.set("stroke-miterlimit", "10"); h.set("fill", "none")
    h.set("x1", "9.5"); h.set("y1", "14.9"); h.set("x2", "27.5"); h.set("y2", "14.9")
    v = ET.SubElement(ul, svgtag("line"))
    v.set("stroke", "#f26522"); v.set("stroke-miterlimit", "10"); v.set("fill", "none")
    v.set("x1", "18.5"); v.set("y1", "5.9"); v.set("x2", "18.5"); v.set("y2", "23.9")

    # Lower-right cross
    lr = ET.SubElement(g, svgtag("g"))
    lr.set("id", "Lower-right_Point")
    h2 = ET.SubElement(lr, svgtag("line"))
    h2.set("stroke", "#f26522"); h2.set("stroke-miterlimit", "10"); h2.set("fill", "none")
    h2.set("x1", "1684.5"); h2.set("y1", "1209.9"); h2.set("x2", "1702.5"); h2.set("y2", "1209.9")
    v2 = ET.SubElement(lr, svgtag("line"))
    v2.set("stroke", "#f26522"); v2.set("stroke-miterlimit", "10"); v2.set("fill", "none")
    v2.set("x1", "1693.5"); v2.set("y1", "1200.9"); v2.set("x2", "1693.5"); v2.set("y2", "1218.9")

    return g


def embed_art(parent: ET.Element, art_path: Path, bx: float, by: float, output_dir: Path) -> None:
    """
    Place badge art as a flat <image> element at (bx, by) in template space.
    art_path is made relative to output_dir so the SVG file is portable.
    """
    rel_path = os.path.relpath(art_path, output_dir)
    img = ET.SubElement(parent, svgtag("image"))
    img.set(f"{{{XLINK_NS}}}href", rel_path)
    img.set("href", rel_path)
    img.set("x", str(bx))
    img.set("y", str(by))
    img.set("width", str(BADGE_W))
    img.set("height", str(BADGE_H))
    img.set("preserveAspectRatio", "xMidYMid meet")


def art_to_template(bx: float, by: float, ax: float, ay: float) -> tuple[float, float]:
    """Convert art-space (ax, ay) to template-space given badge top-left (bx, by)."""
    return bx + ax * ART_SCALE_X, by + ay * ART_SCALE_Y


def choose_font_size(text: str, base_size_t: float, min_size_t: float, available_t: float) -> float:
    """
    Shrink template-space font size until text fits within available_t units wide.
    Uses a rough per-character width estimate.
    """
    size = base_size_t
    while size > min_size_t:
        if size * len(text) * 0.55 <= available_t:
            break
        size -= 1
    return max(size, min_size_t)


def add_name_text(
    parent: ET.Element,
    bx: float,
    by: float,
    first: str,
    last: str,
    style: dict,
) -> None:
    """
    Add first-name and last-name text to the sheet, each rendered as two <text>
    elements: a shadow (offset, dark) drawn first, then the main color on top.
    bx, by are the badge top-left corner in template units.
    """
    ns = style
    # Art-space → template-space for center x and both baselines
    cx_t, first_y_t = art_to_template(bx, by, ns["name_center_x"], ns["first_name_y"])
    _,    last_y_t  = art_to_template(bx, by, ns["name_center_x"], ns["last_name_y"])
    margin_t = ns["name_margin"] * ART_SCALE_X

    # Template-space font sizes
    base_t  = ns["base_font_size"] * ART_SCALE_Y
    min_t   = ns["min_font_size"]  * ART_SCALE_Y
    avail_t = BADGE_W - 2 * margin_t

    main_color   = ns["font_color"]
    shadow_color = ns.get("shadow_color", "#000000")
    # Shadow offset converted to template space (designer sample: dx=dy=1.370 art units)
    shadow_off_t = ns.get("shadow_offset", 1.370) * ART_SCALE_X
    family = ns["font_family"]
    weight = ns.get("font_weight", "bold")

    def make_text(content: str, x_t: float, y_t: float, fill: str, sz: float) -> ET.Element:
        el = ET.Element(svgtag("text"))
        el.set("x", f"{x_t:.2f}")
        el.set("y", f"{y_t:.2f}")
        el.set("text-anchor", "middle")
        el.set("font-family", family)
        el.set("font-size", f"{sz:.1f}")
        el.set("font-weight", weight)
        el.set("fill", fill)
        el.text = content
        return el

    def add_line(content: str, cx: float, y: float) -> None:
        sz = choose_font_size(content, base_t, min_t, avail_t)
        # Shadow drawn first (behind)
        parent.append(make_text(content, cx + shadow_off_t, y + shadow_off_t, shadow_color, sz))
        # Main color on top
        parent.append(make_text(content, cx, y, main_color, sz))

    if first:
        add_line(first, cx_t, first_y_t)
    if last:
        add_line(last, cx_t, last_y_t)


# ---------------------------------------------------------------------------
# Sheet generators
# ---------------------------------------------------------------------------

def generate_front_sheet(cfg: dict) -> Path:
    art_path = cfg["front_art"]
    out_dir = cfg["output_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)

    root = make_sheet_svg()
    art_group = ET.SubElement(root, svgtag("g"))
    art_group.set("id", "Art")

    for _idx, x, y in badge_slots():
        embed_art(art_group, art_path, x, y, out_dir)

    root.append(registration_marks())

    out_path = out_dir / "sheet_front.svg"
    ET.indent(root, space="  ")
    tree = ET.ElementTree(root)
    tree.write(out_path, xml_declaration=True, encoding="UTF-8")
    print(f"  Wrote {out_path}")
    return out_path


def generate_back_sheet(
    cfg: dict,
    names: list[tuple[str, str]],
    sheet_num: int,
) -> Path:
    """
    names: up to 25 (first, last) tuples for this sheet.
    Slots beyond len(names) get art only (no name text) — blanks for reprints.
    """
    art_path = cfg["back_art"]
    out_dir = cfg["output_dir"]
    style = cfg["name_style"]
    out_dir.mkdir(parents=True, exist_ok=True)

    root = make_sheet_svg()
    art_group = ET.SubElement(root, svgtag("g"))
    art_group.set("id", "Art")

    for slot_idx, x, y in badge_slots():
        embed_art(art_group, art_path, x, y, out_dir)
        if slot_idx < len(names):
            first, last = names[slot_idx]
            if first or last:
                add_name_text(art_group, x, y, first, last, style)

    root.append(registration_marks())

    out_path = out_dir / f"sheet{sheet_num}_back.svg"
    ET.indent(root, space="  ")
    tree = ET.ElementTree(root)
    tree.write(out_path, xml_declaration=True, encoding="UTF-8")
    print(f"  Wrote {out_path}")
    return out_path


# ---------------------------------------------------------------------------
# PDF conversion
# ---------------------------------------------------------------------------

def find_pdf_tool() -> tuple[str, list[str]] | None:
    """
    Return (tool_name, command_template) for the first available PDF converter.
    The template uses {svg} and {pdf} as placeholders.
    """
    candidates = [
        ("inkscape",      ["inkscape", "--export-type=pdf", "--export-filename={pdf}", "{svg}"]),
        ("rsvg-convert",  ["rsvg-convert", "-f", "pdf", "-o", "{pdf}", "{svg}"]),
    ]
    for name, cmd in candidates:
        if shutil.which(name):
            return name, cmd

    # Try cairosvg as a Python fallback
    try:
        import cairosvg  # noqa: F401
        return "cairosvg", []
    except ImportError:
        pass

    return None


def svg_to_pdf(svg_path: Path, tool_info) -> Path | None:
    pdf_path = svg_path.with_suffix(".pdf")
    name, cmd_template = tool_info

    if name == "cairosvg":
        import cairosvg
        cairosvg.svg2pdf(url=str(svg_path), write_to=str(pdf_path))
        print(f"  Wrote {pdf_path}")
        return pdf_path

    cmd = [c.format(svg=str(svg_path), pdf=str(pdf_path)) for c in cmd_template]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  WARNING: PDF conversion failed for {svg_path.name}: {result.stderr.strip()}", file=sys.stderr)
        return None
    print(f"  Wrote {pdf_path}")
    return pdf_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate badge print sheets.")
    parser.add_argument("config", type=Path, help="Path to show config YAML")
    parser.add_argument("--no-pdf", action="store_true", help="Skip PDF conversion")
    args = parser.parse_args()

    if not args.config.exists():
        sys.exit(f"Config not found: {args.config}")

    print(f"Loading config: {args.config}")
    cfg = load_config(args.config)

    for key in ("front_art", "back_art", "names_csv"):
        if key not in cfg:
            sys.exit(f"Config missing required key: {key}")
        if not Path(cfg[key]).exists():
            sys.exit(f"File not found ({key}): {cfg[key]}")

    print(f"Loading names: {cfg['names_csv']}")
    names = load_names(cfg["names_csv"])
    print(f"  {len(names)} names loaded")

    pdf_tool = None if args.no_pdf else find_pdf_tool()
    if not args.no_pdf:
        if pdf_tool:
            print(f"PDF conversion: using {pdf_tool[0]}")
        else:
            print(
                "WARNING: No PDF converter found. SVG files only.\n"
                "  Install one of: inkscape, rsvg-convert (librsvg2-bin), or cairosvg"
            )

    svgs = []

    print("\nGenerating front sheet...")
    svgs.append(generate_front_sheet(cfg))

    BATCH = 25
    total_sheets = (len(names) + BATCH - 1) // BATCH
    print(f"\nGenerating {total_sheets} back sheet(s) ({len(names)} names)...")
    for sheet_num in range(1, total_sheets + 1):
        batch = names[(sheet_num - 1) * BATCH : sheet_num * BATCH]
        svgs.append(generate_back_sheet(cfg, batch, sheet_num))

    if pdf_tool:
        print("\nConverting to PDF...")
        for svg_path in svgs:
            svg_to_pdf(svg_path, pdf_tool)

    print(f"\nDone. Output in: {cfg['output_dir']}")


if __name__ == "__main__":
    main()
