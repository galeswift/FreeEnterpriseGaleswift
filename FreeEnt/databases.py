try:
    from . import csvdb
except ImportError:
    import csvdb

import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'assets', 'db')

_doors_db = csvdb.CsvDb(os.path.join(DB_PATH, 'doors.csvdb'), {
    'map': str, 'trigger_number': int, 'x': int, 'y': int, 'dest': str, 'dest_x': int, 'dest_y': int, 'facing': str,
    'type': str, "world":str,
})

_curves_db = csvdb.CsvDb(os.path.join(DB_PATH, 'curves.csvdb'), {
    'wikiindex' : int,
    'tier1' : int,
    'tier2' : int,
    'tier3' : int,
    'tier4' : int,
    'tier5' : int,
    'tier6' : int,
    'tier7' : int,
    'tier8' : int,
    })

_tvanillaish_db = csvdb.CsvDb(os.path.join(DB_PATH, 'tvanillaish.csvdb'), {
    'wikiindex' : int,
    'tier1' : int,
    'tier2' : int,
    'tier3' : int,
    'tier4' : int,
    'tier5' : int,
    'tier6' : int,
    'tier7' : int,
    'tier8' : int,
    })

_treasure_db = csvdb.CsvDb(os.path.join(DB_PATH, 'treasure.csvdb'), {
    'ordr' : int,
    'flag' : csvdb.HexInt,
    'index' : int,
    'x' : int,
    'y' : int,
    'fight' : csvdb.NullableHexInt
    })

_items_db = csvdb.CsvDb(os.path.join(DB_PATH, 'items.csvdb'), {
    'code' : csvdb.HexInt,
    'tier' : int,
    'price' : int,
    'equip' : csvdb.List(',')
    })

_shops_db = csvdb.CsvDb(os.path.join(DB_PATH, 'shops.csvdb'), {
    'id' : csvdb.HexInt,
    'manifest' : csvdb.List('\n', filter_func=str.strip),
    'jmanifest' : csvdb.List('\n', filter_func=str.strip)
    })

_spells_db = csvdb.CsvDb(os.path.join(DB_PATH, 'spells.csvdb'), {
    'code' : csvdb.HexInt,
    'mp' : int,
    'data' : csvdb.List(',', value_type=csvdb.HexInt)
    })

_encounter_groups_db = csvdb.CsvDb(os.path.join(DB_PATH, 'encounter_groups.csvdb'), {
    'id' : csvdb.HexInt
    })

_custom_weapons_db = csvdb.CsvDb(os.path.join(DB_PATH, 'custom_weapons.csvdb'), {
    'id' : csvdb.HexInt,
    'equip' : csvdb.List(','),
    'use' : csvdb.List(','),
    'attack' : int,
    'accuracy' : int,
    'str' : int,
    'agi' : int,
    'vit' : int,
    'wis' : int,
    'wil' : int,
    'spellpower' : int,
    'elements' : csvdb.List(','),
    'anim0' : csvdb.HexInt,
    'anim1' : csvdb.HexInt,
    'anim2' : csvdb.HexInt,
    'anim3' : csvdb.HexInt,
    })

def get_curves_dbview():
    return _curves_db.create_view()

def get_doors_dbview():
    return _doors_db.create_view()

def get_tvanillaish_dbview():
    return _tvanillaish_db.create_view()

def get_treasure_dbview():
    return _treasure_db.create_view()

def get_items_dbview():
    return _items_db.create_view()

def get_shops_dbview():
    return _shops_db.create_view()

def get_spells_dbview():
    return _spells_db.create_view()

def get_encounter_groups_dbview():
    return _encounter_groups_db.create_view()

def get_custom_weapons_dbview():
    return _custom_weapons_db.create_view()

# helper function that some things need, maybe relocate?
_item_spoiler_names = {}
def get_item_spoiler_name(item):
    if not _item_spoiler_names:
        for it in get_items_dbview():
            _item_spoiler_names[it.const] = it.spoilername

    if type(item) is str:
        return _item_spoiler_names[item]
    else:
        return _item_spoiler_names[item.const]

_spell_spoiler_names = {}
def get_spell_spoiler_name(spell):
    if not _spell_spoiler_names:
        for sp in get_spells_dbview():
            if sp.const.startswith('#'):
                _spell_spoiler_names[sp.const] = sp.spoilername

    return _spell_spoiler_names[spell]

_encounter_group_spoiler_names = {}
def get_encounter_group_names(group_id):
    if not _encounter_group_spoiler_names:
        for enc in get_encounter_groups_dbview():
            _encounter_group_spoiler_names[enc.id] = (enc.spoilername, enc.preferredencounter)
    
    return _encounter_group_spoiler_names[group_id]