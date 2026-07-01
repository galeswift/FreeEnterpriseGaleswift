'''
This rando unit handles the logic that assigns the locations
of keyitems, bosses, and monster-in-a-box locations, accounting 
for randomizer flags and interactions between them. The actual 
effects of these assignments are dealt with in keyitem_rando 
and boss_rando.
'''

from .rewards import EmptyReward, KeyItemReward, ItemReward, AxtorReward, AxtorChestReward, RewardSlot, RewardsAssignment, REWARD_SLOT_SPOILER_NAMES
from . import databases
from . import dep_checker
from . import priority_assigner
from . import util
from . import treasure_rando
from . import character_rando
from .spoilers import SpoilerRow

from .address import *
from .boss_slot_ranking_weights_data import *

from f4c import encode_text

import math

DEBUG = 0 # set to > 1 for more detailed checker output
# largest known successful generation: 2837 attempts
# flagset: Onone Kmain/miab:above,below/forge/pink/unweighted/force:hook/unsafer Pkey Cstandard Twild Swild Bstandard/nofree Etoggle Hrandom Gnone Fvanilla Aagnostic Zailments -starting:blackchocobo
MAX_RANDOMIZATION_ATTEMPTS = 5000

COMMON_BRANCHES = [
    ['#item.Magma?', 'underground'],
    ['#item.DarkCrystal?', 'moon'],
    ]

HOOK_UNDERGROUND_BRANCH = ['#item.fe_Hook?', 'kingqueen_slot', 'rubicant_slot', 'underground']

STARTING_ITEM_MAP = {
    'Kstart:package'                        : '#item.Package',
    'Kstart:sandruby'                       : '#item.SandRuby',
    'Kstart:baron'                          : '#item.Baron',
    'Kstart:twinharp'                       : '#item.TwinHarp',
    'Kstart:earthcrystal'                   : '#item.EarthCrystal',
    'Kstart:magma'                          : '#item.Magma',
    'Kstart:tower'                          : '#item.Tower',
    'Kstart:hook'                           : '#item.fe_Hook',
    'Kstart:luca'                           : '#item.Luca',
    'Kstart:darkness'                       : '#item.DarkCrystal',
    'Kstart:rat'                            : '#item.Rat',
    'Kstart:pan'                            : '#item.Pan',
    'Kstart:crystal'                        : '#item.Crystal',
    'Kstart:legend'                         : '#item.Legend',
    'Kstart:adamant'                        : '#item.Adamant',
    'Kstart:spoon'                          : '#item.Spoon',
    'Kstart:pink'                           : '#item.Pink',
    'Kstart:pass'                           : '#item.Pass',
}

ESSENTIAL_KEY_ITEMS = {
    KeyItemReward('#item.Package')         : RewardSlot.starting_item, #'package_slot',
    KeyItemReward('#item.SandRuby')        : RewardSlot.antlion_item, #'sandruby_slot', 
    KeyItemReward('#item.Baron')           : RewardSlot.baron_inn_item, #'baron_key_slot',
    KeyItemReward('#item.TwinHarp')        : RewardSlot.toroia_hospital_item, #'twinharp_slot', 
    KeyItemReward('#item.EarthCrystal')    : RewardSlot.magnes_item, #'earth_crystal_slot',
    KeyItemReward('#item.Magma')           : RewardSlot.zot_item, #'magma_key_slot', 
    KeyItemReward('#item.Tower')           : RewardSlot.babil_boss_item, #'tower_key_slot', 
    KeyItemReward('#item.fe_Hook')         : RewardSlot.cannon_item, #'hook_slot',
    KeyItemReward('#item.Luca')            : RewardSlot.luca_item, #'luca_key_slot', 
    KeyItemReward('#item.DarkCrystal')     : RewardSlot.sealed_cave_item, #'dark_crystal_slot',
    KeyItemReward('#item.Rat')             : RewardSlot.feymarch_item, #'rat_tail_slot', 
    KeyItemReward('#item.Pan')             : RewardSlot.found_yang_item, #'pan_slot', 
    KeyItemReward('#item.Crystal')         : RewardSlot.fallen_golbez_item, #'zeromus_crystal_slot', 
    KeyItemReward('#item.Legend')          : RewardSlot.ordeals_item, #'legend_sword_slot', 
    KeyItemReward('#item.Adamant')         : RewardSlot.rat_trade_item, #'adamant_slot',
    }

NONESSENTIAL_KEY_ITEMS = {
    KeyItemReward('#item.Spoon')           : RewardSlot.pan_trade_item, #'spoon_slot',
    KeyItemReward('#item.Pink')            : None,
    }

SUMMON_QUEST_ITEMS = {
    ItemReward('#item.Sylph')              : RewardSlot.sylph_item, #'sylph_item_slot',
    ItemReward('#item.Asura')              : RewardSlot.feymarch_queen_item, #'asura_item_slot',
    ItemReward('#item.Levia')              : RewardSlot.feymarch_king_item, #'levia_item_slot',
    ItemReward('#item.Odin')               : RewardSlot.baron_throne_item, #'odin_item_slot',
    ItemReward('#item.Baham')              : RewardSlot.bahamut_item, #'baham_item_slot',
    }

MOON_BOSS_ITEMS = {
    ItemReward('#item.Murasame')           : RewardSlot.lunar_boss_1_item, #'murasame_slot',
    ItemReward('#item.CrystalSword')       : RewardSlot.lunar_boss_2_item, #'crystal_sword_slot',
    ItemReward('#item.WhiteSpear')         : RewardSlot.lunar_boss_3_item, #'white_spear_slot',
    ItemReward('#item.Ribbon_1')           : RewardSlot.lunar_boss_4_item_1, #'ribbon1_slot',
    ItemReward('#item.Ribbon_2')           : RewardSlot.lunar_boss_4_item_2, #'ribbon2_slot',
    ItemReward('#item.Masamune')           : RewardSlot.lunar_boss_5_item, #'masamune_slot',
    }

VANILLA_ITEMS = dict()
VANILLA_ITEMS.update(ESSENTIAL_KEY_ITEMS)
VANILLA_ITEMS.update(NONESSENTIAL_KEY_ITEMS)
VANILLA_ITEMS.update(SUMMON_QUEST_ITEMS)
VANILLA_ITEMS.update(MOON_BOSS_ITEMS)

ITEM_SLOTS = {
    RewardSlot.starting_item          : [],
    RewardSlot.antlion_item           : ['antlion_slot'],
    RewardSlot.fabul_item             : ['fabulgauntlet_slot'],
    RewardSlot.ordeals_item           : ['milon_slot', 'milonz_slot', 'mirrorcecil_slot'],
    RewardSlot.baron_inn_item         : ['guard_slot', 'karate_slot'],
    RewardSlot.baron_castle_item      : ['#item.Baron?', 'baigan_slot', 'kainazzo_slot'],
    RewardSlot.toroia_hospital_item   : [],
    RewardSlot.magnes_item            : ['#item.TwinHarp?', 'darkelf_slot'],
    RewardSlot.zot_item               : ['#item.EarthCrystal?', 'magus_slot', 'valvalis_slot'],
    RewardSlot.babil_boss_item        : ['underground?', 'lugae_slot'],
    RewardSlot.cannon_item            : ['underground?', '#item.Tower?', 'darkimp_slot'],
    RewardSlot.luca_item              : ['underground?', 'calbrena_slot', 'golbez_slot'],
    RewardSlot.sealed_cave_item       : ['underground?', '#item.Luca?', 'evilwall_slot'],
    RewardSlot.found_yang_item        : ['underground?'],
    RewardSlot.pan_trade_item         : ['underground?', '#item.Pan?'],
    RewardSlot.feymarch_item          : ['underground?'],
    RewardSlot.rat_trade_item         : ['#item.fe_Hook?', '#item.Rat?'],
    RewardSlot.pink_trade_item        : ['#item.fe_Hook?', '#item.Pink?'],
    RewardSlot.forge_item             : ['underground?', '#item.Adamant?', '#item.Legend?'],
    RewardSlot.rydias_mom_item        : ['dmist?'],
    RewardSlot.dwarf_hospital_item    : ['underground?'],
    }

SUMMON_QUEST_SLOTS = {
    RewardSlot.sylph_item             : ['underground?', '#item.Pan?'],
    RewardSlot.feymarch_queen_item    : ['underground?', 'asura_slot'],
    RewardSlot.feymarch_king_item     : ['underground?', 'leviatan_slot'],
    RewardSlot.baron_throne_item      : ['#item.Baron?', 'baigan_slot', 'odin_slot'],
    RewardSlot.bahamut_item           : ['moon?', 'bahamut_slot'],
    }

MOON_BOSS_SLOTS = {
    RewardSlot.lunar_boss_1_item      : ['moon?', 'paledim_slot'],
    RewardSlot.lunar_boss_2_item      : ['moon?', 'wyvern_slot'],
    RewardSlot.lunar_boss_3_item      : ['moon?', 'plague_slot'],
    RewardSlot.lunar_boss_4_item_1    : ['moon?', 'dlunar_slot'],
    RewardSlot.lunar_boss_4_item_2    : ['moon?', 'dlunar_slot'],
    RewardSlot.lunar_boss_5_item      : ['moon?', 'ogopogo_slot'],
    }

CHEST_ITEM_SLOTS = {
    RewardSlot.zot_chest              : [],
    RewardSlot.eblan_chest_1          : [],
    RewardSlot.eblan_chest_2          : [],
    RewardSlot.eblan_chest_3          : [],
    RewardSlot.lower_babil_chest_1    : ['underground?'],
    RewardSlot.lower_babil_chest_2    : ['underground?'],
    RewardSlot.lower_babil_chest_3    : ['underground?'],
    RewardSlot.lower_babil_chest_4    : ['underground?'],
    RewardSlot.cave_eblan_chest       : ['#item.fe_Hook?'],
    RewardSlot.upper_babil_chest      : ['#item.fe_Hook?'],
    RewardSlot.cave_of_summons_chest  : ['underground?'],
    RewardSlot.sylph_cave_chest_1     : ['underground?'],
    RewardSlot.sylph_cave_chest_2     : ['underground?'],
    RewardSlot.sylph_cave_chest_3     : ['underground?'],
    RewardSlot.sylph_cave_chest_4     : ['underground?'],
    RewardSlot.sylph_cave_chest_5     : ['underground?'],
    RewardSlot.sylph_cave_chest_6     : ['underground?'],
    RewardSlot.sylph_cave_chest_7     : ['underground?'],
    RewardSlot.giant_chest            : ['moon?'],
    RewardSlot.lunar_path_chest       : ['moon?'],
    RewardSlot.lunar_core_chest_1     : ['moon?'],
    RewardSlot.lunar_core_chest_2     : ['moon?'],
    RewardSlot.lunar_core_chest_3     : ['moon?'],
    RewardSlot.lunar_core_chest_4     : ['moon?'],
    RewardSlot.lunar_core_chest_5     : ['moon?'],
    RewardSlot.lunar_core_chest_6     : ['moon?'],
    RewardSlot.lunar_core_chest_7     : ['moon?'],
    RewardSlot.lunar_core_chest_8     : ['moon?'],
    RewardSlot.lunar_core_chest_9     : ['moon?'],
    }

CHEST_ITEM_SLOT_GROUPS = [
        ( [
            RewardSlot.eblan_chest_1,
            RewardSlot.eblan_chest_2,
            RewardSlot.eblan_chest_3,
        ], 'above' ),
        ( [
            RewardSlot.zot_chest,
        ], 'above' ),
        ( [
            RewardSlot.lower_babil_chest_1,
            RewardSlot.lower_babil_chest_2,
            RewardSlot.lower_babil_chest_3,
            RewardSlot.lower_babil_chest_4,
        ], 'below' ),
        ( [
            RewardSlot.cave_eblan_chest,
        ], 'above' ),
        ( [
            RewardSlot.upper_babil_chest,
        ], 'above' ),
        ( [
            RewardSlot.cave_of_summons_chest,
        ], 'below' ),
        ( [
            RewardSlot.sylph_cave_chest_1,
            RewardSlot.sylph_cave_chest_2,
            RewardSlot.sylph_cave_chest_3,
            RewardSlot.sylph_cave_chest_4,
            RewardSlot.sylph_cave_chest_5,
            RewardSlot.sylph_cave_chest_6,
            RewardSlot.sylph_cave_chest_7,
        ], 'below' ),
        ( [
            RewardSlot.giant_chest,
        ], 'above' ),
        ( [
            RewardSlot.lunar_path_chest,
        ], 'above' ),
        ( [
            RewardSlot.lunar_core_chest_1,
            RewardSlot.lunar_core_chest_2,
            RewardSlot.lunar_core_chest_3,
            RewardSlot.lunar_core_chest_4,
            RewardSlot.lunar_core_chest_5,
            RewardSlot.lunar_core_chest_6,
            RewardSlot.lunar_core_chest_7,
            RewardSlot.lunar_core_chest_8,
            RewardSlot.lunar_core_chest_9,
        ], 'lst' ),
    ]

