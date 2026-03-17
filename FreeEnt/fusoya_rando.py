from . import databases
from .boss_rando import BOSS_SPOILER_NAMES
from .util import Distribution

STARTING_WHITE = [    # formerly for Ordeals buff, now for nerfed
    '#spell.Hold', '#spell.Mute', '#spell.Charm', '#spell.Blink',
    '#spell.Fast', '#spell.Peep', '#spell.Cure1', '#spell.Cure2',
    '#spell.Heal', '#spell.Life1', '#spell.Size', '#spell.Exit',
    '#spell.Sight', '#spell.Float'
    ]

STARTING_WHITE_JAPANESE = [    # formerly for Ordeals buff, now for nerfed
    '#spell.Armor', '#spell.Shell', '#spell.Dspel'
    ]

STARTING_BLACK = [    # formerly for Ordeals buff, now for nerfed
    '#spell.Toad', '#spell.Piggy', '#spell.Warp', '#spell.Venom',
    '#spell.Fire1', '#spell.Fire2', '#spell.Ice1', '#spell.Ice2',
    '#spell.Lit1', '#spell.Lit2', '#spell.Sleep', '#spell.Stone',
    '#spell.Drain', '#spell.Psych'
    ]

STARTING_CALL = [    # for nerfed with all_spells
    '#spell.Imp', '#spell.Bomb', '#spell.Choco', 
    ]

JAPANESE_EXCLUSIVE_SPELLS = [
    '#spell.Armor', '#spell.Shell', '#spell.Dspel'
    ]

OMNI_SPELLS = [
    '#spell.Imp',
    '#spell.Bomb',
    '#spell.Mage',
    '#spell.Chocb',
    '#spell.Shiva',
    '#spell.Indra',
    '#spell.Jinn',
    '#spell.Titan',
    '#spell.Mist',
    '#spell.Sylph',
    '#spell.Odin',
    '#spell.Levia',
    '#spell.Asura',
    '#spell.Baham',
    '#spell.Comet',
    '#spell.Flare',
    '#spell.Flame',
    '#spell.Flood',
    '#spell.Blitz',
    '#spell.Smoke',
    '#spell.Pin',
    '#spell.Image'
    ]

OMNI_J_SPELLS = [
    '#spell.Cocka',
    ]

ALL_SPELLS_BY_LEVEL_P = {   # used for sequential Fu. based on a mashup of Porom/Palom's spells
    '#spell.Ice1'  : 1, # 10
    '#spell.Cure1' : 0, # 10
    '#spell.Sight' : 0, # 10
    '#spell.Lit1'  : 1, # 10
    '#spell.Peep'  : 0, # 10
    '#spell.Fire1' : 1, # 10
    '#spell.Hold'  : 0, # 10
    '#spell.Sleep' : 1, # 10
    '#spell.Slow'  : 0, # 10
    '#spell.Venom' : 1, # 10
    '#spell.Ice2'  : 1, # 11
    '#spell.Life1' : 0, # 11
    '#spell.Flare' : 2, # via Twin, give it after three bosses
    '#spell.Piggy' : 1, # 12
    '#spell.Armor' : 0, # 12
    '#spell.Fire2' : 1, # 12
    '#spell.Cure2' : 0, # 12
    '#spell.Lit2'  : 1, # 13
    '#spell.Comet' : 2, # via Twin, give it after five bosses
    '#spell.Stop'  : 1, # 14
    '#spell.Mute'  : 0, # 15
    '#spell.Bersk' : 0, # 18
    '#spell.Exit'  : 0, # 19
    '#spell.Virus' : 1, # 19
    '#spell.Heal'  : 0, # 20
    '#spell.Toad'  : 1, # 22
    '#spell.Blink' : 0, # 23
    '#spell.Quake' : 1, # 23
    '#spell.Charm' : 0, # 25
    '#spell.Flame' : 2, # 25 (Edge)
    '#spell.Drain' : 1, # 26
    '#spell.Pin'   : 2, # 27 (Edge)
    '#spell.Shell' : 0, # 29
    '#spell.Warp'  : 1, # 29
    '#spell.Dspel' : 0, # 31
    '#spell.Size'  : 0, # 31
    '#spell.Ice3'  : 1, # 32
    '#spell.Smoke' : 2, # 33 (Edge)
    '#spell.Cure3' : 0, # 33
    '#spell.Fire3' : 1, # 33
    '#spell.Lit3'  : 1, # 34
    '#spell.Stone' : 1, # 36
    '#spell.Image' : 2, # 38 (Edge)
    '#spell.Fast'  : 0, # 38
    '#spell.Float' : 0, # 40
    '#spell.Psych' : 1, # 40
    '#spell.Wall'  : 0, # 44
    '#spell.Fatal' : 1, # 46
    '#spell.Cure4' : 0, # 48 **** Porom learns it late, b0ard shifted it down to 40 (between Float/Psych) for balance
    '#spell.Weak'  : 1, # 48
    '#spell.Meteo' : 1, # 50
    '#spell.White' : 0, # 52
    '#spell.Nuke'  : 1, # 52
    '#spell.Life2' : 0, # 56 **** Porom learns it super late, b0ard shifted it down to 45 for balance
    }
    
