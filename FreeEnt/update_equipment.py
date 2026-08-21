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
    0x19 : 0b0000000000010000, # Harps (and the Spoon if -spoon is on)
    0x1A : 0b0000000000100000, # unused (Rosa only) -> used for rosadin
    0x1B : 0b0001000001000000, # Claws
    0x1C : 0b0000001000000000, # Holy Swords and Paladin Armour -> changed by rosadin
    0x1D : 0b0000010000000000, # Hammers/"Wrenches"
    0x1E : 0b0001000000000000, # Katanas/Chakra (e.g. Boomerang), Ninja Shirt
    0x1F : 0b0000000000000000, # Darts (Shuriken/Ninja Star, Spoon if not modified)
}

def equip_table(env):
    # things to check collisions for:
    # - -tweak:rydiaredmage
    # - -tweak:rosadin
    # - -tweak:darkpaladin
    
    equip_table_to_change = {}

    if env.options.flags.has('rydiaredmage'):
        # Adult Rydia gets added to the following table entries:
        # equip table entry 0x04 : shields (sure, she can have Axes on -tweak:rosadin, why not)
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
        env.add_binary(BusAddress(0x0FA550 + 0x02*idx), [equip_table_to_change[idx] & 0x00FF, equip_table_to_change[idx]>>8], as_script=True)