CHEST_NUMBERS = {
    RewardSlot.eblan_chest_1         : ['#EblanWestTower1F', 1],
    RewardSlot.eblan_chest_2         : ['#EblanEastTower2F', 3],
    RewardSlot.eblan_chest_3         : ['#EblanBasement', 2],
    RewardSlot.zot_chest             : ['#Zot2F', 0],
    RewardSlot.lower_babil_chest_1   : ['#BabilIcebrandRoom', 0],
    RewardSlot.lower_babil_chest_2   : ['#BabilBlizzardRoom', 0],
    RewardSlot.lower_babil_chest_3   : ['#BabilIceShieldRoom', 0],
    RewardSlot.lower_babil_chest_4   : ['#BabilIceMailRoom', 0],
    RewardSlot.cave_eblan_chest      : ['#CaveEblanSaveRoom', 0],
    RewardSlot.upper_babil_chest     : ['#BabilB2', 0],
    RewardSlot.cave_of_summons_chest : ['#CaveOfSummons3F', 0],
    RewardSlot.sylph_cave_chest_1    : ['#SylvanCave2F', 9],
    RewardSlot.sylph_cave_chest_2    : ['#SylvanCaveTreasury', 0],
    RewardSlot.sylph_cave_chest_3    : ['#SylvanCaveTreasury', 1],
    RewardSlot.sylph_cave_chest_4    : ['#SylvanCaveTreasury', 2],
    RewardSlot.sylph_cave_chest_5    : ['#SylvanCaveTreasury', 3],
    RewardSlot.sylph_cave_chest_6    : ['#SylvanCaveTreasury', 4],
    RewardSlot.sylph_cave_chest_7    : ['#SylvanCaveTreasury', 5],
    RewardSlot.giant_chest           : ['#GiantPassage', 0],
    RewardSlot.lunar_path_chest      : ['#LunarPassage1', 0],
    RewardSlot.lunar_core_chest_1    : ['#LunarSubterran1F', 0],
    RewardSlot.lunar_core_chest_2    : ['#LunarSubterran2F', 1],
    RewardSlot.lunar_core_chest_3    : ['#LunarSubterran4F', 1],
    RewardSlot.lunar_core_chest_4    : ['#LunarSubterran5F', 0],
    RewardSlot.lunar_core_chest_5    : ['#LunarSubterran5F', 1],
    RewardSlot.lunar_core_chest_6    : ['#LunarSubterran5F', 2],
    RewardSlot.lunar_core_chest_7    : ['#LunarSubterran5F', 3],
    RewardSlot.lunar_core_chest_8    : ['#LunarSubterran5F', 4],
    RewardSlot.lunar_core_chest_9    : ['#LunarSubterranTunnelMinerva', 0],
    }

BOSS_SLOTS = {
    'dmist_slot'            : [],
    'officer_slot'          : ['#item.Package?'],
    'octomamm_slot'         : [],
    'antlion_slot'          : [],
    'mombomb_slot'          : [],
    'fabulgauntlet_slot'    : [],
    'milon_slot'            : [],
    'milonz_slot'           : ['milon_slot'],
    'mirrorcecil_slot'      : ['milon_slot', 'milonz_slot'],
    'karate_slot'           : ['guard_slot'],
    'guard_slot'            : [],
    'baigan_slot'           : ['#item.Baron?'],
    'kainazzo_slot'         : ['#item.Baron?', 'baigan_slot'],
    'darkelf_slot'          : ['#item.TwinHarp?'],
    'magus_slot'            : [],
    'valvalis_slot'         : ['#item.EarthCrystal?', 'magus_slot'],
    'calbrena_slot'         : ['underground?'],
    'golbez_slot'           : ['underground?', 'calbrena_slot'],
    'lugae_slot'            : ['underground?'],
    'darkimp_slot'          : ['underground?', '#item.Tower?'],
    'kingqueen_slot'        : ['#item.fe_Hook?'],
    'rubicant_slot'         : ['#item.fe_Hook?', 'kingqueen_slot'],
    'evilwall_slot'         : ['underground?', '#item.Luca?'],
    'asura_slot'            : ['underground?'],
    'leviatan_slot'         : ['underground?'],
    'odin_slot'             : ['#item.Baron?', 'baigan_slot'],
    'bahamut_slot'          : ['moon?'],
    'elements_slot'         : ['moon?'],
    'cpu_slot'              : ['moon?', 'elements_slot'],
    'paledim_slot'          : ['moon?'],
    'wyvern_slot'           : ['moon?'],
    'plague_slot'           : ['moon?'],
    'dlunar_slot'           : ['moon?'],
    'ogopogo_slot'          : ['moon?'], 
    }

BOSSES = [
    'dmist',
    'officer',
    'octomamm',
    'antlion',
    'waterhag',
    'mombomb',
    'fabulgauntlet',
    'milon',
    'milonz',
    'mirrorcecil',
    'guard',
    'karate',
    'baigan',
    'kainazzo',
    'darkelf',
    'magus',
    'valvalis',
    'calbrena',
    'golbez',
    'lugae',
    'darkimp',
    'kingqueen',
    'rubicant',
    'evilwall',
    'asura',
    'leviatan',
    'odin',
    'bahamut',
    'elements',
    'cpu',
    'paledim',
    'wyvern',
    'plague',
    'dlunar',
    'ogopogo',
    ]

BOSS_SLOT_SHUFFLE_GROUPS = {
    'ungated_overworld' : ['dmist_slot', 'octomamm_slot', 'antlion_slot', 'mombomb_slot', 'fabulgauntlet_slot',
                           'milon_slot', 'milonz_slot', 'mirrorcecil_slot', 'karate_slot', 'guard_slot', 'magus_slot'],
    'gated_overworld'   : ['officer_slot', 'baigan_slot', 'kainazzo_slot', 'darkelf_slot', 'valvalis_slot', 'kingqueen_slot', 'rubicant_slot'],
    'underworld'        : ['calbrena_slot', 'golbez_slot', 'lugae_slot', 'darkimp_slot', 'evilwall_slot', 'asura_slot', 'leviatan_slot', 'odin_slot'],
    'darkness'          : ['elements_slot', 'cpu_slot', 'bahamut_slot', 'paledim_slot', 'wyvern_slot', 'plague_slot', 'dlunar_slot', 'ogopogo_slot']
}

BOSS_LOCATION_ZONES = {
    'early_game' : ['dmist_slot', 'officer_slot', 'octomamm_slot', 'antlion_slot', 'mombomb_slot', 'fabulgauntlet_slot',
                    'milon_slot', 'milonz_slot', 'mirrorcecil_slot', 'karate_slot', 'guard_slot'],
    'gated_blue_planet' : ['baigan_slot', 'kainazzo_slot', 'darkelf_slot', 'magus_slot', 'valvalis_slot', 'kingqueen_slot', 'rubicant_slot',
                           'calbrena_slot', 'golbez_slot', 'lugae_slot', 'darkimp_slot', 'evilwall_slot'],
    'summon_darkness' : ['asura_slot', 'leviatan_slot', 'odin_slot', 'elements_slot', 'cpu_slot', 
                         'bahamut_slot', 'paledim_slot', 'wyvern_slot', 'plague_slot', 'dlunar_slot', 'ogopogo_slot']
}

def _get_standard_boss_shuffle(env, slots, bosses, removed_boss_slots,
                                    restricted_boss_slots, objective_bosses_and_maybe_dmist):
    tmp_assignment = {}
    available_unrestricted_boss_slots = [s for s in slots if s not in removed_boss_slots and s not in restricted_boss_slots]
    required_bosses = [b for b in bosses if b in objective_bosses_and_maybe_dmist]
    zone_removed_slots = [s for s in removed_boss_slots if s in slots]
    # first, assign required bosses to unrestricted slots
    env.rnd.shuffle(required_bosses)
    env.rnd.shuffle(available_unrestricted_boss_slots)
    remaining_boss_slots = [s for s in slots if s not in removed_boss_slots]
    for i in range(min(len(required_bosses), len(available_unrestricted_boss_slots))):
        tmp_assignment[available_unrestricted_boss_slots[i]] = required_bosses[i]
        remaining_boss_slots.remove(available_unrestricted_boss_slots[i])

    env.rnd.shuffle(remaining_boss_slots)
    if len(available_unrestricted_boss_slots) < len(required_bosses):
        # if we fill the slots first, then all remaining bosses go somewhere
        # (ensuring required bosses get placed first)
        for i,b in enumerate(required_bosses[len(available_unrestricted_boss_slots):]):
            tmp_assignment[remaining_boss_slots[i]] = b
        slot_idx = len(required_bosses[len(available_unrestricted_boss_slots):])
        remaining_bosses = [b for b in bosses if b not in required_bosses]
        env.rnd.shuffle(remaining_bosses)
        for i,s in enumerate(remaining_boss_slots[slot_idx:] + zone_removed_slots):
            tmp_assignment[s] = remaining_bosses[i]
    else:
        # otherwise we just place all remaining bosses into remaining slots
        remaining_bosses = [b for b in bosses if b not in required_bosses]
        env.rnd.shuffle(remaining_bosses)
        for i,s in enumerate(remaining_boss_slots + zone_removed_slots):
            tmp_assignment[s] = remaining_bosses[i]

    if 'boss' in env.options.test_settings:
        for force_slot in env.options.test_settings['boss']:
            force_boss = env.options.test_settings['boss'][force_slot]
            replaced_boss = tmp_assignment[force_slot]
            if force_boss != replaced_boss:
                for k in tmp_assignment:
                    if tmp_assignment[k] == force_boss:
                        tmp_assignment[k] = replaced_boss
                        break
                tmp_assignment[force_slot] = force_boss
    
    return tmp_assignment

NUM_SWAPS = 200

# list of slots that don't have spell power (so do level-based scaling when not on Bspellpower)
ZERO_SPELL_POWER_SLOTS = [
    'officer_slot',
    'antlion_slot',
    'octomamm_slot',
    'fabulgauntlet_slot',
    'mirrorcecil_slot',
    'karate_slot',
    'darkimp_slot',
    'kingqueen_slot',
    'plague_slot'
]

# list of slots that don't normally have unsafe bosses guarding your logical underground progression
# for now, use the ungated checks and the Hook route
OVERWORLD_PROGRESSION_FIGHT_SLOTS = [
    'antlion_slot', 
    'fabulgauntlet_slot',
    'milon_slot',
    'milonz_slot',
    'mirrorcecil_slot',
    'guard_slot',
    'karate_slot',
    'kingqueen_slot',
    'rubicant_slot',
]

# for -starting:underground, use the ungated boss fights (i.e. not Super Cannon or Sealed Cave)
UNDERWORLD_PROGRESSION_FIGHT_SLOTS = [
    'calbrena_slot',
    'golbez_slot',
    'lugae_slot',
    'asura_slot',
    'wyvern_slot',
]

BEASY_DIFFICULTY = [
    'wyvern',
    'valvalis',
    'golbez',
    'fabulgauntlet',
    'kainazzo',
    'ogopogo',
    'mirrorcecil',
    'dlunar',
    'odin',
    'evilwall',
    'rubicant',
    'baigan',
    'plague',
    'antlion',
    'cpu',
    'asura',
    'leviatan',
    'paledim',
    'dmist',
    'karate',
    'elements',
    'magus',
    'darkelf',
    'lugae',
    'octomamm',
    'mombomb',
    'bahamut',
    'calbrena',
    'milonz',
    'milon',
    'guard',
    'darkimp',
    'waterhag',
    'officer',
    'kingqueen',
    ]

def _set_scoring_parameters(env):
    scoring_parameters = {
        'alt_gauntlet'    : env.options.flags.has('bosses_alt_gauntlet'),
        'boss_spellpower' : env.options.flags.has('bosses_nonzero_spellpower'),
        'cecil_in_seed'   : 'cecil' in env.meta['available_characters'],
        'jump_available'  : 'kain' in env.meta['available_characters'] or env.options.flags.has('jump'),
        'atb_scale_1'     : False,
        'party_size_1'    : False,
        'start_dwarf'     : env.options.flags.has('starting_underground'),
        'danger_anchor'   : (env.options.flags.has_any('hero_challenge', 'superhero_challenge') and env.options.flags.has('no_cursed_rings'))
                                or env.options.flags.has_any('fastest_agility', 'random_agility', 'monster_agility'),
        'woahdin'         : env.options.flags.has('odin_random_spell'),
        'thehades'        : env.options.flags.has('kingqueen_fire_upgrade'),
        'no_lit_shops'    : env.options.flags.has_any('shops_no_damage_items', 'shops_no_j_items'),
        'whichburn'       : env.options.flags.has('wyvern_random_meganuke'),
        'itburns'         : env.options.flags.has('wyvern_all_bad_things'),
        'whyburn'         : env.options.flags.has('wyvern_no_meganuke'),
        'no_free'         : env.options.flags.has('no_free_bosses'),
        'unsafe'          : env.options.flags.has('bosses_unsafe'),
        'no_veils_shops'  : env.options.flags.has('shops_no_starveil'),
        'no_life_shops'   : env.options.flags.has('shops_no_life'),
        'whybez'          : env.options.flags.has('golbez_no_shadow'),
        'whichbez'        : env.options.flags.has('golbez_random_spells'),
    }
    agility_scale_suffix = env.options.flags.get_suffix('Ascale:')
    if agility_scale_suffix:
        if int(agility_scale_suffix) == 1:
            scoring_parameters.update({'atb_scale_1' : True})
    party_size_suffix = env.options.flags.get_suffix('Cparty:')
    if party_size_suffix:
        if int(party_size_suffix) == 1:
            scoring_parameters.update({'party_size_1' : True})

    return scoring_parameters

