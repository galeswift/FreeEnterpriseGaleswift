from . import databases
import re
from .rewards import RewardSlot

KIT_SPECS = {
    'basic' : [
        ( 'Life',       [(10, 15)] ),
        ( 'Cure2',      [(10, 15)] ),
        ( 'StarVeil',   [(2, 4)]   ),
        ( 'Tent',       [(3, 5)]   ),
        ],

    'better' : [
        ( 'Life',       [(10, 15)] ),
        ( 'Cure2',      [(10, 15)] ),
        ( 'StarVeil',   [(2, 4)]   ),
        ( 'Tent',       [(3, 5)]   ),
        ( [
            'Exit',
            'ThorRage',
            'SilkWeb',
            'Kamikaze',
            'Heal',
            'Ether1',
            'FireBomb',
            'Blizzard',
            'LitBolt',
            'Cabin',
            'Cure3'
          ], [(1,3), (0,2)]              ),
        ( [
            'Vampire',
            'SomaDrop',
            'GaiaDrum',
            'Grimoire',
            'Stardust',
            'BigBomb',
            'Boreas',
            'ZeusRage',
            'Illusion',
            'Siren',
            'HrGlass1',
            'HrGlass2',
            'HrGlass3',
            'Bacchus',
            'Coffin',
            'Elixir',
            'MoonVeil',
            'Sylph',
          ], [(1,2), (0,1)]              ),
        ],

    'loaded' : [
        ( 'Cure2',      [20]       ),
        ( 'Life',       [20]       ),
        ( 'Exit',       [5]        ),
        ( 'Ether2',     [3]        ),
        ( 'StarVeil',   [10]       ),
        ( 'HrGlass1',   [(3,5)]    ),
        ( 'Cabin',      [(3,5)]    ),
        ( [
            'Vampire',
            'SomaDrop',
            'GaiaDrum',
            'Grimoire',
            'Stardust',
            'BigBomb',
            'Boreas',
            'ZeusRage',
            'Illusion',
            'Bacchus',
            'Coffin',
            'Elixir',
            'MoonVeil',
            'Sylph',
          ], [(1,2), (1,2)] ),
        ],

    'cata' : [
        ( 'Life',       [3]        ),
        ( 'StarVeil',   [1]        ),
        ],

    'freedom' : [
        ( 'Life',       [10]       ),
        ( 'StarVeil',   [(3, 5)]   ),
        ( 'Siren',      [(1, 2)]   ),
        ( 'ThorRage',   [10]       ),
        ],

    'cid' : [
        ( 'Cure2',      [5] ),
        ( 'Bacchus',    [1] ),
        ( 'Unihorn',    [1] ),
        ( ['Dwarf', 'Ogre', 'PoisonAxe', 'RuneAxe'],  [1] ),
        ],

    'yang' : [
        ( 'CatClaw',    [2] ),
        ],

    'money' : [
        ( 'GP',         [(20000, 80000)] ),
        ],

    'grabbag' : None,  # special case handling

    'miab' : [
        ( 'HrGlass2',   [3] ),
        ( 'MuteBell',   [3] ),
        ( 'Assassin',   [1] ),
        ],

    'archer' : [
        ( ['ElvenBow', 'SamuraiBow', 'ArtemisBow'],  [1] ),
        ( ['PoisonArrow', 'MuteArrow', 'CharmArrow', 'SamuraiArrow'],  [20] ),
        ],

    'fabul' : [
        ( 'BlackSword', [1] ),
        ],

    'castlevania' : [
        ( ['Blitz', 'FlameWhip', 'DragonWhip'],  [1] ),
        ( 'Cross', [3] )
        ],

    'summon' : [
        ( ['Sylph', 'Odin', 'Levia', 'Asura', 'Baham'], [1] )
        ],

    'notdeme' : [
        ( 'Cure3',      [3] ),
        ( 'Elixir',     [2] ),
        ( 'Illusion',   [1] ),
        ],

    'meme' : [
        ( 'NinjaArmor', [1] ),
        ( 'DrainSpear', [1] ),
        ],

    'defense' : [
        ( 'DragonArmor', [1] ),
        ( 'DiamondHelm', [1] ),
        ],

    'mist' : [
        ( 'Dancing',    [10] ),
        ( 'Tiara',      [1]  ),
        ( 'Change',     [1]  )
        ],

    'mysidia' : [
        ( 'Cure2',         [70] ),
        ( 'Life',          [70] ),
        ( 'Heal',          [70] ),
        ( 'Ether1',        [70] ),
        ( 'GaeaHat',       [1]  ),
        ( 'PaladinShield', [1]  ),
        ( 'SilverRing',    [1]  ),
        ],

    'baron' : [
        ( 'Headband',    [10] ),
        ( 'Karate',      [10] ),
        ( 'ThunderClaw', [1]  ),
        ( 'ThunderRod',  [1]  ),
        ],

    'dwarf' : [
        ( 'WizardHat',   [1]  ),
        ( 'WizardArmor', [1]  ),
        ( 'Rune',        [10] ),
        ( 'Dwarf',       [1]  ),
        ( 'Elixir',      [1]  ),
        ( 'Strength',    [1]  ),
        ],

    'eblan' : [
        ( 'IceBrand',      [1] ),
        ( 'BlizzardSpear', [1] ),
        ],

    'libra' : [
        ( 'Bestiary',      [50] )
    ],

    '99' : None,  # special case handling

    'green' : [
        ( ['Glass','NinjaHelm'],   [1] ),   # b0ard
        ( ['Heroine', 'Carrot'],   [1] ),   # rivers
        ( ['Tiara', 'Grimoire'],   [1] ),   # schala
        ( ['RubyRing', 'CharmHarp'],   [1] ),   # zoe
        ( ['Sleep', 'Hermes'],     [1] ),   # wylem
        ( ['Rune', 'Stardust'],    [1] ),   # leggy
    ],

    'atb' : [
        ( 'SilkWeb',  [(2,3)] ),
        ( 'Hermes',   [(4,5)] ),
        ( 'HrGlass1', [1] ),
        ( 'Heal',     [(3,4)] ),
    ],

    'adamant' : [
        ( 'AdamantArmor',   [1]  )
    ],

    'cursed': [
        ( 'Cursed',         [1]  )
    ],

    'exit': [
        ('Exit', [(5,10)])
    ],

    'hero' : None, # special case handling
     
    'egg' : None, # special case handling
}