ALL_SPELLS_BY_LEVEL_R = {   # used for sequential Rosa/Rydia-based Fu, based on their spells instead (no Fire1 or Exit or tier2s)
    '#spell.Chocb' : 2, # 1 
    '#spell.Ice1'  : 1, # 2 
    '#spell.Cure1' : 0, # 3 (Child Rydia)
    '#spell.Sight' : 0, # 4 (Child Rydia)
    '#spell.Lit1'  : 1, # 5
    '#spell.Hold'  : 0, # 7 (Child Rydia)
    '#spell.Sleep' : 1, # 8
    '#spell.Slow'  : 0, # 10
    '#spell.Venom' : 1, # 10
    '#spell.Peep'  : 0, # 10
    '#spell.Life1' : 0, # 11
    '#spell.Warp'  : 1, # 12
    '#spell.Toad'  : 1, # 13
    '#spell.Cure2' : 0, # 13
    '#spell.Stop'  : 1, # 15
    '#spell.Mute'  : 0, # 15
    '#spell.Heal'  : 0, # 18
    '#spell.Piggy' : 1, # 20
    '#spell.Bersk' : 0, # 20
    '#spell.Blink' : 0, # 23
    '#spell.Charm' : 0, # 24
    '#spell.Flame' : 2, # 25 (Edge)
    '#spell.Virus' : 1, # 26    
    '#spell.Pin'   : 2, # 27 (Edge)
    '#spell.Cure3' : 0, # 28 (here's where Rosa's j-spells diverge)
    '#spell.Size'  : 0, # 29
    '#spell.Fast'  : 0, # 30
    '#spell.Psych' : 1, # 31 (here's where Rydia's j-spells diverge)
    '#spell.Float' : 0, # 32
    '#spell.Smoke' : 2, # 33 (Edge)
    '#spell.Wall'  : 0, # 34
    '#spell.Drain' : 1, # 35    
    '#spell.Image' : 2, # 38 (Edge)
    '#spell.Ice3'  : 1, # 38
    '#spell.Cure4' : 0, # 38
    '#spell.Fire3' : 1, # 40
    '#spell.Lit3'  : 1, # 42
    '#spell.Life2' : 0, # 42
    '#spell.Quake' : 1, # 44    
    '#spell.Stone' : 1, # 46    
    '#spell.Weak'  : 1, # 48  
    '#spell.White' : 0, # 48
    '#spell.Fatal' : 1, # 49    
    '#spell.Nuke'  : 1, # 50    
    '#spell.Meteo' : 1, # 60    
    }

ALL_SPELLS_BY_LEVEL_R_J = {   # used for sequential Rosa/Rydia-based Fu, based on their j-spells instead (no Fire1 or Exit or tier2s)
    '#spell.Chocb' : 2, # 1 
    '#spell.Ice1'  : 1, # 2 
    '#spell.Cure1' : 0, # 3 (Child Rydia)
    '#spell.Sight' : 0, # 4 (Child Rydia)
    '#spell.Lit1'  : 1, # 5
    '#spell.Hold'  : 0, # 7 (Child Rydia)
    '#spell.Sleep' : 1, # 8
    '#spell.Slow'  : 0, # 10
    '#spell.Venom' : 1, # 10
    '#spell.Peep'  : 0, # 10
    '#spell.Life1' : 0, # 11
    '#spell.Warp'  : 1, # 12
    '#spell.Armor' : 0, # 12
    '#spell.Toad'  : 1, # 13
    '#spell.Cure2' : 0, # 13
    '#spell.Mute'  : 0, # 15
    '#spell.Stop'  : 1, # 15
    '#spell.Heal'  : 0, # 18
    '#spell.Piggy' : 1, # 20
    '#spell.Bersk' : 0, # 20
    '#spell.Blink' : 0, # 23
    '#spell.Charm' : 0, # 24
    '#spell.Flame' : 2, # 25 (Edge)
    '#spell.Virus' : 1, # 26    
    '#spell.Pin'   : 2, # 27 (Edge)
    '#spell.Cure3' : 0, # 28 (here's where Rosa's j-spells diverge)
    '#spell.Shell' : 0, # 29
    '#spell.Size'  : 0, # 30
    '#spell.Dspel' : 0, # 31
    '#spell.Psych' : 1, # 32 (here's where Rydia's j-spells diverge)
    '#spell.Smoke' : 2, # 33 (Edge)
    '#spell.Fast'  : 0, # 33
    '#spell.Float' : 0, # 35
    '#spell.Wall'  : 0, # 36
    '#spell.Drain' : 1, # 36    
    '#spell.Image' : 2, # 38 (Edge)
    '#spell.Cure4' : 0, # 38
    '#spell.Ice3'  : 1, # 39
    '#spell.Fire3' : 1, # 42
    '#spell.Lit3'  : 1, # 45
    '#spell.Life2' : 0, # 45
    '#spell.Quake' : 1, # 47    
    '#spell.Stone' : 1, # 49    
    '#spell.Weak'  : 1, # 51  
    '#spell.Fatal' : 1, # 52    
    '#spell.White' : 0, # 55
    '#spell.Nuke'  : 1, # 55    
    '#spell.Meteo' : 1, # 60    
    }