def _set_stats_weights(scoring_parameters):
    stats_weights = BOSS_STATS_WEIGHTS_DIFFICULTY
    if scoring_parameters['boss_spellpower']:
        stats_weights['antlion'].update({
            'speed' : 20,
            'spell power' : 30,
            'hp' : 10,
        })
        stats_weights['kingqueen'].update({
            'spell power' : 40,
            'hp' : 10,
        })
    if not scoring_parameters['cecil_in_seed']:
        stats_weights['karate'].update({
            'attack' : 30,
            'hp' : 30,
            'difficulty' : 1,
        })
    if not scoring_parameters['jump_available']:
        stats_weights['valvalis']['difficulty'] += 0.3
    if scoring_parameters['atb_scale_1']:
        stats_weights['evilwall']['difficulty'] += 0.2
    if scoring_parameters['danger_anchor'] or scoring_parameters['party_size_1']:
        stats_weights['plague']['difficulty'] += 0.5
    if scoring_parameters['woahdin'] and not scoring_parameters['no_lit_shops']:
        stats_weights['odin']['difficulty'] -= 0.4
    elif scoring_parameters['no_lit_shops']:
        stats_weights['kainazzo']['difficulty'] += 0.2
    if scoring_parameters['whichburn']:
        stats_weights['wyvern']['difficulty'] -= 0.2
    elif scoring_parameters['itburns']:
        stats_weights['wyvern']['difficulty'] += 1
    if scoring_parameters['no_free']:
        for boss in ['waterhag', 'mombomb', 'milon', 'guard', 'darkimp', 'darkelf']:
            stats_weights[boss].update({'difficulty' : 1})
        stats_weights['kingqueen'].update({'difficulty' : (1 if scoring_parameters['boss_spellpower'] else 0.4)})
        stats_weights['mirrorcecil'].update({'difficulty' : 1.5})
    if scoring_parameters['thehades'] and scoring_parameters['boss_spellpower']:
        stats_weights['kingqueen']['difficulty'] += 0.3
    if scoring_parameters['unsafe']:
        if scoring_parameters['whichburn']:
            stats_weights['wyvern']['difficulty'] += 0.2
        if scoring_parameters['whichbez']:
            stats_weights['golbez']['difficulty'] += 0.2
    if scoring_parameters['no_veils_shops']: # plague, wyvern, bahamut, golbez, asura, leviatan, dlunar
        for boss in ['asura', 'leviatan', 'plague', 'dlunar']:
            stats_weights[boss]['difficulty'] += 0.2
        stats_weights['bahamut'].update({
            'hp' : 20,
            'speed' : 50,
            'difficulty' : 1
        })
        stats_weights['golbez']['difficulty'] += 0.3
        if not (scoring_parameters['whichburn'] or scoring_parameters['itburns'] or scoring_parameters['whyburn']):
            stats_weights['wyvern']['difficulty'] += 0.3
    if scoring_parameters['no_life_shops']:
        stats_weights['wyvern']['difficulty'] += 0.2
        if not scoring_parameters['whybez'] and not scoring_parameters['whichbez']:
            stats_weights['golbez']['difficulty'] += 0.2
    if scoring_parameters['whybez'] and not scoring_parameters['whichbez']:
        stats_weights['golbez']['difficulty'] -= 0.2

    return stats_weights

def _get_pairing_score(slot, boss, rankings_data, stats_weights, scoring_parameters):
    if boss == 'fabulgauntlet' and scoring_parameters['alt_gauntlet']:
        score = ALT_GAUNTLET_WEIGHTS[slot] + 7
        if slot == 'ogopogo_slot':
            score += 5
    else:
        weights_vector = {}
        for stat in ['speed', 'spell power', 'attack', 'hp', 'level', 'magic defense', 'defense']:
            weights_vector[stat] = stats_weights[boss][stat]
        if not scoring_parameters['boss_spellpower'] and slot in ZERO_SPELL_POWER_SLOTS:
            # swap spell power and level weights, because level impacts the spell power, not the slot's spell power ranking
            weights_vector.update({
                'level' : stats_weights[boss]['spell power'],
                'spell power' : stats_weights[boss]['level'],
            })
        score = stats_weights[boss]['difficulty'] * sum(
            [(weights_vector[stat]/100) * rankings_data[slot][stat] for stat in ['speed', 'spell power', 'attack', 'hp', 'level', 'magic defense', 'defense']]
            )
        if scoring_parameters['unsafe']:
            # add some weight to the normally-prevented bosses in overworld spots that could gate underground access, to encourage Bunsafe behaviour
            # ... needs to be modified a bit for starting underground, of course
            if slot in (UNDERWORLD_PROGRESSION_FIGHT_SLOTS if scoring_parameters['start_dwarf'] else OVERWORLD_PROGRESSION_FIGHT_SLOTS):
                if boss in ['valvalis', 'golbez', 'wyvern']: # Kainazzo on 5.0
                    score += 12
                if boss == 'mirrorcecil' and scoring_parameters['no_free']:
                    score += 12
    if slot == 'milonz_slot':
        if boss in ['golbez', 'plague', 'fabulgauntlet', 'magus']:
            score += 5
        if not scoring_parameters['jump_available'] and boss == 'valvalis':
            score += 5      

    return score  

def _try_allowed_boss_swap(env, assignment, slot_lookup, bosses, stats_slots, 
                           rankings_data, stats_weights, scoring_parameters,
                           removed_boss_slots, restricted_boss_slots, 
                           objective_bosses_and_maybe_dmist, filter):
    # idea: we cannot swap a required boss in an unrestricted slot with a non-required boss in a restricted slot or a removed slot,
    # but we can make any other swap, because:
    # 1. a required boss in a restricted slot means there are no non-required bosses in unrestricted slots, so the only
    # swaps are this required boss with another required boss or with another boss in a restricted slot, and
    # 2. swapping with a non-required boss in an unrestricted slot is fine.
    two_bosses = env.rnd.sample(bosses, k=2)
    b0 = two_bosses[0]
    b1 = two_bosses[1]
    # if a boss is required, then it isn't in a removed slot
    if ((b0 in objective_bosses_and_maybe_dmist and slot_lookup[b0] not in restricted_boss_slots) and
        (b1 not in objective_bosses_and_maybe_dmist and (slot_lookup[b1] in restricted_boss_slots or slot_lookup[b1] in removed_boss_slots))):
            return
    elif ((b1 in objective_bosses_and_maybe_dmist and slot_lookup[b1] not in restricted_boss_slots) and
          (b0 not in objective_bosses_and_maybe_dmist and (slot_lookup[b0] in restricted_boss_slots or slot_lookup[b0] in removed_boss_slots))):
            return
    
    # now that we've confirmed that in principle we can make this swap, check for scoring in/decrease
    num_in_assignment = 2
    unavailable_slots = removed_boss_slots.union(set(['none']))
    for b in two_bosses:
        if slot_lookup[b] in unavailable_slots:
            num_in_assignment -= 1
    make_swap = False
    if num_in_assignment == 0:
        return
    elif num_in_assignment == 1:
        if slot_lookup[b0] in unavailable_slots:
            b_in_slot = b1
            b_not_in_slot = b0
        else:
            b_in_slot = b0
            b_not_in_slot = b1
        old_score = _get_pairing_score(stats_slots[slot_lookup[b_in_slot]], b_in_slot, rankings_data, stats_weights, scoring_parameters)
        new_score = _get_pairing_score(stats_slots[slot_lookup[b_in_slot]], b_not_in_slot, rankings_data, stats_weights, scoring_parameters)
        if filter == 'friendly':
            if new_score < old_score:
                make_swap = True
        else:
            if new_score > old_score:
                make_swap = True
        if make_swap:
            # print(f"Swapping {b_in_slot} in {slot_lookup[b_in_slot]} with {b_not_in_slot} in {slot_lookup[b_not_in_slot]}"
            #       + (" **********" if slot_lookup[b_not_in_slot] == 'none' else ""))
            assignment.update({
                slot_lookup[b_in_slot] : b_not_in_slot
            })
            if slot_lookup[b_not_in_slot] != 'none':
                assignment.update({
                    slot_lookup[b_not_in_slot] : b_in_slot
                })
            slot_lookup.update({
                b_in_slot : slot_lookup[b_not_in_slot],
                b_not_in_slot : slot_lookup[b_in_slot]
            })
    else:
        old_score = (_get_pairing_score(stats_slots[slot_lookup[b0]], b0, rankings_data, stats_weights, scoring_parameters)
                     + _get_pairing_score(stats_slots[slot_lookup[b1]], b1, rankings_data, stats_weights, scoring_parameters))
        new_score = (_get_pairing_score(stats_slots[slot_lookup[b0]], b1, rankings_data, stats_weights, scoring_parameters)
                     + _get_pairing_score(stats_slots[slot_lookup[b1]], b0, rankings_data, stats_weights, scoring_parameters))
        if filter == 'friendly':
            if new_score < old_score:
                make_swap = True
        else:
            if new_score > old_score:
                make_swap = True
        if make_swap:
            # print(f"Swapping {b0} in {slot_lookup[b0]} with {b1} in {slot_lookup[b1]}")
            assignment.update({
                slot_lookup[b0] : b1,
                slot_lookup[b1] : b0
            })
            slot_lookup.update({
                b0 : slot_lookup[b1],
                b1 : slot_lookup[b0]
            })

