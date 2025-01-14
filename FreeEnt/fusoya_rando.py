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

JAPANESE_EXCLUSIVE_SPELLS = [
    '#spell.Armor', '#spell.Shell', '#spell.Dspel'
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
    '#spell.Piggy' : 1, # 12
    '#spell.Armor' : 0, # 12
    '#spell.Fire2' : 1, # 12
    '#spell.Cure2' : 0, # 12
    '#spell.Lit2'  : 1, # 13
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
    '#spell.Drain' : 1, # 26
    '#spell.Shell' : 0, # 29
    '#spell.Warp'  : 1, # 29
    '#spell.Dspel' : 0, # 31
    '#spell.Size'  : 0, # 31
    '#spell.Ice3'  : 1, # 32
    '#spell.Cure3' : 0, # 33
    '#spell.Fire3' : 1, # 33
    '#spell.Lit3'  : 1, # 34
    '#spell.Stone' : 1, # 36
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
    '#spell.Virus' : 1, # 26    
    '#spell.Cure3' : 0, # 28 (here's where Rosa's j-spells diverge)
    '#spell.Size'  : 0, # 29
    '#spell.Fast'  : 0, # 30
    '#spell.Psych' : 1, # 31 (here's where Rydia's j-spells diverge)
    '#spell.Float' : 0, # 32
    '#spell.Wall'  : 0, # 34
    '#spell.Drain' : 1, # 35    
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
    '#spell.Virus' : 1, # 26    
    '#spell.Cure3' : 0, # 28 (here's where Rosa's j-spells diverge)
    '#spell.Shell' : 0, # 29
    '#spell.Size'  : 0, # 30
    '#spell.Dspel' : 0, # 31
    '#spell.Psych' : 1, # 32 (here's where Rydia's j-spells diverge)
    '#spell.Fast'  : 0, # 33
    '#spell.Float' : 0, # 35
    '#spell.Wall'  : 0, # 36
    '#spell.Drain' : 1, # 36    
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
    '#spell.Venom' : 1,
    '#spell.Toad'  : 1,
    '#spell.Piggy' : 1,
    '#spell.Ice1'  : 1,
    '#spell.Lit1'  : 1,
    '#spell.Fire1' : 1,
    '#spell.Sleep' : 1,
    '#spell.Charm' : 0,
    '#spell.Drain' : 1,
    '#spell.Shell' : 0,
    '#spell.Psych' : 1,
    '#spell.Mute'  : 0,
    '#spell.Size'  : 0,
    '#spell.Armor' : 0,
    '#spell.Dspel' : 0,

    '#spell.Slow'  : 0,
    '#spell.Cure2' : 0,
    '#spell.Float' : 0,
    '#spell.Hold'  : 0,
    '#spell.Blink' : 0,
    '#spell.Ice2'  : 1,
    '#spell.Life1' : 0,
    '#spell.Fire2' : 1,
    '#spell.Lit2'  : 1,
    '#spell.Stop'  : 1,
    '#spell.Exit'  : 0,
    '#spell.Heal'  : 0,
    '#spell.Warp'  : 1,
    '#spell.Cure3' : 0,
    '#spell.Stone' : 1,
    '#spell.Fast'  : 0,
    '#spell.Wall'  : 0,

    '#spell.Virus' : 1,
    '#spell.Fire3' : 1,
    '#spell.Ice3'  : 1,
    '#spell.Lit3'  : 1,
    '#spell.Quake' : 1,
    '#spell.Bersk' : 0,
    '#spell.Cure4' : 0,
    '#spell.Life2' : 0,
    '#spell.Fatal' : 1,
    '#spell.Weak'  : 1,
    '#spell.Meteo' : 1,
    '#spell.White' : 0,
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

    '#spell.White' : 'great',
    '#spell.Nuke'  : 'great',
}

MOD_BOSS_SLOT_SPOILER_NAMES = { f"{b}_slot": BOSS_SPOILER_NAMES[b] + " position" for b in BOSS_SPOILER_NAMES if b != 'waterhag'}

MAYBE_THRESHOLD = 0.15