def equipment(env):
    # handle changes to equipment bytes, except for the custom FF4A weapon
    # to consider: -tweak:rosadin, -tweak:darkpaladin, -spoon, wacky flags

    # dictionary with keys = equip IDs, values = dictionaries with keys = byte offsets and values = new byte
    equipment_to_change = {}

    if env.options.flags.has('edward_spoon'):
        # point the Spoon to the Harps equip index
        equipment_to_change.setdefault(0x3E,{}).update({0x06 : 0x19})

    if env.options.flags.has('darkpaladin'):
        dark_sword_index = 0x15
        # make the Ancient Sword a Dark sword, equippable only by DKC/Dark Pally Cecil
        equipment_to_change.setdefault(0x20,{}).update({0x06 : dark_sword_index})
        # env.add_script(f'patch(${0x0F9100 + 0x06 + 0x08 * item_id:06X}) {{{dark_sword_index:02X}}}')
        # change attack powers of weaker Dark swords
        equipment_to_change.setdefault(0x17,{}).update({0x01 : 0x1E}) # Darkness: 20 -> 30
        equipment_to_change.setdefault(0x20,{}).update({0x01 : 0x32}) # Ancient: 35 -> 50
        equipment_to_change.setdefault(0x18,{}).update({0x01 : 0x46}) # Black: 30 -> 70
        # Light/CS become Dark elemental
        for item_id in [0x1A, 0x3F]:
            equipment_to_change.setdefault(item_id,{}).update({0x04 : 0x04})
        # Crystal sword loses undead-hitting
        equipment_to_change.setdefault(0x3F,{}).update({0x05 : 0x00})

        if not 'whatsmygear' in env.meta.get('wacky_challenge',[]):
            equipment_to_change.setdefault(0x1A,{}).update({0x07 : 0x90}) # Str/Wis+3 for Light/Chaos Sword
            equipment_to_change.setdefault(0x3F,{}).update({0x07 : 0xB3}) # Str/Vit/Wis+15 for Crystal/Hades Sword
            for gear_id in [0x64, 0x6C, 0x71, 0x76, 0x85, 0x8C, 0xA0, 0xA6]:
                equipment_to_change.setdefault(gear_id,{}).update({0x07 : 0x10}) # Wis+3 for all Pally/Ancient and Crystal/Hades gear

    elif env.options.flags.has('rosapaladin'):
        holy_sword_index = 0x1A
        non_paladin_shield_index = 0x04
        # reroute Axes to the non-Paladin shields index, so Rosa gets them and PCecil loses them
        # also ensure that Poison/Rune axes are two-handed
        # the Gigant Axe is handled in custom_weapon_rando
        for item_id in [0x38, 0x39, 0x3A, 0x47, 0x48]:
            new_byte = non_paladin_shield_index | (0x20 if item_id >= 0x47 else 0x00)
            equipment_to_change.setdefault(item_id,{}).update({0x06 : new_byte})
        # reroute Holy Swords/Paladin Shields to the normally unused Rosa-only index $1A, so Rosa gets them and PCecil loses them
        if not env.options.flags.has('spoilsmith'):
            # only handle the Legend Sword if custom_weapon_rando isn't
            equipment_to_change.setdefault(0x19,{}).update({0x06 : holy_sword_index})
        for item_id in [0x1A, 0x1B, 0x3F, 0x64, 0x6C]:
            equipment_to_change.setdefault(item_id,{}).update({0x06 : holy_sword_index})

    if 'advertising' in env.meta.get('wacky_challenge',[]):
        # equipment bytes are changed here; hits/element table stuff is changed in apply_advertising
        # Ice weaponry changes, to hit reptiles (Claw, Brand, Spear, Arrows)
        for item_id in [0x02, 0x1D, 0x26, 0x57]:
            equipment_to_change.setdefault(item_id,{}).update({0x05 : 0x04})
        # Bolt weaponry changes, to hit robots (Thunder Rod, Blitz Whip)
        for item_id in [0x0A, 0x35]:
            equipment_to_change.setdefault(item_id,{}).update({0x05 : 0x02})
        # Earth hammer isn't Fire elemental
        equipment_to_change.setdefault(0x4A,{}).update({0x04 : 0x00})
        # Dwarf Axe should hit Air weakness
        equipment_to_change.setdefault(0x39,{}).update({0x04 : 0x06})
        # Drain Spear needs a new element/status entry, for Air/Absorb
        # Note that the forge weapon takes entry 0x3B, so start after that (0x3C)
        equipment_to_change.setdefault(0x29,{}).update({0x04 : 0x3C})
        # Darkness arrows also need a new element/status entry (0x3D), for Dark/Blind
        equipment_to_change.setdefault(0x59,{}).update({0x04 : 0x3E})
        # the Spoon, being a dinner utensil, should be effective against dessert monsters (Slimes)
        equipment_to_change.setdefault(0x3E,{}).update({0x05 : 0x20})
        # ElvenBow gets to actually cast Shell
        equipment_to_change.setdefault(0x51,{}).update({0x03 : 0x06})
        # Lunar gets to actually cast Dspel
        equipment_to_change.setdefault(0x13,{}).update({0x03 : 0x0C})
        # Defense gets to cast Armor
        equipment_to_change.setdefault(0x1E,{}).update({0x03 : 0x05})
        # Murasame gets to cast Slow instead of Armor; thematic with Masamune
        equipment_to_change.setdefault(0x2F,{}).update({0x03 : 0x07})
        # Power staff gets to *cast* Bersk, not just proc it. Need to add its hits data though.
        equipment_to_change.setdefault(0x12,{}).update({0x02 : 0xE3, 0x03 : 0x09})
        # Blitz whip casts Blitz (the Ninja spell, not the enemy spell, as partially busted as that would be). Also needs hits.
        equipment_to_change.setdefault(0x35,{}).update({0x02 : 0xBC, 0x03 : 0x44})
        # Flame whip casts Flame. Also needs... a bit more damage for hits, for balance.
        equipment_to_change.setdefault(0x36,{}).update({0x02 : 0xC1, 0x03 : 0x42})

    if 'fistfight' in env.meta.get('wacky_challenge',[]):
        # change claws to be universally equippable, all other weapons not
        for item_id in range(0x01, 0x60):
            if item_id < 0x07:
                # is claw
                eqp_byte = 0x00
            elif item_id == 0x19 and env.options.flags.has('spoilsmith'): # ignore custom Legend
                eqp_byte = None
            elif item_id not in [0x3E, 0x46]: # ignore Spoon and custom weapon
                eqp_byte = 0x1F
            else:
                eqp_byte = None

            if eqp_byte is not None:
                equipment_to_change.setdefault(item_id,{}).update({0x06 : eqp_byte})

    if not 'whatsmygear' in env.meta.get('wacky_challenge',[]):
        # Black Shirt fix: +3 Wil -> +3 Wis
        equipment_to_change.setdefault(0x91,{}).update({0x07 : 0x11})

    # implement patches to equipment bytes
    for idx in equipment_to_change:
        for offset in equipment_to_change[idx]:
            env.add_binary(BusAddress(0x0F9100 + offset + 0x08 * idx), [equipment_to_change[idx][offset]], as_script=True)