def _get_scored_placement(env, slots, stats_slots, bosses, slot_rankings, stats_weights, scoring_parameters, leftover_bosses,
                          removed_boss_slots, restricted_boss_slots, objective_bosses_and_maybe_dmist, boss_mode):
    # set up slot-boss scores, and sort in ascending order
    # ignore removed slots; handle at the end
    zone_removed_slots = [s for s in removed_boss_slots if s in slots]
    slot_boss_pairing_values = []
    for slot in [s for s in slots if s not in zone_removed_slots]:
        for boss in bosses:
            score = _get_pairing_score(stats_slots[slot], boss, slot_rankings, stats_weights, scoring_parameters)
            # randomly add some noise (-10 to 10, obviously can change) to the score, clamp to [5,45] (min, max can also change)
            score += (env.rnd.random() - 0.5) * 2 * 10
            score = max(5,min(45,score))

            slot_boss_pairing_values.append((slot, boss, score))
            # print(slot + ' - ' + boss + ' : ' + f'{weight}')            

    slot_boss_pairing_values.sort(key=(lambda s: s[2]))
    # for t in slot_boss_pairing_values:
    #     print(t[0] + ' - ' + t[1] + ' : ' + f'{t[2]}')

    # idea: place required bosses first, randomly shifting down some slots to avoid placing them too highly.
    assignment = {}
    required_bosses = [b for b in bosses if b in objective_bosses_and_maybe_dmist]
    available_unrestricted_boss_slots = [s for s in slots if s not in removed_boss_slots and s not in restricted_boss_slots]
    remaining_boss_slots = [s for s in slots if s not in zone_removed_slots]
    remaining_required_bosses = [b for b in required_bosses]

    # first, put as many required bosses into available unrestricted slots as possible
    required_available_slot_boss_pairs = [t for t in slot_boss_pairing_values if t[1] in required_bosses and t[0] in available_unrestricted_boss_slots]
    while required_available_slot_boss_pairs:
        desired_pair = required_available_slot_boss_pairs[-1]
        pair_options = [t for t in required_available_slot_boss_pairs if t[1] == desired_pair[1]]
        orig_idx = slot_boss_pairing_values.index(desired_pair)
        bosses_until_desired_pair = []
        slots_until_desired_pair = []
        # scan through the big list to see roughly how many bosses/slots we'd take first before this pair
        for i in range(len(slot_boss_pairing_values)-1,orig_idx,-1):
            t = slot_boss_pairing_values[i]
            if t[1] == boss:
                break
            if t[0] not in slots_until_desired_pair:
                slots_until_desired_pair.append(t)
            if t[1] not in bosses_until_desired_pair:
                bosses_until_desired_pair.append(t)
        m = min(len(slots_until_desired_pair), len(bosses_until_desired_pair), len(pair_options)-1)
        if boss_mode == 'easy':
            # look from the bottom and subtract from m the number of slot pairs that would not have been removed
            m = max(0,m-len([p for p in pair_options[:(m+1)] if p[0] not in slots_until_desired_pair]))
        # pick a random number of slots (in [m // 2, m]) to pass by, to simulate having picked other bosses first
        skip_n_slots = env.rnd.randrange(m // 2, m+1)
        chosen_idx = (skip_n_slots if boss_mode == 'easy' else -(1+skip_n_slots))
        chosen_pair = pair_options[chosen_idx]
        assignment[chosen_pair[0]] = chosen_pair[1]
        # prune the slot-boss pairs, to start over
        slot_boss_pairing_values = [t for t in slot_boss_pairing_values if t[0] != chosen_pair[0] and t[1] != chosen_pair[1]]
        required_available_slot_boss_pairs = [t for t in required_available_slot_boss_pairs if t[0] != chosen_pair[0] and t[1] != chosen_pair[1]]
        remaining_boss_slots.remove(chosen_pair[0])
        remaining_required_bosses.remove(chosen_pair[1])

    # now, two cases: either we have placed all required bosses, or we have at least one left and we ran out of unrestricted slots
    # once we handle all remaining required bosses, then we have no restrictions on placement, so do that first
    if remaining_required_bosses:
        required_boss_remaining_pairs = [t for t in slot_boss_pairing_values if t[0] in remaining_boss_slots and t[1] in remaining_required_bosses]
        while required_boss_remaining_pairs:
            pair_to_assign = required_boss_remaining_pairs[-1]
            if boss_mode == 'easy':
                pairs_with_boss = [t for t in required_boss_remaining_pairs if t[1] == pair_to_assign[1]]
                pair_to_assign = pairs_with_boss[0]
            assignment[pair_to_assign[0]] = pair_to_assign[1]
            required_boss_remaining_pairs = [t for t in required_boss_remaining_pairs if t[0] != pair_to_assign[0] and t[1] != pair_to_assign[1]]
            remaining_boss_slots.remove(pair_to_assign[0])

    # all remaining bosses are not required; if we've run out of slots, then all that's left are removed slots/bosses not in the seed
    remaining_pairs = [t for t in slot_boss_pairing_values if t[0] in remaining_boss_slots and t[1] not in required_bosses]
    # special case: on Beasy, we tend to end up with KQ Eblan/a weak boss *excluded* if we don't intentionally remove a harder boss first. 
    while remaining_pairs:
        pair_to_assign = remaining_pairs[-1]
        if boss_mode == 'easy':
            pairs_with_boss = [t for t in remaining_pairs if t[1] == pair_to_assign[1]]
            pair_to_assign = pairs_with_boss[0]
        assignment[pair_to_assign[0]] = pair_to_assign[1]
        remaining_pairs = [t for t in remaining_pairs if t[0] != pair_to_assign[0] and t[1] != pair_to_assign[1]]        

    if zone_removed_slots:
        # it doesn't matter how these slots are assigned; just do it randomly
        # on Beasy, we've pre-assigned the leftover_bosses; on Bcruel, get the unused ones
        if not leftover_bosses:
            leftover_bosses = [b for b in bosses if b not in assignment.values()]
        # print("Leftover bosses in this zone:")
        # print(leftover_bosses)
        for i,s in enumerate(zone_removed_slots):
            assignment[s] = leftover_bosses[i]

    return assignment

QUEST_REWARD_CURVES = {
    'Ungated_Quest' : [
        RewardSlot.starting_item,
        RewardSlot.antlion_item,
        RewardSlot.fabul_item,
        RewardSlot.ordeals_item,
        RewardSlot.baron_inn_item,
        RewardSlot.toroia_hospital_item,
        RewardSlot.rydias_mom_item,
    ],

    'Gated_Quest' : [
        RewardSlot.baron_castle_item,
        RewardSlot.magnes_item,
        RewardSlot.zot_item,
        RewardSlot.babil_boss_item,
        RewardSlot.cannon_item,
        RewardSlot.luca_item,
        RewardSlot.sealed_cave_item,
        RewardSlot.found_yang_item,
        RewardSlot.pan_trade_item,
        RewardSlot.feymarch_item,
        RewardSlot.rat_trade_item,
        RewardSlot.pink_trade_item,
        RewardSlot.sylph_item,
        RewardSlot.feymarch_queen_item,
        RewardSlot.feymarch_king_item,
        RewardSlot.baron_throne_item,
        RewardSlot.forge_item,
        RewardSlot.dwarf_hospital_item,
    ],

    'Moon_Quest' : [
        RewardSlot.bahamut_item,
        RewardSlot.lunar_boss_1_item,
        RewardSlot.lunar_boss_2_item,
        RewardSlot.lunar_boss_3_item,
        RewardSlot.lunar_boss_4_item_1,
        RewardSlot.lunar_boss_4_item_2,
        RewardSlot.lunar_boss_5_item,
    ]
}

default_item_reward = ItemReward('#item.Cure1')

def apply(env):
    if (env.options.flags.has('no_free_key_item_package')):
        ITEM_SLOTS[RewardSlot.rydias_mom_item] = ['#item.Package?']

    if env.options.flags.has('starting_blackchocobo'):
        # add the Enterprise as a restriction for using the Hook
        for slot_group in [ITEM_SLOTS, SUMMON_QUEST_SLOTS, MOON_BOSS_SLOTS, CHEST_ITEM_SLOTS, BOSS_SLOTS]:
            for slot in slot_group:
                if '#item.fe_Hook?' in slot_group[slot]:
                    slot_group[slot].insert(0, 'enterprise?')
                    
        # Antlion Nest and Waterfall Cave require you to go through Mist Cave, or
        # else have the Enterprise; the latter requirement will be dealt with later
        ITEM_SLOTS[RewardSlot.antlion_item].insert(0, 'dmist_slot')
        BOSS_SLOTS['antlion_slot'] = ['dmist_slot']
        BOSS_SLOTS['octomamm_slot'] = ['dmist_slot']

    elif env.options.flags.has('starting_underground'):
        # we need to modify all of the item slot dependencies, because by starting underground,
        # we have removed that dependency but have *added* getting 'aboveground' as requirement for some checks
        for slot_group in [ITEM_SLOTS, SUMMON_QUEST_SLOTS, MOON_BOSS_SLOTS, CHEST_ITEM_SLOTS, BOSS_SLOTS]:
            for slot in slot_group:
                if 'underground?' in slot_group[slot]:
                    slot_group[slot].remove('underground?')
                elif not (slot == RewardSlot.starting_item):
                    slot_group[slot].insert(0, 'aboveground?')

                if '#item.fe_Hook?' in slot_group[slot]:
                    slot_group[slot].insert(0, 'enterprise')

        # fix up special cases: the Sheila checks need you to go above ground
        ITEM_SLOTS[RewardSlot.found_yang_item] = ['aboveground?']
        ITEM_SLOTS[RewardSlot.pan_trade_item].insert(0, 'aboveground?')

    treasure_dbview = databases.get_treasure_dbview()
    treasure_dbview.refine(lambda t: not t.exclude)

    items_dbview = databases.get_items_dbview()
    treasure_rando.refineItemsView(items_dbview, env)

    unsafe = False
    if env.options.flags.has('key_items_unsafe') or env.options.flags.has('key_items_unsafer'):
        unsafe = True

    keyitem_assigner = priority_assigner.PriorityAssigner()

    # slot tiers:
    #  0 - slots allowed to contain progression items, other than MIABs
    #  1 - MIABs allowed to contain progression items
    #  2 - slots without progression items but with good stuff
    #  3 - remaining slots

    # item tiers:
    #  0 - items that cannot be in MIABs under any circumstances ... which nothing uses now, probably.
    #  1 - progression items
    #  2 - non-progression key items
    #  3 - good non-progression items
    #  4 - less good non-progression items ... which nothing uses.

    keyitem_assigner.item_tier(0).set_max_slot_bucket(0)
    keyitem_assigner.item_tier(1).set_max_slot_bucket(1)
    keyitem_assigner.item_tier(2).set_max_slot_bucket(2)
    keyitem_assigner.item_tier(3).set_max_slot_bucket(2)

    keyitem_assigner.slot_tier(0).extend(ITEM_SLOTS)
    if not env.options.flags.has('key_item_from_forge'):
        keyitem_assigner.slot_tier(0).remove(RewardSlot.forge_item)
    if not env.options.flags.has('key_item_from_pink_tail'):
        keyitem_assigner.slot_tier(0).remove(RewardSlot.pink_trade_item)
    if env.options.flags.has('no_free_key_item_dwarf'):
        keyitem_assigner.slot_tier(0).remove(RewardSlot.toroia_hospital_item)
        keyitem_assigner.slot_tier(0).remove(RewardSlot.rydias_mom_item)
    elif env.options.flags.has_any('no_free_key_item', 'no_free_key_item_package'):
        keyitem_assigner.slot_tier(0).remove(RewardSlot.toroia_hospital_item)
        keyitem_assigner.slot_tier(0).remove(RewardSlot.dwarf_hospital_item)
    else:
        keyitem_assigner.slot_tier(0).remove(RewardSlot.rydias_mom_item)
        keyitem_assigner.slot_tier(0).remove(RewardSlot.dwarf_hospital_item)

    keyitem_assigner.item_tier(1).extend(ESSENTIAL_KEY_ITEMS)
    keyitem_assigner.item_tier(2).extend(NONESSENTIAL_KEY_ITEMS)

    if env.options.flags.has('pass_in_key_items') and not env.options.flags.has('key_items_start_pass'):
        keyitem_assigner.item_tier(1).append(ItemReward('#item.Pass'))

    forced_hook_route = env.options.flags.has('key_items_force_hook')
    has_magma_key = True
    # assign gated objective item and metadata
    gated_objective_item = env.meta['gated_objective_reward']           
    if '#' not in gated_objective_item:
        env.add_substitution('has gated objective', '')
    else:
        # Remove both methods of underground access when magma is specified
        if gated_objective_item == "#item.Magma":
            forced_hook_route = True
            has_magma_key = False
        elif gated_objective_item == "#item.fe_Hook":
            forced_hook_route = False
        keyitem_assigner.remove_item(gated_objective_item)
        env.meta['gated_objective_reward'] = gated_objective_item
        env.add_substitution('no gated objective', '')

    forced_starting_key_item = ''
    for f in env.options.flags.get_list(rf'^Kstart:'):
        if f == 'Kstart:zonk':
            keyitem_assigner.slot_tier(0).remove(RewardSlot.starting_item)
            keyitem_assigner.slot_tier(3).append(RewardSlot.starting_item)
        else:
            forced_starting_key_item = STARTING_ITEM_MAP[f]
            keyitem_assigner.slot_tier(0).remove(RewardSlot.starting_item)
            keyitem_assigner.remove_item(forced_starting_key_item)
        break

    if env.meta.get('has_objectives', False) and env.meta.get('zeromus_required', True):
        keyitem_assigner.item_tier(1).remove(KeyItemReward('#item.Crystal'))
        if env.options.flags.has('objective_mode_classicforge'):
            keyitem_assigner.item_tier(3).append(ItemReward('#item.Excalibur'))

    if env.options.flags.has('key_item_from_forge'):
        keyitem_assigner.item_tier(3).append(ItemReward('#item.Excalibur'))
    if env.options.flags.has('key_item_from_pink_tail') and not env.options.flags.has('no_adamants'):
        keyitem_assigner.item_tier(3).append(ItemReward('#item.AdamantArmor'))

    for item in env.meta.get('objective_required_key_items', []):
        reward = KeyItemReward(item)
        for item_tier in range(2, 4):
            if reward in keyitem_assigner.item_tier(item_tier):
                keyitem_assigner.item_tier(item_tier).remove(reward)
                keyitem_assigner.item_tier(1).append(reward)
                break

    keyitem_capable_fight_slots = []
    keyitem_incapable_fight_slots = []
    moon_fight_slots_available = False

    if env.options.flags.has('key_items_in_summon_quests'):
        keyitem_capable_fight_slots.extend(SUMMON_QUEST_SLOTS)
        moon_fight_slots_available = True
    else:
        keyitem_incapable_fight_slots.extend(SUMMON_QUEST_SLOTS)

    if env.options.flags.has('key_items_in_moon_bosses'):
        keyitem_capable_fight_slots.extend(MOON_BOSS_SLOTS)
        moon_fight_slots_available = True
    else:
        keyitem_incapable_fight_slots.extend(MOON_BOSS_SLOTS)

    env.rnd.shuffle(keyitem_capable_fight_slots)
    if not env.options.flags.has('key_items_unweighted'):
        num_privileged_fight_slots = int(math.ceil(len(keyitem_capable_fight_slots) / 2))

        # limit the number of fight slots that may contain key items according to probability curve
        r = env.rnd.random()
        while r < 0.5:
            num_privileged_fight_slots += 1
            r *= 2.0

        keyitem_assigner.slot_tier(0).extend(keyitem_capable_fight_slots[:num_privileged_fight_slots])
        keyitem_assigner.slot_tier(2).extend(keyitem_capable_fight_slots[num_privileged_fight_slots:])
    else:
        # every possible KI capable fight slot gets a uniform chance
        keyitem_assigner.slot_tier(0).extend(keyitem_capable_fight_slots)

    keyitem_assigner.slot_tier(3).extend(keyitem_incapable_fight_slots)

    # limit the number of MIABs that may contain key items according to probability curve
    # Kmiab granularity: instead of splitting it up into LST and not-LST, split into "above ground", "below ground", and LST
    # also pre-process to handle "standard" and "all" (according to Kunsafe/moon in the case of standard); "all" takes priority
    # over "standard", which takes priority over the subsets. CHEST_ITEM_SLOT_GROUPS is modified to be tuples containing the
    # broad grouping information (which is why a list comprehension is necessary to pick out the groups).
    # potential_miabs is to be used later, for hinting purposes/etc.

    # need to strip off 'Kmiab:' from the potentially multiple flags, so can't just use get_suffix (only gets the first)
    miab_flags = [flag[6:] for flag in env.options.flags.get_list('Kmiab:')]
    if miab_flags:
        good_miab_groups = []
        bad_miab_groups = []
        if 'all' in miab_flags:
            good_miab_groups.extend([group for group, flag in CHEST_ITEM_SLOT_GROUPS])
        elif 'standard' in miab_flags:
            if env.options.flags.has('key_items_in_moon_bosses') or unsafe:
                good_miab_groups.extend([group for group, flag in CHEST_ITEM_SLOT_GROUPS])
            else:
                good_miab_groups.extend([group for group, flag in CHEST_ITEM_SLOT_GROUPS if flag != 'lst'])
                bad_miab_groups.extend([group for group, flag in CHEST_ITEM_SLOT_GROUPS if flag == 'lst'])
        else:
            good_miab_groups.extend([group for group, flag in CHEST_ITEM_SLOT_GROUPS if flag in miab_flags])
            bad_miab_groups.extend([group for group, flag in CHEST_ITEM_SLOT_GROUPS if flag not in miab_flags])

        good_miabs = []
        bad_miabs = []
        potential_miabs = []
        if not env.options.flags.has('key_items_unweighted'):
            # limit the number of MIABs that may contain key items according to probability curve
            max_good_per_area = 2
            r = env.rnd.random()
            while r < 0.5:
                max_good_per_area += 1
                r *= 2.0
            
            for group in good_miab_groups:
                potential_miabs.extend(group)
                if len(group) > max_good_per_area:
                    group = list(group)
                    env.rnd.shuffle(group)
                    good_miabs.extend(group[:max_good_per_area])
                    bad_miabs.extend(group[max_good_per_area:])
                else:
                    good_miabs.extend(group)

            for group in bad_miab_groups:
                bad_miabs.extend(group)

            if 'all' in miab_flags or 'standard' in miab_flags or len(miab_flags) != 1:
                env.rnd.shuffle(good_miabs)
                if env.options.flags.has('key_items_unsafer') and not moon_fight_slots_available:
                    def ensure_moon(miab_list):
                        ensured = False
                        for slot in miab_list:
                            if 'moon?' in CHEST_ITEM_SLOTS[slot]:
                                if (slot == RewardSlot.giant_chest and env.options.flags.has('vanilla_giant')
                                    and not env.options.flags.has_any('bosses_unsafe', 'vanilla_bosses')):
                                    continue
                                else:
                                    ensured = True
                                    break
                        return ensured
                    while not ensure_moon(good_miabs[3:]):
                        env.rnd.shuffle(good_miabs)
                    bad_miabs.extend(good_miabs[:3])
                    good_miabs = good_miabs[3:]
                else:
                    bad_miabs.extend(good_miabs[:3])
                    good_miabs = good_miabs[3:]

        else:
            for group in good_miab_groups:
                good_miabs.extend(group)
                potential_miabs.extend(group)
            for group in bad_miab_groups:
                bad_miabs.extend(group)
        keyitem_assigner.slot_tier(1).extend(good_miabs)
        keyitem_assigner.slot_tier(3).extend(bad_miabs) 

    else:
        keyitem_assigner.slot_tier(3).extend(CHEST_ITEM_SLOTS)

    ## Deprecated no_magma code, preserving in case of future implementation.
    # if env.options.flags.has('key_items_no_magma'):
    #     keyitem_assigner.item_tier(1).remove(KeyItemReward('#item.Magma'))
    #     layout = '"Package  SandRuby   [lightsword]Legend"      [[ 01 ]]\n        "[key]Baron   [harp]TwinHarp  [crystal]Earth" [[ 01 ]]\n        "         [key]Tower     Hook"            [[ 01 ]]\n        "[key]Luca    [crystal]Darkness  [tail]Rat"   [[ 01 ]]\n        "Adamant  Pan        [knife]Spoon"            [[ 01 ]]\n        "[tail]Pink    [crystal]Crystal"              [[ 00 ]]'
    #     env.add_substitution('tracker layout', layout)

    # ... but we can still use the substitution to handle the renaming of Hook to Drill!
    if env.options.flags.has('starting_underground'):
        layout = '''        "Package  SandRuby   [lightsword]Legend"      [[ 01 ]]\n        "[key]Baron   [harp]TwinHarp  [crystal]Earth" [[ 01 ]]\n        "[key]Magma   [key]Tower     Drill"            [[ 01 ]]\n        "[key]Luca    [crystal]Darkness  [tail]Rat"   [[ 01 ]]\n        "Adamant  Pan        [knife]Spoon"            [[ 01 ]]\n        "[tail]Pink    [crystal]Crystal"              [[ 00 ]]
        '''
        env.add_substitution('tracker layout', layout) 

        # also update the item description data while we're at it, since the Drill text should say something else
        drill_description_row1 = '[$00][$fa]Drill                       [$fb][$00]'
        drill_description_row2 = '[$00][$fa]Allows the Falcon to        [$fb][$00]'
        drill_description_row3 = '[$00][$fa]dig up to the Overworld.    [$fb][$00]'
        env.meta.setdefault('item_description_overrides', {})[0xFC] = encode_text(drill_description_row1 
                                                                                  + drill_description_row2 
                                                                                  + drill_description_row3 
                                                                                  + '[$00][$fa]                            [$fb][$00]')

    if env.options.flags.has('key_items_force_magma'):
        prevent_hook_seed = True
    elif not (env.options.flags.has_any('key_items_in_summon_quests', 'key_items_in_moon_bosses') or miab_flags) and not forced_hook_route:
        prevent_hook_seed = (env.rnd.random() < 0.5)
    else:
        prevent_hook_seed = False

    # need to possibly modify HOOK_UNDERGROUND_BRANCH in case the KQ Eblan slot isn't fought
    if env.options.flags.has('no_kingqueen_slot'):
        HOOK_UNDERGROUND_BRANCH.remove('kingqueen_slot')

    # set up boss assignment parameters
    removed_boss_slots = set()
    if env.options.flags.has('no_officer_slot'):
        removed_boss_slots.add('officer_slot')
    if env.options.flags.has('no_kingqueen_slot'):
        removed_boss_slots.add('kingqueen_slot')
    restricted_boss_slots = set()
    if env.options.flags.has('bosses_no_required_at_summon'):
        restricted_boss_slots.update({'asura_slot', 'leviatan_slot', 'odin_slot', 'bahamut_slot'})
    if env.options.flags.has('bosses_no_required_on_moon'):
        restricted_boss_slots.update({'bahamut_slot', 'paledim_slot', 'wyvern_slot', 'plague_slot', 'dlunar_slot', 'ogopogo_slot'})
    if env.options.flags.has('bosses_no_required_in_zot'):
        restricted_boss_slots.update({'magus_slot', 'valvalis_slot'})
    if env.options.flags.has('bosses_no_required_on_hook'):
        restricted_boss_slots.update({'kingqueen_slot', 'rubicant_slot'})
    if env.options.flags.has('bosses_no_required_in_giant'):
        restricted_boss_slots.update({'elements_slot', 'cpu_slot'})
    if env.options.flags.has('bosses_no_required_in_sealedcave'):
        restricted_boss_slots.update({'evilwall_slot'})
    if env.options.flags.has('bosses_no_required_at_package'):
        restricted_boss_slots.update({'officer_slot'})
    objective_bosses_and_maybe_dmist = env.meta['objective_required_bosses']
    if env.options.flags.has('no_free_key_item'):
        objective_bosses_and_maybe_dmist.add('dmist')    

    # perform assignment
    attempts = 0
    found_valid_assignment = False
    while not found_valid_assignment and attempts < MAX_RANDOMIZATION_ATTEMPTS:
        boss_assignment = {}
        rewards_assignment = RewardsAssignment()
        boss_stats_slots = {}

        # for restricted boss shuffle, define lists of zones; if no restriction, then it's just one list!
        # need to redo every time because bosses_by_zone's lists get modified
        if env.options.flags.has('bosses_within_zones'):
            slots_by_zone = {}
            bosses_by_zone = {}
            for zone in BOSS_LOCATION_ZONES:
                slots_by_zone[zone] = BOSS_LOCATION_ZONES[zone]
                bosses_by_zone[zone] = [s[:-5] for s in slots_by_zone[zone]]
            bosses_by_zone['early_game'].append('waterhag')
            # for potential Beasy calculations later, ID the boss that doesn't correspond to a slot
            extra_boss = 'waterhag'
            # special case handling for bosses without slots (e.g. Waterhag, or Officer/KQ Eblan under Bremove);
            # to help the randomizer succeed in randomizing bosses, carve out subsets of bosses to use
            # (normally it's not that hard, because all the bosses are shuffled together)
            # notes: - early_game is 10-11 spots for 12 bosses, so *if* it's Knofree (normal) *and* Omode:fiends *and* Bremove:officer_slot *and*
            # all 8 specified objective bosses are from this zone, then we need to shuffle one of the required bosses to a different zone.
            # if summon_darkness is all restricted, then shift to gated_blue_planet, otherwise it doesn't matter. If Waterhag is required, move
            # Waterhag, otherwise pick one at random (and Waterhag will not be placed).
            # - gated_blue_planet is 11-12 spots for 12 bosses, so *if* it's Omode:fiends *and* all 8 objective bosses are from this zone,
            # then we're still fine.
            # - summon_darkness is 11 spots for 11 bosses, only one is a fiend; no special cases are required.
            # print(objective_bosses_and_maybe_dmist)
            # print(set(bosses_by_zone['early_game']).intersection(objective_bosses_and_maybe_dmist))
            if (env.options.flags.has('no_free_key_item') and env.options.flags.has('Omode:fiends') and env.options.flags.has('no_officer_slot')
                and len(set(bosses_by_zone['early_game']).intersection(objective_bosses_and_maybe_dmist)) > 10):
                # note that this can only happen if D.Mist is *not* an objective-required boss! if it doubles, then no big deal.
                if 'waterhag' in objective_bosses_and_maybe_dmist:
                    boss_to_move = 'waterhag'
                else:
                    boss_to_move = env.rnd.choice(list(set(bosses_by_zone['early_game']).intersection(objective_bosses_and_maybe_dmist)))
                    extra_boss = boss_to_move
                    # print(boss_to_move)
                bosses_by_zone['early_game'].remove(boss_to_move)
                if not set(slots_by_zone['summon_darkness']).difference(restricted_boss_slots):
                    # if every boss slot in the summon_darkness zone is restricted, put the shifting boss in the gated_blue_planet zone
                    # (which cannot only have restricted slots)
                    bosses_by_zone['gated_blue_planet'].append(boss_to_move)
                else:
                    bosses_by_zone[env.rnd.choice(['gated_blue_planet','summon_darkness'])].append(boss_to_move)
            # print(bosses_by_zone)
        else:
            slots_by_zone = {'all' : list(BOSS_SLOTS)}
            bosses_by_zone = {'all' : BOSSES.copy()}     

        # Assume no gated objective by default
        rewards_assignment[RewardSlot.gated_objective] = EmptyReward()

        # assign key items
        if env.options.flags.has('key_items_vanilla'):
            # vanilla assignment
            rewards_assignment[RewardSlot.fabul_item] = ItemReward('#item.BlackSword')
            rewards_assignment[RewardSlot.baron_castle_item] = (ItemReward('#item.Pass') if env.options.flags.has('pass_in_key_items') else EmptyReward())

            used_keyitems = set()
            for item in ESSENTIAL_KEY_ITEMS:
                if item.item == "#item.Crystal" and env.meta.get('has_objectives', False) and env.meta.get('zeromus_required', True):
                    continue
                    
                slot = ESSENTIAL_KEY_ITEMS[item]
                if slot:
                    if env.options.flags.has('no_free_key_item_dwarf') and slot == RewardSlot.toroia_hospital_item:
                        slot = RewardSlot.dwarf_hospital_item
                    if env.options.flags.has_any('no_free_key_item', 'no_free_key_item_package') and slot == RewardSlot.toroia_hospital_item:
                        slot = RewardSlot.rydias_mom_item
                    rewards_assignment[slot] = item
                    used_keyitems.add(item.item)
            for item in NONESSENTIAL_KEY_ITEMS:
                slot = NONESSENTIAL_KEY_ITEMS[item]
                if slot:
                    rewards_assignment[slot] = item
                    used_keyitems.add(item.item)

            if not set(env.meta.get('objective_required_key_items', [])).issubset(used_keyitems):
                raise Exception("Objective required key item is not present in vanilla key item assignment.")

            remaining_slots = []
            for slot_tier in range(4):
                for slot in keyitem_assigner.slot_tier(slot_tier):
                    if slot not in rewards_assignment:
                        remaining_slots.append(slot)
        else:
            if forced_starting_key_item != '':
                rewards_assignment[RewardSlot.starting_item] = KeyItemReward(forced_starting_key_item)
            keyitem_assignment, remaining_slots, remaining_items = keyitem_assigner.assign(env.rnd)
            rewards_assignment.update(keyitem_assignment)

        # shuffle boss slot stats; under Bremove, some slots might be unused, and that's fine
        # need to shuffle slots before assigning bosses for score-dependent assignments
        if env.options.flags.has('boss_slot_shuffle'):
            if env.options.flags.has('bosses_unsafe'):
                BOSS_SLOT_SHUFFLE_GROUPS['underworld'].remove('odin_slot')
                BOSS_SLOT_SHUFFLE_GROUPS['gated_overworld'].append('odin_slot')
            for group in BOSS_SLOT_SHUFFLE_GROUPS:
                shuffled_slots_in_group = BOSS_SLOT_SHUFFLE_GROUPS[group].copy()
                env.rnd.shuffle(shuffled_slots_in_group)
                for i, slot in enumerate(BOSS_SLOT_SHUFFLE_GROUPS[group]):
                    # key: visible slot, value: the new stats
                    boss_stats_slots[slot] = shuffled_slots_in_group[i]
        else:
            for slot in BOSS_SLOTS:
                boss_stats_slots[slot] = slot
        env.meta['boss_stats_slots'] = boss_stats_slots

        # assign bosses
        bosses_in_restricted_slots = set()
        bosses_in_removed_slots = set()
        if env.options.flags.has('bosses_vanilla'):
            # vanilla assignment; note that Bzones cannot be on, so use 'all'
            used_bosses = set()
            for k in slots_by_zone['all']:
                boss = k.replace('_slot', '')
                boss_assignment[k] = boss
                if not k in removed_boss_slots:
                    used_bosses.add(boss)
                    if k in restricted_boss_slots:
                        bosses_in_restricted_slots.add(boss)
                else:
                    bosses_in_removed_slots.add(boss)

            if not set(env.meta['objective_required_bosses']).issubset(used_bosses):
                raise Exception("Objective required boss is not present in vanilla boss assignment.")

        elif env.options.flags.has('bosses_standard'):
            for zone in slots_by_zone:
                temp_boss_assignment = _get_standard_boss_shuffle(env, slots_by_zone[zone], bosses_by_zone[zone], 
                                                                  removed_boss_slots, restricted_boss_slots, objective_bosses_and_maybe_dmist)
                for s in temp_boss_assignment:
                    boss_assignment[s] = temp_boss_assignment[s]
            for s in removed_boss_slots:
                bosses_in_removed_slots.add(boss_assignment[s])
            for s in restricted_boss_slots:
                bosses_in_restricted_slots.add(boss_assignment[s])

        else:
            # score-dependent assignment; set up all scoring parameters
            scoring_parameters = _set_scoring_parameters(env)
            # modify slot-independent weights according to flag info
            stats_weights = _set_stats_weights(scoring_parameters)
            # pull the correct slot stats ranks
            if env.options.flags.has_any('japanese_bosses', 'easy_type_bosses'):
                slot_rankings = (BOSS_SLOT_STATS_RANKINGS_J if env.options.flags.has('japanese_bosses') else BOSS_SLOT_STATS_RANKINGS_ET)
            else:
                slot_rankings = BOSS_SLOT_STATS_RANKINGS

            if env.options.flags.has_any('bosses_pro', 'bosses_friendly'):
                for zone in slots_by_zone:
                    # obtain a standard shuffle, then make a number of swaps, checking to ensure difficulty goes up or down
                    temp_boss_assignment = _get_standard_boss_shuffle(env, slots_by_zone[zone], bosses_by_zone[zone], 
                                                                    removed_boss_slots, restricted_boss_slots, objective_bosses_and_maybe_dmist)
                    # print(temp_boss_assignment)
                    slot_lookup = {}
                    for s in temp_boss_assignment:
                        slot_lookup[temp_boss_assignment[s]] = s
                    for b in [b for b in bosses_by_zone[zone] if b not in temp_boss_assignment.values() ]:
                        slot_lookup[b] = 'none'
                    for _ in range(NUM_SWAPS // len(slots_by_zone)):
                        _try_allowed_boss_swap(env, temp_boss_assignment, slot_lookup, bosses_by_zone[zone], boss_stats_slots, 
                                               slot_rankings, stats_weights, scoring_parameters, 
                                               removed_boss_slots, restricted_boss_slots, objective_bosses_and_maybe_dmist, 
                                               filter=('pro' if env.options.flags.has_any('bosses_pro') else 'friendly'))
                    for s in temp_boss_assignment:
                        boss_assignment[s] = temp_boss_assignment[s]

            elif env.options.flags.has_any('bosses_cruel', 'bosses_easy'):
                # need to handle placing objective bosses in a way that isn't too predictable;
                # possibly just placing them first but skipping a random number of slots to simulate not placing them first
                # also, on Beasy we need to pre-cull a "hard" boss to avoid having a boss like KQ always removed
                unused_bosses = {}
                for zone in bosses_by_zone:
                    unused_bosses[zone] = []
                if env.options.flags.has('bosses_easy'):
                    if len(bosses_by_zone) > 1:
                        # on Bzones, we remove bosses within the zones.
                        # first, no matter which zone the extra_boss (default Waterhag) is in, a boss from that zone is being removed
                        # then, for each Bremove flag, remove one boss from the appropriate zone
                        for zone in bosses_by_zone:
                            removable_bosses = [h for h in BEASY_DIFFICULTY if h not in objective_bosses_and_maybe_dmist and h in bosses_by_zone[zone]]
                            def remove_one_boss(env, removable_bosses, zone_bosses, unused_zone_bosses):
                                for b in removable_bosses:
                                    if env.rnd.random() < 0.3 or b == removable_bosses[-1]:
                                        zone_bosses.remove(b)
                                        unused_zone_bosses.append(b)
                                        break
                                removable_bosses = [h for h in removable_bosses if h not in unused_zone_bosses]
                            if extra_boss in bosses_by_zone[zone]:
                                remove_one_boss(env, removable_bosses, bosses_by_zone[zone], unused_bosses[zone])
                            if 'officer_slot' in removed_boss_slots and zone == 'early_game':
                                remove_one_boss(env, removable_bosses, bosses_by_zone[zone], unused_bosses[zone])
                            if 'kingqueen_slot' in removed_boss_slots and zone == 'gated_blue_planet':
                                remove_one_boss(env, removable_bosses, bosses_by_zone[zone], unused_bosses[zone])
                    else:
                        num_bosses_to_remove = 1 + len(removed_boss_slots)
                        removable_bosses = [h for h in BEASY_DIFFICULTY if h not in objective_bosses_and_maybe_dmist]
                        for b in removable_bosses:
                            if env.rnd.random() < 0.3:
                                bosses_by_zone['all'].remove(b)
                                unused_bosses['all'].append(b)
                                num_bosses_to_remove -= 1
                            elif b == removable_bosses[-num_bosses_to_remove]:
                                # if unlucky, we can get to the end of the list without removing enough bosses,
                                # so just remove the last ones
                                unused_bosses['all'].extend(removable_bosses[-num_bosses_to_remove:])
                                bosses_by_zone['all'] = bosses_by_zone['all'][:-num_bosses_to_remove]
                                num_bosses_to_remove = 0
                            if not num_bosses_to_remove:
                                break

                for zone in slots_by_zone:
                    temp_boss_assignment = _get_scored_placement(env, slots_by_zone[zone], boss_stats_slots, bosses_by_zone[zone], 
                                                                    slot_rankings, stats_weights, scoring_parameters, unused_bosses[zone],
                                                                    removed_boss_slots, restricted_boss_slots, objective_bosses_and_maybe_dmist,
                                                                    boss_mode=('cruel' if env.options.flags.has('bosses_cruel') else 'easy'))
                    for s in temp_boss_assignment:
                        boss_assignment[s] = temp_boss_assignment[s]

        # vanilla assignment has already updated these sets, but the other assignments haven't
        if not env.options.flags.has('bosses_vanilla'):   
            for s in removed_boss_slots:
                bosses_in_removed_slots.add(boss_assignment[s])
            for s in restricted_boss_slots:
                bosses_in_restricted_slots.add(boss_assignment[s])

        if DEBUG:
            print('assignment {}:'.format(attempts))
            for k in rewards_assignment:
                print('  {} <- {}'.format(k.name, rewards_assignment[k]))
            for k in boss_assignment:
                print('  {} <- {}'.format(k, boss_assignment[k]))
            print('remaining slots: {' + '\n'.join([s.name for s in remaining_slots]) + '}')

        # build dependency checker
        checker = dep_checker.DepChecker()
        def add_branch_with_substitutions(*steps):
            b = []
            for step in steps:
                if step in rewards_assignment:
                    if rewards_assignment[step] != EmptyReward():
                        b.append(rewards_assignment[step].item)
                elif step in boss_assignment:
                    b.append(boss_assignment[step])
                else:
                    b.append(step)
            checker.add_branch(*b)

        if env.options.flags.has('starting_blackchocobo'):
            add_branch_with_substitutions(*['enterprise?', 'antlion_slot'])
            add_branch_with_substitutions(*['enterprise?', 'octomamm_slot'])
            add_branch_with_substitutions(*['#item.Baron?', 'baigan_slot', 'kainazzo_slot', 'enterprise'])
            add_branch_with_substitutions(*['#item.DarkCrystal?', 'moon'])
            add_branch_with_substitutions(*['enterprise?', '#item.Magma?', 'underground'])
            if not prevent_hook_seed:
                add_branch_with_substitutions(*(['enterprise?'] + HOOK_UNDERGROUND_BRANCH))
        elif env.options.flags.has('starting_underground'):
            add_branch_with_substitutions(*['#item.fe_Hook?', 'aboveground'])
            add_branch_with_substitutions(*['aboveground?', '#item.Baron?', 'baigan_slot', 'kainazzo_slot', 'enterprise'])
            add_branch_with_substitutions(*['#item.DarkCrystal?', 'moon'])
        else:
            for branch in COMMON_BRANCHES:
                add_branch_with_substitutions(*branch)
            if not prevent_hook_seed:
                add_branch_with_substitutions(*HOOK_UNDERGROUND_BRANCH)

        
        if gated_objective_item != '':
            rewards_assignment[RewardSlot.gated_objective] = ItemReward(gated_objective_item,True)

        for slot in rewards_assignment:            
            if rewards_assignment[slot] == EmptyReward():
                continue

            if slot == RewardSlot.gated_objective:
                if gated_objective_item == "#item.Magma" or gated_objective_item == "#item.fe_Hook":
                    src_branch = ['moon?', 'underground']
                else:
                    continue
            elif slot in ITEM_SLOTS:
                src_branch = ITEM_SLOTS[slot]
            elif slot in SUMMON_QUEST_SLOTS:
                src_branch = SUMMON_QUEST_SLOTS[slot]
            elif slot in MOON_BOSS_SLOTS:
                src_branch = MOON_BOSS_SLOTS[slot]
            elif slot in CHEST_ITEM_SLOTS:
                src_branch = CHEST_ITEM_SLOTS[slot]

            add_branch_with_substitutions(*src_branch, rewards_assignment[slot].item)

        for slot in boss_assignment:        
            add_branch_with_substitutions(*BOSS_SLOTS[slot], boss_assignment[slot])

        checker.resolve()

        # make sure key items are all obtainable
        if DEBUG:
            print('testing reachability')
        tests = keyitem_assigner.item_tier(0).items + keyitem_assigner.item_tier(1).items
        tests = [reward.item for reward in tests]
        if env.options.flags.has('key_items_vanilla'):
            if '#item.Crystal' in tests:
                tests.remove('#item.Crystal')

        if env.options.flags.has('key_item_from_pink_tail'):
            tests.append('#item.Pink')

        if env.options.flags.has('starting_underground'):
            aboveground_path_disallowed = []
            # we'll still prevent you from having to go through awful fights, e.g. Valvalis at Calbrena,
            # but there are slightly fewer restrictions to get above ground
            if not env.options.flags.has('bosses_vanilla') and not env.options.flags.has('bosses_unsafe'):
                # leave Golbez, Wyvern, Valvalis, Bnofree Pain Man as mean, put no summon spots in because of possible exp
                mean_bosses = ['golbez', 'wyvern', 'valvalis']

                if env.options.flags.has('no_free_bosses'):
                    mean_bosses.append('mirrorcecil')

                aboveground_path_disallowed.extend(mean_bosses)    

            if aboveground_path_disallowed:
                tests.append(['aboveground', aboveground_path_disallowed])
                        
        else:
            underground_path_disallowed = []
            if not env.options.flags.has('bosses_vanilla') and not env.options.flags.has('bosses_unsafe'):
                # must be able to access underground without encountering, golbez, wyvern, valvalis or odin replacement
                # (or Dark Cecil in NFL2)
                # ... or having to go through the Giant bosses, on -vanilla:giant
                mean_bosses = ['golbez', 'wyvern', 'valvalis', boss_assignment['odin_slot']]

                if env.options.flags.has('no_free_bosses') and 'mirrorcecil' not in mean_bosses:
                    mean_bosses.append('mirrorcecil')
                    
                # obscure special case: if a mean boss is in Yang's slot, and
                #  DMist is in guard slot, and DMist gates underworld, then
                #  that's bad
                if env.options.flags.has('no_free_key_item') and boss_assignment['guard_slot'] == 'dmist' and boss_assignment['karate_slot'] in mean_bosses:
                    mean_bosses.append('dmist')

                # you should not have to go through the Giant to get your underground access from Last Arm (or D.Mist, obviously)
                # ... but, vanilla Elements and CPU are exploitable, like vanilla Odin is.
                if env.options.flags.has('vanilla_giant'):
                    mean_bosses.extend([boss_assignment['elements_slot'], boss_assignment['cpu_slot']])

                underground_path_disallowed.extend(mean_bosses)

            if not env.options.flags.has('key_items_vanilla') and not unsafe:
                # must be able to access underground without accessing moon
                underground_path_disallowed.append('moon')

            if env.options.flags.has('key_items_force_magma'):
                # bypass the prevent_hook_route code to directly rule out D.Mist at Rubicant,
                # so that not-Kforce:magma seeds can have uncertainty (and memes)
                underground_path_disallowed.append(boss_assignment['rubicant_slot'])

            if prevent_hook_seed:
                # you probably also shouldn't need to beat the boss with Rubi's stats;
                # we'll ensure this is the case whenever the Magma Key is ensured available
                if env.options.flags.has('boss_slot_shuffle'):
                    rubi_stats_slot = None
                    for slot in boss_stats_slots:
                        if boss_stats_slots[slot] == 'rubicant_slot':
                            rubi_stats_slot = slot
                            break
                    if (not (env.options.flags.has('no_kq_eblan_slot') and slot == 'kingqueen_slot')
                        and not (env.options.flags.has('no_officer_slot') and slot == 'officer_slot')):
                        underground_path_disallowed.append(boss_assignment[rubi_stats_slot])

            if underground_path_disallowed:
                tests.append(['underground', underground_path_disallowed])

            magma_path_forced = None 

            if env.options.flags.has('key_items_unsafer'):
                if not forced_hook_route:
                    magma_path_forced = 'moon'
                tests.append(['#item.fe_Hook', [], 'moon'])

            if forced_hook_route:
                magma_path_forced = 'underground'

            if magma_path_forced and has_magma_key:
                tests.append(['#item.Magma', [], magma_path_forced])

            if env.options.flags.has('key_items_late_darkness'):
                tests.append(['#item.DarkCrystal', [], 'underground'])

            if not unsafe and env.options.flags.has('key_items_unreliable_darkness') and (env.rnd.random() < 0.25):
                tests.append(['#item.DarkCrystal', [], 'underground'])

        # must be able to encounter all bosses required of forced objective flags (and possibly d.mist)
        tests.extend(list(objective_bosses_and_maybe_dmist))

        found_valid_assignment = True

        for test in tests:
            if type(test) is list:
                if len(test) == 3:
                    qualification, without, force = test
                else:    
                    qualification, without = test
            else:
                qualification = test
                without = []
                force = None

            result, path = checker.check(qualification, without=without, force=force)
            if not result:
                # item is unreachable, assignment fails
                if DEBUG > 1:
                    br = None
                    for b in checker._branches:
                        if b[-1] == str(qualification):
                            br = b
                            break
                    print(f"  FAILED: no path to {qualification}"  + (f", forcing {force}" if force else "") + (f", without {without}" if without else "") + f" ({br}" + ")")
                found_valid_assignment = False
                break            
            else:
                if DEBUG:
                    print('  {} : {}'.format(qualification, ', '.join(path)))

        attempts += 1

    if not found_valid_assignment:
        raise Exception("Failed to find valid assignment after too many attempts; aborting")

    if DEBUG:
        result, path = checker.check('#item.Magma', without=['#item.fe_Hook'])
        print(f"Hook seed? : {not result}")


    # assign remaining treasures now since they don't have dependency concerns
    if env.options.flags.has('treasure_shuffle') or env.options.flags.has('treasure_vanilla'):
        # Tvanilla acts like Tshuffle, except that only the K categories specified partake
        # in the shuffle, and unspecifed K categories get vanilla assignment

        is_vanilla = env.options.flags.has('treasure_vanilla')
        pool = []
        if is_vanilla and not env.options.flags.has('key_items_in_summon_quests'):
            for item in SUMMON_QUEST_ITEMS:
                slot = SUMMON_QUEST_ITEMS[item]
                if slot not in rewards_assignment:
                    rewards_assignment[slot] = item
        else:
            pool.extend(SUMMON_QUEST_ITEMS)

        if is_vanilla and not env.options.flags.has('key_items_in_moon_bosses'):
            for item in MOON_BOSS_ITEMS:
                slot = MOON_BOSS_ITEMS[item]
                if slot not in rewards_assignment:
                    rewards_assignment[slot] = item
        else:
            pool.extend(MOON_BOSS_ITEMS)
        
        if is_vanilla and not miab_flags:
            for slot in CHEST_NUMBERS:
                if slot not in rewards_assignment:
                    treasure = treasure_dbview.find_one(lambda t : [t.map, t.index] == CHEST_NUMBERS[slot])
                    rewards_assignment[slot] = ItemReward(treasure.jcontents if (treasure.jcontents and not env.options.flags.has('treasure_no_j_items')) else treasure.contents)
        else:
            for slot in CHEST_NUMBERS:
                treasure = treasure_dbview.find_one(lambda t : [t.map, t.index] == CHEST_NUMBERS[slot])
                pool.append(ItemReward(treasure.jcontents if (treasure.jcontents and not env.options.flags.has('treasure_no_j_items')) else treasure.contents))

        env.rnd.shuffle(pool)
        for slot_tier in range(4):
            for slot in keyitem_assigner.slot_tier(slot_tier):
                if slot not in rewards_assignment:
                    try:          
                        rewards_assignment[slot] = pool.pop()
                    except:
                        # Pnone + win:crystal causes an issue under Tvanilla | Tshuffle. This is a workaround to that.
                        # ... and, to prevent further issues, just always give the default reward, instead of nothing.
                        rewards_assignment[slot] = default_item_reward
    else:
        # revised Rivers rando
        if env.options.flags.has('treasure_vanillaish'):
            curves_dbview = databases.get_tvanillaish_dbview() if env.options.flags.has('treasure_no_j_items') else databases.get_tvanillaish_j_dbview()
        else:
            curves_dbview = databases.get_buffed_curves_dbview() if env.options.flags.has('treasure_buffed_pro_weights') else databases.get_curves_dbview()

        unassigned_quest_slots = [slot for slot in (list(ITEM_SLOTS) + list(SUMMON_QUEST_SLOTS) + list(MOON_BOSS_SLOTS)) if slot not in rewards_assignment]
        if env.options.flags.has('no_free_key_item_dwarf'):
            unassigned_quest_slots.remove(RewardSlot.toroia_hospital_item)
            unassigned_quest_slots.remove(RewardSlot.rydias_mom_item)
        elif env.options.flags.has_any('no_free_key_item', 'no_free_key_item_package'):
            unassigned_quest_slots.remove(RewardSlot.toroia_hospital_item)
            unassigned_quest_slots.remove(RewardSlot.dwarf_hospital_item)
        else:
            unassigned_quest_slots.remove(RewardSlot.rydias_mom_item)
            unassigned_quest_slots.remove(RewardSlot.dwarf_hospital_item)

        if not env.options.flags.has('key_item_from_forge'):
            unassigned_quest_slots.remove(RewardSlot.forge_item)
        if not env.options.flags.has('key_item_from_pink_tail'):
            unassigned_quest_slots.remove(RewardSlot.pink_trade_item)

        # for later, find items by tier (to see if there are any left)
        items_by_tier = {}
        for i in range(1,9):
            items_by_tier[i] = items_dbview.find_all(lambda it: it.tier == i)

        if env.options.flags.has('treasure_standard') or env.options.flags.has('treasure_wild'):
            low_tier = 6
            src_pool = items_dbview.find_all(lambda it: it.tier in range(low_tier, 9))
            while not src_pool:
                low_tier -= 1
                src_pool = items_dbview.find_all(lambda it: it.tier in range(low_tier, 9))
            pool = list(src_pool)
            while len(pool) < len(unassigned_quest_slots):
                pool.append(env.rnd.choice(src_pool))
            env.rnd.shuffle(pool)
            for slot in unassigned_quest_slots:
                rewards_assignment[slot] = ItemReward(pool.pop().const)
        else:
            for curve_name in QUEST_REWARD_CURVES:
                quest_curve = curves_dbview.find_one(lambda c: c.area == curve_name)
                unassigned_quest_slots_for_curve = [s for s in unassigned_quest_slots if s in QUEST_REWARD_CURVES[curve_name]]
                weights = {i : getattr(quest_curve, f"tier{i}") for i in range(1,9)}

                if env.options.flags.has('treasure_wild_weighted'):
                    weights = util.get_boosted_weights(weights, 'wildish')
                elif env.options.flags.has('treasure_semipro'):
                    weights = util.get_boosted_weights(weights, 'semipro')
                elif env.options.flags.has('treasure_standard_weighted'):
                    weights = util.get_boosted_weights(weights, 'standardish')

                # as written, quest rewards have their tiers pre-chosen, so if we want to avoid giving out many Cure1s,
                # we need to remove the weights for empty tiers, and then potentially assign a default tier if no weights are left
                # (this change brings the reward assignment more in line with vanilla FE 4.6/5.0... and also removes the need
                # for some of the sanity checking a bit later, but here we are)
                avg_curve_tier = sum([i*weights[i] for i in weights]) // sum([weights[i] for i in weights])
                for i in range(1,9):
                    if not items_by_tier[i]:
                        weights[i] = 0
                empty_weights = True
                for i in range(1,9):
                    if weights[i]:
                        empty_weights = False
                        break
                if empty_weights:
                    a = avg_curve_tier
                    b = avg_curve_tier
                    while empty_weights:
                        for i in range(a,b+1):
                            if items_by_tier[i]:
                                weights[i] = 1
                                empty_weights = False
                        if empty_weights:
                            a -= 1
                            b += 1

                quest_distribution = util.Distribution(weights)
                tier_counts = quest_distribution.choose_many(env.rnd, len(unassigned_quest_slots_for_curve))
                pool = []
                for tier in tier_counts:
                    if tier_counts[tier] <= 0:
                        continue

                    tier_src_pool = items_dbview.find_all(lambda it: it.tier == tier)
                    tier_pool = list(tier_src_pool)

                    if len(tier_pool) == 0:
                        continue

                    if len(tier_pool) > tier_counts[tier]:
                        tier_pool = env.rnd.sample(tier_pool, tier_counts[tier])
                    else:
                        while len(tier_pool) < tier_counts[tier]:
                            tier_pool.append(env.rnd.choice(tier_src_pool))
                    pool.extend(tier_pool)

                env.rnd.shuffle(pool)                
                for slot in unassigned_quest_slots_for_curve:
                    reward_to_insert = default_item_reward
                    if len(pool) > 0:
                        reward_to_insert = ItemReward(pool.pop().const)
                    rewards_assignment[slot] = reward_to_insert
            
            for slot in unassigned_quest_slots:
                if slot not in rewards_assignment:     
                    rewards_assignment[slot] = default_item_reward

        unassigned_chest_slots = [slot for slot in CHEST_ITEM_SLOTS if slot not in rewards_assignment]

        if not env.options.flags.has('characters_in_treasure_relaxed') and (env.options.flags.has('characters_in_treasure_earned') or env.options.flags.has('characters_in_treasure_free')):
            for target_slot in character_rando.RESTRICTED_SLOTS:                
                # Find the slot this character was assigned to                
                if (target_slot in character_rando.FREE_SLOTS and env.options.flags.has('characters_in_treasure_free') or
                    target_slot in character_rando.EARNED_SLOTS and env.options.flags.has('characters_in_treasure_earned')):
                    print(f'Putting restricted slot {target_slot} in a MIAB chest')
                    character_slot = character_rando.SLOTS[target_slot]
                    rnd_chest_slot = env.rnd.choice(unassigned_chest_slots)
                    rewards_assignment[rnd_chest_slot] = AxtorChestReward('#item.fe_CharacterChestItem#_'+"{:02d}".format(character_slot))
                    t = treasure_dbview.find_one(lambda t: [t.map, t.index] == CHEST_NUMBERS[rnd_chest_slot])
                    print(f'AxtorChestReward for slot {target_slot} {t.spoilerarea} - {t.spoilersubarea} - {t.spoilerdetail}')
                    unassigned_chest_slots.remove(rnd_chest_slot)
                        
        if env.options.flags.has('treasure_standard') or env.options.flags.has('treasure_wild'):
            # exclude HrGlass1 and HrGlass3 from MIAB items if HrGlass2 is excluded
            min_miab_tier = 5
            max_miab_tier = 98 if env.options.flags.has('treasure_standard') else 99
            # future-proofing the selection of src_pool items in case items are restricted to where tier 5 is impossible
            src_pool = items_dbview.find_all(lambda it: it.tier >= min_miab_tier and it.tier <= max_miab_tier)
            while not src_pool:
                min_miab_tier -= 1
                src_pool = items_dbview.find_all(lambda it: it.tier >= min_miab_tier and it.tier <= max_miab_tier)
            pool = list(src_pool)
            while len(pool) < len(unassigned_chest_slots):
                pool.append(env.rnd.choice(src_pool))

            env.rnd.shuffle(pool)
            for slot in unassigned_chest_slots:
                rewards_assignment[slot] = ItemReward(pool.pop().const)
        else:
            unassigned_chest_slots_by_area = {}
            for slot in unassigned_chest_slots:
                t = treasure_dbview.find_one(lambda t: [t.map, t.index] == CHEST_NUMBERS[slot])
                unassigned_chest_slots_by_area.setdefault(t.area, []).append(slot)

            miab_distributions = {}
            for c in curves_dbview.find_all(lambda c: c.area.startswith("MIAB_")):
                weights = {i : getattr(c, f"tier{i}") for i in range(1,9)}
                if env.options.flags.has('treasure_wild_weighted'):
                    weights = util.get_boosted_weights(weights, 'wildish')
                elif env.options.flags.has('treasure_semipro'):
                    weights = util.get_boosted_weights(weights, 'semipro')
                elif env.options.flags.has('treasure_standard_weighted'):
                    weights = util.get_boosted_weights(weights, 'standardish')

                # handle item restrictions per MIAB area, in the same way as for quests
                avg_c_tier = sum([i*weights[i] for i in weights]) // sum([weights[i] for i in weights])
                for i in range(1,9):
                    if not items_by_tier[i]:
                        weights[i] = 0
                empty_weights = True
                for i in range(1,9):
                    if weights[i]:
                        empty_weights = False
                        break
                if empty_weights:
                    a = avg_c_tier
                    b = avg_c_tier
                    while empty_weights:
                        for i in range(a,b+1):
                            if items_by_tier[i]:
                                weights[i] = 1
                                empty_weights = False
                        if empty_weights:
                            a -= 1
                            b += 1

                miab_distributions[c.area[len("MIAB_"):]] = util.Distribution(weights)

            tier_counts_by_area = {}
            total_tier_counts = {}
            for area in unassigned_chest_slots_by_area:
                raw_counts = miab_distributions[area].choose_many(env.rnd, len(unassigned_chest_slots_by_area[area]))
                tier_counts_by_area[area] = {}
                for tier in raw_counts:
                    tier_counts_by_area[area].setdefault(tier, 0)
                    tier_counts_by_area[area][tier] += raw_counts[tier]
                    total_tier_counts.setdefault(tier, 0)
                    total_tier_counts[tier] += raw_counts[tier]

            pools = {}
            for tier in total_tier_counts:
                src_pool = items_dbview.find_all(lambda it: it.tier == tier)
                if len(src_pool) == 0:
                    continue

                if len(src_pool) > total_tier_counts[tier]:
                    pools[tier] = env.rnd.sample(src_pool, total_tier_counts[tier])
                else:
                    pools[tier] = list(src_pool)
                    while len(pools[tier]) < total_tier_counts[tier]:
                        pools[tier].append(env.rnd.choice(src_pool))
                env.rnd.shuffle(pools[tier])            

            for area in unassigned_chest_slots_by_area:
                
                area_pool = []
                for tier in tier_counts_by_area[area]:
                    if tier not in pools:
                        continue

                    for i in range(tier_counts_by_area[area][tier]):
                        area_pool.append(pools[tier].pop())
                env.rnd.shuffle(area_pool)                
                for slot in unassigned_chest_slots_by_area[area]:
                    reward_to_insert = default_item_reward
                    if len(area_pool) != 0:
                        reward_to_insert = ItemReward(area_pool.pop().const)
                    rewards_assignment[slot] = reward_to_insert

    # randomize fight treasure locations (keyitem rando needs to know this for ending)
    env.meta['miab_locations'] = {}
    if env.options.flags.has('vanilla_miabs'):
        for slot in CHEST_NUMBERS:
            env.meta['miab_locations'][slot] = CHEST_NUMBERS[slot]
    else:
        areas = {}
        for slot in CHEST_NUMBERS:
            treasure = treasure_dbview.find_one(lambda t: [t.map, t.index] == CHEST_NUMBERS[slot])
            areas.setdefault(treasure.area, []).append(slot)
        for area in areas:
            new_chests = env.rnd.sample(treasure_dbview.find_all(lambda t: t.area == area), len(areas[area]))
            for i,slot in enumerate(areas[area]):
                #print(f'New MAIB location is {new_chests[i].spoilerarea} - {new_chests[i].spoilersubarea} - {new_chests[i].spoilerdetail}')
                env.meta['miab_locations'][slot] = [new_chests[i].map, new_chests[i].index]

    # hacky cleanup step for _1 and _2 suffixes, and build key item metadata for random objectives
    env.meta['available_key_items'] = set()
    for slot in rewards_assignment:
        reward = rewards_assignment[slot]
        if reward:
            try:
                item = reward.item
            except AttributeError:
                continue

            if type(item) is str and (item.endswith('_1') or item.endswith('_2')):
                rewards_assignment[slot] = ItemReward(item[:-2])

            if reward.is_key:
                env.meta['available_key_items'].add(reward.item)

    # assign fixed reward slots
    #  (note: smith reward is assigned in custom_weapon_rando)
    if env.meta.get('has_objectives', False) and env.meta.get('zeromus_required', True):
        rewards_assignment[RewardSlot.fixed_crystal] = KeyItemReward('#item.Crystal')

    if not env.options.flags.has('key_item_from_pink_tail'):
        if env.options.flags.has('no_adamants'):
            lbound = 7
            items = items_dbview.find_all(lambda it: it.tier in range(lbound, 9))
            while not items:
                lbound -= 1
                items = items_dbview.find_all(lambda it: it.tier in range(lbound, 9))
            pink_tail_item = env.rnd.choice(items)
            rewards_assignment[RewardSlot.pink_trade_item] = ItemReward(pink_tail_item.const)
        else:
            rewards_assignment[RewardSlot.pink_trade_item] = ItemReward('#item.AdamantArmor')

    # for now, assign flat character positions
    rewards_assignment[RewardSlot.starting_character] = AxtorReward('#actor.DKCecil')
    rewards_assignment[RewardSlot.starting_partner_character] = AxtorReward('#actor.Kain1')
    rewards_assignment[RewardSlot.mist_character] = AxtorReward('#actor.CRydia')
    rewards_assignment[RewardSlot.watery_pass_character] = AxtorReward('#actor.Tellah1')
    rewards_assignment[RewardSlot.damcyan_character] = AxtorReward('#actor.Edward')
    rewards_assignment[RewardSlot.kaipo_character] = AxtorReward('#actor.Rosa1')
    rewards_assignment[RewardSlot.hobs_character] = AxtorReward('#actor.Yang1')
    rewards_assignment[RewardSlot.mysidia_character_1] = AxtorReward('#actor.Palom')
    rewards_assignment[RewardSlot.mysidia_character_2] = AxtorReward('#actor.Porom')
    rewards_assignment[RewardSlot.ordeals_character] = AxtorReward('#actor.Tellah2')
    rewards_assignment[RewardSlot.baron_inn_character] = AxtorReward('#actor.Yang2')
    rewards_assignment[RewardSlot.baron_castle_character] = AxtorReward('#actor.Cid')
    rewards_assignment[RewardSlot.zot_character_1] = AxtorReward('#actor.Kain2')
    rewards_assignment[RewardSlot.zot_character_2] = AxtorReward('#actor.Rosa2')
    rewards_assignment[RewardSlot.dwarf_castle_character] = AxtorReward('#actor.ARydia')
    rewards_assignment[RewardSlot.cave_eblan_character] = AxtorReward('#actor.Edge')
    rewards_assignment[RewardSlot.lunar_palace_character] = AxtorReward('#actor.Fusoya')
    rewards_assignment[RewardSlot.giant_character] = AxtorReward('#actor.Kain3')

    combined_assignments = {k : rewards_assignment[k] for k in rewards_assignment}
    combined_assignments.update(boss_assignment)
    env.update_assignments(combined_assignments)

    if DEBUG:
        print('FINAL ASSIGNMENT:')
        max_slot_length = max([len((s.name if type(s) == RewardSlot else s)) for s in combined_assignments])
        format_str = '  {{:{}}} <- {{}}'.format(max_slot_length)
        for k in combined_assignments:
            print(format_str.format((k.name if type(k) == RewardSlot else k), combined_assignments[k]))
        print('ATTEMPTS: {}'.format(attempts))

        print('BREAKDOWN of gating key items:')
        breakdown_items = list(ESSENTIAL_KEY_ITEMS)
        if env.options.flags.has('pass_in_key_items'):
            breakdown_items.append('#item.Pass')
        breakdown = {'normal':0, 'summon':0, 'moonboss':0, 'chests':0};
        for item in ESSENTIAL_KEY_ITEMS:
            for k in rewards_assignment:
                if rewards_assignment[k] == item:
                    if k in ITEM_SLOTS:
                        breakdown['normal'] += 1
                    elif k in SUMMON_QUEST_SLOTS:
                        breakdown['summon'] += 1
                    elif k in MOON_BOSS_SLOTS:
                        breakdown['moonboss'] += 1
                    elif k in CHEST_ITEM_SLOTS:
                        breakdown['chests'] += 1
        for k in breakdown:
            print(f'{k} : {breakdown[k]}')

    # need a table indicating which slots could contain key items for hinting
    # purposes, might as well do that here
    if env.options.hide_flags:
        potential_key_item_slots = list(ITEM_SLOTS) + list(SUMMON_QUEST_SLOTS) + list(MOON_BOSS_SLOTS) + list(CHEST_ITEM_SLOTS)
    elif env.options.flags.has('key_items_vanilla'):
        potential_key_item_slots = [s for s in range(RewardSlot.MAX_COUNT) if s in rewards_assignment and isinstance(rewards_assignment[s], ItemReward) and rewards_assignment[s].is_key]
        if env.options.flags.has('objective_zeromus'):
            potential_key_item_slots.remove(RewardSlot.fixed_crystal)
    else:
        potential_key_item_slots = list(ITEM_SLOTS)
        if env.options.flags.has('no_free_key_item_dwarf'):
            potential_key_item_slots.remove(RewardSlot.toroia_hospital_item)
            potential_key_item_slots.remove(RewardSlot.rydias_mom_item)
        elif env.options.flags.has('no_free_key_item'):
            potential_key_item_slots.remove(RewardSlot.toroia_hospital_item)
            potential_key_item_slots.remove(RewardSlot.dwarf_hospital_item)
        else:
            potential_key_item_slots.remove(RewardSlot.rydias_mom_item)
            potential_key_item_slots.remove(RewardSlot.dwarf_hospital_item)
        if env.options.flags.has('key_items_in_summon_quests'):
            potential_key_item_slots.extend(SUMMON_QUEST_SLOTS)
        if env.options.flags.has('key_items_in_moon_bosses'):
            potential_key_item_slots.extend(MOON_BOSS_SLOTS)        
        if not env.options.flags.has('key_item_from_forge'):
            potential_key_item_slots.remove(RewardSlot.forge_item)
        if not env.options.flags.has('key_item_from_pink_tail'):
            potential_key_item_slots.remove(RewardSlot.pink_trade_item)
        if miab_flags:
            potential_key_item_slots.extend(potential_miabs)
    # put this information in env to facilitate Xkicheckbonus:num
    env.meta['number_key_item_slots'] = len(potential_key_item_slots)
    env.add_binary(BusAddress(0x21dc00), [1 if s in potential_key_item_slots else 0 for s in range(RewardSlot.MAX_COUNT)], as_script=True)
    env.add_substitution('randomizer key item count', '{:02X}'.format(rewards_assignment.count_key_items()))

    # setup objectives reference table, and create boss metadata for random objectives purposes
    boss_objective_consts = []
    env.meta['available_bosses'] = set()
    for slot in BOSS_SLOTS:
        boss_objective_consts.append(f'#objective.boss_{boss_assignment[slot]}')
        if slot not in removed_boss_slots:
            env.meta['available_bosses'].add(boss_assignment[slot])
    env.add_script('patch($21f860 bus) {\n' + '\n'.join(boss_objective_consts) + '\n}')
    env.meta['bosses_in_restricted_slots'] = bosses_in_restricted_slots
    env.meta['unrestricted_non_objective_bosses'] = (
        env.meta['available_bosses'].difference(env.meta['objective_required_bosses'].union(bosses_in_restricted_slots))
    )
    # if we are removing boss slots, then we don't necessarily have all 34 slots anymore
    env.add_substitution('randomizer boss count', '{:02X}'.format(len(BOSS_SLOTS)-len(removed_boss_slots)))

    # remove golbez item delivery if not needed
    if (RewardSlot.fallen_golbez_item not in rewards_assignment):
        env.add_substitution('golbez awards item', '')

    # generate spoiler logs
    item_spoiler_names = {it.const: it.spoilername for it in databases.get_items_dbview()}
    if env.options.flags.has('darkpaladin'):
        item_spoiler_names.update(
            {'#item.Light' : 'Chaos Sword',
            '#item.CrystalSword' : 'Hades Sword',
            '#item.PaladinShield' : 'Ancient Shield',
            '#item.PaladinHelm' : 'Ancient Helm',
            '#item.PaladinArmor' : 'Ancient Armor',
            '#item.PaladinGauntlet' : 'Ancient Gauntlet',
            '#item.CrystalShield' : 'Hades Shield',
            '#item.CrystalHelm' : 'Hades Helm',
            '#item.CrystalArmor' : 'Hades Armor',
            '#item.CrystalGauntlet' : 'Hades Gauntlet'}
        )
    if env.options.flags.has('starting_underground'):
        item_spoiler_names.update({'#item.fe_Hook' : 'Drill'})

    key_item_spoilers = []
    for key_item_reward in list(ESSENTIAL_KEY_ITEMS) + list(NONESSENTIAL_KEY_ITEMS) + [ItemReward("#item.Pass")]:
        slot = rewards_assignment.find_slot(key_item_reward)
        if slot is None:
            slot = RewardSlot.none
        key_item_spoilers.append( SpoilerRow(item_spoiler_names[key_item_reward.item], REWARD_SLOT_SPOILER_NAMES[slot], obscurable=True) )
    env.spoilers.add_table("KEY ITEM LOCATIONS (and Pass if Pkey)", key_item_spoilers, public=env.options.flags.has_any('-spoil:all', '-spoil:keyitems'))

    quest_spoilers = []
    for slot in list(ITEM_SLOTS) + list(SUMMON_QUEST_SLOTS) + list(MOON_BOSS_SLOTS):
        if slot in rewards_assignment:
            reward = rewards_assignment[slot]
            if type(reward) is EmptyReward:
                reward_text = "(nothing)"
            else:
                reward_text = item_spoiler_names[reward.item]
            quest_spoilers.append( SpoilerRow(REWARD_SLOT_SPOILER_NAMES[slot], reward_text, obscurable=True) )
    env.spoilers.add_table("QUEST REWARDS", quest_spoilers, public=env.options.flags.has_any('-spoil:all', '-spoil:rewards'))

    # leave rewards assignment in meta for later use (TODO: later make it a first class member of env)
    env.meta['rewards_assignment'] = rewards_assignment


if __name__ == '__main__':
    import FreeEnt
    import random
    import argparse

    parser = argparse.ArgumentParser();
    parser.add_argument('-f', '--flags', default='Kstandard Tshuffle')
    parser.add_argument('-s', '--seed', default=None)
    parser.add_argument('-b', '--bulk', default='')
    parser.add_argument('-n', '--iterations', type=int, default=10000)
    args = parser.parse_args();

    options = FreeEnt.FreeEntOptions()
    options.flags.load(args.flags)

    if args.seed:
        options.seed = args.seed

    env = FreeEnt.Environment(options)

    if args.bulk:
        import json
        import zipfile

        with open(args.bulk, 'wb') as outfile:
            archive = zipfile.ZipFile(outfile, mode='w', compression=zipfile.ZIP_DEFLATED)

            for i in range(args.iterations):
                result = randomize(env)

                key_item_slots = list(ITEM_SLOTS)
                if options.flags.has('Kq'):
                    key_item_slots.extend(SUMMON_QUEST_SLOTS)
                if options.flags.has('Km'):
                    key_item_slots.extend(MOON_BOSS_SLOTS)
                if options.flags.has('Kt'):
                    key_item_slots.extend(CHEST_ITEM_SLOTS)

                data_obj = {
                    'key_items' : {slot : result['assignments'][slot] for slot in key_item_slots},
                    'bosses' : {slot : result['assignments'][slot] for slot in BOSS_SLOTS}
                    }

                data = json.dumps(data_obj, indent=2)

                archive.writestr(f'{i+1:0{len(str(args.iterations))}}.json', data)

                if ((i + 1) % 1000) == 0:
                    print(f'Completed {i+1} of {args.iterations}')

            archive.close()

    else:
        DEBUG = 1
        apply(env)