EGG_METHODS = {
    'coffin' : 
        { 'freq' : 5, 
          'users' : ['dkcecil', 'pcecil', 'kain', 'crydia', 'tellah', 'edward', 'rosa', 'yang', 'palom', 'porom', 'cid', 'edge', 'fusoya'],
          'type' : 'item',
          'items' : [
              ('Siren', [1]),
              ('Coffin', [1])
              ] },
    
    'grimoire' : 
        { 'freq' : 2,
          'users' : ['dkcecil', 'pcecil', 'kain', 'crydia', 'tellah', 'edward', 'rosa', 'yang', 'palom', 'porom', 'cid', 'edge', 'fusoya'],
          'type' : 'item',
          'items' : [
              ('Siren', [1]),
              ('Grimoire', [1])
              ] },

    'black' : 
        { 'freq' : 3,
          'users' : ['dkcecil'],
          'type' : 'fight',
          'items' : [
              ('Siren', [1]),
              ('BlackSword', [1]), 
              (['SilkWeb', 'HrGlass1'], [1]),
              ] },

    'medusa' : 
        { 'freq' : 4,
          'users' : ['pcecil', 'crydia', 'edward', 'rosa', 'palom', 'porom', 'cid', 'fusoya'],
          'type' : 'fight',
          'items' : [
              ('Siren', [1]),
              ('MedusaArrow', [1]),
              ('Archer', [1]), 
              (['SilkWeb', 'HrGlass1'], [1]),
              ] },

    'assassin' : 
        { 'freq' : 4,
          'users' : ['pcecil', 'kain', 'crydia', 'edward', 'palom', 'edge'],
          'type' : 'fight',
          'items' : [
              ('Siren', [1]),
              ('Assassin', [1]),
              (['SilkWeb', 'HrGlass1'], [1]),
              ] },

    'ninjastar' : 
        { 'freq' : 4,
          'users' : ['edge'],
          'type' : 'dart',
          'items' : [
              ('Siren', [1]),
              ('NinjaStar', [1])
              ] },

    'recall' : 
        { 'freq' : 2,
          'users' : ['tellah'],
          'type' : 'magic',
          'items' : [
              ('Siren', [1]),
              ('Ether2', [2]),
              ('PowerStaff', [1])
              ] },

    'baham' : 
        { 'freq' : 2,
          'users' : ['crydia'],
          'type' : 'magic',
          'items' : [
              ('Siren', [1]),
              ('Baham', [1]),
              ('SomaDrop', [5]),
              ('Change', [1])
              ] },

    'levia' : 
        { 'freq' : 1,
          'users' : ['crydia'],
          'type' : 'magic',
          'items' : [
              ('Siren', [1]),
              ('Levia', [1]),
              ('SomaDrop', [4]),
              ('ThunderRod', [1]),
              ('Tiara', [1]),
              ('Rune', [1])
              ] },

    'dragoon' : 
        { 'freq' : 2,
          'users' : ['kain'],
          'type' : 'jump',
          'items' : [
              ('Siren', [1]),
              ('DragoonSpear', [1]),
              ('Headband', [1]),
              ('Strength', [1])
              ] },

    'poisonaxe' : 
        { 'freq' : 1,
          'users' : ['pcecil', 'kain', 'cid'],
          'type' : 'fight',
          'items' : [
              ('Siren', [1]),
              ('SilkWeb', [1]),
              ('StarVeil', [1]),
              ('PoisonAxe', [1])
              ] },

    'venom' : 
        { 'freq' : 1,
          'users' : ['palom'],
          'type' : 'magic',
          'items' : [
              ('Siren', [1]),
              ('SilkWeb', [1]),
              ('StarVeil', [1])
              ] },

    'dragonwhip' : 
        { 'freq' : 3,
          'users' : ['crydia'],
          'type' : 'fight',
          'items' : [
              ('Siren', [1]),
              ('DragonWhip', [1]),
              ('CrystalRing', [1])
              ] },

    'heavyarmor' : # includes special processing to add a weapon
        { 'freq' : 2,
          'users' : ['pcecil', 'kain', 'cid'],
          'type' : 'fight',
          'items' : [
              ('Siren', [1]),
              ('Glass', [1]),
              ('DragonArmor', [1]),
              ('Cursed', [1]) 
              ] },

    'moonveil' : # includes special processing to add a weapon
        { 'freq' : 2,
          'users' : ['dkcecil', 'pcecil', 'kain', 'crydia', 'tellah', 'edward', 'rosa', 'yang', 'palom', 'porom', 'cid', 'edge', 'fusoya'],
          'type' : 'fight',
          'items' : [
              ('Siren', [1]),
              ('MoonVeil', [1]),
              ('Cure2', [10]),
              ('BlBelt', [1])
              ] },

    'magicspear' : 
        { 'freq' : 2,
          'users' : ['kain'],
          'type' : 'fight',
          'items' : [
              ('Siren', [1]),
              (['FlameSpear', 'BlizzardSpear', 'WhiteSpear'], [1]),
              ('StarVeil', [(2,3)])
              ] },

    'drain' : 
        { 'freq' : 1,
          'users' : ['pcecil', 'kain'],
          'type' : 'fight',
          'items' : [
              ('Siren', [1]),
              ('DrainSword', [1]),
              ('Glass', [1]),
              ('DragoonArmor', [1])
              ] },

    'artemis' : 
        { 'freq' : 1,
          'users' : ['pcecil', 'crydia', 'edward', 'rosa', 'palom', 'porom', 'cid', 'fusoya'],
          'type' : 'fight',
          'items' : [
              ('Siren', [1]),
              ('ArtemisArrow', [2]),
              ('ArtemisBow', [1]),
              ('NinjaHelm', [1])
              ] },

    'spoon' : 
        { 'freq' : 1,
          'users' : ['edward'],
          'type' : 'fight',
          'items' : [
              ('Siren', [1]),
              ('NinjaHelm', [1]),
              ('PowerShirt', [1]),
              ('CrystalRing', [1]),
              ('Bacchus', [1])
          ] },

    'bear' :
        { 'freq' : 1, 
          'users' : ['yang'],
          'type' : 'bear',
          'items' : [
              ('Siren', [1]),
              ('PoisonClaw', [1]),
              ('Cure2', [10])
          ] },
}

