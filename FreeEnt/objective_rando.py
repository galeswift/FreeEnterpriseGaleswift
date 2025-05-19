from .address import *
from .objective_data import *
from .errors import *
from . import util
from .spoilers import SpoilerRow
from . import character_rando

MODES = {
    'Omode:classicforge'  : ['quest_forge'],
    'Omode:classicgiant'  : ['quest_giant'],
    'Omode:fiends'        : ['boss_milon', 'boss_milonz', 'boss_kainazzo', 'boss_valvalis', 'boss_rubicant', 'boss_elements'],
    'Omode:external'      : ['internal_external']
}

OBJECTIVE_SLUGS_TO_IDS = {}
for objective_id in OBJECTIVES:
    OBJECTIVE_SLUGS_TO_IDS[OBJECTIVES[objective_id]['slug']] = objective_id

CHAR_OBJECTIVE_PREFIX = "char_"
BOSS_OBJECTIVE_PREFIX = "boss_"
INTERNAL_OBJECTIVE_PREFIX = "internal_"

CUSTOM_OBJECTIVE_COUNT = 8

MAX_OBJECTIVE_COUNT = 0x20

RANDOM_CATEGORY_WEIGHTS = {
    'char' : 20,
    'boss' : 20,
    'quest' : 60,
    }

TOUGH_QUEST_OBJECTIVES_EXCLUDED = [
    'quest_mistcave',
    'quest_waterfall',
    'quest_antlionnest',
    'quest_hobs',
    'quest_fabul',
    'quest_ordeals',
    'quest_baroninn',
    'quest_pass',
    'quest_dwarfcastle',
    'quest_lowerbabil',
    'quest_unlocksewer',
    'quest_music',
    'quest_toroiatreasury',
    'quest_magma',
    'quest_unlocksealedcave',
    'quest_bigwhale',
    'quest_wakeyang',
]

TOUGH_QUEST_OBJECTIVES_WEIGHTED = [
    'quest_monsterking',
    'quest_monsterqueen',
    'quest_cavebahamut',
    'quest_murasamealtar',
    'quest_crystalaltar',
    'quest_whitealtar',
    'quest_ribbonaltar',
    'quest_masamunealtar'
]


def _split_lines(text, line_length=24):
    pieces = text.split()
    lines = []
    while pieces:
        if len(pieces[0]) > line_length:
            lines.append(pieces[0][:line_length])
            pieces[0] = pieces[0][line_length:]
        elif not lines or len(lines[-1] + ' ' + pieces[0]) > line_length:
            lines.append(pieces[0])
            pieces.pop(0)
        else:
            lines[-1] += ' ' + pieces[0]
            pieces.pop(0)
    return lines