ALL_SPELLS_BY_GOODNESS = { # used for maybe and regular
    '#spell.Sight' : 0,
    '#spell.Peep'  : 0,
    '#spell.Cure1' : 0,
    '#spell.Imp'   : 2,
    '#spell.Venom' : 1,
    '#spell.Toad'  : 1,
    '#spell.Piggy' : 1,
    '#spell.Ice1'  : 1,
    '#spell.Lit1'  : 1,
    '#spell.Fire1' : 1,
    '#spell.Sleep' : 1,
    '#spell.Charm' : 0,
    '#spell.Drain' : 1,
    '#spell.Chocb' : 2,
    '#spell.Shell' : 0,
    '#spell.Psych' : 1,
    '#spell.Mute'  : 0,
    '#spell.Size'  : 0,
    '#spell.Pin'   : 2,
    '#spell.Smoke' : 2,
    '#spell.Armor' : 0,
    '#spell.Dspel' : 0,
    '#spell.Bomb'  : 2,

    '#spell.Slow'  : 0,
    '#spell.Image' : 2,
    '#spell.Cure2' : 0,
    '#spell.Float' : 0,
    '#spell.Hold'  : 0,
    '#spell.Blink' : 0,
    '#spell.Ice2'  : 1,
    '#spell.Life1' : 0,
    '#spell.Fire2' : 1,
    '#spell.Lit2'  : 1,
    '#spell.Mage'  : 2,
    '#spell.Cocka' : 2,
    '#spell.Stop'  : 1,
    '#spell.Exit'  : 0,
    '#spell.Heal'  : 0,
    '#spell.Flare' : 2,
    '#spell.Shiva' : 2,
    '#spell.Indra' : 2,
    '#spell.Jinn'  : 2,
    '#spell.Warp'  : 1,
    '#spell.Mist'  : 2,
    '#spell.Asura' : 2,
    '#spell.Odin'  : 2,
    '#spell.Comet' : 2,
    '#spell.Flame' : 2,
    '#spell.Cure3' : 0,
    '#spell.Stone' : 1,
    '#spell.Flood' : 2,
    '#spell.Fast'  : 0,
    '#spell.Wall'  : 0,

    '#spell.Virus' : 1,
    '#spell.Sylph' : 2,
    '#spell.Blitz' : 2,
    '#spell.Titan' : 2,
    '#spell.Fire3' : 1,
    '#spell.Ice3'  : 1,
    '#spell.Lit3'  : 1,
    '#spell.Quake' : 1,
    '#spell.Bersk' : 0,
    '#spell.Cure4' : 0,
    '#spell.Levia' : 2,
    '#spell.Life2' : 0,
    '#spell.Fatal' : 1,
    '#spell.Weak'  : 1,
    '#spell.Meteo' : 1,
    '#spell.White' : 0,
    '#spell.Baham' : 2,
    '#spell.Nuke'  : 1,
    }
    
INTERNAL_SPELL_ORDER = { # used for (vanilla plus maybe)
    '#spell.Hold'  : 0,
    '#spell.Mute'  : 0,
    '#spell.Charm' : 0,
    '#spell.Blink' : 0,
    '#spell.Armor' : 0,
    '#spell.Shell' : 0,
    '#spell.Slow'  : 0,
    '#spell.Fast'  : 0,
    '#spell.Bersk' : 0,
    '#spell.Wall'  : 0,
    '#spell.White' : 0,
    '#spell.Dspel' : 0,
    '#spell.Peep'  : 0,
    '#spell.Cure1' : 0,
    '#spell.Cure2' : 0,
    '#spell.Cure3' : 0,
    '#spell.Cure4' : 0,
    '#spell.Heal'  : 0,
    '#spell.Life1' : 0,
    '#spell.Life2' : 0,
    '#spell.Size'  : 0,
    '#spell.Exit'  : 0,
    '#spell.Sight' : 0,
    '#spell.Float' : 0,
    
    '#spell.Toad'  : 1,
    '#spell.Piggy' : 1,
    '#spell.Warp'  : 1,
    '#spell.Venom' : 1,
    '#spell.Fire1' : 1,
    '#spell.Fire2' : 1,
    '#spell.Fire3' : 1,
    '#spell.Ice1'  : 1,
    '#spell.Ice2'  : 1,
    '#spell.Ice3'  : 1,
    '#spell.Lit1'  : 1,
    '#spell.Lit2'  : 1,
    '#spell.Lit3'  : 1,
    '#spell.Virus' : 1,
    '#spell.Weak'  : 1,
    '#spell.Quake' : 1,
    '#spell.Sleep' : 1,
    '#spell.Stone' : 1,
    '#spell.Fatal' : 1,
    '#spell.Stop'  : 1,
    '#spell.Drain' : 1,
    '#spell.Psych' : 1,
    '#spell.Meteo' : 1,
    '#spell.Nuke'  : 1,

    '#spell.Imp'   : 2,
    '#spell.Bomb'  : 2,
    '#spell.Cocka' : 2,
    '#spell.Mage'  : 2,
    '#spell.Chocb' : 2,
    '#spell.Shiva' : 2,
    '#spell.Indra' : 2,
    '#spell.Jinn'  : 2,
    '#spell.Titan' : 2,
    '#spell.Mist'  : 2,
    '#spell.Sylph' : 2,
    '#spell.Odin'  : 2,
    '#spell.Levia' : 2,
    '#spell.Asura' : 2,
    '#spell.Baham' : 2,
    '#spell.Comet' : 2,
    '#spell.Flare' : 2,
    '#spell.Flame' : 2,
    '#spell.Flood' : 2,
    '#spell.Blitz' : 2,
    '#spell.Smoke' : 2,
    '#spell.Pin'   : 2,
    '#spell.Image' : 2,
    }

