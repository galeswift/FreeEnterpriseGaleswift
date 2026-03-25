from . import boss_rando_formation_data
from . import boss_rando_formation_data_j
from . import boss_rando_formation_data_et

from .boss_rando import _get_cumulative_formation, _get_total_hp_xp_gp_qty, _get_leader, FORMATION_MAP
from .core_rando import BOSS_SLOTS, BOSSES

slot_rankings = {}
slot_data_lists = {}
version_data = {}
version_data['US'] = {
    'formations' : boss_rando_formation_data.FORMATION_DATA,
    'stats_table' : boss_rando_formation_data.STATS_TABLE,
    'speed_table' : boss_rando_formation_data.SPEED_TABLE 
}
version_data['J'] = {
    'formations' : boss_rando_formation_data_j.FORMATION_DATA,
    'stats_table' : boss_rando_formation_data_j.STATS_TABLE,
    'speed_table' : boss_rando_formation_data_j.SPEED_TABLE 
}
version_data['ET'] = {
    'formations' : boss_rando_formation_data_et.FORMATION_DATA,
    'stats_table' : boss_rando_formation_data_et.STATS_TABLE,
    'speed_table' : boss_rando_formation_data_et.SPEED_TABLE 
}
for version in ['US', 'J', 'ET']:
    # sort the speed table; tuples automatically get sorted by first entry then second
    version_data[version]['speed_table'].sort()
    # the (0,0,5) entry in the stats table needs to get shifted backwards.
    version_data[version]['stats_table'].insert(100,version_data[version]['stats_table'].pop(158))
    slot_rankings[version] = {}
    slot_data_lists[version] = []

    for slot in BOSS_SLOTS:
        slot_boss = slot[:-5] # remove '_slot'
        slot_formation = FORMATION_MAP[slot_boss]
        slot_formation_list = (slot_formation if type(slot_formation) == list else [slot_formation])
        
        slot_cumulative_formation_data = {}
        slot_cumulative_hp = {}
        slot_leader = {}
        slot_rankings[version][slot] = {}

        slot_cumulative_formation_data[version] = _get_cumulative_formation(slot_formation_list, version_data[version]['formations'])
        slot_cumulative_hp[version] = _get_total_hp_xp_gp_qty(slot_cumulative_formation_data[version], version_data[version]['formations'])[0]
        slot_leader[version] = _get_leader(slot_cumulative_formation_data[version], version_data[version]['formations'])
    
        slot_data_lists[version].append({
            'slot'          : slot,
            'attack'        : slot_leader[version]['attack'], 
            'defense'       : slot_leader[version]['defense'],
            'magic defense' : slot_leader[version]['magic defense'],
            'speed'         : slot_leader[version]['speed'],
            'spell power'   : (0 if slot_leader[version]['spell power'] == None else slot_leader[version]['spell power']),
            'hp'            : slot_cumulative_hp[version],
            'level'         : slot_leader[version]['level']
        })
        slot_rankings[version].update({slot : {}})

    for stat in ['speed', 'spell power', 'attack', 'hp', 'level', 'magic defense', 'defense']:
        if stat in ['attack', 'magic defense', 'defense']:
            sorting_key = (lambda s: version_data[version]['stats_table'].index(s[stat]))
        elif stat == 'speed':
            sorting_key = (lambda s: version_data[version]['speed_table'].index(s[stat]))
        else:
            sorting_key = (lambda s: s[stat])
        slot_data_lists[version].sort(key=sorting_key)
        temp_enum = enumerate(slot_data_lists[version])
        for i,slot_data in temp_enum:
            slot_rankings[version][slot_data['slot']].update({stat : i+1})

