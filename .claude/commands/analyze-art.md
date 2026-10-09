Analyze a badge SVG art file to extract key measurements for name placement.

Usage: /analyze-art shows/2026_The_Sound_of_Music/back_art.svg

The file to analyze is: $ARGUMENTS

Use lxml to parse the SVG and report:
1. The SVG viewBox dimensions (expected: 0 0 252 180 for standard badges)
2. The bounding box of the dog logo / graphic element (leftmost block)
3. The bounding box of the "RUNNING DOG PRODUCTIONS" text block (rightmost block in the header)
   - Report x_left, x_right, y_top, y_bottom in art-space coordinates
   - Compute the horizontal center: (x_left + x_right) / 2
4. The vertical range occupied by the full logo+text header block
5. Recommended config.yaml values:
   - name_center_x: horizontal center of the text-only portion
   - first_name_y: a y value safely below the header block (header_bottom + 25)
   - last_name_y: first_name_y + 30

To find the text block, look for groups with transform containing a translate near (85, 50) or similar large x offset, which positions content to the right of the logo. Trace the full transform chain from root to each path element and report absolute coordinates.

Also check if there is a sample name already in the file (paths colored with a non-black, non-white fill) — if so, measure its x extent and center as a cross-check.
