import os
from . import databases
from .rewards import RewardSlot, ItemReward
from .spoilers import SpoilerRow
from .address import *
from .errors import BuildError

CUSTOM_WEAPON_ITEM_ID = 0x46  # Dummy Crystal sword
CUSTOM_WEAPON_ITEM_CONST = '#item.fe_CustomWeapon'
CUSTOM_WEAPON_EQUIP_TABLE_INDEX = 0x10
CUSTOM_WEAPON_ELEMENT_TABLE_INDEX = 0x3B

CUSTOM_LEGEND_ITEM_ID = 0x19  # still the Legend Sword, #item.Legend, use the Custom Weapon's equip table index 0x10
CUSTOM_LEGEND_ELEMENT_TABLE_INDEX = 0x3E # 0x3C and 0x3D are used for -wacky:advertising
CUSTOM_WEAPON_TO_LEGEND = {
    0x101 : 0x201, # holy swords
    0x102 : 0x201,
    0x103 : 0x201,
    0x104 : 0x202, # sword
    0x105 : 0x203, # spear
    0x106 : 0x204, # axe
    0x107 : 0x205, # bow
    0x108 : 0x206, # arrow
    0x109 : 0x207, # whip
    0x10A : 0x208, # dagger
    0x10B : 0x209, # katanas
    0x10C : 0x209,
    0x10D : 0x20A, # shuriken
    0x10E : 0x20B, # boomerang
    0x10F : 0x20C, # claws
    0x110 : 0x20C,
    0x111 : 0x20C,
    0x112 : 0x20D, # wrenches
    0x113 : 0x20D,
    0x114 : 0x20E, # rod
    0x115 : 0x20F, # staves
    0x116 : 0x20F,
    0x117 : 0x210, # harps
    0x118 : 0x210,
    0x119 : 0x210,
}
CUSTOM_LEGEND_GENERIC_NAME_ICON = {
    0x201 : ['sword', 0x2E],
    0x202 : ['sword', 0x2D],
    0x203 : ['spear', 0x2F], 
    0x204 : ['axe', 0x34],
    0x205 : ['bow', 0x37],
    0x206 : ['arrow', 0x38],
    0x207 : ['whip', 0x3A],
    0x208 : ['dagger', 0x30],
    0x209 : ['katana', 0x31],
    0x20A : ['shuriken', 0x32],
    0x20B : ['chakram', 0x33], # 'boomerang' is too long to sub in-place in the textbox
    0x20C : ['claw', 0x29],
    0x20D : ['hammer', 0x35], # replace 0x35 with 0x39 on Truth in Advertising
    0x20E : ['rod', 0x2A],
    0x20F : ['staff', 0x2B],
    0x210 : ['harp', 0x36]
}

# Lightbringer, Piggy Stick, Abel's Lance, Gigant Axe, Perseus Bow, Perseus Arrow, Mist Whip, Sasuke Katana, Mutsunokami, Rising Sun, Tiger Claw, Dragon Claw, Godhand, Thor's Hammer, Fiery Hammer, Nirvana, Apollo Harp, Loki's Lute
GOOD_CUSTOM_WEAPONS = [0x103, 0x104, 0x105, 0x106, 0x107, 0x108, 0x109, 0x10B, 0x10C, 0x10E, 0x10F, 0x110, 0x111, 0x112, 0x113, 0x116, 0x117, 0x118, 0x119]
# Adamant, CS, Excal, Avenger, MoonVeil, Dragoon Spear, Arty Arrows, Masamune, White Shirt
ORDERED_GOOD_ALT_ITEMS = [0x9A, 0x3F, 0x1B, 0x4C, 0xC5, 0x27, 0x5F, 0x30, 0x93]

_CAST_TABLE = {
    'White' : 0x0B,
    'Weak' : 0x27,
    'Flood' : 0x43,
    'Blink' : 0x04,
    'Blitz' : 0x44,
    'Nuke' : 0x30,
    'Heal' : 0x12,
    'Wall' : 0x0A,
    'Fatal' : 0x2B,
    'Stop' : 0x2C,
    'Cure2' : 0x0F,
    'Virus' : 0x26,
    'Float' : 0x18,
}

