# The goal here is to take the in-game Big Chocobo portrait
# and turn it into a 4x4 (normally it's 2x2), for use with
# the -tweak:chocobosummon flag.
#  
# We need to pull the data, blow it up 200%, and return a
# text file that we can copy into big_chocobo_summon.f4c
# to inject into the ROM.
# 
# The palette data will stay the same, but we need to
# ensure that the correct tile data is supplied and that
# the map data is accurate.

with open("PATH_TO_ROM", "rb") as rom_file:
    rom_file.seek(0x0df200)
    big_choco_data = rom_file.read(384)

# For each 24 bytes in big_choco_data (one 8x8 tile),
# create four 8x8 tiles by doubling the pixel data
# in width and in height. We'll deal with fine-tuning later.

big_choco_data_ints = [int(b) for b in big_choco_data]
tiles_data = [big_choco_data_ints[24*i:24*i+24] for i in range(16)]
new_tiles_data = []
new_tilemap_data = [[]] * 8

for tile in tiles_data:
    bp12 = tile[:16]
    bp3 = tile[16:]

    new_t00 = [] # top-left
    new_t01 = [] # top-right
    new_t10 = [] # bottom-left
    new_t11 = [] # bottom-right

    # handle the first four rows of the original tile, to get the top two tiles
    for i in range(len(bp12) // 4):
        up_nib0 = (bp12[2*i] >> 4) & 0x0F
        t0r0bp1 = 0
        for j in range(4):
            t0r0bp1 += ((up_nib0 & (1 << j)) << j) + ((up_nib0 & (1 << j)) << j+1)        
        
        up_nib1 = (bp12[2*i+1] >> 4) & 0x0F
        t0r0bp2 = 0
        for j in range(4):
            t0r0bp2 += ((up_nib1 & (1 << j)) << j) + ((up_nib1 & (1 << j)) << j+1) 

        # the next two rows of the top-left tile are described by these bytes
        new_t00.extend([t0r0bp1, t0r0bp2, t0r0bp1, t0r0bp2])

        lo_nib0 = bp12[2*i] & 0x0F
        t1r0bp1 = 0
        for j in range(4):
            t1r0bp1 += ((lo_nib0 & (1 << j)) << j) + ((lo_nib0 & (1 << j)) << j+1)

        lo_nib1 = bp12[2*i+1] & 0x0F
        t1r0bp2 = 0
        for j in range(4):
            t1r0bp2 += ((lo_nib1 & (1 << j)) << j) + ((lo_nib1 & (1 << j)) << j+1)

        # the next two rows of the top-right tile are described by these bytes
        new_t01.extend([t1r0bp1, t1r0bp2, t1r0bp1, t1r0bp2])

    # handle the next four rows of the original tile, to get the bottom two tiles
    for i in range(4,4+(len(bp12) // 4)):
        up_nib0 = (bp12[2*i] >> 4) & 0x0F
        t0r0bp1 = 0
        for j in range(4):
            t0r0bp1 += ((up_nib0 & (1 << j)) << j) + ((up_nib0 & (1 << j)) << j+1) 
        
        up_nib1 = (bp12[2*i+1] >> 4) & 0x0F
        t0r0bp2 = 0
        for j in range(4):
            t0r0bp2 += ((up_nib1 & (1 << j)) << j) + ((up_nib1 & (1 << j)) << j+1) 

        # the next two rows of the bottom-left tile are described by these bytes
        new_t10.extend([t0r0bp1, t0r0bp2, t0r0bp1, t0r0bp2])

        lo_nib0 = bp12[2*i] & 0x0F
        t1r0bp1 = 0
        for j in range(4):
            t1r0bp1 += ((lo_nib0 & (1 << j)) << j) + ((lo_nib0 & (1 << j)) << j+1)

        lo_nib1 = bp12[2*i+1] & 0x0F
        t1r0bp2 = 0
        for j in range(4):
            t1r0bp2 += ((lo_nib1 & (1 << j)) << j) + ((lo_nib1 & (1 << j)) << j+1)

        # the next two rows of the bottom-right tile are described by these bytes
        new_t11.extend([t1r0bp1, t1r0bp2, t1r0bp1, t1r0bp2])

    # handle the first half of bitplane 3, for the top two tiles
    for b in bp3[:4]:
        up_nib = (b >> 4) & 0x0F
        lo_nib = b & 0x0F

        r00 = 0
        for j in range(4):
            r00 += ((up_nib & (1 << j)) << j) + ((up_nib & (1 << j)) << j+1)

        r01 = 0
        for j in range(4):
            r01 += ((lo_nib & (1 << j)) << j) + ((lo_nib & (1 << j)) << j+1)

        new_t00.extend([r00,r00])
        new_t01.extend([r01,r01])

    # handle the second half of bitplane 3, for the bottom two tiles
    for b in bp3[4:]:
        up_nib = (b >> 4) & 0x0F
        lo_nib = b & 0x0F

        r10 = 0
        for j in range(4):
            r10 += ((up_nib & (1 << j)) << j) + ((up_nib & (1 << j)) << j+1)

        r11 = 0
        for j in range(4):
            r11 += ((lo_nib & (1 << j)) << j) + ((lo_nib & (1 << j)) << j+1)

        new_t10.extend([r10,r10])
        new_t11.extend([r11,r11])

    new_tiles_data.extend(new_t00)
    new_tiles_data.extend(new_t01)
    new_tiles_data.extend(new_t10)
    new_tiles_data.extend(new_t11)

# add to tilemap data so we don't have to manually write it
# ... or not. 

print(new_tiles_data)

# write the output to a text file, which we'll paste into an f4c file
with open("big_big_chocobo_data.txt", "w") as outfile:
    outfile.write(" \n".join([" ".join([f"{b:02X}" for b in new_tiles_data[24*i:24*(i+1)]]) for i in range(64)]))