SPELL_TIERS = { 
    'bad' : {
        1 : 50, 
        2 : 30, 
        3 : 15, 
        4 : 5, 
        5 : 0, 
        6 : 0, 
        7 : 0, 
        8 : 0
        }, 
    'okay' : {
        1 : 0, 
        2 : 15, 
        3 : 35, 
        4 : 35, 
        5 : 15, 
        6 : 0, 
        7 : 0, 
        8 : 0 
        }, 
    'good' : {
        1 : 0, 
        2 : 0, 
        3 : 0, 
        4 : 10, 
        5 : 10, 
        6 : 20, 
        7 : 30, 
        8 : 30 
        }, 
    'great' : {
        1 : 0, 
        2 : 0, 
        3 : 0, 
        4 : 0, 
        5 : 0, 
        6 : 30, 
        7 : 30, 
        8 : 40 
        }
    }

LOCATION_SLOTS = {   # dict of location slots, which are the boss slots plus two starting slots, with their tier as values
    'starting1_slot'        : 1,
    'starting2_slot'        : 1,
    'dmist_slot'            : 2,
    'officer_slot'          : 5,  # gated/uncommon checks, tier higher to incentivize
    'octomamm_slot'         : 5,  # gated/uncommon checks, tier higher to incentivize
    'antlion_slot'          : 2,
    'mombomb_slot'          : 2,
    'fabulgauntlet_slot'    : 3,
    'milon_slot'            : 3,
    'milonz_slot'           : 3,
    'mirrorcecil_slot'      : 3,
    'karate_slot'           : 3,
    'guard_slot'            : 3,
    'baigan_slot'           : 4,
    'kainazzo_slot'         : 4,
    'darkelf_slot'          : 4,
    'magus_slot'            : 4,
    'valvalis_slot'         : 4,
    'calbrena_slot'         : 5,
    'golbez_slot'           : 5,
    'lugae_slot'            : 5,
    'darkimp_slot'          : 5,
    'kingqueen_slot'        : 6,
    'rubicant_slot'         : 6,
    'evilwall_slot'         : 6,
    'asura_slot'            : 7,
    'leviatan_slot'         : 7,
    'odin_slot'             : 7,
    'bahamut_slot'          : 7,
    'elements_slot'         : 6,
    'cpu_slot'              : 6,
    'paledim_slot'          : 8,
    'wyvern_slot'           : 8,
    'plague_slot'           : 8,
    'dlunar_slot'           : 8,
    'ogopogo_slot'          : 8, 
    }

ALL_SPELLS_BY_LOCATION_TIERING = { # tiering info for all spells; 18 'bad', 16 'okay', 12 'good', 2 'great'
    '#spell.Sight' : 'bad',
    '#spell.Peep'  : 'bad',
    '#spell.Cure1' : 'bad',
    '#spell.Venom' : 'bad',
    '#spell.Toad'  : 'bad',
    '#spell.Piggy' : 'bad',
    '#spell.Ice1'  : 'bad',
    '#spell.Lit1'  : 'bad',
    '#spell.Fire1' : 'bad',
    '#spell.Sleep' : 'bad',
    '#spell.Charm' : 'bad',
    '#spell.Drain' : 'bad',
    '#spell.Shell' : 'bad',
    '#spell.Psych' : 'bad',
    '#spell.Hold'  : 'bad',
    '#spell.Size'  : 'bad',
    '#spell.Armor' : 'bad',
    '#spell.Dspel' : 'bad',
    '#spell.Imp'   : 'bad',
    '#spell.Bomb'  : 'bad',
    '#spell.Mage'  : 'bad',
    '#spell.Chocb' : 'bad',
    '#spell.Smoke' : 'bad',
    '#spell.Pin'   : 'bad',

    '#spell.Slow'  : 'okay',
    '#spell.Cure2' : 'okay',
    '#spell.Float' : 'okay',
    '#spell.Mute'  : 'okay',
    '#spell.Blink' : 'okay',
    '#spell.Ice2'  : 'okay',
    '#spell.Life1' : 'okay',
    '#spell.Fire2' : 'okay',
    '#spell.Lit2'  : 'okay',
    '#spell.Stop'  : 'okay',
    '#spell.Exit'  : 'okay',
    '#spell.Heal'  : 'okay',
    '#spell.Warp'  : 'okay',
    '#spell.Cure3' : 'okay',
    '#spell.Stone' : 'okay',
    '#spell.Fast'  : 'okay',
    '#spell.Cocka' : 'okay',
    '#spell.Shiva' : 'okay',
    '#spell.Indra' : 'okay',
    '#spell.Jinn'  : 'okay',
    '#spell.Titan' : 'okay',
    '#spell.Mist'  : 'okay',
    '#spell.Sylph' : 'okay',
    '#spell.Odin'  : 'okay',
    '#spell.Comet' : 'okay',
    '#spell.Flare' : 'okay',
    '#spell.Flame' : 'okay',
    '#spell.Flood' : 'okay',
    '#spell.Image' : 'okay',
    
    '#spell.Wall'  : 'good',
    '#spell.Virus' : 'good',
    '#spell.Fire3' : 'good',
    '#spell.Ice3'  : 'good',
    '#spell.Lit3'  : 'good',
    '#spell.Quake' : 'good',
    '#spell.Bersk' : 'good',
    '#spell.Cure4' : 'good',
    '#spell.Life2' : 'good',
    '#spell.Fatal' : 'good',
    '#spell.Weak'  : 'good',
    '#spell.Meteo' : 'good',
    '#spell.Levia' : 'good',
    '#spell.Asura' : 'good',
    '#spell.Blitz' : 'good',

    '#spell.White' : 'great',
    '#spell.Baham' : 'great',
    '#spell.Nuke'  : 'great',
}

MOD_BOSS_SLOT_SPOILER_NAMES = { f"{b}_slot": BOSS_SPOILER_NAMES[b] + " position" for b in BOSS_SPOILER_NAMES if b != 'waterhag'}