_EQUIP = ['dkcecil', 'kain', 'crydia', 'tellah', 'edward', 'rosa', 'yang', 'palom', 'porom', 'pcecil', 'cid', 'arydia', 'edge', 'fusoya']
_ELEMENTS = ['fire', 'ice', 'lightning', 'dark', 'holy', 'air', 'drain', 'immune', 'poison', 'blind', 'mute', 'piggy', 'mini', 'toad', 'stone', 'swoon', 'calcify1', 'calcify2', 'berserk', 'charm', 'sleep', 'paralyze', 'float', 'curse']
_RACES = ['dragons', 'robots', 'reptiles', 'spirits', 'giants', 'slimes', 'mages', 'undead']

_PLUS_STATS = [3, 5, 10, 15, 5, 10, 15, 5]
_MINUS_STATS = [0, 0, 0, 0, -5, -10, -15, -10]
_PLUS_MINUS_PAIRS = list(zip(_PLUS_STATS, _MINUS_STATS))

_CHARACTER_TO_USERS = {
    'cecil' : ['dkcecil', 'pcecil'],
    'rydia' : ['crydia', 'arydia']
}

def _is_user(cw, character):
    return bool(set(cw.equip + cw.use).intersection(set(_CHARACTER_TO_USERS.get(character, [character]))))

# check for multiple users and not just one; characters is an iterable
def _are_users(cw, characters):
    users_set = set()
    for ch in characters:
        users_set = users_set.union(set(_CHARACTER_TO_USERS.get(ch, [ch])))
    return bool(set(cw.equip + cw.use).intersection(users_set))

def _expand_chars_to_jobs(characters):
    jobs = set()
    for ch in characters:
        jobs.update(set(_CHARACTER_TO_USERS.get(ch, [ch])))
    return jobs

def _calculate_stats_byte(*stats):
    # stats is in the order: STR, AGI, VIT, WIS, WIL
    plus_bonus = 0
    minus_bonus = 0

    def raise_error():
        raise BuildError(f"Cannot represent stats bonus: " + str(stats))

    all_minus = True
    for stat in stats:
        if stat > 0:
            if plus_bonus not in (0, plus_bonus) or stat not in _PLUS_STATS:
                raise_error()
            plus_bonus = stat
            all_minus = False
        elif stat < 0:
            if minus_bonus not in (0, minus_bonus) or stat not in _MINUS_STATS:
                raise_error()
            minus_bonus = stat

    pair = (plus_bonus, minus_bonus)
    if (pair == (0,0)):
        return 0x00

    if all_minus:
        stats_byte = _MINUS_STATS.index(minus_bonus)
    else:
        if pair not in _PLUS_MINUS_PAIRS:
            raise_error()
            
        stats_byte = _PLUS_MINUS_PAIRS.index(pair)

    for i,stat in enumerate(stats):
        bit_index = 7 - i
        if stat > 0:
            stats_byte |= (1 << bit_index)

    return stats_byte



