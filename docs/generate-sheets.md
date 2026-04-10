# Generating Print Sheets

`generate_sheets.py` builds the printable SVG and PDF sheet files for a show.  It produces one front sheet (identical art on all 25 badge slots) and one back sheet per 25 names (back art with student names overlaid), keeping both SVG and PDF versions of each.

## Requirements

- Python 3.12+
- `python3-yaml` (`sudo apt install python3-yaml`)
- `librsvg2-bin` for PDF export (`sudo apt install librsvg2-bin`)
  - Alternatively: `inkscape` or the `cairosvg` Python package

## Show configuration

Each show needs a `config.yaml` in its show directory.  Example (`shows/2026_The_Sound_of_Music/config.yaml`):

```yaml
orientation: landscape

front_art: "FINAL SoM Bag Tag - (Front).svg"
back_art:  "FINAL 2026 SoM Bag Tag (Back.Blank).svg"
names_csv: "../../names.csv"

output_dir: "output"

name_style:
  font_family: "Sour Gummy"
  font_color:  "#0194e9"     # main name color
  shadow_color: "#000000"    # drop-shadow color
  shadow_offset: 1.370       # diagonal offset in art-space units
  font_weight: "normal"
  base_font_size: 24         # auto-shrinks for long names
  min_font_size:  10

  # Name placement in art-coordinate space (badge viewBox 0 0 252 180).
  # Adjust if names land in the wrong position for a specific badge design.
  name_center_x: 126   # horizontal center
  first_name_y:  110   # baseline y for first name
  last_name_y:   140   # baseline y for last name
```

Paths for `front_art`, `back_art`, and `names_csv` are relative to the show directory.

## Names CSV

The CSV file has a single header row followed by one full name per row:

```
Sound of Music Cast and Crew
Firstname Lastname
Joan Collins
Patrick Stewart
…
```

Names are split on the first space into first and last name, converted to uppercase, and placed on two lines on each badge.

## Running the script

```bash
python3 generate_sheets.py shows/2026_The_Sound_of_Music/config.yaml
```

Output is written to `output/` inside the show directory:

```
shows/2026_The_Sound_of_Music/output/
  sheet_front.svg
  sheet_front.pdf
  sheet1_back.svg
  sheet1_back.pdf
  sheet2_back.svg
  sheet2_back.pdf
  …
```

Pass `--no-pdf` to skip PDF conversion and produce SVG files only.

## Adjusting name position

If names appear too high or too low on the badge after reviewing the output in Inkscape, edit `first_name_y` and `last_name_y` in `config.yaml` and re-run.  These values are in art-coordinate space where the badge height is 180 units (y=0 at top, y=180 at bottom).  For the standard back design the Running Dog Productions logo and text occupy approximately y=23–80, so name values above 80 will overlap that block.
