from . import databases
from .address import *

# update equipment and equip table entries
# except for the forge item of course which
# happens in custom_weapon_rando.py

CHARS_TO_EQUIP_BIT = {
    'DKCecil' : 0x0,
    'Kain'    : 0x1,
    'CRydia'  : 0x2,
    'Tellah'  : 0x3,
    'Edward'  : 0x4,
    'Rosa'    : 0x5,
    'Yang'    : 0x6,
    'Palom'   : 0x7,
    'Porom'   : 0x8,
    'PCecil'  : 0x9,
    'Cid'     : 0xA,
    'ARydia'  : 0xB,
    'Edge'    : 0xC,
    'FuSoYa'  : 0xD,    
} # "Golbez" and "Anna" are the unused 0xE/0xF index bits

EQUIP_TABLE = {
    0x00 : 0b1111111111111111, # Cursed Ring
    0x01 : 0b0011111111111110, # Clothes/"all" equips like Ribbon/Crystal Ring/Adamant
    0x02 : 0b0010111110110100, # Bows and Arrows
    0x03 : 0b0001111001000010, # Zeus/Strength
    0x04 : 0b0000011000000010, # non-Cecil Shields -> changed by rosadin, rydiaredmage
    0x05 : 0b0001011000000010, # Samurai-ish Armour
    0x06 : 0b0000011000000010, # Axes, Heavy Armour
    0x07 : 0b0000001000000010, # non-Cecil Swords -> changed by rosadin, rydiaredmage
    0x08 : 0b0010101110101100, # All-mage armour
    0x09 : 0b0010100110101100, # unused (all mages and Edward)
    0x0A : 0b0010001100101100, # basic Staves and White Shirt (for WMs/Cecil) -> changed by rydiaredmage
    0x0B : 0b0010000100101100, # White Mage Staves -> changed by rosadin, rydiaredmage
    0x0C : 0b0010100010001100, # Black Mage Rods
    0x0D : 0b0000000000000000, # unused
    0x0E : 0b0000100100100100, # Tiara/Heroine (for female characters)
    0x0F : 0b0000000000000000, # unused
    0x10 : 0b0000000000000000, # reserved for the custom FF4 weapon
    0x11 : 0b0000000000000000, # unused
    0x12 : 0b0000000000000000, # unused
    0x13 : 0b0001101010010110, # Knives -> changed by rosadin
    0x14 : 0b0011100111111100, # Mage Rings
    0x15 : 0b0000000000000001, # DKC swords/shields/armour -> changed by rydiaredmage and darkpaladin
    0x16 : 0b0000000000000010, # Spears
    0x17 : 0b0000100000000100, # Whips
    0x18 : 0b0000000000001000, # unused (Tellah only)
    0x19 : 0b0000000000010000, # Harps -> changed by -spoon
    0x1A : 0b0000000000100000, # unused (Rosa only) -> used for rosadin
    0x1B : 0b0001000001000000, # Claws
    0x1C : 0b0000001000000000, # Holy Swords and Paladin Armour -> changed by rosadin
    0x1D : 0b0000010000000000, # Hammers/"Wrenches"
    0x1E : 0b0001000000000000, # Katanas/Chakra (e.g. Boomerang), Ninja Shirt
    0x1F : 0b0000000000000000, # Darts (Shuriken/Ninja Star, Spoon is modified elsewhere)
}

def equip_table(env):
    # things to check collisions for:
    # - -tweak:rydiaredmage
    # - -tweak:rosadin
    # - -tweak:darkpaladin
    
    equip_table_to_change = {}

    if env.options.flags.has('rydiaredmage'):
        # Adult Rydia gets added to the following table entries:
        # equip table entry 0x04 : shields
        # equip table entry 0x07 : normal swords
        # equip table entry 0x0A/0x0B : white mage armour/staves
        # equip table entry 0x15 : ... *all* DKC gear, including not-swords, heh; it's fine
        arydia_bit = (0x1 << CHARS_TO_EQUIP_BIT['ARydia'])
        for idx in [0x04, 0x07, 0x0A, 0x0B, 0x15]:
            equip_table_to_change[idx] = equip_table_to_change.setdefault(idx, EQUIP_TABLE[idx]) | arydia_bit

    if env.options.flags.has('darkpaladin'):
        # PCecil gets DKC gear; that's all
        pcecil_bit = (0x1 << CHARS_TO_EQUIP_BIT['PCecil'])
        equip_table_to_change[0x15] = equip_table_to_change.setdefault(0x15, EQUIP_TABLE[0x15]) | pcecil_bit

    elif env.options.flags.has('rosapaladin'):
        rosa_bit = (0x1 << CHARS_TO_EQUIP_BIT['Rosa'])
        pcecil_bit = (0x1 << CHARS_TO_EQUIP_BIT['PCecil'])
        # Rosa gets non-Paladin shields, swords, daggers
        # PCecil loses access to all of these equip fields
        for idx in [0x04, 0x07, 0x13]:
            equip_table_to_change[idx] = (equip_table_to_change.setdefault(idx, EQUIP_TABLE[idx]) | rosa_bit) & (0xFFFF ^ pcecil_bit)
        # PCecil gets (real) White Mage staves; Rosa loses access
        equip_table_to_change[0x0B] = (equip_table_to_change.setdefault(0x0B, EQUIP_TABLE[0x0B]) | pcecil_bit) & (0xFFFF ^ rosa_bit)
        # Rosa gaining holy swords/shields and PCecil losing them is managed
        # by changing the equipment data itself, not the equip table
        
    # implement patches to the equip table
    for idx in equip_table_to_change:
        env.add_script(f'patch(${0x0FA550 + 0x02*idx:06X} bus) {{{(equip_table_to_change[idx] & 0x00FF):02X} {(equip_table_to_change[idx]>>8):02X}}}')

def equipment(env):
    # handle changes to equipment bytes, except for the custom FF4A weapon and the Spoon (legacy)
    # to consider: -tweak:rosadin

    if env.options.flags.has('rosapaladin'):
        holy_sword_index = 0x1A
        non_paladin_shield_index = 0x04
        # reroute Axes to the non-Paladin shields index, so Rosa gets them and PCecil loses them
        for item_id in [0x38, 0x39, 0x3A, 0x47, 0x48]:
            new_byte = non_paladin_shield_index | (0x20 if item_id >= 0x47 else 0x00)
            env.add_script(f'patch(${0x0F9100 + 0x06 + 0x08 * item_id}) {{{new_byte:02X}}}')
        # reroute Holy Swords/Paladin Shields to the normally unused Rosa-only index $1A, so Rosa gets them and PCecil loses them
        for item_id in [0x19, 0x1A, 0x1B, 0x3F, 0x64, 0x6C]:
            new_byte = holy_sword_index | (0x20 if item_id != 0x6C else 0x00)
            env.add_script(f'patch(${0x0F9100 + 0x06 + 0x08 * item_id}) {{{new_byte:02X}}}')