def apply(env):
    kits = []
    items_dbview = databases.get_items_dbview()

    kit_names = []
    for flag_prefix in ['-kit:', '-kit2:', '-kit3:']:
        kit_name = env.options.flags.get_suffix(flag_prefix)
        if kit_name in KIT_SPECS:
            kit_names.append(kit_name)
        elif kit_name == 'random':
            kit_names.append(env.rnd.choice(list(KIT_SPECS)))

    if env.meta.get('wacky_starter_kit'):
        kit_names.append('wacky_challenge')
    if env.meta.get('objective_starter_kit'):
        kit_names.append('objective')

    for kit_name in kit_names:
        if kit_name == 'grabbag':
            kit_spec = [
                ( items_dbview.find_all(lambda it: it.tier >= 1 and it.tier <= 5), [1] * 8 )
                ]
        elif kit_name == '99':
            kit_spec = [
                ( items_dbview.find_all(lambda it: it.tier >= 1 and it.tier <= 8), [99] )
                ]
        elif kit_name == 'hero':
            char = env.meta['starting_character']
            if (char == 'cecil'):
                char = 'pcecil'
            if (char == 'rydia'):
                char = 'arydia'
            weapons_dbview = items_dbview.get_refined_view(lambda it: it.category == 'weapon' and it.subtype != 'arrow' and it.tier in (4,5) and char in it.equip)
            arrows_dbview = items_dbview.get_refined_view(lambda it: it.category == 'weapon' and it.subtype == 'arrow' and it.tier in (4,5) and char in it.equip)
            armor_dbview = items_dbview.get_refined_view(lambda it: it.category == 'armor' and it.subtype in ('armor','robe') and it.tier in (4,5) and char in it.equip)
            head_dbview = items_dbview.get_refined_view(lambda it: it.category == 'armor' and it.subtype in ('hat','helmet') and it.tier in (4,5) and char in it.equip)
            hand_dbview = items_dbview.get_refined_view(lambda it: it.category == 'armor' and it.subtype in ('ring','gauntlet') and it.tier in (4,5) and it.const != '#item.Cursed' and char in it.equip)
            weapon1 = env.rnd.choice(weapons_dbview.find_all())
            weapon2 = None
            if weapon1.subtype == 'bow':
                weapon2 = env.rnd.choice(arrows_dbview.find_all())
            elif ((char == 'edge') or ('omnidextrous' in env.meta.get('wacky_challenge', []))):
                weapon2 = env.rnd.choice(weapons_dbview.find_all())
            armor = env.rnd.choice(armor_dbview.find_all())
            head = env.rnd.choice(head_dbview.find_all())
            hand = env.rnd.choice(hand_dbview.find_all())
            kit_spec = [ ( [ weapon1 ], [1]) ]
            if weapon2:
                quantity = [20] if (weapon1.subtype == 'bow' and ('unstackable' not in env.meta.get('wacky_challenge', []))) else [1]
                kit_spec = kit_spec + [ ( [ weapon2 ], quantity ) ]
            kit_spec = kit_spec + [ ([ armor ], [1]), ( [ head ], [1]), ( [ hand ], [1]) ]
        elif kit_name == 'egg':
            char = env.meta['starting_character']
            if char == 'cecil':
                if env.options.flags.has('characters_cecil_paladin'):
                    char = 'pcecil'
                else:
                    char = 'dkcecil'
            if char == 'rydia':
                char = 'crydia'
            egg_kits = []
            egg_weights = []
            for ekit in EGG_METHODS:
                to_add = False
                wackies = env.meta.get('wacky_challenge', [])
                starting_item = env.meta['rewards_assignment'][RewardSlot.starting_item].item
                if EGG_METHODS[ekit]['type'] == 'item':
                    to_add = True
                elif (EGG_METHODS[ekit]['type'] == 'fight' and 'omnidextrous' in wackies
                                                        and ekit in ['magicspear', 'poisonaxe']):
                    to_add = True
                elif (EGG_METHODS[ekit]['type'] == 'fight' and 'fistfight' in wackies):
                    continue
                elif (EGG_METHODS[ekit]['type'] == 'fight' and 'musical' in wackies and not env.options.flags.has('jump')
                                                        and ekit not in ['magicspear', 'poisonaxe', 'spoon'] and char not in ['kain', 'rosa']):
                    continue
                elif EGG_METHODS[ekit]['type'] == 'fight' and 'darts' in wackies and not (env.options.flags.has('jump') or char == 'kain'):
                    if ((ekit in ['dragoon', 'poisonaxe', 'magicspear'] and char in ['tellah', 'cid', 'edge', 'fusoya'])
                        or (ekit in ['artemis'] and char in ['edge', 'fusoya'])):
                        to_add = True
                    else:
                        continue
                elif ((starting_item != '#item.Spoon') 
                            or (not env.options.flags.has('edward_spoon') and not 'omnidextrous' in wackies)
                            or (('menarepigs' in wackies and char not in ['crydia', 'rosa', 'porom']) and not env.options.flags.has('jump'))) and ekit == 'spoon':
                    continue
                elif EGG_METHODS[ekit]['type'] == 'fight' and 'omnidextrous' in wackies:
                    to_add = True
                elif EGG_METHODS[ekit]['type'] == 'jump' and 'omnidextrous' in wackies and env.options.flags.has('jump'):
                    to_add = True
                elif EGG_METHODS[ekit]['type'] == 'dart' and 'darts' in wackies and char in ['edge', 'fusoya']:
                    to_add = True
                elif not env.options.flags.has('japanese_abilities') and ekit in ['recall', 'bear']:
                    continue
                elif 'misspelled' in wackies and ekit in ['baham', 'levia', 'venom']:
                    continue
                elif 'unstackable' in wackies and ekit in ['baham', 'levia', 'bear', 'moonveil']:
                    continue
                elif char in EGG_METHODS[ekit]['users']:
                    to_add = True
                if to_add:
                    egg_kits.append(ekit)
                    egg_weights.append(EGG_METHODS[ekit]['freq'])
            chosen_kit = env.rnd.choices(egg_kits, weights=egg_weights, k=1)[0]
            kit_spec = EGG_METHODS[chosen_kit]['items']
            if chosen_kit in ['heavyarmor', 'sorcrobe', 'moonveil']:
                weapons_dbview = items_dbview.get_refined_view(lambda it: it.category == 'weapon' and it.subtype != 'arrow' and it.tier in (3,5) and char in it.equip)
                if 'unstackable' in wackies:
                    weapons_dbview.refine(lambda it: it.subtype != 'bow')
                weapon1 = env.rnd.choice(weapons_dbview.find_all())
                kit_spec.append( (weapon1.const[6:], [1]) )
                if weapon1.subtype == 'bow':
                    arrows_dbview = items_dbview.get_refined_view(lambda it: it.category == 'weapon' and it.subtype == 'arrow' and it.tier in (3,5) and char in it.equip)
                    weapon2 = env.rnd.choice(arrows_dbview.find_all())
                    kit_spec.append( (weapon2.const[6:], [30]) )
            elif chosen_kit in ['baham', 'levia'] and 'tellahmaneuver' in wackies:
                kit_spec[2] = ('AuApple', [(6 if chosen_kit == 'baham' else 5)])
            elif chosen_kit in ['magicspear'] and 'darts' in wackies:
                if char in ['tellah', 'cid']:
                    kit_spec[1] = ('WhiteSpear', [1])
                elif char == 'edge':
                    kit_spec[1] = (['BlizzardSpear', 'WhiteSpear'], [1])
        elif kit_name == 'wacky_challenge':
            kit_spec = env.meta['wacky_starter_kit']
        elif kit_name == 'objective':
            kit_spec = env.meta['objective_starter_kit']
        else:
            kit_spec = KIT_SPECS[kit_name]

        kit = []
        for entry in kit_spec:
            item_set = entry[0]
            if type(item_set) is str:
                item_set = [item_set]

            if '3point' in env.meta.get('wacky_challenge', []):
                item_set = list(filter(lambda i: i != 'SomaDrop', item_set))

            qty_list = entry[1]
            items = env.rnd.sample(item_set, len(qty_list))
            for i,qty_spec in enumerate(qty_list):
                if type(qty_spec) is int:
                    qty = qty_spec
                else:
                    qty = env.rnd.randint(*qty_spec)

                item = items.pop(0)
                if qty > 0:
                    if item == 'GP':
                        qty = 1000 * round(qty / 1000)
                        kit.append( ('GP', qty) )
                    else:
                        item_const = (f'#item.{item}' if type(item) is str else item.const)
                        if kit_name == 'grabbag' and item.subtype == 'arrow':
                            qty = env.rnd.randint(1,10)
                        if 'unstackable' in env.meta.get('wacky_challenge', []):
                            qty = 1
                        kit.append( (items_dbview.find_one(lambda it: it.const == item_const), qty) )

        if kit:
            kits.append(kit)

    patch_lines = []

    altered_item_names = env.meta.get('altered_item_names', {})
    for i in range(5):
        if not kits:
            env.add_substitution(f'starterkit{i} message enable', '')
        else:        
            kit = kits.pop(0)
            print(kit)

            message_lines = []
            spoiler_rows = []

            message_lines.append('Received supplies:')
            for entry in kit:
                item,qty = entry
                print(item)
                print(qty)
                if (item == 'GP'):
                    message_lines.append(f'    {qty} GP')
                    patch_lines.append(f'FE {qty & 0xFF:02X} {(qty >> 8) & 0xFF:02X} {(qty >> 16) & 0xFF:02X}')
                    spoiler_rows.append( (str(qty), 'GP') )
                else:
                    item_name = altered_item_names.get(item.code, item.name)
                    message_lines.append(f'    {qty:>2} {item_name}')
                    patch_lines.append(f'{item.const} {qty:02X}')
                    spoiler_rows.append( (str(qty), databases.get_item_spoiler_name(item)) )

            env.add_substitution(f'starterkit{i} message text', '\n'.join(message_lines))

            env.spoilers.add_table(f'STARTER KIT {i+1}', spoiler_rows, public=env.options.flags.has_any('-spoil:all', '-spoil:misc'))


    env.add_script('patch($21dd00 bus) {\n' + '\n'.join(patch_lines) + '\nFF FF\n}')
