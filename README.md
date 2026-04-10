Break-a-Leg Tags

*Credit to Jason McCoy for the original design and years of supporting the SBHS Running Dog Productions*

During the shows put on by [Running Dog Productions](https://www.sbhstheater.org), the Stone Bridge High School (Loudoun County, VA) theater program, students traditionally get custom printed name tags in the weeks running up to the show.  The tags are printed on 1/8th inch plywood with the show name and design on one side, the student name on the other.  The tags are normally 3 inches by 5 inches, in either portrait or landscape orientation.  

Parent volunteers, who are also members of [Makersmiths](https://www.makersmiths.org/) use the [Roland LEF2-200 UV printer](http://wiki.makersmiths.org/display/MAK/UV+Printer+-+Roland+LEF2-200) to print the design.  The indivdual tags are then cut on the [Thunder Nova 51 laser cutter](http://wiki.makersmiths.org/display/MAK/Laser+-+CO2+-+Thunder+Nova+24+and+51).  While the Nova 51 is needed for cutting the initial sheet to size that can also be done with power tools.  The remainder of the cuts can be done on either laser.  While parent volunteers are not required to be members of Makersmiths the operator of the machine must have the appropriate red-tool training on the machines and signed a waiver.  Cost of operating the machines is much lower for members..

# Materials and Preparation
Start with a full sheet of 1/4 inch plywood.  Better quality plywood such as Birch; standard or builder grade plywood has more knots and voids and will not cut as well.  

Cut the plywood into 4 equal size pieces 48" x 24".  Optionally sand the sheets to remove any rough areas.  

Use the laser to cut the 4 pieces into 39.2" x 12.9" pieces.  Use the [cutting template](BoardCut_39.2x18.5-12.9x18x3.svg) to cut the pieces on the laser.  These individual sheets will fit into the UV printer and hold a 5x5 grid of tags, where the tags are 3.5" x 2.5".

Clean the sheets with isopropyl alcohol to remove any grease or debris that might interfere with printing.

# Art Prep

## Test Print
Test the art on the UV printer using scrap plywood.  No need to do double sided.  This step is to evaluate how well the art prints, what settings are needed.  Work with the designer to resolve any issues.  In particular, white areas can be problematic.  Use standard quality, and set the special printing to use white under print.  Don't print the entire background white, if that is needed then just spray paint the plywood.

## Layout
Each 5x5 grid of tags needs to have 2 layouts, front and back.  These will be printed with registry marks, flipped and printed again, then run through a "print and cut" operation on the laser.

Select which template will be used for the grid based on the orientation of the tags.  The only difference is the location of the slot for the ribbon/clip.
* [template_18x12.9_3.5x2.5x25_landscape.svg](template_18x12.9_3.5x2.5x25_landscape.svg) for landscape - 3.5 long at the top/bottom
* [template_18x12.9_3.5x2.5x25_portrait.svg](template_18x12.9_3.5x2.5x25_portrait.svg) for portrait - 2.5 long at top/bottom

Make a copy of the template as "sheet_front.svg".  Copy the "front" art to each badge area, aligning the art to the center of the badge. If the art is in portrait layout then make sure to rotate properly to fit the template layout.  Remove the outline and clip area lines from the file, we don't need to print those.  DO NOT remove the registration marks (crosses) in either corner, those are required for print/cut operation on the laser.  Save the file as "sheet_front.pdf".

Make a new copy of the template as "sheet1_back.svg".  Copy the "back" art, without student name, to each badge area following the same approach as the front.  Usually the designer provides a version of the back with a sample name and a version without the name.  

At this time we need a list of all students participating in the show.  The list should include cast, crew, and orchestra if it is a musical.  Take the first 25 names from the list and enter one on each badge in the sheet1_back.svg file.  First name should go above the last name.  Match the color and font as closely as possible, it may not always be possible to be exact.  Scale the font to ensure that the student's name fits on the badge without overwriting any art work.  Center the first name and last name on each other, but the alignment on the overall badge is flexible to allow the name to fit around any art.  Save this file as "sheet1_back.pdf"

Repeat creating the back files for the next 25 students as "sheet2_back".  There is no need to have multiple front sheets, as that does not change across badges. Continue creating new sheets until all names are done.  If there are more badges than names on the final sheet then leave the name area blank, we may use that later to print corrections or if there is a new student participating.


# Print 

## Prep
Tape a piece of brown paper to the UV printer bed.  The paper should be a few inches larger than the plywood sheet to give us room.  Auto set the print height, then set the lower right/upper left locations to the size of the paper.  Print the 5x5 badge template without any art, center on the specified print area (or whatever alignment works for you. I prefer chaotic good.)  This will provide guides for placing each piece.  Leave the paper taped down for the duration of the print session.

## Print
Position a sheet of plywood on the outline printed on the paper.  Possibly use a flat magnet at the top and one side of the plywood to make it easier to align future sheets.  Run through setup on the first print; once the positioning setup is done then it should be good for the session unless something gets moved.

Load the PDF for the first sheet, front, and check print settings (Get Dimensions, quality, white printing).  Print.  Flip the art over, make sure to flip left-to-right, not top to bottom.  Flipping top to bottom will make the back upside down.  Print the back for the sheet.

Continue printing front/back of sheets until complete.

# Cut
Cutting uses the 5x5 badge template that matches the layout.  Load the template into Lightburn and set the speed/power for all lines to the appropriate values for the material.

Lay a sheet on the printer.  Try to aling the sheet square to the sides of the beds.  It doesn't have to be perfect, but the straighter it is the faster the cuts will be.  Place flat magnets on the honeycomb along the edges of the board so we can lay the board in the same location every time.  If not then we will need to run the print and cut registration each time.

Perform the print and cut operation to align to the crosses on the corners of the print.

Cut.

Hopefully we now have 25 double sided badges.