def setup(env):
    env.meta['has_objectives'] = False
    env.meta['zeromus_required'] = True
    env.meta['gated_objective_reward'] = ''
    env.meta['has_gated_objective'] = False
    env.meta.setdefault('objectives_from_flags', [])
    env.meta.setdefault('objective_required_characters', set())
    env.meta.setdefault('objective_required_bosses', set())
    env.meta.setdefault('required_treasures', {})
    env.meta.setdefault('objective_required_key_items', set())
    if not env.options.flags.has('objective_none'):
        env.meta['has_objectives'] = True
        env.meta['zeromus_required'] = env.options.flags.has("objective_zeromus")

        specified_objectives = dict()
        for i in range(CUSTOM_OBJECTIVE_COUNT):
            slug = env.options.flags.get_suffix(f"O{i+1}:")
            env.meta['objectives_from_flags'].append(slug)
            specified_objectives[slug] = True 

        for mode in MODES:
            if env.options.flags.has(mode):
                for slug in MODES[mode]:
                    specified_objectives[slug] = True

        if env.options.flags.get_suffix('Omode:dkmatter'):
            specified_objectives['internal_dkmatter'] = True
        if env.options.flags.get_suffix('Omode:ki'):
            specified_objectives['internal_ki'] = True
        if env.options.flags.get_suffix('Omode:bosscollector'):
            specified_objectives['internal_bosscollector'] = True
        if env.options.flags.get_suffix('Omode:goldhunter'):
            specified_objectives['internal_goldhunter'] = True

        for objective_id in OBJECTIVES:
            objective = OBJECTIVES[objective_id]
            slug = objective['slug']            
            if specified_objectives.get(slug, False):
                if slug.startswith(CHAR_OBJECTIVE_PREFIX):
                    env.meta['objective_required_characters'].add(slug[len(CHAR_OBJECTIVE_PREFIX):])
                elif slug.startswith(BOSS_OBJECTIVE_PREFIX):
                    env.meta['objective_required_bosses'].add(slug[len(BOSS_OBJECTIVE_PREFIX):])
                elif slug == 'quest_tradepink':
                    env.meta['objective_required_key_items'].add('#item.Pink')                

        if env.options.flags.get_suffix('Omode:dkmatter'):
            env.meta['required_treasures'].setdefault('#item.DkMatter', 0)
            env.meta['required_treasures']['#item.DkMatter'] += 45
        
        if env.options.flags.has('objective_mode_external'):
            env.meta['objective_starter_kit'] = [( 'fe_EagleEye', [1] )]

        random_objective_only_characters = set()
        for random_prefix in ['Orandom:', 'Orandom2:', 'Orandom3:']:
            for f in env.options.flags.get_list(rf'^{random_prefix}[^\d]'):               
                allowed_type = f[len(random_prefix):]
                if allowed_type.startswith('only'):                
                    random_objective_only_characters.add(allowed_type[len('only'):])
        for random_char in random_objective_only_characters:
            env.meta['objective_required_characters'].add(random_char)
        

        # Handle gated objectives
        objective_ids = get_unique_objective_ids(env)
        total_objective_count = get_total_objective_count(env)
        gated_objective_specifier = env.options.flags.get_suffix(f"Ogated:")
        if gated_objective_specifier != None:
            gated_objective_specifier = int(gated_objective_specifier)-1
            target_objective_id = objective_ids[gated_objective_specifier]
            target_objective = OBJECTIVES[target_objective_id]
            
            if target_objective['reward'][0] != '#':
                raise BuildError(f"Flags stipulate generating gated objective #{gated_objective_specifier+1}, objective {target_objective['slug']} has no reward")
            elif total_objective_count <= 1:
                raise BuildError(f"Flags stipulate generating gated objective #{gated_objective_specifier+1}, but there is only one objective. (You need at least two)")
            elif total_objective_count < gated_objective_specifier:
                raise BuildError(f"Flags stipulate generating gated objective #{gated_objective_specifier+1}, but there are only {len(objective_ids)} custom objectives")
            else:
                env.meta['gated_objective_reward'] = target_objective['reward']
                env.meta['has_gated_objective'] = True
                env.meta['gated_objective_id'] = target_objective_id                
            env.add_substitution('gated objective id', f'{target_objective_id:02X}')

def get_total_objective_count(env):
    random_objective_count = 0
    for random_prefix in ['Orandom:', 'Orandom2:', 'Orandom3:']:
        for f in env.options.flags.get_list(rf'^{random_prefix}\d'):            
            random_objective_count += int(f[len(random_prefix):])
    return len(get_unique_objective_ids(env)) + random_objective_count

def get_objective_ids(env):
    objective_ids = []

    # apply objectives from modes
    for objective_flag in MODES:
        if env.options.flags.has(objective_flag):
            objective_ids.extend([OBJECTIVE_SLUGS_TO_IDS[q] for q in MODES[objective_flag]])

    if env.options.flags.get_suffix('Omode:dkmatter'):
        objective_ids.extend([OBJECTIVE_SLUGS_TO_IDS['internal_dkmatter']])
    if env.options.flags.get_suffix('Omode:ki'):
        objective_ids.extend([OBJECTIVE_SLUGS_TO_IDS['internal_ki']])
    if env.options.flags.get_suffix('Omode:bosscollector'):
        objective_ids.extend([OBJECTIVE_SLUGS_TO_IDS['internal_bosscollector']])
    if env.options.flags.get_suffix('Omode:goldhunter'):
        objective_ids.extend([OBJECTIVE_SLUGS_TO_IDS['internal_goldhunter']])

    # custom objectives from flags
    for slug in env.meta['objectives_from_flags']:
        for objective_id in OBJECTIVES:
            if OBJECTIVES[objective_id]['slug'] == slug:            
                objective_ids.append(objective_id)
                break

    return objective_ids

def get_unique_objective_ids(env):
    objective_ids = get_objective_ids(env)
    # remove duplicates, but maintain order
    result_ids = []
    for id in objective_ids:
        if id not in result_ids:
            result_ids.append(id)
    return result_ids

