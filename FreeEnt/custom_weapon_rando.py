import os
from . import databases
from .rewards import RewardSlot, ItemReward
from .spoilers import SpoilerRow
from .address import *
from .errors import BuildError

CUSTOM_WEAPON_ITEM_ID = 0x46  # Dummy Legend sword
CUSTOM_WEAPON_ITEM_CONST = '#item.fe_CustomWeapon'
CUSTOM_WEAPON_EQUIP_TABLE_INDEX = 0x10
CUSTOM_WEAPON_ELEMENT_TABLE_INDEX = 0x3B

_CAST_TABLE = {
    'White' : 0x0B,
    'Weak' : 0x27,
    'Flood' : 0x43,
    'Blink' : 0x04,
    'Blitz' : 0x44,
    'Nuke' : 0x30,
    'Heal' : 0x12,
    'Wall' : 0x0A,
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
    if 'custom_weapon' in env.options.test_settings:
        custom_weapon = databases.get_custom_weapons_dbview().find_one(lambda cw: env.options.test_settings['custom_weapon'].lower() in f"{cw.name}|{cw.spoilername}".lower())
    elif env.options.flags.has('hero_challenge') or env.options.flags.has('superhero_challenge'):
        available_weapons = databases.get_custom_weapons_dbview().find_all(lambda cw: not cw.disabled and _is_user(cw, env.meta['starting_character']))
        custom_weapon = env.rnd.choice(available_weapons)
    elif env.options.flags.has('supersmith'):
        if env.options.flags.has('playablesmith') and not env.meta.get('wacky_challenge') == 'omnidextrous':
            if env.meta.get('wacky_challenge') == 'fistfight':
                available_weapons = databases.get_custom_weapons_dbview().find_all(lambda cw: not cw.disabled and _is_user(cw, 'yang'))
            else:
                available_weapons = databases.get_custom_weapons_dbview().find_all(lambda cw: not cw.disabled and _are_users(cw, env.meta['available_characters']))
        else:
            available_weapons = databases.get_custom_weapons_dbview().find_all(lambda cw: not cw.disabled)
        custom_weapon = env.rnd.choice(available_weapons)
    elif env.options.flags.has('altsmith'):
        items_dbview = databases.get_items_dbview()
        # to match the Pink Tail turn-in reward, also restrict the MoonVeil if Tno:j is on
        if env.options.flags.has('treasure_no_j_items'):
            items_dbview.refine(lambda it: not it.j)
        if env.options.flags.has('no_adamants'):
            items_dbview.refine(lambda it: it.const != '#item.AdamantArmor')
        if env.options.flags.has('playablesmith'):
            # alt smith item can't be a MoonVeil if Tno:j is on! So restricting to Yang-only without Adamants would be bad; don't restrict in that case.
            if not (env.options.flags.has('no_adamants') and env.options.flags.has('treasure_no_j_items') and (env.meta['available_characters']).issubset(set(['yang']))):
                items_dbview.refine(lambda it: it.category == 'item' or not set(it.equip).isdisjoint(env.meta['available_characters']))
        items = items_dbview.find_all(lambda it: it.tier in [7, 8])
        smith_reward = env.rnd.choice(items)
        env.meta['rewards_assignment'][RewardSlot.forge_item] = ItemReward(smith_reward.const)
        env.spoilers.add_table("MISC", [SpoilerRow("Smithy item", smith_reward.spoilername, obscurable=True)],
            public=env.options.flags.has_any('-spoil:all', '-spoil:misc'))
    else:
        env.meta['rewards_assignment'][RewardSlot.forge_item] = ItemReward('#item.Excalibur')

    if custom_weapon is None:
        env.add_substitution('custom weapon enabled', '')
        return

    # write item name
    env.add_script(f'text(item name ${CUSTOM_WEAPON_ITEM_ID:02X}) {{{custom_weapon.name}}}')

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
    
    if env.meta.get('wacky_challenge') == 'whatsmygear':
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
    for i,job in enumerate(_EQUIP):
        if job in custom_weapon.equip:
            equip_value |= (1 << i)
    env.add_binary(UnheaderedAddress(0x7A550 + CUSTOM_WEAPON_EQUIP_TABLE_INDEX * 0x02), [equip_value & 0xFF, (equip_value >> 8) & 0xFF], as_script=True)

    # write element table entry
    element_value = 0x000000
    for i,elem in enumerate(_ELEMENTS):
        if elem in custom_weapon.elements:
            element_value |= (1 << i)
    env.add_binary(UnheaderedAddress(0x7A590 + CUSTOM_WEAPON_ELEMENT_TABLE_INDEX * 0x03), [element_value & 0xFF, (element_value >> 8) & 0xFF, (element_value >> 16) & 0xFF], as_script=True)

    # set override item description
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
