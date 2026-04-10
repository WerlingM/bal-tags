# Art Prep

## Test Print

Test the art on the UV printer using scrap plywood.  No need to do double sided.  This step is to evaluate how well the art prints, what settings are needed.  Work with the designer to resolve any issues.  In particular, white areas can be problematic.  Use standard quality, and set the special printing to use white under print.  Don't print the entire background white, if that is needed then just spray paint the plywood.

## Layout

Each 5x5 grid of tags needs to have 2 layouts, front and back.  These will be printed with registry marks, flipped and printed again, then run through a "print and cut" operation on the laser.

[template_5x5_3.5x2.5_all.svg](../template_5x5_3.5x2.5_all.svg) is the layout sized to fit the UV printer with all lanyard holes for portrait and landscape layout, for reference.  Work with the designer to determine the orientation and choose the corresponding landscape or portrait base; those have removed the unused lanyard holes.

### Generating the print sheets

Use `generate_sheets.py` to build the front and back PDFs automatically.  See [Generating print sheets](generate-sheets.md) for setup and usage.  The script produces:

- `sheet_front.pdf` — front art repeated across all 25 badge slots
- `sheet1_back.pdf`, `sheet2_back.pdf`, … — back art with student names, 25 per sheet

### Manual layout (if not using the script)

Make a copy of the template as "sheet_front.svg".  Copy the "front" art to each badge area, aligning the art to the center of the badge.  If the art is in portrait layout then make sure to rotate properly to fit the template layout.  Remove the outline and clip area lines from the file, we don't need to print those.  DO NOT remove the registration marks (crosses) in either corner, those are required for print/cut operation on the laser.  Save the file as "sheet_front.pdf".

Make a new copy of the template as "sheet1_back.svg".  Copy the "back" art, without student name, to each badge area following the same approach as the front.  Usually the designer provides a version of the back with a sample name and a version without the name.

At this time we need a list of all students participating in the show.  The list should include cast, crew, and orchestra if it is a musical.  Take the first 25 names from the list and enter one on each badge in the sheet1_back.svg file.  First name should go above the last name.  Match the color and font as closely as possible, it may not always be possible to be exact.  Scale the font to ensure that the student's name fits on the badge without overwriting any art work.  Match the color and any embellishments like shadowing.  Center the first name and last name on each other, but the alignment on the overall badge is flexible to allow the name to fit around any art.  Save this file as "sheet1_back.pdf".

Repeat creating the back files for the next 25 students as "sheet2_back".  There is no need to have multiple front sheets, as that does not change across badges.  Continue creating new sheets until all names are done.  If there are more badges than names on the final sheet then leave the name area blank, we may use that later to print corrections or if there is a new student participating.
