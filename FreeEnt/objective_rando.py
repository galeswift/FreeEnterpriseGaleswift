from .address import *
from .objective_data import *
from .errors import *
from . import util
from .spoilers import SpoilerRow
from . import character_rando
from .core_rando import STARTING_ITEM_MAP

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
    env.meta['objective_req_char_count'] = 0
    if not env.options.flags.has('objective_none'):
        env.meta['has_objectives'] = True
        env.meta['zeromus_required'] = env.options.flags.has("objective_zeromus")

        specified_objectives = dict()
        for i in range(CUSTOM_OBJECTIVE_COUNT):
            slug = env.options.flags.get_suffix(f"O{i+1}:")
            if slug:
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

        total_char_count = 0
        for objective_id in OBJECTIVES:
            objective = OBJECTIVES[objective_id]
            slug = objective['slug']            
            if specified_objectives.get(slug, False):
                if slug.startswith(CHAR_OBJECTIVE_PREFIX):
                    env.meta['objective_required_characters'].add(slug[len(CHAR_OBJECTIVE_PREFIX):])
                    total_char_count += 1
                elif slug.startswith(BOSS_OBJECTIVE_PREFIX):
                    env.meta['objective_required_bosses'].add(slug[len(BOSS_OBJECTIVE_PREFIX):])
                elif slug == 'quest_tradepink':
                    env.meta['objective_required_key_items'].add('#item.Pink')                

        if env.options.flags.get_suffix('Omode:dkmatter'):
            env.meta['required_treasures'].setdefault('#item.DkMatter', 0)
            env.meta['required_treasures']['#item.DkMatter'] += 45
        
        if env.options.flags.has('objective_mode_external'):
            env.meta['objective_starter_kit'] = [( 'fe_EagleEye', [1] )]

        # copy some of the logic from flagsetcore, in order to say exactly how many distinct characters we need
        # and how many tough quests we need, so that we have enough characters for character_rando
        # and save enough tough quests for the apply phase

        flags_objective_chars = []
        if env.options.flags.has('Cvanilla'):
            if not (env.options.flags.has('Cnofree') and not env.options.flags.has('Ctreasure:free')):
                for c in ['edward', 'tellah', 'palom', 'porom']:
                    flags_objective_chars.append(c)
            if not (env.options.flags.has('Cnoearned') and not env.options.flags.has('Ctreasure:earned')):
                for c in ['rydia', 'kain', 'rosa', 'yang', 'cid', 'edge', 'fusoya']:
                    flags_objective_chars.append(c)
            flags_objective_chars_num = len(flags_objective_chars)
        else:
            only_flags = env.options.flags.get_list(r'^Conly:')
            if len(only_flags) > 0:
                for f in only_flags:
                    ch = f[len('Conly:'):]
                    flags_objective_chars.append(ch)
            else:
                flags_objective_chars = ['cecil', 'kain', 'rydia', 'edward', 'tellah', 'rosa', 'yang', 'palom', 'porom', 'cid', 'edge', 'fusoya']
                for f in env.options.flags.get_list(r'^Cno:'):
                    ch = f[len('Cno:'):]
                    flags_objective_chars.remove(ch)
            flags_objective_chars_num = len(flags_objective_chars)
            distinct_flags = env.options.flags.get_list(r'^Cdistinct:')
            if len(distinct_flags) > 0:
                distinct_count = int(distinct_flags[0][len('Cdistinct:'):])
                flags_objective_chars_num = min(flags_objective_chars_num, distinct_count)

        max_non_tough_quests = len(TOUGH_QUEST_OBJECTIVES_EXCLUDED)
        if not specified_objectives.get('quest_pass', False) and not env.options.flags.has_any('Pkey', 'Pchests', 'Pshop'):
            max_non_tough_quests -= 1
        max_tough_quests = 22
        if not specified_objectives.get('quest_tradepink', False):
            if env.options.flags.has('Kvanilla') or (not env.options.flags.has_any('Ksummon', 'Kmoon', 'Kforge', 'Kpink', 'Kmiab:standard', 'Kmiab:above', 'Kmiab:below', 'Kmiab:lst', 'Kmiab:all') and env.options.flags.has('Pkey') and not env.options.flags.has('Owin:crystal') and env.options.flags.has('Kstart:zonk')):
                max_tough_quests -= 1
        group_scores = []
        for rand_pref in ['Orandom:', 'Orandom2:', 'Orandom3:']:
            rand_only_char_flags = env.options.flags.get_list(f'{rand_pref}only')

            all_customized_rand_flags = env.options.flags.get_list(f'^{rand_pref}'+ r'[^\d]')
            num_rand_objectives = env.options.flags.get_list(f'^{rand_pref}'+ r'[\d]')
            if len(num_rand_objectives) == 0:
                group_scores.append(0)
                continue
            grp_obj_num = int(num_rand_objectives[0][len(rand_pref):])

            # strip out only[char] flags to get only: boss, quest or tough_quest, char
            rand_category_flags = []
            for fl in all_customized_rand_flags:
                if fl not in rand_only_char_flags:
                    rand_category_flags.append(fl)

            if len(rand_category_flags) == 0 or f'{rand_pref}boss' in rand_category_flags:
                group_scores.append(100)
                continue

            # only len == 1 or 2 cases left, so just check and add
            grp_sc = 0
            if f'{rand_pref}char' in rand_category_flags:
                if len(rand_only_char_flags) > 0 and len(rand_only_char_flags) < flags_objective_chars_num:
                    grp_sc += len(rand_only_char_flags)
                else:
                    grp_sc += flags_objective_chars_num
            if f'{rand_pref}tough_quest' in rand_category_flags:
                grp_sc += max_tough_quests
            elif f'{rand_pref}quest' in rand_category_flags:
                grp_sc += max_tough_quests + max_non_tough_quests + 20

            grp_sc += (grp_obj_num - 4)
            group_scores.append(grp_sc)

        # sort the groups by score (lower score -> harder to place -> do first)
        sorted_prefixes_scores = sorted(zip(['Orandom:', 'Orandom2:', 'Orandom3:'], group_scores), key=(lambda p : p[1]))
        sorted_groups = [pair[0] for pair in sorted_prefixes_scores]
        env.meta['objective_group_order'] = sorted_groups

        total_mandatory_bosses = 0
        total_flexible_bosses = 0
        total_mandatory_tough_quests = 0
        total_flexible_tough_quests = 0
        total_mandatory_non_tough_quests = 0
        total_flexible_non_tough_quests = 0
        flexible_random_objective_count = 0
        total_objective_count = len(specified_objectives)

        flexible_char_count = 0
        flexible_char_pool = set()
        nonstarting_character_slots = 16
        if env.options.flags.has('Cnofree') and not env.options.flags.has('Ctreasure:free'):
            nonstarting_character_slots -= 5
        if env.options.flags.has('Cnoearned') and not env.options.flags.has('Ctreasure:earned'):
            nonstarting_character_slots -= 11
        elif env.options.flags.has('Omode:classicgiant'):
            nonstarting_character_slots -= 1
        # cap the number of characters we can actually have objectives for by the number of slots there are available
        flags_objective_chars_num = min(flags_objective_chars_num, nonstarting_character_slots)

        specific_boss_objectives = env.options.flags.get_list(r'^O[\d]:boss_')
        specific_tough_quest_objectives = env.options.flags.get_list(r'^O[\d]:quest_')
        for f in TOUGH_QUEST_OBJECTIVES_EXCLUDED:
            if f in specific_tough_quest_objectives:
                total_mandatory_non_tough_quests += 1
                specific_tough_quest_objectives.remove(f)
        total_mandatory_bosses += len(specific_boss_objectives)
        total_mandatory_tough_quests += len(specific_tough_quest_objectives)
        if env.options.flags.has('Omode:fiends'):
            total_mandatory_bosses += 6
        if env.options.flags.has('Omode:classicforge'):
            total_mandatory_tough_quests += 1
        if env.options.flags.has('Omode:classicgiant'):
            total_mandatory_tough_quests += 1


        # here's the big counting section from flagsetcore
        for random_prefix in sorted_groups:
            if len(env.options.flags.get_list(f'^{random_prefix}')) == 0:
                continue

            random_only_char_flags = env.options.flags.get_list(f'{random_prefix}only')

            # skip if no number of objectives has been set
            all_customized_random_flags = env.options.flags.get_list(f'^{random_prefix}'+ r'[^\d]')
            num_random_objectives = env.options.flags.get_list(f'^{random_prefix}'+ r'[\d]')
            if len(num_random_objectives) == 0:
                continue
            group_obj_num = int(num_random_objectives[0][len(random_prefix):])
            total_objective_count += group_obj_num

            # strip out only[char] flags to get only: boss, quest or tough_quest, char
            random_category_flags = []
            for fl in all_customized_random_flags:
                if fl not in random_only_char_flags:
                    random_category_flags.append(fl)

            # if bosses are available, they allow all other objective types to be skipped because there are >=32 of them
            # (if we run into issues with too many boss objectives, then we've already hit the objective cap)
            # note: this logic does not survive into 5.0, but that's already got a different objective group system
            bosses_available = False
            if f'{random_prefix}boss' in random_category_flags or len(random_category_flags) == 0:
                bosses_available = True

            # identify how many character objectives are *actually* available for this group, based on only[char] flags
            # and the characters available/seen so far
            only_chars_list = []
            for fl in random_only_char_flags:
                only_chars_list.append(fl[len(f'{random_prefix}only'):])
            just_in_case_mandatory_char_pool = set()

            # identify if there are only character objectives or not
            only_char_objectives = False
            if f'{random_prefix}char' in random_category_flags and len(random_category_flags) == 1:
                only_char_objectives = True

            # the next section only matters if we even have character objectives: otherwise, default
            # to no available character objectives (which makes sense)
            theoretical_available_characters = 0
            actual_available_characters = 0
            duplicate_char_count = 0 # len(character_pool)
            if f'{random_prefix}char' in random_category_flags:
                if len(random_only_char_flags) > 0:
                    # at this point, the character *can* be in the game (is in flags_objective_chars)
                    ch_list = only_chars_list
                    ch_count_cap = len(random_only_char_flags)
                else:
                    # start with the number of possible character objectives in the seed (possibly smaller than the number
                    # of characters that are available, due to slot restrictions/character uncertainty)
                    ch_list = flags_objective_chars
                    ch_count_cap = flags_objective_chars_num
                for current_char in ch_list:
                    # at this point, the character *can* be in the game (is in flags_objective_chars)
                    theoretical_available_characters += 1
                    # is this character already a mandatory char objective? 
                    if current_char in env.meta['objective_required_characters']:
                        duplicate_char_count += 1
                    else:
                        # if this is a guaranteed character objective, and it *must* be chosen, push to character_pool
                        if only_char_objectives and ch_count_cap == group_obj_num:
                            env.meta['objective_required_characters'].add(current_char)
                            flexible_char_pool.discard(current_char)
                        else:
                            just_in_case_mandatory_char_pool.add(current_char)
                            if current_char not in flexible_char_pool:
                                flexible_char_pool.add(current_char)

                # ensure that we can't actually have try to assign too many character objectives
                if theoretical_available_characters > flags_objective_chars_num:
                    theoretical_available_characters = flags_objective_chars_num
                # and ensure that we're counting the real number of character objectives that we've already assigned,
                # given by total_char_count: if total_char_count > duplicate_char_count, then increase duplicate_char_count,
                # but only if we weren't restricting characters to only specific ones
                if total_char_count > duplicate_char_count and len(random_only_char_flags) == 0:
                    duplicate_char_count = total_char_count
                # theoretical_available_characters - duplicate_char_count is the number of new potential char objectives that
                # this group can assign that we haven't already guaranteed
                actual_available_characters = theoretical_available_characters - duplicate_char_count

            # if we're here, then either it's not only character objectives, or there are 
            # at least as many actual_available_characters as group_obj_num.
            # in the former case, it's possible that we have a minimum number of required non-charater objectives,
            # which is hyper relevant if we don't have bosses. If we didn't have character objectives to begin with,
            # min_non_char_objectives will always be group_obj_num
            min_non_char_objectives = 0
            if actual_available_characters < group_obj_num:
                min_non_char_objectives = group_obj_num - actual_available_characters
            max_char_objectives = actual_available_characters
            # in addition, there may be all characters available, but of course we can only pick out so many objectives total
            while max_char_objectives > group_obj_num:
                max_char_objectives -= 1

            # now we start adding to our objective counts.
            # key thing to keep in mind: if we have mandatory objective types and we run out of room (which would otherwise
            # throw an error), we can use some of the flexible objectives to compensate (until we use them up)
            if bosses_available:
                # when bosses are available, everything is flexible (unless we're hitting the 32 objective cap,
                # which takes priority)
                if len(random_category_flags) == 1:
                    # in this case, there are only boss objectives
                    total_mandatory_bosses += group_obj_num
                elif len(random_category_flags) == 2 and f'{random_prefix}char' in random_category_flags:
                    # here, we have bosses and characters only, so some bosses may be required
                    total_mandatory_bosses += min_non_char_objectives
                    total_flexible_bosses += group_obj_num - min_non_char_objectives
                    flexible_char_count += max_char_objectives
                    flexible_random_objective_count += group_obj_num - min_non_char_objectives
                elif len(random_category_flags) == 2 and f'{random_prefix}char' not in random_category_flags:
                    # here we have bosses and either quests or tough quests
                    if f'{random_prefix}quest' in random_category_flags:
                        # here we need to ensure that our flexible counts are not exceeding the max
                        # allowed counts for these objectives: 22 for tough quests, 17 for non-tough quests
                        non_tough_quest_room = max_non_tough_quests - total_mandatory_non_tough_quests - total_flexible_non_tough_quests
                        tough_quest_room = max_tough_quests - total_mandatory_tough_quests - total_flexible_tough_quests
                        # we have four cases (and one subcase), depending on how many quests/tough quests we can have
                        if non_tough_quest_room < group_obj_num and tough_quest_room >= group_obj_num:
                            total_flexible_non_tough_quests += non_tough_quest_room
                            total_flexible_tough_quests += group_obj_num
                            total_flexible_bosses += group_obj_num
                            flexible_random_objective_count += group_obj_num
                        elif non_tough_quest_room >= group_obj_num and tough_quest_room < group_obj_num:
                            total_flexible_non_tough_quests += group_obj_num
                            total_flexible_tough_quests += tough_quest_room
                            total_flexible_bosses += group_obj_num
                            flexible_random_objective_count += group_obj_num
                        elif non_tough_quest_room < group_obj_num and tough_quest_room < group_obj_num:
                            total_flexible_non_tough_quests += non_tough_quest_room
                            total_flexible_tough_quests += tough_quest_room
                            if non_tough_quest_room + tough_quest_room < group_obj_num:
                                total_mandatory_bosses += group_obj_num - non_tough_quest_room - tough_quest_room
                                total_flexible_bosses += non_tough_quest_room + tough_quest_room
                                flexible_random_objective_count += non_tough_quest_room + tough_quest_room
                            else:
                                total_flexible_bosses += group_obj_num
                                flexible_random_objective_count += group_obj_num
                        else:
                            total_flexible_non_tough_quests += group_obj_num
                            total_flexible_tough_quests += group_obj_num
                            total_flexible_bosses += group_obj_num
                            flexible_random_objective_count += group_obj_num
                    elif f'{random_prefix}tough_quest' in random_category_flags:
                        # same, but only for tough_quests, which decreases the number of cases
                        tough_quest_room = max_tough_quests - total_mandatory_tough_quests - total_flexible_tough_quests
                        if tough_quest_room < group_obj_num:
                            total_flexible_tough_quests += tough_quest_room
                            total_mandatory_bosses += group_obj_num - tough_quest_room
                            total_flexible_bosses += tough_quest_room
                            flexible_random_objective_count += tough_quest_room
                        else:
                            total_flexible_tough_quests += group_obj_num
                            total_flexible_bosses += group_obj_num
                            flexible_random_objective_count += group_obj_num
                elif len(random_category_flags) == 3 and f'{random_prefix}tough_quest' in random_category_flags:
                    # here, we have all possible objectives available except non-tough quests
                    tough_quest_room = max_tough_quests - total_mandatory_tough_quests - total_flexible_tough_quests
                    # so, we have three cases
                    if tough_quest_room < group_obj_num and min_non_char_objectives == 0:
                        total_flexible_tough_quests += tough_quest_room
                        flexible_char_count += max_char_objectives # which in this case is group_obj_num
                        total_flexible_bosses += group_obj_num
                        flexible_random_objective_count += group_obj_num
                    elif tough_quest_room < group_obj_num and min_non_char_objectives > 0:
                        # possibly have mandatory bosses here
                        total_flexible_tough_quests += tough_quest_room
                        flexible_char_count += max_char_objectives
                        if tough_quest_room + max_char_objectives < group_obj_num:
                            total_mandatory_bosses += group_obj_num - tough_quest_room - max_char_objectives
                            total_flexible_bosses += tough_quest_room + max_char_objectives
                            flexible_random_objective_count += tough_quest_room + max_char_objectives
                        else:
                            total_flexible_bosses += group_obj_num
                            flexible_random_objective_count += group_obj_num
                    else: 
                        # tough_quest_room >= group_obj_num means we don't care what min_non_char_objectives does
                        flexible_char_count += max_char_objectives
                        total_flexible_tough_quests += group_obj_num
                        total_flexible_bosses += group_obj_num
                        flexible_random_objective_count += group_obj_num
                else:
                    # all types of objectives are available
                    non_tough_quest_room = max_non_tough_quests - total_mandatory_non_tough_quests - total_flexible_non_tough_quests
                    tough_quest_room = max_tough_quests - total_mandatory_tough_quests - total_flexible_tough_quests
                    if non_tough_quest_room < group_obj_num:
                        total_flexible_non_tough_quests += non_tough_quest_room
                    else:
                        total_flexible_non_tough_quests += group_obj_num
                    if tough_quest_room < group_obj_num:
                        total_flexible_non_tough_quests += tough_quest_room
                    else:
                        total_flexible_tough_quests += group_obj_num
                    flexible_char_count += max_char_objectives
                    total_flexible_bosses += group_obj_num
                    flexible_random_objective_count += group_obj_num

            # now bosses are *not* available, which means we either have just characters, just quests/tough quests,
            # or both of those categories.
            elif len(random_category_flags) == 1:
                if f'{random_prefix}char' in random_category_flags:
                    # only characters! so we have mandatory character objectives, and we've already
                    # confirmed that we have enough characters available for them, and handled with
                    # mandatory/flexible character pool stuff
                    total_char_count += group_obj_num
                elif f'{random_prefix}quest' in random_category_flags:
                    # quests and tough quests, do similar to the above
                    non_tough_quest_room = max_non_tough_quests - total_mandatory_non_tough_quests - total_flexible_non_tough_quests
                    tough_quest_room = max_tough_quests - total_mandatory_tough_quests - total_flexible_tough_quests
                    # now, we carefully add to totals
                    if non_tough_quest_room < group_obj_num and tough_quest_room >= group_obj_num:
                        total_flexible_non_tough_quests += non_tough_quest_room
                        total_mandatory_tough_quests += group_obj_num - non_tough_quest_room
                        total_flexible_tough_quests += non_tough_quest_room
                        flexible_random_objective_count += non_tough_quest_room
                    elif non_tough_quest_room >= group_obj_num and tough_quest_room < group_obj_num:
                        total_flexible_tough_quests += tough_quest_room
                        total_mandatory_non_tough_quests += group_obj_num - tough_quest_room
                        total_flexible_non_tough_quests += tough_quest_room
                        flexible_random_objective_count += tough_quest_room
                    elif non_tough_quest_room < group_obj_num and tough_quest_room < group_obj_num:
                        total_mandatory_non_tough_quests += group_obj_num - tough_quest_room
                        total_flexible_non_tough_quests += non_tough_quest_room - (group_obj_num - tough_quest_room)
                        total_mandatory_tough_quests += group_obj_num - non_tough_quest_room
                        total_flexible_tough_quests += tough_quest_room - (group_obj_num - non_tough_quest_room)
                        flexible_random_objective_count += non_tough_quest_room + tough_quest_room - group_obj_num
                    else:
                        total_flexible_non_tough_quests += group_obj_num
                        total_flexible_tough_quests += group_obj_num
                        flexible_random_objective_count += group_obj_num
                else:
                    # just tough quests! that's the only case left
                    tough_quest_room = max_tough_quests - total_mandatory_tough_quests - total_flexible_tough_quests
                    if tough_quest_room < group_obj_num:
                        total_mandatory_tough_quests += tough_quest_room
                        total_flexible_tough_quests -= (group_obj_num - tough_quest_room)
                    else:
                        total_mandatory_tough_quests += group_obj_num
            
            else:
                # we have characters and either all quests or just tough quests.
                if f'{random_prefix}tough_quest' in random_category_flags:
                    tough_quest_room = max_tough_quests - total_mandatory_tough_quests - total_flexible_tough_quests
                    if tough_quest_room + max_char_objectives < group_obj_num:
                        total_mandatory_tough_quests += tough_quest_room
                        total_flexible_tough_quests -= (group_obj_num - tough_quest_room - max_char_objectives)
                        total_char_count += max_char_objectives
                    elif tough_quest_room < min_non_char_objectives:
                        total_mandatory_tough_quests += tough_quest_room
                        total_flexible_tough_quests -= (min_non_char_objectives - tough_quest_room)
                        total_char_count += max_char_objectives
                    elif min_non_char_objectives == 0:
                        # we can fill the entire group with character objectives!
                        # but we might have *guaranteed* char objectives
                        if tough_quest_room < group_obj_num:
                            total_char_count += group_obj_num - tough_quest_room
                            flexible_char_count += tough_quest_room
                            total_flexible_tough_quests += tough_quest_room
                            # if tough_quest_room was actually just 0, then these are *mandatory* character objectives,
                            # so if actual_available_characters is equal to group_obj_num, then we need to
                            # push all of the characters to character_pool (possibly removing from flexible_char_pool)
                            if actual_available_characters == group_obj_num:
                                for ch in just_in_case_mandatory_char_pool:
                                    env.meta['objective_required_characters'].add(current_char)
                                    flexible_char_pool.discard(current_char)
                            else:
                                flexible_random_objective_count += tough_quest_room
                        else:
                            flexible_char_count += group_obj_num
                            total_flexible_tough_quests += group_obj_num
                            flexible_random_objective_count += group_obj_num
                    else:
                        # we *must* have non-character objectives.
                        if tough_quest_room < group_obj_num:
                            # keeping flexibility in tough quests in mind, we might not have character objectives at all
                            if tough_quest_room + total_flexible_tough_quests < group_obj_num:
                                # we also *must* have some character objectives
                                total_char_count += group_obj_num - (tough_quest_room + total_flexible_tough_quests)
                                flexible_char_count += max_char_objectives - (group_obj_num - tough_quest_room - total_flexible_tough_quests)
                                total_mandatory_tough_quests += min_non_char_objectives
                                # before we change total_flexible_tough_quests, we need to up the flexible random objective count;
                                # the amount we add is just group_obj_num minus the amounts we added to total_char_count and total_mandatory_tough_quests
                                flexible_random_objective_count += tough_quest_room + total_flexible_tough_quests - min_non_char_objectives
                                total_flexible_tough_quests += tough_quest_room - min_non_char_objectives
                            else:
                                # we can use flexible tough quests to handle everything
                                if tough_quest_room < min_non_char_objectives:
                                    total_mandatory_tough_quests += tough_quest_room
                                    total_flexible_tough_quests += (group_obj_num - min_non_char_objectives) - (min_non_char_objectives - tough_quest_room)
                                    flexible_char_count += max_char_objectives
                                    flexible_random_objective_count += group_obj_num - min_non_char_objectives
                                else:
                                    total_mandatory_tough_quests += min_non_char_objectives
                                    total_flexible_tough_quests += group_obj_num - min_non_char_objectives
                                    flexible_char_count += max_char_objectives
                                    flexible_random_objective_count += group_obj_num - min_non_char_objectives
                        else:
                            # some mandatory tough_quests, and the rest are flexible
                            total_mandatory_tough_quests += min_non_char_objectives
                            total_flexible_tough_quests += group_obj_num - min_non_char_objectives
                            flexible_char_count += max_char_objectives
                            flexible_random_objective_count += group_obj_num - min_non_char_objectives
                
                else:
                    # chars, non-tough quests, and tough quests are what's left. This should never
                    # pose issues, given how many non-tough quests there are. In particular, 
                    # even in the last group, you can only have 2+8+8+8 = 26 quest/tough quests used up, and 39-26 = 13 > 8,
                    # so non_tough_quest_room + tough_quest_room will always be larger than group_obj_num here.
                    non_tough_quest_room = max_non_tough_quests - total_mandatory_non_tough_quests - total_flexible_non_tough_quests
                    tough_quest_room = max_tough_quests - total_mandatory_tough_quests - total_flexible_tough_quests
                    if min_non_char_objectives == 0:
                        # can fill with char objectives; we'll never *need* char objectives, but
                        # there might be caps on non/tough quests
                        flexible_char_count += group_obj_num
                        flexible_random_objective_count += group_obj_num
                        if non_tough_quest_room < group_obj_num:
                            total_flexible_non_tough_quests += non_tough_quest_room
                        else:  
                            total_flexible_non_tough_quests += group_obj_num
                        if tough_quest_room < group_obj_num:
                            total_flexible_tough_quests += tough_quest_room
                        else:
                            total_flexible_tough_quests += group_obj_num
                    else:
                        # there are guaranteed non-char objectives.
                        # which mostly just means that we cap the char objective addition,
                        # and exactly one of tough/non-tough quests because of the above calculation
                        flexible_char_count += group_obj_num - min_non_char_objectives
                        flexible_random_objective_count += group_obj_num
                        if non_tough_quest_room < group_obj_num:
                            total_flexible_non_tough_quests += non_tough_quest_room
                            total_flexible_tough_quests += group_obj_num
                        elif tough_quest_room < group_obj_num:
                            total_flexible_non_tough_quests += group_obj_num
                            total_flexible_tough_quests += tough_quest_room
                        else:
                            # can fill the group with either non/tough quests
                            total_flexible_non_tough_quests += group_obj_num
                            total_flexible_tough_quests += group_obj_num

            # we have now, finally, hopefully, added to all of the relevant counts as required
            # by the flags and what we've seen previously

        env.meta['objective_req_char_count'] += total_char_count # at least as many as the required objective characters
        env.meta['allowable_removed_tough_quests'] = min(max_tough_quests - total_mandatory_tough_quests, 8) # possibly none, up to 8
        # edge case handling: *if* the Pink Tail can potentially be removed from this seed given the KI slots, then do the following:
        #  - if max_tough_quests - total_mandatory_tough_quests == 0, then guarantee the Pink Tail into the seed as an objective-required item
        #  - if it's > 0, then subtract 1 from this value to ensure that we save a tough quest in case the Pink Tail gets randomly removed
        #    by core_rando's priority assigner. 
        if not env.options.flags.has_any('Ksummon', 'Kmoon', 'Kpink', 'Kmiab:standard', 'Kmiab:above', 'Kmiab:below', 'Kmiab:lst', 'Kmiab:all'):
            slots_num_pink = 0
            if env.options.flags.has('Kforge'):
                slots_num_pink += 1
            if env.options.flags.has('Pkey'):
                slots_num_pink -= 1
            if not env.options.flags.has('Owin:crystal'):
                slots_num_pink -= 1
            if env.options.flags.has('Kstart:zonk'):
                slots_num_pink -= 1
            if slots_num_pink < 0:
                if max_non_tough_quests - total_mandatory_tough_quests == 0:
                    env.meta['objective_required_key_items'].add('#item.Pink')
                else:
                    # that difference is positive, so the min of that value and 8 is positive
                    env.meta['allowable_removed_tough_quests'] -= 1

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
                starting_key_items = env.options.flags.get_list(rf'^Kstart:')
                for key_item in starting_key_items:
                    if STARTING_ITEM_MAP.get(key_item,'zonk') == env.meta['gated_objective_reward']:
                        raise BuildError(f"The starting item cannot also be the gated objective reward.")
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

    # objective_ids = get_unique_objective_ids(env)
    # generate random objectives
    # try multiple times, in case the chosen objectives in the first groups
    # do not allow all objectives to be chosen in the latter groups
    # (e.g. too many character objectives in early groups and only character objectives in the last group)
    MAX_OBJECTIVE_ATTEMPTS = 100
    rand_objective_attempts = 0
    found_valid_objective_set = False

    bosses_in_restricted_slots = env.meta['bosses_in_restricted_slots']

    while not found_valid_objective_set and rand_objective_attempts < MAX_OBJECTIVE_ATTEMPTS:
        objective_ids = get_unique_objective_ids(env)
        restart_all_groups = False

        # prune the allowable tough quests here, using env.meta['allowable_removed_tough_quests']
        potential_removed_tough_quest_num = env.meta['allowable_removed_tough_quests']
        tough_quests_to_remove = env.rnd.sample(TOUGH_QUEST_OBJECTIVES_WEIGHTED, potential_removed_tough_quest_num)
        # print(tough_quests_to_remove)

        unrestricted_non_objective_bosses = env.meta['unrestricted_non_objective_bosses'].copy()

        # print("Objectives randomization attempt number " + f"{rand_objective_attempts}")
        for random_prefix in env.meta['objective_group_order']:
            # print("Now handling group " + random_prefix)
            random_objective_count = 0
            for f in env.options.flags.get_list(rf'^{random_prefix}\d'):            
                random_objective_count = int(f[len(random_prefix):])

            # print(f"Random objective count is {random_objective_count} for {random_prefix}")
            random_objective_allowed_types = set()
            random_objective_allowed_characters = set()
            tough_quests_only = False
            for f in env.options.flags.get_list(rf'^{random_prefix}[^\d]'):
                allowed_type = f[len(random_prefix):]   
                if (allowed_type == 'tough_quest'):
                    allowed_type = 'quest'
                    tough_quests_only = True
                if allowed_type.startswith('only'): 
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
                        if obj['slug'] in tough_quests_to_remove and env.rnd.random() < 0.40:
                            # only possibly remove tough quests that we specified could be removed earlier
                            continue
                        if objective_id in objective_ids:
                            # pre-cull objectives we've already specified, to help the randomizer
                            continue
                        random_objective_pool.setdefault(category, []).append(objective_id)
            random_category_weights = RANDOM_CATEGORY_WEIGHTS
            if random_objective_allowed_types:
                random_category_weights = { k : RANDOM_CATEGORY_WEIGHTS[k] for k in RANDOM_CATEGORY_WEIGHTS if k in random_objective_allowed_types }
            random_category_distribution = util.Distribution(**random_category_weights)

            # 10k is probably overkill. Try 100 attempts to choose the objectives (per group). or some smaller number.
            MAX_RANDOMIZATION_ATTEMPTS = 200
            retry_count = 0
            for i in range(random_objective_count):
                while retry_count <= MAX_RANDOMIZATION_ATTEMPTS:     
                    retry_count += 1         
                    category = random_category_distribution.choose(env.rnd)
                    q = env.rnd.choice(random_objective_pool[category])
                    slug = OBJECTIVES[q]['slug']    
                    # print(f'Considering {slug}')            
                    if q in objective_ids:
                        continue
                    if slug.startswith(CHAR_OBJECTIVE_PREFIX):
                        char = slug[len(CHAR_OBJECTIVE_PREFIX):]
                        if char not in env.meta['available_nonstarting_characters']:
                            # print(f'{char} is only a starting/partner character, or is not available at all')
                            continue
                        if len(random_objective_allowed_characters) != 0 and (char not in random_objective_allowed_characters):
                            # print(f'{char} not allowed in types {random_objective_allowed_characters}')
                            continue
                    elif slug.startswith(BOSS_OBJECTIVE_PREFIX):
                        boss = slug[len(BOSS_OBJECTIVE_PREFIX):]
                        if boss not in env.meta['available_bosses']:
                            continue
                        if (boss in bosses_in_restricted_slots) and unrestricted_non_objective_bosses:
                            continue
                        # keep this boss objective; update set if we need to
                        unrestricted_non_objective_bosses.difference_update(set([boss]))
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
                if retry_count > MAX_RANDOMIZATION_ATTEMPTS:
                    # give up on this objectives assignment, and try again from the beginning of all three groups
                    # (yes, the attempt where retry_count == MAX_... is ignored; suboptimal coding)
                    # raise BuildError(f"Failed to generate {random_objective_count} randomized objectives after many attempts. ({total_char_count} total unique characters)")
                    # print(f"Failed to generate {random_objective_count} randomized objectives after {MAX_RANDOMIZATION_ATTEMPTS} attempts. ({total_char_count} total unique characters)")
                    rand_objective_attempts += 1
                    found_valid_objective_set = False
                    restart_all_groups = True
                    break
                else:
                    objective_ids.append(q)
                #     print(objective_ids)
                #     print("Attempts: " + f"{retry_count}")
                # print(f"i = {i}")

            if restart_all_groups:
                restart_all_groups = False
                # print("Restarting all three groups over")
                break
            else:
                found_valid_objective_set = True




    if not found_valid_objective_set or rand_objective_attempts >= MAX_OBJECTIVE_ATTEMPTS:
        raise BuildError(f"Failed to generate randomized objectives after {MAX_OBJECTIVE_ATTEMPTS} attempts; aborting")
    # else:
    #     print("Successfully randomized objectives! It took " + f"{rand_objective_attempts+1} attempts.")

    # shuffle boss objectives so that it's not obvious which bosses are in restricted slots (the algorithm above,
    # combined with the printing of the boss objectives in order, means bosses in restricted slots are listed last,
    # if there are any)
    all_boss_objectives = []
    for obj_id in objective_ids:
        if 'boss' in OBJECTIVES[obj_id]['slug']:
            all_boss_objectives.append(obj_id)
    env.rnd.shuffle(all_boss_objectives)
    boss_idx = 0
    for i in range(len(objective_ids)):
        if 'boss' in OBJECTIVES[objective_ids[i]]['slug']:
            objective_ids[i] = all_boss_objectives[boss_idx]
            boss_idx += 1

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
        if boss_hunt_count == 34:
            # let Omode:bosscollector34 also function as "all"
            if env.options.flags.has('no_kingqueen_slot'):
                boss_hunt_count -= 1
            if env.options.flags.has('no_officer_slot'):
                boss_hunt_count -= 1

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
        # add key to gated objective, add crystals to hard-required objectives;
        # note that this step happens after the split/sanity check, so if a line is too long
        # the text will overflow onto e.g. the tracker screen (capped at 24 chars per line).
        # the pre-game screen has no border, so it gets an extra character, and the textbox 
        # upon completion can have 26+ characters per line.
        # so far, the only problematic objective for the tracker is Break the Dark Elf's spell
        # with the TwinHarp.
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
            if '[key]' in line:
                env.add_binary(BusAddress(addr), [len(line)-4], as_script=True)
            elif '[crystal]' in line:
                env.add_binary(BusAddress(addr), [len(line)-8], as_script=True)
            else:
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