# weight data to be transferred to an auto-generated file
# should really tailor the Alt Gauntlet weights a bit more; there's probably a bit more tiering that should occur
WEIGHT_DATA_STRING = '''
BOSS_STATS_WEIGHTS_DIFFICULTY = {
    'dmist'         : {'speed' : 30, 'spell power' : 5,  'attack' : 30, 'hp' : 35, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 1,     },
    'officer'       : {'speed' : 20, 'spell power' : 0,  'attack' : 30, 'hp' : 50, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 0.3,   },
    'octomamm'      : {'speed' : 40, 'spell power' : 0,  'attack' : 40, 'hp' : 20, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 0.8,   },
    'antlion'       : {'speed' : 30, 'spell power' : 0,  'attack' : 40, 'hp' : 30, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 1,     },
    'waterhag'      : {'speed' : 50, 'spell power' : 0,  'attack' : 50, 'hp' : 0,  'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 0.5,   },
    'mombomb'       : {'speed' : 25, 'spell power' : 15, 'attack' : 25, 'hp' : 35, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 0.8,   },
    'fabulgauntlet' : {'speed' : 15, 'spell power' : 5,  'attack' : 30, 'hp' : 50, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 0.8,   },
    'milon'         : {'speed' : 20, 'spell power' : 20, 'attack' : 30, 'hp' : 30, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 0.8,   },
    'milonz'        : {'speed' : 35, 'spell power' : 0,  'attack' : 35, 'hp' : 30, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 1,     },
    'mirrorcecil'   : {'speed' : 40, 'spell power' : 0,  'attack' : 60, 'hp' : 0,  'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 0.9,   },
    'guard'         : {'speed' : 30, 'spell power' : 15, 'attack' : 30, 'hp' : 25, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 0.5,   },
    'karate'        : {'speed' : 40, 'spell power' : 0,  'attack' : 60, 'hp' : 0,  'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 0.8,   },
    'baigan'        : {'speed' : 40, 'spell power' : 5,  'attack' : 40, 'hp' : 15, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 1,     },
    'kainazzo'      : {'speed' : 20, 'spell power' : 0,  'attack' : 15, 'hp' : 60, 'level' : 0, 'magic defense' : 0,  'defense' : 5,  'difficulty' : 1.2,   },
    'darkelf'       : {'speed' : 30, 'spell power' : 20, 'attack' : 20, 'hp' : 30, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 0.8,   },
    'magus'         : {'speed' : 20, 'spell power' : 25, 'attack' : 25, 'hp' : 30, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 1,     },
    'valvalis'      : {'speed' : 20, 'spell power' : 0,  'attack' : 20, 'hp' : 10, 'level' : 0, 'magic defense' : 25, 'defense' : 25, 'difficulty' : 1.2,   },
    'calbrena'      : {'speed' : 30, 'spell power' : 5,  'attack' : 30, 'hp' : 35, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 0.8,   },
    'golbez'        : {'speed' : 40, 'spell power' : 40, 'attack' : 0,  'hp' : 20, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 1.2,   },
    'lugae'         : {'speed' : 30, 'spell power' : 10, 'attack' : 25, 'hp' : 35, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 1,     },
    'darkimp'       : {'speed' : 35, 'spell power' : 0,  'attack' : 35, 'hp' : 30, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 0.5,   },
    'kingqueen'     : {'speed' : 50, 'spell power' : 0,  'attack' : 0,  'hp' : 50, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 0.2,   },
    'rubicant'      : {'speed' : 30, 'spell power' : 25, 'attack' : 25, 'hp' : 20, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 1,     },
    'evilwall'      : {'speed' : 40, 'spell power' : 0,  'attack' : 35, 'hp' : 25, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 1,     },
    'asura'         : {'speed' : 30, 'spell power' : 15, 'attack' : 35, 'hp' : 20, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 1,     },
    'leviatan'      : {'speed' : 30, 'spell power' : 40, 'attack' : 0,  'hp' : 30, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 1,     },
    'odin'          : {'speed' : 25, 'spell power' : 30, 'attack' : 20, 'hp' : 25, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 1,     },
    'bahamut'       : {'speed' : 20, 'spell power' : 30, 'attack' : 0,  'hp' : 50, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 0.7,   },
    'elements'      : {'speed' : 25, 'spell power' : 25, 'attack' : 25, 'hp' : 25, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 1      },
    'cpu'           : {'speed' : 40, 'spell power' : 10, 'attack' : 0,  'hp' : 50, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 1      },
    'paledim'       : {'speed' : 30, 'spell power' : 15, 'attack' : 35, 'hp' : 20, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 1      },
    'wyvern'        : {'speed' : 40, 'spell power' : 25, 'attack' : 0,  'hp' : 35, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 1.2,   },
    'plague'        : {'speed' : 55, 'spell power' : 0,  'attack' : 0,  'hp' : 45, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 1,     },
    'dlunar'        : {'speed' : 30, 'spell power' : 25, 'attack' : 20, 'hp' : 25, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 1,     },
    'ogopogo'       : {'speed' : 30, 'spell power' : 15, 'attack' : 30, 'hp' : 25, 'level' : 0, 'magic defense' : 0,  'defense' : 0,  'difficulty' : 1,     },
}

ALT_GAUNTLET_WEIGHTS = {
'dmist_slot'            : 1,
'officer_slot'          : 2,
'octomamm_slot'         : 3,
'antlion_slot'          : 3,
'mombomb_slot'          : 4,
'fabulgauntlet_slot'    : 5,
'milon_slot'            : 6,
'milonz_slot'           : 8,
'mirrorcecil_slot'      : 7,
'karate_slot'           : 9,
'guard_slot'            : 10,
'baigan_slot'           : 11,
'kainazzo_slot'         : 12,
'darkelf_slot'          : 13,
'magus_slot'            : 14,
'valvalis_slot'         : 15,
'calbrena_slot'         : 17,
'golbez_slot'           : 18,
'lugae_slot'            : 20,
'darkimp_slot'          : 19,
'kingqueen_slot'        : 21,
'rubicant_slot'         : 22,
'evilwall_slot'         : 23,
'asura_slot'            : 25,
'leviatan_slot'         : 26,
'odin_slot'             : 24,
'bahamut_slot'          : 29,
'elements_slot'         : 27,
'cpu_slot'              : 28,
'paledim_slot'          : 30,
'wyvern_slot'           : 33,
'plague_slot'           : 31,
'dlunar_slot'           : 31,
'ogopogo_slot'          : 34, 
}'''

with open('FreeEnt\\boss_slot_ranking_weights_data.py', 'w') as outfile:
    outfile.write('# Auto-generated by generate_boss_slot_rankings.py\n\n')
    for version in ['US', 'J', 'ET']:
        rankings_lines = [f'BOSS_SLOT_STATS_RANKINGS{("_" + version if version != "US" else "")} = {{']
        for slot in BOSS_SLOTS:
            rankings_lines.append(f'    "{slot}"' + ' '*(18 - len(slot)) + ' : {' 
                                  + ' '.join([f'"{stat}" : {slot_rankings[version][slot][stat]}{(", " if slot_rankings[version][slot][stat] < 10 else ",")}' 
                                               for stat in ['speed', 'spell power', 'attack', 'hp', 'level', 'magic defense', 'defense']])
                                  + ' },')
        rankings_lines.append('}\n\n')
        outfile.write('\n'.join(rankings_lines))
    outfile.write(WEIGHT_DATA_STRING)