![The Enterprise template](/static/enterprise_template.png){: style="width: 832px; image-rendering: pixelated;" }

# Editing the little block in the lower right (The palette)
The template is a 104 x 16 pixel PNG, and the little block of colored squares in its bottom-right corner is the sprite's palette (the only colors your Enterprise can use). It holds 16 colors as 2 x 2 squares, numbered left to right and top to bottom, so the top row is colors 0-3 and the bottom row is colors 12-15. Color 0, the bright purple, is the transparent color: anything painted in it is see-through in the game. 

Colors 1-7 are shared with the hovercraft, ship, yellow chocobo, tanks and the vehicles' shadows, so changing them recolors those as well. Colors 8-15 belong to the Enterprise alone, which makes them the best place for your own colors. To change a color, repaint its whole square. The 8 x 8 area above the palette isn't used.

# Editing the sprite itself
The rest of the image is six 16 x 16 frames, from left to right: facing down (two frames), facing up (two frames) and facing left (two frames). The two frames of each direction alternate as the propeller spins. The game makes the right-facing frames by mirroring the left ones, so draw them to look right when flipped. Paint each frame with a pencil tool, one pixel at a time, and leave the background bright purple wherever the ship shouldn't be. Every pixel must be exactly one of the palette's colors: brushes, soft edges, smoothing and resizing all blend in new colors, and the page will reject the image and point to the first pixel that doesn't match. 

The SNES can't show every color, so colors are rounded down to the nearest multiple of 8 in each of red, green and blue (`rgb(153, 80, 68)` becomes `rgb(152, 80, 64)`); picking values that are already multiples of 8 means you see exactly what you get. Save the result as a PNG at its original 104 x 16 size.