MAYBE_THRESHOLD = 0.15

def remove_spells_by_list(p_dict,sp_list):
    # removes specific spells from a given dictionary, without worrying if the spells are even there
    spells_to_remove = set(sp_list)
    for spell in spells_to_remove:
        p_dict.pop(spell, None)    

def get_random_hp_gains(env, max_credits, credits_to_distribute, required_zeros=0, max_gain=1):
    # the condition parameter is a non-increasing and non-negative quantity; all valid choices leave those two
    # properties invariant. since max_credits strictly decreases, the recursion has at most the initial max_credits
    # plus 1 steps. the last step is guaranteed to hit the condition parameter == 0 case because when max_credits is 1, 
    # required_zeros is either 1 or 0; if it's 1, then credits_to_distribute is already 0, so we choose 0 and in the 
    # next step the condition parameter is 0. if it's 0, then the only valid option is to choose the value of 
    # credits_to_distribute, meaning in the next step the condition parameter is exactly 0. 
    condition_parameter = max_gain * (max_credits - required_zeros) - credits_to_distribute

    if condition_parameter < 0:
        raise Exception('Invalid parameter combination; please ensure the condition parameter is initially non-negative')
    # the base case is that there's only one choice for the last few entries, up to permutation    
    elif condition_parameter == 0:
        equality_case_list = [max_gain] * (max_credits - required_zeros) + [0] * required_zeros
        env.rnd.shuffle(equality_case_list)
        return equality_case_list
    # when there is flexibility, randomly choose a valid option 
    # (possible options are bounded above by the max gain or the credits left, and bounded below by the non-negativity restriction)
    # note that if required_zeros is not as big as possible, the distribution will be somewhat front-loaded because
    # zeros will be more frequent near the beginning of the list
    else:
        possible_options = list(range(max(max_gain - condition_parameter, 0), min(credits_to_distribute,max_gain)+1))
        # can change the weights to influence the distribution of outcomes; exponential is pretty good here
        # option_weights = [2 ** ((2 * i) // max_gain) for i in range(len(possible_options))]
        # option_weights = list(range(len(possible_options)+1))
        option_weights = [2 ** i for i in range(len(possible_options))]
        option_weights.reverse()
        gain_choice = env.rnd.choices(possible_options,weights=option_weights,k=1)
        return gain_choice + get_random_hp_gains(env, max_credits-1, credits_to_distribute-gain_choice[0], max(required_zeros-(1 if gain_choice[0] == 0 else 0),0), max_gain)

