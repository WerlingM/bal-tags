Scaffold a new show directory with a config.yaml template.

Usage: /new-show 2027_Wicked
       /new-show 2027_Wicked landscape
       /new-show 2027_Wicked portrait

Show name (and optional orientation): $ARGUMENTS

Steps:
1. Parse the arguments: first token is the show name, second (optional) is orientation (default: landscape)
2. Create the directory: shows/<show-name>/
3. Create shows/<show-name>/config.yaml using the template below
4. Report the directory created and next steps (drop art files in, update front_art/back_art filenames, run /sheets)

Template config.yaml:
```yaml
# Badge sheet config for <show-name>
# Run from the repo root: python3 generate_sheets.py shows/<show-name>/config.yaml

orientation: <orientation>

front_art: ""   # filename of front SVG art (relative to this show directory)
back_art:  ""   # filename of back SVG art, blank name version
names_csv: "../../names.csv"

output_dir: "output"

name_style:
  font_family: "Sour Gummy"
  font_color: "#0194e9"     # blue for student names
  shadow_color: "#000000"   # black shadow
  shadow_offset: 1.370      # art-space units
  font_weight: "normal"
  base_font_size: 24
  min_font_size: 10

  # Name placement in art-coordinate space (badge viewBox 0 0 252 180).
  # Run /analyze-art on the back art SVG to get recommended values.
  name_center_x: 162   # horizontal center aligned to RDP text region
  first_name_y: 110    # baseline y for first name
  last_name_y:  140    # baseline y for last name
```

After creating the files, remind the user to:
- Drop the front and back SVG art files into shows/<show-name>/
- Update front_art and back_art in config.yaml with the actual filenames
- Run /analyze-art on the back art to confirm name_center_x and y positions
- Run /sheets shows/<show-name> to generate the sheets