def apply(env):
    if not env.meta['has_objectives']:
        env.add_substitution('gated objective reward text', '')
        return

    env.add_substitution('intro disable', '')
    if not env.meta['zeromus_required']:
        env.add_file('scripts/zeromus_trigger_reassign.f4c')

    objective_ids = get_unique_objective_ids(env)
    # generate random objectives    
    for random_prefix in ['Orandom:', 'Orandom2:', 'Orandom3:']:
        random_objective_count = 0
        for f in env.options.flags.get_list(rf'^{random_prefix}\d'):            
            random_objective_count = int(f[len(random_prefix):])

        #print(f"Random objective count is {random_objective_count} for {random_prefix}")
        random_objective_allowed_types = set()
        random_objective_allowed_characters = set()
        tough_quests_only = False
        specific_random_chars_only = False
        for f in env.options.flags.get_list(rf'^{random_prefix}[^\d]'):
            allowed_type = f[len(random_prefix):]   
            if (allowed_type == 'tough_quest'):
                allowed_type = 'quest'
                tough_quests_only = True
            if allowed_type.startswith('only'): 
                specific_random_chars_only = True               
                random_objective_allowed_characters.add(allowed_type[len('only'):])
            else:
                random_objective_allowed_types.add(allowed_type)
        
        only_characters = []
        allowed_characters = list(character_rando.CHARACTERS)
        for ch in list(character_rando.CHARACTERS):
            if env.options.flags.has(f'Conly:{ch}'):
                only_characters.append(ch)            
            if env.options.flags.has(f'Cno:{ch}'):
                allowed_characters.remove(ch)
        
        # if any Conly flags were specified, count them to make sure the # of random objectives doesn't exceed the total chars allowed
        unique_hero_list = []
        for slot in env.assignments:
            assignment = env.assignments[slot]
            if slot in character_rando.SLOTS and assignment is not None and assignment not in unique_hero_list:
                unique_hero_list.append(assignment)

        total_char_count = len(unique_hero_list)
        # Check if the number of random character objectives desired exceed the amount specified via Orandomonly, and there is only character quests allowed
        if len(random_objective_allowed_types) == 1 and 'char' in random_objective_allowed_types and random_objective_count > total_char_count:
            raise BuildError(f"Flags stipulate generating ({random_objective_count}) random objectives with specific characters, but only {total_char_count} unique characters were found {','.join(unique_hero_list)}")

        random_objective_pool = {}
        for objective_id in OBJECTIVES:
            obj = OBJECTIVES[objective_id]
            category = obj['slug'].split('_')[0]

            if (not random_objective_allowed_types) or (category in random_objective_allowed_types):
                if (category != 'quest') or (not tough_quests_only) or (obj['slug'] not in TOUGH_QUEST_OBJECTIVES_EXCLUDED):
                    if obj['slug'] in TOUGH_QUEST_OBJECTIVES_WEIGHTED and env.rnd.random() < 0.40:
                        continue
                    random_objective_pool.setdefault(category, []).append(objective_id)

        random_category_weights = RANDOM_CATEGORY_WEIGHTS
        if random_objective_allowed_types:
            random_category_weights = { k : RANDOM_CATEGORY_WEIGHTS[k] for k in RANDOM_CATEGORY_WEIGHTS if k in random_objective_allowed_types }
        random_category_distribution = util.Distribution(**random_category_weights)

        MAX_CHARACTER_RANDOMIZATION_ATTEMPTS = 10000
        retry_count = 0
        for i in range(random_objective_count):
            while True and retry_count < MAX_CHARACTER_RANDOMIZATION_ATTEMPTS:     
                retry_count += 1         
                category = random_category_distribution.choose(env.rnd)
                q = env.rnd.choice(random_objective_pool[category])
                slug = OBJECTIVES[q]['slug']    
                #print(f'Considering {slug}')            
                if q in objective_ids:
                    continue
                if slug.startswith(CHAR_OBJECTIVE_PREFIX):
                    char = slug[len(CHAR_OBJECTIVE_PREFIX):]
                    if char not in env.meta['available_nonstarting_characters']:
                        continue
                    if len(random_objective_allowed_characters) != 0 and (char not in random_objective_allowed_characters):
                        print(f'{char} not allowed in types {random_objective_allowed_characters}')
                        continue
                elif slug.startswith(BOSS_OBJECTIVE_PREFIX):
                    boss = slug[len(BOSS_OBJECTIVE_PREFIX):]
                    if boss not in env.meta['available_bosses'] or boss in env.meta['banned_objective_bosses']:
                        continue
                elif slug == 'quest_tradepink':
                    if '#item.Pink' not in env.meta['available_key_items']:
                        continue
                elif slug == 'quest_pass':
                    if env.options.flags.has('pass_none'):
                        continue
                elif slug.startswith(INTERNAL_OBJECTIVE_PREFIX):
                    # don't allow internal objectives to be selected as random ones
                    continue
                break
            if retry_count >= MAX_CHARACTER_RANDOMIZATION_ATTEMPTS:
                raise BuildError(f"Failed to generate {random_objective_count} randomized objectives after many attempts. ({total_char_count} total unique characters)")
            else:
                objective_ids.append(q)

    if env.options.test_settings.get('objectives'):
        objective_ids = [OBJECTIVE_SLUGS_TO_IDS[s.strip()] for s in env.options.test_settings.get('objectives').split(',')]

    if len(objective_ids) > MAX_OBJECTIVE_COUNT:
        reduced_objective_ids = env.rnd.sample(objective_ids, MAX_OBJECTIVE_COUNT)
        objective_ids = sorted(reduced_objective_ids, key = objective_ids.index)

    required_objective_count = env.options.flags.get_suffix('Oreq:')

    # write list of objective IDs and thresholds
    total_objective_count = len(objective_ids)

    env.add_substitution('objective count', f'{total_objective_count:02X}')
    objective_ids.extend([0x00] * (MAX_OBJECTIVE_COUNT - len(objective_ids)))
    env.add_substitution('objective ids', ' '.join([f'{b:02X}' for b in objective_ids]))   
    threshold_list = []

    gold_hunt_count = 0
    boss_hunt_count = 0
    
    if env.options.flags.get_suffix(f"Omode:bosscollector") != None:
        boss_hunt_count = int(env.options.flags.get_suffix(f"Omode:bosscollector"))

    if env.options.flags.get_suffix(f"Omode:goldhunter") != None:
        gold_hunt_count = int(env.options.flags.get_suffix(f"Omode:goldhunter"))
    
    for b in objective_ids:
        if b == 0xFF:
            threshold_list.append('00')
        elif b != 0 and OBJECTIVES[b]['slug'] == 'internal_bosscollector':
            threshold_list.append(f'{boss_hunt_count:02X}')
            
            # inject the location of the boss slot id
            env.add_substitution('boss hunt id', f'{b:02X}')
        elif b != 0 and OBJECTIVES[b]['slug'] == 'internal_goldhunter':
            # The threshold is stored in a gold specific location
            threshold_list.append('01') 

            # inject the location of the gold hunter slot id
            env.add_substitution('gold hunt id', f'{b:02X}')
        else:
            threshold_list.append('01')
    env.add_substitution('objective thresholds', ' '.join(threshold_list))
    
    # handle changes for partial objectives
    if required_objective_count == 'all' or required_objective_count is None:
        if env.meta['has_gated_objective']:
            required_objective_count = total_objective_count-1
        else:
            required_objective_count = total_objective_count
    else:
        required_objective_count = int(required_objective_count)
    
    # Gated objectives reduce the # of total objectives required by 1
    if env.meta['has_gated_objective']:
        env.add_substitution('gated objective required count', f'{(required_objective_count):02X}' )

    # handle hard required objective ids
    hard_required_objective_ids = []
    hard_required_objective_count = 0    
    for i in objective_ids:
        hard_required_objective_ids.append(0x00)

    if required_objective_count != total_objective_count:        
        for f in env.options.flags.get_list(r'^Ohardreq:\d'):
            hard_required_objective_index = int(f[len('Ohardreq:'):])
            if hard_required_objective_index >total_objective_count:
                raise BuildError(f"Flags stipulate that objective # {hard_required_objective_index} is required, but there are only {total_objective_count} objectives specified.")
            hard_required_objective_ids[hard_required_objective_index-1] = objective_ids[hard_required_objective_index-1]
            hard_required_objective_count += 1
            
    #print(f'hard_required_objective_count {hard_required_objective_count} hard_required_objective_ids {hard_required_objective_ids} {f'{b:02X}}')
    env.add_substitution('hard required objective ids', ' '.join([f'{b:02X}' for b in hard_required_objective_ids]))
    env.add_substitution('hard objective required count', f'{hard_required_objective_count:02X}')
    boss_required_objective_count = 1
    env.add_substitution('boss objective required count', f'{boss_required_objective_count:02X}')    
    env.add_substitution('objective required count', f'{required_objective_count:02X}')
    if required_objective_count > total_objective_count:
        raise BuildError(f"Flags stipulate that {required_objective_count} objectives must be completed, but there are only {total_objective_count} objectives specified.")
    elif required_objective_count < total_objective_count:
        required_objective_count_text = f'{required_objective_count} objective{"s" if required_objective_count > 1 else ""}'
        env.add_substitution('completion objective count text', required_objective_count_text)
    else:
        required_objective_count_text = 'all objectives'
        env.add_substitution('completion objective count text', 'All objectives')
    if env.options.hide_flags:
        required_objective_count_text = 'objectives'

    env.add_substitution('required objective count text', required_objective_count_text)
    env.add_substitution('hard required objective count text', f'{hard_required_objective_count}')

    gated_objective_reward_text = ''
    if env.meta['has_gated_objective']:
        reward = env.meta['gated_objective_reward']
        if reward == '#item.DarkCrystal':
            gated_objective_reward_text = f'[crystal]Darkness'
        elif reward == '#item.EarthCrystal':
            gated_objective_reward_text = f'[crystal]Earth'
        elif reward == '#item.Baron':
            gated_objective_reward_text = f'[key]Baron'
        elif reward == '#item.Tower':
            gated_objective_reward_text = f'[key]Tower'
        elif reward == '#item.Luca':
            gated_objective_reward_text = f'[key]Luca'
        elif reward == '#item.Magma':
            gated_objective_reward_text = f'[key]Magma'
        elif reward == '#item.Pink':
            gated_objective_reward_text = f'[tail]Pink'
        elif reward == '#item.Rat':
            gated_objective_reward_text = f'[tail]Rat'
        elif reward == '#item.fe_Hook':
            gated_objective_reward_text = f'Hook'
        elif reward == '#item.TwinHarp':
            gated_objective_reward_text = f'[harp]TwinHarp'  
        elif reward == '#item.SandRuby':
            gated_objective_reward_text = f'[stone]Sandruby'  
        else:
            gated_objective_reward_text = f'{reward[6:]}'        
    env.add_substitution('gated objective reward text', gated_objective_reward_text)
            
    gold_hunt_text = str(gold_hunt_count) + ',000'
    if gold_hunt_count >= 1000:
        gold_hunt_text = gold_hunt_text[:1]+',' + gold_hunt_text[1:] + ',000'

    # write objective descriptions and compile spoilers
    spoilers = []
    pregame_text_lines = []
    for i,objective_id in enumerate(objective_ids):
        if objective_id == 0x00:
            continue 
        text = OBJECTIVES[objective_id]['desc']

        # string formatting for objective text
        if OBJECTIVES[objective_id]['slug'] == 'internal_bosscollector':
            text = text.replace('%d', f'{boss_hunt_count}' )
            text = text.replace('%t', 'bosses' if boss_hunt_count > 1 else 'boss' )
        elif OBJECTIVES[objective_id]['slug'] == 'internal_goldhunter':
            text = text.replace('%d', f'{gold_hunt_text}' )
        # special case for dkmatter
        elif OBJECTIVES[objective_id]['slug'] == 'internal_dkmatter':
            dkmatter_count = int(env.options.flags.get_suffix('Omode:dkmatter'))
            text = f'Bring {dkmatter_count} DkMatters to Kory in Agart'
        # special case for KI hunt
        elif OBJECTIVES[objective_id]['slug'] == 'internal_ki':
            ki_count = int(env.options.flags.get_suffix('Omode:ki'))
            text = text.replace('%d', f'{ki_count}' )
            text = text.replace('%t', 'items' if ki_count > 1 else 'item' )

        lines = _split_lines(text)
        if env.meta['has_gated_objective'] and objective_id == env.meta['gated_objective_id']:
            lines[-1] = lines[-1] + ' [key]'
        elif objective_id in hard_required_objective_ids:
            lines[-1] = lines[-1] + ' [crystal]'
        env.meta.setdefault('objective_descriptions', []).append(text)
        spoilers.append( SpoilerRow(f"{i+1}. {text}") )
        
        if len(lines) > 2:
            raise ValueError(f"Objective text cannot fit on 2 lines; text is {text}")
        while len(lines) < 2:
            lines.append('')

        for j,line in enumerate(lines):
            addr = 0x23C000 + (i * 0x40) + (j * 0x20)          
            env.add_binary(BusAddress(addr), [len(line)], as_script=True)            
            encoded_line = line.replace('(', '[$cc]').replace(')', '[$cd]')            
            env.add_script(f'text(${addr + 1:06X} bus) {{{encoded_line}}}')

            if line.strip():
                prefix = f"{i+1}" + '.' + (" " if i < 9 else "")
                if j > 0:                    
                    prefix = " " * len(prefix)
                pregame_text_lines.append(prefix + line)
        pregame_text_lines.append("")


    pregame_text_lines.append(" Complete " + required_objective_count_text)
    completion_reward_text = 'the Crystal' if env.options.flags.has('objective_zeromus') else 'the game'

    if env.meta['has_gated_objective']:
        pregame_text_lines.append(f" to win {gated_objective_reward_text}.\n")
        gated_desc = ' Then ' + OBJECTIVES[env.meta['gated_objective_id']]['desc'] + " to win " + completion_reward_text
        split_desc_lines = _split_lines(gated_desc)
        for j,gated_desc_line in enumerate(split_desc_lines):
            pregame_text_lines.append(f' {gated_desc_line}')
    else:
        # handle hard required objectives        
        if hard_required_objective_count > 0:
            pregame_text_lines.append(f'({hard_required_objective_count} hard required)')        
        pregame_text_lines.append(" to win " + completion_reward_text)

    env.spoilers.add_table("OBJECTIVES", spoilers, public=env.options.flags.has_any('-spoil:all', '-spoil:misc'))
    env.add_pregame_text("OBJECTIVES", "\n".join(pregame_text_lines), center=False)

    # apply additional objective needs
    if OBJECTIVE_SLUGS_TO_IDS['internal_dkmatter'] in objective_ids:
        dkmatter_count = int(env.options.flags.get_suffix('Omode:dkmatter'))
        env.add_substitution('dkmatter condition', f'    [#B #If #not_HasDkMatter {dkmatter_count}] {{')
        if dkmatter_count == 45:
            # special text for all 45
            env.add_substitution('kory dkmatter request', "Hi, I'm Kory! Could you\ndo me a favor and bring\nme all 45 DkMatters?\n\nThey are scattered in\nchests all across the\nworld and the moon!\nThanks!")
        else:
            request_text = f"Hi, I'm Kory! Could you\ndo me a favor and bring\nme {dkmatter_count} DkMatters?\n\nThere are 45 of them\nscattered in chests\nall across the world\nand the moon!\nBut I only need {dkmatter_count}.\nThanks!"
            env.add_substitution('kory dkmatter request', request_text) 
        env.add_file('scripts/dark_matter_hunt.f4c')
        
    if OBJECTIVE_SLUGS_TO_IDS['internal_goldhunter'] in objective_ids:
        target_gold = gold_hunt_count * 1000
        target_bin = [((target_gold >> (i * 8)) & 0xFF) for i in range(4)]
        env.add_binary(BusAddress(0x21fa06), target_bin,  as_script=True)
        env.add_file('scripts/gold_hunt.f4c')
        env.add_script('text(map #AstroTower message 7) {\nHi, I\'m Tory! Could you \ndo me a favor and get me\n'+gold_hunt_text+' GP? \n\nI\'m trying to buy one of \nthose fancy airships...}')
    
    if OBJECTIVE_SLUGS_TO_IDS['internal_external'] in objective_ids:
        env.add_file('scripts/external_objective.f4c')

    if OBJECTIVE_SLUGS_TO_IDS['internal_ki'] in objective_ids:
        env.add_toggle('ki_objective')
        if env.options.flags.has("objective_zeromus"):
            env.add_toggle('ki_objective_crystal')
        ki_count = int(env.options.flags.get_suffix('Omode:ki'))
        env.add_substitution('completed ki objective check', f"        cmp #${ki_count:02x}")

if __name__ == '__main__':
    print("Checking line lengths")
    for q in OBJECTIVES:
        desc = OBJECTIVES[q]['desc']
        lines = _split_lines(desc)
        if len(lines) > 2:
            print(f"Too long: {desc}")