def apply(env):

    maybe_spells = False
    if env.options.flags.has('maybe_fusoya'):
        maybe_spells = True

    excluded_spells = []
    
    j_spells = False
    if env.options.flags.has('japanese_spells'):
        j_spells = True
    else:
        excluded_spells.extend(JAPANESE_EXCLUSIVE_SPELLS + OMNI_J_SPELLS)

    all_spells = False
    if env.options.flags.has('add_spells_fusoya'):
        all_spells = True
        env.add_file('scripts/fusoya_omnimage.f4c')
    else:
        excluded_spells.extend(OMNI_SPELLS + OMNI_J_SPELLS)

    no_lance = True
    if env.options.flags.has('kainmagic'):
        no_lance = False
        excluded_spells.extend(['#spell.Sight'])

    if env.options.flags.has('antidale_spells_progression') and not env.options.flags.has('unlearn_fusoya'):
        # Funlearn overrides Cspells:anti re: Weak.
        excluded_spells.extend(['#spell.Weak'])
        if not env.options.flags.has('fusoya_nerfed'):
            env.add_scripts(
            'spellset(#FusoyaBlack) {{ learned {{ 53  #spell.Weak }} }}'
            )

    max_credits = 14
    if env.options.flags.has('uncapped_fusoya'):
        # determine how many credits based on how many boss spots there are available
        max_credits = 34
        if env.options.flags.has('no_officer_slot'):
            max_credits -= 1
        if env.options.flags.has('no_kingqueen_slot'):
            max_credits -= 1
    elif all_spells and not env.options.flags.has('location_fusoya'):
        max_credits = (27 if env.options.flags.has('slowstart_fusoya') else 22)
        if not j_spells:
            max_credits -= 1
    elif env.options.flags.has('slowstart_fusoya'):
        # note that this flag is incompatible with uncapped_fusoya;
        # exclusion will occur in flagsetcore
        max_credits = 19
    elif env.options.flags.has('nerfed_fusoya'):
        max_credits = 6

    # create the max credits substitution
    env.add_substitution('fusoya credits', f'${max_credits:02X}')

    if env.options.flags.has_any('slowstart_fusoya','randomhp_fusoya'):
        env.add_toggle('modified_hp_gains')

    # Now, handle the actual spells
    if env.options.flags.has('vanilla_fusoya'):
        env.add_substitution('fusoya initial hp', '#$01f4') # unimportant, but need to provide a default inline substitution value
        if max_credits > 14:
            max_hp = 500 + max_credits * 100
            if all_spells:
                max_hp -= 400
            env.add_scripts(f'patch($0faa87 bus) {{ {max_hp % 0x100:02X} {max_hp // 0x100:02X} {max_hp % 0x100:02X} {max_hp // 0x100:02X} }}')

        potential_spells = INTERNAL_SPELL_ORDER.copy()
        remove_spells_by_list(potential_spells,excluded_spells)

        if maybe_spells:
            missing_spells = []
            for spell in potential_spells:                    
                if env.rnd.random() < MAYBE_THRESHOLD:
                    missing_spells.append(spell)
            for spell in missing_spells:
                potential_spells.pop(spell)                

        white = [s for s in potential_spells if INTERNAL_SPELL_ORDER[s] == 0]
        black = [s for s in potential_spells if INTERNAL_SPELL_ORDER[s] == 1]
        omni = [s for s in potential_spells if INTERNAL_SPELL_ORDER[s] == 2]
                
        env.add_substitution('fusoya initial spells', '')
        env.add_scripts(
        'spellset(#FusoyaWhite) {{ initial {{ {} }} }}'.format(' '.join(white)),
        'spellset(#FusoyaBlack) {{ initial {{ {} }} }}'.format(' '.join(black)),
        )
        if all_spells:
            env.add_script('spellset(#FusoyaOmni) {{ initial {{ {} }} }}'.format(' '.join(omni)))

        if maybe_spells:
            spoilers = [ ("Missing spells", ', '.join([databases.get_spell_spoiler_name(s) for s in missing_spells])) ]
            env.spoilers.add_table("FUSOYA SPELLS", spoilers, public=env.options.flags.has_any('-spoil:all', '-spoil:misc'), ditto_depth=1)            
            
    elif env.options.flags.has('nerfed_fusoya'):
        env.add_substitution('fusoya initial hp', '#$01f4')

        white = STARTING_WHITE.copy()
        if j_spells:
            white.extend(STARTING_WHITE_JAPANESE)
        if not no_lance:
            white.remove('#spell.Sight')
        black = STARTING_BLACK.copy()
        omni = STARTING_CALL.copy()
        
        if maybe_spells:
            for spell in STARTING_WHITE + (STARTING_WHITE_JAPANESE if j_spells else []):
                if env.rnd.random() < MAYBE_THRESHOLD:
                    white.remove(spell)
            for spell in STARTING_BLACK:
                if env.rnd.random() < MAYBE_THRESHOLD:
                    black.remove(spell)
            for spell in STARTING_CALL:
                if env.rnd.random() < MAYBE_THRESHOLD:
                    omni.remove(spell)

        if env.options.flags.has('randomhp_fusoya'):
            # in this case, either the HP max is 3900 or it's 1100, no slowstart option
            hp_gains = get_random_hp_gains(env, max_credits, max_credits, 0, (5 if max_credits > 14 else 2))
            env.add_substitution('fusoya challenge hp gains', ' '.join([f'{gain:02X}' for gain in hp_gains]))
    
        env.add_substitution('fusoya initial spells', '')
        env.add_scripts(
            'spellset(#FusoyaWhite) {{ initial {{ {} }} }}'.format(' '.join(white)),
            'spellset(#FusoyaBlack) {{ initial {{ {} }} }}'.format(' '.join(black))
            )
        spoilers = []
        spoilers.append( ("Initial white magic", ', '.join([databases.get_spell_spoiler_name(s) for s in white])) )
        spoilers.append( ("Initial black magic", ', '.join([databases.get_spell_spoiler_name(s) for s in black])) )
        if all_spells:
            env.add_script('spellset(#FusoyaOmni) {{ initial {{ {} }} }}'.format(' '.join(omni)))
            spoilers.append( ("Initial other magic", ', '.join([databases.get_spell_spoiler_name(s) for s in omni])) )
        if env.options.flags.has('harmspell'):
            spoilers = [(p, s.replace('Sight', 'Harm')) for p,s in spoilers]
        env.spoilers.add_table("FUSOYA SPELLS", spoilers, public=env.options.flags.has_any('-spoil:all', '-spoil:misc'), ditto_depth=1)

    elif env.options.flags.has('location_fusoya'):
        env.add_substitution('fusoya initial hp', '#$01f4')

        # shuffle locations in each tier so that location slots are filled up in a random order
        location_tiers = {} 
        if env.options.flags.has('no_officer_slot'):
            LOCATION_SLOTS.pop('officer_slot')
            MOD_BOSS_SLOT_SPOILER_NAMES.pop('officer_slot')
        if env.options.flags.has('no_kingqueen_slot'):
            LOCATION_SLOTS.pop('kingqueen_slot')
            MOD_BOSS_SLOT_SPOILER_NAMES.pop('kingqueen_slot')
        
        for i in LOCATION_SLOTS.values():
            slot_order = [slot for slot in LOCATION_SLOTS if LOCATION_SLOTS[slot] == i]
            env.rnd.shuffle(slot_order)
            location_tiers[i] = slot_order 

        spell_slots = { location : [] for location in LOCATION_SLOTS }
            
        available_tiers = SPELL_TIERS.copy()        
        available_spells = ALL_SPELLS_BY_LOCATION_TIERING.copy()
        # build a dict of Distributions (see util.py)
        available_distributions = { tier : Distribution(SPELL_TIERS[tier]) for tier in SPELL_TIERS }
        
        remove_spells_by_list(available_spells,excluded_spells)
        
        shuffled_spells = [spell for spell in available_spells]
        env.rnd.shuffle(shuffled_spells)

        if env.options.flags.has('unlearn_fusoya'):
            full_spell_list = shuffled_spells.copy()
            
        # every spell can be placed at least once, due to combinatorics
        # probably true when a couple slots are removed, but not going to worry about it
            
        while location_tiers:   # going to remove slots when they're full, stop when all slots full/list is empty
            for spell in shuffled_spells: 
                if max(available_tiers[available_spells[spell]].values()) == 0:
                    available_spells.pop(spell)   # remove spells that can't select an available tier anymore
                    continue
                tier = available_distributions[available_spells[spell]].choose(env.rnd)   # choose a tier for the spell based on the spell's weight data
                location_slot = location_tiers[tier][0]   # we're guaranteed that this tier has a location_slot in it; pick the first element of that list
                if spell in spell_slots[location_slot]:
                    continue
                elif location_slot in ['starting1_slot', 'starting2_slot']:
                    if spell in spell_slots[('starting1_slot' if location_slot == 'starting2_slot' else 'starting2_slot')]:
                        continue
                spell_slots[location_slot].append(spell)   # add that spell to the slots for that location if it isn't already there
            
                # if a location has all its spells, remove that slot, and then check if that's the last slot from a tier; if so, remove weights
                if len(spell_slots[location_slot]) == 3:
                    location_tiers[tier].remove(location_slot)
                    if not location_tiers[tier]:
                        location_tiers.pop(tier)
                        for quality in SPELL_TIERS:
                            available_tiers[quality].pop(tier)
                        # rebuild the available_distributions dict so that weights are removed
                        available_distributions = { tier : Distribution(available_tiers[tier]) for tier in available_tiers } 

                # after the last slot is filled, need to break out before max() checks an empty list
                if not location_tiers:
                    break
                
            shuffled_spells = [spell for spell in available_spells] # update the spells to be placed
            env.rnd.shuffle(shuffled_spells)

        if env.options.flags.has('unlearn_fusoya'):
            white = [s for s in full_spell_list if ALL_SPELLS_BY_GOODNESS[s] == 0]
            black = [s for s in full_spell_list if ALL_SPELLS_BY_GOODNESS[s] == 1]
            omni = [s for s in full_spell_list if ALL_SPELLS_BY_GOODNESS[s] == 2]
        else:         
            initial_spells = spell_slots['starting1_slot']
            initial_spells.extend(spell_slots['starting2_slot'])
            white = [s for s in initial_spells if ALL_SPELLS_BY_GOODNESS[s] == 0]
            black = [s for s in initial_spells if ALL_SPELLS_BY_GOODNESS[s] == 1]
            omni = [s for s in initial_spells if ALL_SPELLS_BY_GOODNESS[s] == 2]
        
        env.add_substitution('fusoya initial spells', '')
        env.add_scripts(
            'spellset(#FusoyaWhite) {{ initial {{ {} }} }}'.format(' '.join(white)),
            'spellset(#FusoyaBlack) {{ initial {{ {} }} }}'.format(' '.join(black))
                )
        if all_spells:
            env.add_script('spellset(#FusoyaOmni) {{ initial {{ {} }} }}'.format(' '.join(omni)))
            
        learned_spells = []
        spell_slots.pop('starting1_slot')
        spell_slots.pop('starting2_slot')
        for location_slot in spell_slots:
            learned_spells.extend(spell_slots[location_slot])
        if env.options.flags.has('no_officer_slot'):
            learned_spells.insert(3, 'FF') # Officer is the second slot, so its spells would normally start at index 3
            learned_spells.insert(4, 'FF')
            learned_spells.insert(5, 'FF') 
        if env.options.flags.has('no_kingqueen_slot'):
            learned_spells.insert(60, 'FF') # King/Queen Eblan is the twenty-first slot, so its spells would normally start at index 60
            learned_spells.insert(61, 'FF')
            learned_spells.insert(62, 'FF') 
        env.add_substitution('fusoya challenge spells', '\n'.join(learned_spells))

        if env.options.flags.has('randomhp_fusoya'):
            hp_gains = get_random_hp_gains(env, max_credits, max_credits, 0, (5 if max_credits > 14 else 3))
            env.add_substitution('fusoya challenge hp gains', ' '.join([f'{gain:02X}' for gain in hp_gains]))

        spoilers = []
        if not env.options.flags.has('unlearn_fusoya'):
            spoilers.append( ("Initial spells", ', '.join([databases.get_spell_spoiler_name(s) for s in initial_spells])) )
        for position in MOD_BOSS_SLOT_SPOILER_NAMES: 
            spoilers.append( (MOD_BOSS_SLOT_SPOILER_NAMES[position], ', '.join([databases.get_spell_spoiler_name(s) for s in spell_slots[position]]) ) )
        if env.options.flags.has('harmspell'):
            spoilers = [(p, s.replace('Sight', 'Harm')) for p,s in spoilers]
        env.spoilers.add_table("FUSOYA SPELLS", spoilers, public=env.options.flags.has_any('-spoil:all', '-spoil:misc'), ditto_depth=1)
        
    else:
        starting_max_hp = (100 if all_spells else 500)
        env.add_substitution('fusoya initial hp', f'#${starting_max_hp:04X}')

        ranked_spells = []
        if env.options.flags.has('sequential_p_fusoya'):
            level_p_spells = ALL_SPELLS_BY_LEVEL_P.copy()
            remove_spells_by_list(level_p_spells,excluded_spells)
            for position,spell in enumerate(level_p_spells):
                ranked_spells.append( (position, spell) )
        elif env.options.flags.has('sequential_r_fusoya'):
            if j_spells:
                level_rj_spells = ALL_SPELLS_BY_LEVEL_R_J.copy()
                remove_spells_by_list(level_rj_spells,excluded_spells)
                for position,spell in enumerate(level_rj_spells):
                    ranked_spells.append( (position, spell) )
            else:
                level_r_spells = ALL_SPELLS_BY_LEVEL_R.copy()
                remove_spells_by_list(level_r_spells,excluded_spells)
                for position,spell in enumerate(level_r_spells):
                    ranked_spells.append( (position, spell) )
        else:
            goodness_spells = ALL_SPELLS_BY_GOODNESS.copy()
            remove_spells_by_list(goodness_spells,excluded_spells)
            for i,spell in enumerate(goodness_spells):
                position = float(i) / len(goodness_spells)
                #position += (env.rnd.random() - 0.5) * 0.5
                position += (env.rnd.random() - 0.5)
                #position = max(0.0, min(1.0, position))
                ranked_spells.append( (position, spell) )           

        if maybe_spells:
            missing_spells = []
            for position, spell in ranked_spells:
                if env.rnd.random() < MAYBE_THRESHOLD:
                    missing_spells.append( (position, spell) )
            for position, spell in missing_spells:
                ranked_spells.remove( (position, spell) )

        ranked_spells.sort()
        initial_spells = [p[1] for p in ranked_spells[:6]]
        learned_spells = [p[1] for p in ranked_spells[6:]]

        if env.options.flags.has('randomhp_fusoya'):
            if env.options.flags.has('slowstart_fusoya'):
                hp_gains = get_random_hp_gains(env, 6, 3, 3, 1) + get_random_hp_gains(env, 6, 4, 2, 1)
                hp_gains += get_random_hp_gains(env, max_credits-12, max_credits-7, 0, 3)
            else:
                hp_gains = get_random_hp_gains(env, max_credits, max_credits, 0, (5 if max_credits > 14 else 3))
            env.add_substitution('fusoya challenge hp gains', ' '.join([f'{gain:02X}' for gain in hp_gains]))
        elif env.options.flags.has('slowstart_fusoya'):
            hp_gains = get_random_hp_gains(env, 6, 3, 3, 1) + get_random_hp_gains(env, 6, 4, 2, 1) + [1] * (max_credits - 12)
            env.add_substitution('fusoya challenge hp gains', ' '.join([f'{gain:02X}' for gain in hp_gains]))

        # for slowstart, add in 5 sets of FF FF FF into learned_spells, to simulate not learning spells there.
        # since it is three FFs and not just two/one, the textbox won't pop up, as desired.
        # then also deal with the spoiler log
        if env.options.flags.has('slowstart_fusoya'):
            for idx in range(12):
                if not hp_gains[idx]:
                    learned_spells.insert(3*idx,'FF')
                    learned_spells.insert(3*idx + 1,'FF')
                    learned_spells.insert(3*idx + 2,'FF')

        if env.options.flags.has('unlearn_fusoya'):
            env.rnd.shuffle(ranked_spells)
            white = [s[1] for s in ranked_spells if ALL_SPELLS_BY_GOODNESS[s[1]] == 0]
            black = [s[1] for s in ranked_spells if ALL_SPELLS_BY_GOODNESS[s[1]] == 1]
            omni = [s[1] for s in ranked_spells if ALL_SPELLS_BY_GOODNESS[s[1]] == 2]
            learned_spells.reverse()
        else:
            white = [s for s in initial_spells if ALL_SPELLS_BY_GOODNESS[s] == 0]
            black = [s for s in initial_spells if ALL_SPELLS_BY_GOODNESS[s] == 1]
            omni = [s for s in initial_spells if ALL_SPELLS_BY_GOODNESS[s] == 2]

        env.add_substitution('fusoya initial spells', '') # under vanilla Fu, the j-spells f4c adds spells here, so blank that out
        env.add_substitution('fusoya challenge spells', '\n'.join(learned_spells))

        env.add_scripts(
            'spellset(#FusoyaWhite) {{ initial {{ {} }} }}'.format(' '.join(white)),
            'spellset(#FusoyaBlack) {{ initial {{ {} }} }}'.format(' '.join(black))
            )
        if all_spells:
            env.add_script('spellset(#FusoyaOmni) {{ initial {{ {} }} }}'.format(' '.join(omni)))

        spoilers = []
        if not env.options.flags.has('unlearn_fusoya'):
            spoilers.append( ("Initial spells", ', '.join([databases.get_spell_spoiler_name(s) for s in initial_spells])) )
        for i in range(0, len(learned_spells), 3):
            boss_number = (i // 3) + 1
            level_spells = learned_spells[i:i+3] # syntax handles fewer than three spells for free
            if level_spells[0] == 'FF': # happens only under slowstart_fusoya
                spoilers.append( (f"Boss {boss_number}", 'No spells learned') )
            else:
                spoilers.append( (f"Boss {boss_number}", ', '.join([databases.get_spell_spoiler_name(s) for s in level_spells])) )
        if env.options.flags.has('unlearn_fusoya'):
             spoilers.append( ("Permanent spells", ', '.join([databases.get_spell_spoiler_name(s) for s in initial_spells])) )
        if env.options.flags.has('harmspell'):
            spoilers = [(p, s.replace('Sight', 'Harm')) for p,s in spoilers]
        env.spoilers.add_table("FUSOYA SPELLS", spoilers, public=env.options.flags.has_any('-spoil:all', '-spoil:misc'), ditto_depth=1)

if __name__ == '__main__':
    from .FreeEnt import FreeEntOptions
    import random
    import argparse

    parser = argparse.ArgumentParser();
    parser.add_argument('flags', nargs='?')
    args = parser.parse_args();

    options = FreeEntOptions()
    options.flags.load(args.flags if args.flags else 'F')

    rnd = random.Random()
    result = randomize(rnd, options, {})

    print('\n'.join(result['scripts']))
    print(result['substitutions']['fusoya challenge spells'])