def apply(env):
    custom_weapon = None
    if env.options.flags.has('key_item_from_forge'):
        pass # do nothing, since we'll overwrite the key item otherwise
    elif 'custom_weapon' in env.options.test_settings:
        custom_weapon = databases.get_custom_weapons_dbview().find_one(lambda cw: env.options.test_settings['custom_weapon'].lower() in f"{cw.name}|{cw.spoilername}".lower())
    elif env.options.flags.has('hero_challenge') or env.options.flags.has('superhero_challenge'):
        # you should expect to get a weapon associated to your hero, regardless of anything else
        weapons_dbview = databases.get_custom_weapons_dbview()
        if env.options.flags.has('goodsmith'):
            if env.meta['starting_character'] not in ['palom', 'fusoya']:
                # Palom and Fu do not have "good" custom weapons, per the list above
                weapons_dbview.refine(lambda cw: cw.id in GOOD_CUSTOM_WEAPONS)
        available_weapons = weapons_dbview.find_all(lambda cw: not cw.disabled and _is_user(cw, env.meta['starting_character']))
        custom_weapon = env.rnd.choice(available_weapons)
    elif env.options.flags.has('supersmith'):
        weapons_dbview = databases.get_custom_weapons_dbview()
        if 'omnidextrous' in env.meta.get('wacky_challenge',[]) or env.options.flags.has('omnismith'):
            if env.options.flags.has('goodsmith'):
                # Perseus bow/arrow aren't good on Omnidex/when you can't necessarily equip the other required item.
                weapons_dbview.refine(lambda cw: cw.id in GOOD_CUSTOM_WEAPONS and not cw.id in [0x107, 0x108])
        elif 'fistfight' in env.meta.get('wacky_challenge',[]):
            if env.options.flags.has_any('playablesmith', 'goodsmith'):
                # all of the Claws are considered good
                weapons_dbview.refine(lambda cw: _is_user(cw, 'yang'))
        else:
            if env.options.flags.has_any('playablesmith', 'goodsmith'):
                weapons_dbview.refine(lambda cw: _are_users(cw, env.meta['available_characters']))
                if env.options.flags.has('goodsmith') and not set(env.meta['available_characters']).issubset(set(['palom', 'fusoya'])):
                    weapons_dbview.refine(lambda cw: cw.id in GOOD_CUSTOM_WEAPONS)
        available_weapons = weapons_dbview.find_all(lambda cw: not cw.disabled)
        custom_weapon = env.rnd.choice(available_weapons)
    elif env.options.flags.has('altsmith'):
        items_dbview = databases.get_items_dbview()
        # to match the Pink Tail turn-in reward, also restrict the MoonVeil if Tno:j is on
        if env.options.flags.has('treasure_no_j_items'):
            items_dbview.refine(lambda it: not it.j)
        if env.options.flags.has('no_adamants'):
            items_dbview.refine(lambda it: it.const != '#item.AdamantArmor')
        if env.options.flags.has_any('playablesmith', 'goodsmith') and not 'omnidextrous' in env.meta.get('wacky_challenge',[]):
            # alt smith item can't be a MoonVeil if Tno:j is on! So restricting to Yang-only without Adamants would be bad; don't restrict in that case.
            # also, all of these items *are* good, even the White Shirt. Have you looked at its defensive stats recently?
            if not (env.options.flags.has('no_adamants') and env.options.flags.has('treasure_no_j_items') 
                    and (env.meta['available_characters'].issubset(set(['yang'])) or 'fistfight' in env.meta.get('wacky_challenge',[]))):
                items_dbview.refine(lambda it: it.category == 'item' or not set(it.equip).isdisjoint(_expand_chars_to_jobs(env.meta['available_characters'])))
        items = items_dbview.find_all(lambda it: it.tier in [7, 8])
        if env.options.flags.has('goodsmith'):
            # if we want "good" items, take the best according to the list above (we've already guaranteed there's something available)
            smith_reward = None
            for desired_item in ORDERED_GOOD_ALT_ITEMS:
                for it in items:
                    if it.code == desired_item:
                        smith_reward = it
                        break
                if smith_reward:
                    break
        else:
            smith_reward = env.rnd.choice(items)
        env.meta['rewards_assignment'][RewardSlot.forge_item] = ItemReward(smith_reward.const)
        env.spoilers.add_table("MISC", [SpoilerRow("Smithy item", smith_reward.spoilername, obscurable=True)],
            public=env.options.flags.has_any('-spoil:all', '-spoil:misc'))
    else: 
        env.meta['rewards_assignment'][RewardSlot.forge_item] = ItemReward('#item.Excalibur')

    if custom_weapon is None:
        env.add_substitution('custom weapon enabled', '')
        return

    if custom_weapon.id == 0x103 and env.options.flags.has('darkpaladin'):
        custom_weapon.name = '[darksword]Bringer'
        custom_weapon.spoilername = 'Deathbringer'
        custom_weapon.elements = ['dark']
        custom_weapon.cast = 'Fatal'
        custom_weapon.spellpower = 8
        custom_weapon.dragons = 'y'
        custom_weapon.spirits = ''
        custom_weapon.undead = ''
        custom_weapon.anim0 = 0x1C # Black Sword palette

    if custom_weapon.id == 0x106 and env.options.flags.has('rosapaladin'):
        custom_weapon.equip = ['kain', 'rosa', 'cid']

    if 'advertising' in env.meta.get('wacky_challenge',[]):
        if custom_weapon.id == 0x106:
            custom_weapon.giants = 'y'
        elif custom_weapon.id in [0x112, 0x113]:
            custom_weapon.name = '[hammer]' + custom_weapon.name[8:]

    # write item name
    env.add_script(f'text(item name ${CUSTOM_WEAPON_ITEM_ID:02X}) {{{custom_weapon.name}}}')

    # if necessary, alter the item price to make it worth selling
    env.meta.setdefault('altered_item_prices',{}).update({CUSTOM_WEAPON_ITEM_ID : custom_weapon.price})

    # write 8-byte equipment record
    gear_bytes = [0x00] * 8

    if custom_weapon.metallic:
        gear_bytes[0] |= 0x80
    if custom_weapon.throwable:
        gear_bytes[0] |= 0x40
    if custom_weapon.longrange:
        gear_bytes[0] |= 0x20
    
    gear_bytes[1] = custom_weapon.attack
    gear_bytes[2] = custom_weapon.accuracy
    gear_bytes[3] = _CAST_TABLE.get(custom_weapon.cast, 0x00)
    gear_bytes[4] = CUSTOM_WEAPON_ELEMENT_TABLE_INDEX
    
    for i,race in enumerate(_RACES):
        if getattr(custom_weapon, race):
            gear_bytes[5] |= (1 << i)
    
    gear_bytes[6] = CUSTOM_WEAPON_EQUIP_TABLE_INDEX
    if custom_weapon.twohanded:
        gear_bytes[6] |= 0x20
    if custom_weapon.arrow:
        gear_bytes[6] |= 0x40
    if custom_weapon.bow:
        gear_bytes[6] |= 0x80
    
    if 'whatsmygear' in env.meta.get('wacky_challenge',[]):
        # can't double-patch the weapon, so patch only the first seven bytes and leave the eighth for the wacky to handle
        env.add_binary(UnheaderedAddress(0x79100 + CUSTOM_WEAPON_ITEM_ID * 0x08), gear_bytes[0:7], as_script=True)
    else:
        gear_bytes[7] = _calculate_stats_byte(custom_weapon.str, custom_weapon.agi, custom_weapon.vit, custom_weapon.wis, custom_weapon.wil)
        env.add_binary(UnheaderedAddress(0x79100 + CUSTOM_WEAPON_ITEM_ID * 0x08), gear_bytes, as_script=True)

    # write spell data
    env.add_binary(UnheaderedAddress(0x79070 + CUSTOM_WEAPON_ITEM_ID), [custom_weapon.spellpower], as_script=True)
    env.add_binary(UnheaderedAddress(0x7D4E0 + CUSTOM_WEAPON_ITEM_ID), [_CAST_TABLE.get(custom_weapon.cast, 0x00)], as_script=True)

    # write animation data
    env.add_binary(UnheaderedAddress(0x79E10 + CUSTOM_WEAPON_ITEM_ID * 0x04), [custom_weapon.anim0, custom_weapon.anim1, custom_weapon.anim2, custom_weapon.anim3], as_script=True)

    # write equip table entry
    equip_value = 0x0000
    if env.options.flags.has('omnismith'):
        users_set = set()
        for ch in env.meta['available_characters']:
            users_set = users_set.union(set(_CHARACTER_TO_USERS.get(ch, [ch])))
    else:
        users_set = set(custom_weapon.equip)
    for i,job in enumerate(_EQUIP):
        if job in users_set:
            equip_value |= (1 << i)
    env.add_binary(UnheaderedAddress(0x7A550 + CUSTOM_WEAPON_EQUIP_TABLE_INDEX * 0x02), [equip_value & 0xFF, (equip_value >> 8) & 0xFF], as_script=True)

    # write element table entry
    element_value = 0x000000
    for i,elem in enumerate(_ELEMENTS):
        if elem in custom_weapon.elements:
            element_value |= (1 << i)
    env.add_binary(UnheaderedAddress(0x7A590 + CUSTOM_WEAPON_ELEMENT_TABLE_INDEX * 0x03), [element_value & 0xFF, (element_value >> 8) & 0xFF, (element_value >> 16) & 0xFF], as_script=True)

    # set override item description
    if custom_weapon.id == 0x103 and env.options.flags.has('darkpaladin'):
        with open(os.path.join(os.path.dirname(__file__), 'assets', 'item_info', f'dp_custom_weapon_{custom_weapon.id:X}_description.bin'), 'rb') as infile:
            description_data = infile.read()
    elif custom_weapon.id in [0x106, 0x112, 0x113] and 'advertising' in env.meta.get('wacky_challenge',[]):
        with open(os.path.join(os.path.dirname(__file__), 'assets', 'item_info', f'advertising_custom_weapon_{custom_weapon.id:X}_description.bin'), 'rb') as infile:
            description_data = infile.read()
    else: 
        with open(os.path.join(os.path.dirname(__file__), 'assets', 'item_info', f'custom_weapon_{custom_weapon.id:X}_description.bin'), 'rb') as infile:
            description_data = infile.read()
    env.meta.setdefault('item_description_overrides', {})[CUSTOM_WEAPON_ITEM_ID] = description_data

    # write proxy item value
    env.add_script(f'patch ($21f0f8 bus) {{ {custom_weapon.proxy} }}')

    # add needed script
    env.add_file(f'scripts/custom_weapon_support.f4c')

    # assign to smith
    env.meta['rewards_assignment'][RewardSlot.forge_item] = ItemReward(CUSTOM_WEAPON_ITEM_CONST)

    # spoiler
    env.spoilers.add_table("MISC", [SpoilerRow("Supersmith weapon", custom_weapon.spoilername, obscurable=True)],
        public=env.options.flags.has_any('-spoil:all', '-spoil:misc'))

    # for -smith:superspoiler, we need to update the Legend Sword to have many of the same properties, including animations/etc.
    # also override the word "sword" with the correct weapon type if necessary
    # animation note: palette (colours!), weapon_sprite (the thing your character is holding), effect_sprite (), effect; table for weapons is at $0F9E10
    # -- go with holy palette 0x20, tailored weapon_sprite per type, similar effect_sprite per type, and effect routine
    if env.options.flags.has('spoilsmith'):
        custom_legend = databases.get_custom_legend_dbview().find_one(lambda cl : cl.id == CUSTOM_WEAPON_TO_LEGEND[custom_weapon.id])

        if custom_weapon.id == 0x103 and env.options.flags.has('darkpaladin'):
            custom_legend.name = '[darksword]Legend'
            custom_legend.elements = ['holy', 'dark', 'poison']
            custom_legend.anim1 = 0x06
            custom_legend.anim2 = 0x03
            custom_legend.proxy = '#item.BlackSword'
        elif custom_legend.id == 0x201:
            # making no changes if it's a holy sword
            return 

        # replace [wrench] with [hammer] on Truth in Advertising and update Tracker menu icon
        if custom_legend.id == 0x20D and 'advertising' in env.meta.get('wacky_challenge', []):
            custom_legend.name = '[hammer]Legend'
            env.add_substitution('legend icon', '0x39')
        else:
            env.add_substitution('legend icon', f'#${CUSTOM_LEGEND_GENERIC_NAME_ICON[custom_legend.id][1]:02X}')

        # write item name
        env.add_script(f'text(item name ${CUSTOM_LEGEND_ITEM_ID:02X}) {{{custom_legend.name}}}')
        # change smithy textboxes
        env.add_substitution('legend generic name', CUSTOM_LEGEND_GENERIC_NAME_ICON[custom_legend.id][0])
        env.add_substitution('legend weapon name', custom_legend.name)

        # change required equipment bytes: $00 (metallic bit 7/long-range bit 5), sometimes $03 (spell), $04 (elem/status, always 0x3C), $05 (trait weakness), $06 (bow bit 7, arrow bit 6, two-handed bit 5, equip index bits 0-4)
        legend_bytes = [0x80, 0x28, 0x63, 
                        _CAST_TABLE.get(custom_legend.cast, 0x00), 
                        CUSTOM_LEGEND_ELEMENT_TABLE_INDEX, 
                        0x00, CUSTOM_WEAPON_EQUIP_TABLE_INDEX, 0x08]

        if custom_legend.longrange:
            legend_bytes[0] |= 0x20
        for i,race in enumerate(_RACES):
            if getattr(custom_legend, race):
                legend_bytes[5] |= (1 << i)
        if custom_legend.bow:
            legend_bytes[6] |= 0x80
        if custom_legend.arrow:
            legend_bytes[6] |= 0x40
        if custom_legend.twohanded:
            legend_bytes[6] |= 0x20

        # don't need to patch the stats byte, to save What's My Gear Again? effort
        env.add_binary(UnheaderedAddress(0x79100 + CUSTOM_LEGEND_ITEM_ID * 0x08), legend_bytes[0:7], as_script=True)

        # write spell data
        env.add_binary(UnheaderedAddress(0x79070 + CUSTOM_LEGEND_ITEM_ID), [custom_legend.spellpower], as_script=True)
        env.add_binary(UnheaderedAddress(0x7D4E0 + CUSTOM_LEGEND_ITEM_ID), [_CAST_TABLE.get(custom_legend.cast, 0x00)], as_script=True)

        # write animation data
        env.add_binary(UnheaderedAddress(0x79E10 + CUSTOM_LEGEND_ITEM_ID * 0x04), [custom_legend.anim0, custom_legend.anim1, custom_legend.anim2, custom_legend.anim3], as_script=True)

        # write element table entry
        legend_element_value = 0x000000
        for i,elem in enumerate(_ELEMENTS):
            if elem in custom_legend.elements:
                legend_element_value |= (1 << i)
        env.add_binary(UnheaderedAddress(0x7A590 + CUSTOM_LEGEND_ELEMENT_TABLE_INDEX * 0x03), [legend_element_value & 0xFF, (legend_element_value >> 8) & 0xFF, (legend_element_value >> 16) & 0xFF], as_script=True)

        # set override item description; unfortunately, we need to modify the description no matter what, due to weapon properties.
        if custom_weapon.id == 0x103 and env.options.flags.has('darkpaladin'):
            with open(os.path.join(os.path.dirname(__file__), 'assets', 'item_info', f'dp_custom_legend_{custom_legend.id:X}_description.bin'), 'rb') as infile:
                description_data = infile.read()
        elif custom_legend.id == 0x20D and 'advertising' in env.meta.get('wacky_challenge',[]):
            with open(os.path.join(os.path.dirname(__file__), 'assets', 'item_info', f'advertising_custom_legend_{custom_legend.id:X}_description.bin'), 'rb') as infile:
                description_data = infile.read()
        else: 
            with open(os.path.join(os.path.dirname(__file__), 'assets', 'item_info', f'custom_legend_{custom_legend.id:X}_description.bin'), 'rb') as infile:
                description_data = infile.read()
        env.meta.setdefault('item_description_overrides', {})[CUSTOM_LEGEND_ITEM_ID] = description_data

        # add protection from losing the Legend Arrow
        if custom_legend.id == 0x206:
            env.add_toggle('legend_arrow')