def apply(env):

    maybe_spells = False
    if env.options.flags.has('maybe_fusoya'):
        maybe_spells = True
    
    j_spells = False
    if env.options.flags.has('japanese_spells'):
        j_spells = True

    if env.options.flags.has('vanilla_fusoya'):
        if maybe_spells:
            potential_spells = INTERNAL_SPELL_ORDER.copy()
            if not j_spells:
                for spell in JAPANESE_EXCLUSIVE_SPELLS:
                    potential_spells.pop(spell)
               
            missing_spells = []
            for spell in potential_spells:                    
                if env.rnd.random() < MAYBE_THRESHOLD:
                    missing_spells.append(spell)
            for spell in missing_spells:
                potential_spells.pop(spell)
            
            white = [s for s in potential_spells if INTERNAL_SPELL_ORDER[s] == 0]
            black = [s for s in potential_spells if INTERNAL_SPELL_ORDER[s] == 1]
                    
            env.add_substitution('fusoya initial spells', '')
            env.add_scripts(
	        'spellset(#FusoyaWhite) {{ initial {{ {} }} }}'.format(' '.join(white)),
	        'spellset(#FusoyaBlack) {{ initial {{ {} }} }}'.format(' '.join(black))
            )
            spoilers = [ ("Missing spells", ', '.join([databases.get_spell_spoiler_name(s) for s in missing_spells])) ]
            if env.options.flags.has('kainmagic'):
                spoilers = [(p, s.replace('Sight', 'Lance')) for p,s in spoilers]
            env.spoilers.add_table("FUSOYA SPELLS", spoilers, public=env.options.flags.has_any('-spoil:all', '-spoil:misc'), ditto_depth=1)
            
    elif env.options.flags.has('nerfed_fusoya'):
        white = STARTING_WHITE.copy()
        if j_spells:
            white.extend(STARTING_WHITE_JAPANESE)
        black = STARTING_BLACK.copy()
        
        if maybe_spells:
            for spell in STARTING_WHITE:
                if env.rnd.random() < MAYBE_THRESHOLD:
                    white.remove(spell)
            if j_spells:
                for spell in STARTING_WHITE_JAPANESE:
                    if env.rnd.random() < MAYBE_THRESHOLD:
                        white.remove(spell)
            for spell in black:
                if env.rnd.random() < MAYBE_THRESHOLD:
                    black.remove(spell)
    
        env.add_substitution('fusoya initial spells', '')
        env.add_scripts(
            'spellset(#FusoyaWhite) {{ initial {{ {} }} }}'.format(' '.join(white)),
            'spellset(#FusoyaBlack) {{ initial {{ {} }} }}'.format(' '.join(black))
            )
        spoilers = []
        spoilers.append( ("Initial white magic", ', '.join([databases.get_spell_spoiler_name(s) for s in white])) )
        spoilers.append( ("Initial black magic", ', '.join([databases.get_spell_spoiler_name(s) for s in black])) )
        if env.options.flags.has('kainmagic'):
            spoilers = [(p, s.replace('Sight', 'Lance')) for p,s in spoilers]
        env.spoilers.add_table("FUSOYA SPELLS", spoilers, public=env.options.flags.has_any('-spoil:all', '-spoil:misc'), ditto_depth=1)

    elif env.options.flags.has('location_fusoya'):
        # shuffle locations in each tier so that location slots are filled up in a random order
        location_tiers = {} 
        if env.options.flags.has('no_officer_slot'):
            LOCATION_SLOTS.pop('officer_slot')
            MOD_BOSS_SLOT_SPOILER_NAMES.pop('officer_slot')
        if env.options.flags.has('no_kq_eblan_slot'):
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
            
        if not j_spells:
             for spell in JAPANESE_EXCLUSIVE_SPELLS:
                available_spells.pop(spell)
        
        if maybe_spells:
            for spell in ALL_SPELLS_BY_LOCATION_TIERING:
                if env.rnd.random() < MAYBE_THRESHOLD:
                    available_spells.pop(spell)
        
        shuffled_spells = [spell for spell in available_spells]
        env.rnd.shuffle(shuffled_spells)
            
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
            
        initial_spells = spell_slots['starting1_slot']
        initial_spells.extend(spell_slots['starting2_slot'])
        white = [s for s in initial_spells if ALL_SPELLS_BY_GOODNESS[s] == 0]
        black = [s for s in initial_spells if ALL_SPELLS_BY_GOODNESS[s] == 1]
        
        env.add_substitution('fusoya initial spells', '')
        env.add_scripts(
            'spellset(#FusoyaWhite) {{ initial {{ {} }} }}'.format(' '.join(white)),
            'spellset(#FusoyaBlack) {{ initial {{ {} }} }}'.format(' '.join(black))
                )
            
        learned_spells = []
        spell_slots.pop('starting1_slot')
        spell_slots.pop('starting2_slot')
        for location_slot in spell_slots:
            learned_spells.extend(spell_slots[location_slot])
        if env.options.flags.has('no_officer_slot'):
            learned_spells.insert(3, '00') # Officer is the second slot, so its spells would normally start at index 3
            learned_spells.insert(4, '00')
            learned_spells.insert(5, '00') 
        if env.options.flags.has('no_kq_eblan_slot'):
            learned_spells.insert(60, '00') # King/Queen Eblan is the twenty-first slot, so its spells would normally start at index 60
            learned_spells.insert(61, '00')
            learned_spells.insert(62, '00') 
        env.add_substitution('fusoya challenge spells', '\n'.join(learned_spells))
            
        spoilers = []
        spoilers.append( ("Initial spells", ', '.join([databases.get_spell_spoiler_name(s) for s in initial_spells])) )
        for position in MOD_BOSS_SLOT_SPOILER_NAMES: 
            spoilers.append( (MOD_BOSS_SLOT_SPOILER_NAMES[position], ', '.join([databases.get_spell_spoiler_name(s) for s in spell_slots[position]]) ) )
        if env.options.flags.has('kainmagic'):
            spoilers = [(p, s.replace('Sight', 'Lance')) for p,s in spoilers]
        env.spoilers.add_table("FUSOYA SPELLS", spoilers, public=env.options.flags.has_any('-spoil:all', '-spoil:misc'), ditto_depth=1)
        
    else:
        ranked_spells = []
        if env.options.flags.has('sequential_p_fusoya'):
            for position,spell in enumerate(ALL_SPELLS_BY_LEVEL_P):
                if spell in JAPANESE_EXCLUSIVE_SPELLS and not j_spells:
                    continue
                ranked_spells.append( (position, spell) )
        elif env.options.flags.has('sequential_r_fusoya'):
            if j_spells:
                for position,spell in enumerate(ALL_SPELLS_BY_LEVEL_R_J):
                    ranked_spells.append( (position, spell) )
            else:
                for position,spell in enumerate(ALL_SPELLS_BY_LEVEL_R):
                    ranked_spells.append( (position, spell) )
        else:
            for i,spell in enumerate(ALL_SPELLS_BY_GOODNESS):
                if spell in JAPANESE_EXCLUSIVE_SPELLS and not j_spells:
                    continue
                position = float(i) / len(ALL_SPELLS_BY_GOODNESS)
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

        white = [s for s in initial_spells if ALL_SPELLS_BY_GOODNESS[s] == 0]
        black = [s for s in initial_spells if ALL_SPELLS_BY_GOODNESS[s] == 1]

        env.add_substitution('fusoya initial spells', '') # this is residual from when Fu Challenge level 1 had you starting with spells
        env.add_substitution('fusoya challenge spells', '\n'.join(learned_spells))

        env.add_scripts(
            'spellset(#FusoyaWhite) {{ initial {{ {} }} }}'.format(' '.join(white)),
            'spellset(#FusoyaBlack) {{ initial {{ {} }} }}'.format(' '.join(black))
            )

        spoilers = []
        spoilers.append( ("Initial spells", ', '.join([databases.get_spell_spoiler_name(s) for s in initial_spells])) )
        for i in range(0, len(learned_spells), 3):
            boss_number = (i // 3) + 1
            level_spells = learned_spells[i:i+3] # syntax handles fewer than three spells for free
            spoilers.append( (f"Boss {boss_number}", ', '.join([databases.get_spell_spoiler_name(s) for s in level_spells])) )
        if env.options.flags.has('kainmagic'):
            spoilers = [(p, s.replace('Sight', 'Lance')) for p,s in spoilers]
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