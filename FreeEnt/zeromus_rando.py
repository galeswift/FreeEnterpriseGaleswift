from . import databases
from . import address

# values not used for whichbang; instead used for chaos
POSSIBLE_BIGBANG_COMMANDS = {
    '#spell.Quake' : (True, 'spell power', 32, 'all characters'),
    '#spell.Meteo' : (True, 'spell power', 32, 'all characters'), # needs spell power adjustment for no-nerfs
    '#spell.Enemy_Charm' : (False, 'spell power', 20, 'all characters'),
    '#spell.Enemy_Whisper' : (False, 'spell power', 20, 'all characters'),
    '#spell.Enemy_Storm' : (True, 'spell power', 20, 'all characters'),
    '#spell.Enemy_Blitz' : (True, 'spell power', 20, 'all characters'),
    '#spell.Enemy_Blizzard' : (True, 'spell power', 20, 'all characters'),
    '#spell.Enemy_Glare' : (True, 'spell power', 32, 'all characters'),
    '#spell.Enemy_Wave' : (True, 'spell power', 20, 'all characters'),
    '#spell.Enemy_Tornado' : (True, 'spell power', 20, 'all characters'),
    '#spell.Enemy_Laser' : (True, 'spell power', 20, 'all characters'),
    '#spell.Enemy_Odin' : (True, 'spell power', 20, 'all characters'),
    '#spell.Enemy_Globe199' : (True, 'spell power', 32, 'all characters'), # needs spell power adjustment for no-nerfs
    '#spell.Enemy_BigBang' : (True, 'spell power', 32, 'all characters'),
    '#spell.Enemy_MegaNuke' : (True, 'spell power', 32, 'all characters'),
}

BIGBANG_5_COMMANDS = {
    '#spell.Enemy_Count' : (False, 'spell power', 20, 'all characters'), # battle-cheesing but it's fine if it's only the very last BB
    '#spell.Enemy_Dancing' : (False, 'spell power', 20, 'all characters'), # script-breaking but it's fine if it's only the very last BB
}

# some scripts are just... unused. Should they be in here?
# omitting some scripts because they aren't threatening or are copies.
# **** for scripts that are questionable
POSSIBLE_SCRIPTS_DICT = {
    0x07 : 'Basilisk, Ice Liz',
    0x15 : 'Ghost',
    0x1D : 'SwordRat, Needler, StingRat',
    0x1E : 'TinyMage Charm script', # (Fatal)
    0x25 : 'Sandpede, Talantla', # (skip related 0x26)
    0x29 : 'SandWorm', # **** Tornado only
    0x2B : 'AquaWorm', # (and Calbrena Ice counter)
    0x2F : 'Gargoyle',
    0x30 : 'Hooligan magic counter',
    0x3D : 'VampGirl',
    0x3E : 'VampLady',
    0x40 : 'FlameDog (alone, not miab), D.Machin',
    0x42 : 'Yellow D counter', # (and Calbrena Lit counter)
    0x46 : 'Blademan counter',
    0x4A : 'Hydra, Python',
    0x55 : 'Unused (Fight -> Charm -> Fight)', # **** (by Dummy) 
    0x57 : 'Chimera, Mantcore',
    0x5A : 'IceBeast',
    0x6B : 'Unused (Fight -> Nuke)', # ****
    0x6C : 'Unused (Fire2 -> Psych -> Drain -> Fatal)', # ****
    0x6F : 'Raven, Roc, Aligator, Crocdile, charmed Green/Yellow Ds', # (chained Fight)
    0x70 : 'Green D',
    0x76 : 'Clapper',
    0x79 : 'Unused (Laser)', # ****
    0x7A : 'FlameDog (miab)',
    0xA0 : 'Baigan\'s left arm',
    0xA1 : 'Baigan\'s right arm',
    0xAB : 'Dark Elf ("YOU FOOLS!")',
    0xAC : 'Dark Elf',
    0xAE : 'Dark Dragon',
    0xB0 : 'Sandy (alone)',
    0xB5 : 'Valvalis (tornado)',
    0xCE : 'Dr. Lugae 2nd form post-Poison',
    0xD0 : 'EvilWall Crush phase',
    0xD5 : 'Leviatan', # **** sprite issues?
    0xD6 : 'Attacker',
    0xDA : 'unused (Jump)', # ****
    0xE2 : 'Golbez', # (with whichbez built-in when that gets merged)
    0xEB : 'Elements (Milon)', # ****
    0xED : 'Elements (Rubi)',
    0xF1 : 'Elements (Valvalis)', # (can't use Kainazzo)
    0xF4 : 'Calbrena',
    0xF8 : 'Mantcore',
    0x100 : 'Warlock',
    0x102 : 'Warlock (alone)',
    0x106 : 'RedGiant',
    0x10B : 'Ging-Ryu', # similar to Mantcore
    0x10E : 'Blue D',
    0x110 : 'Blue D Fire counter', # **** Blizzard only
    0x113 : 'FatalEye', # once your party is under Count
    0x114 : 'D.Fossil',
    0x116 : 'King-Ryu',
    0x119 : 'Red D',
    0x11B : 'Red D (alone)',
    0x11E : 'Behemoth Holy counter',
    0x122 : 'Tricker ("It\'s my turn now!")',
    0x127 : 'Wyvern Call counter', # weaker spell power
    0x128 : 'Ogopogo',
    0x12B : 'D.Lunars', # **** worth leaving in, for cheese potential?
    0x130 : 'Pale Dim', # (this is the "fight only" script we'll use)
    0x131 : 'Pale Dim Call counter',
    0x133 : 'Pale Dim Fire counter',
    0x138 : 'Mind',
    0x14C : 'Zeromus Virus phase',
    0x14D : 'Zeromus counter Nuke',
    0x150 : 'Pink Puff', # yes, music is broken
    0x151 : 'Bahamut', # sprite glitches briefly but is fine; skip the duplicate normal script $D8
    0x155 : 'Zeromus Nuke phase',
    0x157 : 'Zeromus Meteo phase',
    0x158 : 'Zeromus counter Virus',
    0x159 : 'Unused (Virus)', # ****
}

POSSIBLE_BNOFREE_SCRIPTS_DICT = {
    0x9E : 'D.Knight',
}

# keys are spells/attacks, values are 4-tuples where you note damaging/"will eventually cause game over, barring status protection", 
# set attack/spell power, set a value for it (depending on targeting!), then possibly set targeting in via string (that gets split into a list)
POSSIBLE_CHAOS_COMMANDS = {
    'fight' : (True, 'attack index', 0x5F, 'random character'),
    'pass' : (False, '', 0, 'self'),
    '#Jump' : (True, 'attack index', 0x5F, 'random character'),
    '#Kick' : (True, 'attack index', 0x5F, 'all characters'),
    '#Change' : (False, '', 0, 'all characters'),
    '#spell.Mute' : (False, 'spell power', [20], 'all characters'),
    '#spell.Blink' : (False, 'spell power', [20], 'self'),
    '#spell.Slow' : (False, 'spell power', [20], 'all characters'),
    '#spell.Fast' : (False, 'spell power', [20], 'self'),
    '#spell.Bersk' : (False, 'spell power', [20, 20], 'front row / back row'),
    '#spell.White' : (True, 'spell power', [16, 24], 'random character / all characters'),
    '#spell.Size' : (False, 'spell power', [20], 'all characters'),
    '#spell.Toad' : (False, 'spell power', [20], 'all characters'),
    '#spell.Piggy' : (False, 'spell power', [20], 'all characters'),
    '#spell.Venom' : (False, 'spell power', [20], 'all characters'),
    '#spell.Fire3' : (True, 'spell power', [20, 28], 'random character / all characters'),
    '#spell.Ice3' : (True, 'spell power', [20, 28], 'random character / all characters'),
    '#spell.Lit3' : (True, 'spell power', [20, 28], 'random character / all characters'),
    '#spell.Virus' : (True, 'spell power', [36, 48], 'random character / all characters'),
    '#spell.Weak' : (False, 'spell power', [20], 'all characters'),
    '#spell.Stone' : (False, 'spell power', [20], 'random character'),
    '#spell.Fatal' : (False, 'spell power', [20], 'random character'),
    '#spell.Stop' : (False, 'spell power', [20], 'random character'),
    '#spell.Drain' : (True, 'spell power', [128, 172], 'random character / all characters'),
    '#spell.Psych' : (True, 'spell power', [64, 96], 'random character / all characters'),
    '#spell.Nuke' : (True, 'spell power', [16], 'random character'),
    '#spell.Enemy_Slap' : (False, 'spell power', [20], 'all characters'),
    '#spell.Enemy_Powder' : (False, 'spell power', [20], 'all characters'),
    '#spell.Enemy_Glance' : (False, 'spell power', [20], 'random character'),
    '#spell.Enemy_Tongue' : (False, 'spell power', [20, 20], 'front row / back row'),
    '#spell.Enemy_Curse' : (False, 'spell power', [20], 'all characters'),
    '#spell.Enemy_Ray' : (True, 'spell power', [20], 'all characters'),
    '#spell.Enemy_Petrify' : (False, 'spell power', [20, 20], 'front row / back row'),
    '#spell.Enemy_Whisper' : (False, 'spell power', [20], 'random character'),
    '#spell.Enemy_Entangle' : (False, 'spell power', [20, 20], 'front row / back row'),
    '#spell.Enemy_WeakEnemy' : (False, 'spell power', [20], 'all characters'),
    '#spell.Enemy_HoldGas' : (False, 'spell power', [20, 20], 'front row / back row'),
    '#spell.Enemy_Gas' : (False, 'spell power', [20, 20], 'front row / back row'),
    '#spell.Enemy_Poison' : (False, 'spell power', [20], 'all characters'),
    '#spell.Enemy_Maser' : (True, 'spell power', [20], 'all characters'),
    '#spell.Enemy_Demolish' : (True, 'spell power', [20], 'random character'),
    '#spell.Enemy_Remedy' : (False, 'spell power', [20], 'self'),
    '#spell.Enemy_Absorb' : (False, 'spell power', [20], 'self'),
    '#spell.Enemy_Vampire' : (True, 'spell power', [128, 172], 'random character / all characters'),
    '#spell.Enemy_Crush' : (True, 'spell power', [20], 'random character'),
    '#spell.Enemy_Beam' : (True, 'spell power', [20, 20], 'front row / back row'),
    '#spell.Enemy_Globe199' : (True, 'spell power', [16], 'random character'),
    '#spell.Enemy_Fire' : (True, 'spell power', [20], 'all characters'),
    '#spell.Enemy_Blaze' : (True, 'spell power', [20], 'all characters'),
    '#spell.Enemy_Thunder' : (True, 'spell power', [20], 'all characters'),
    '#spell.Enemy_DBreath' : (True, 'spell power', [20], 'all characters'),
    '#spell.Enemy_BigWave' : (True, 'spell power', [20], 'all characters'),
    '#spell.Enemy_Laser' : (True, 'spell power', [20], 'random character'),
    '#spell.Enemy_HeatRay' : (True, 'spell power', [48], 'all characters'),
    '#spell.Enemy_Glare' : (True, 'spell power', [16], 'random character'),
    '#spell.Enemy_Needle' : (True, 'spell power', [32, 40], 'random character / all characters'),
    }

POSSIBLE_CHAOS_REACTIONS = {
    'fight' : (True, 'attack index', 0x5F, 'random character'),
    '#Change' : (False, '', 0, 'all characters'),
    '#spell.White' : (True, 'spell power', [14], 'random character'),
    '#spell.Fire3' : (True, 'spell power', [14], 'random character'),
    '#spell.Ice3' : (True, 'spell power', [14], 'random character'),
    '#spell.Lit3' : (True, 'spell power', [14], 'random character'),
    '#spell.Nuke' : (True, 'spell power', [14], 'random character'),
    '#spell.Enemy_Remedy' : (False, 'spell power', [14], 'self'),
    '#spell.Enemy_WeakEnemy' : (False, 'spell power', [14], 'random character'),
    '#spell.Enemy_BlkHole' : (False, 'spell power', [14], 'all characters'),
    '#spell.Enemy_MegaNuke' : (True, 'spell power', [6], 'all characters'),
    '#spell.Enemy_Demolish' : (True, 'spell power', [14], 'random character'),
    '#spell.Enemy_Laser' : (True, 'spell power', [14], 'random character'),
    '#spell.Enemy_Counter' : (True, 'spell power', [14, 14], 'random character / all characters'),
}

def apply(env):
    # if not env.options.flags.has_any('z_physical_script','z_physical_or_magical_script','-z:chaos','-z:lavosshell','z_random_bigbangs','z_random_phases','z_no_nerfs','z_must_nerf'):
    #     return
    
    bigbang_replacements = [[], [], [], [], [], []]
    script_nuke_replacement = []
    script_virus_replacement = []
    meteo_replacement = []
    counter_nuke_replacement = []
    counter_nuke_call_replacement = []
    counter_weak_replacement = []
    counter_virus_replacement = []
    stat_changes = ['monster($C9)\n', '{\n']
    bb_spell_powers = [31, 31, 32, 32, 31, 32]
    physicalflag = False
    whichbangflag = False
    replacescriptflag = False
    statchangeflag = False
    fixjumpflag = False

    # main script changes: physical, chaos, or three random scripts. Handle each of the applicable subflags as well, except for phaseshift.
    # at the end, check for other flags that impact the vanilla script.

    if env.options.flags.has('z_physical_script') or ((env.rnd.random() < 1/2) and env.options.flags.has('z_physical_or_magical_script')):
        physicalflag = True
        replacescriptflag = True
        statchangeflag = True
        fixjumpflag = True
        # repurpose attack index $5D to be (20, 99, 200) and $5E to be (18, 99, 255), set Z's base attack index to be $5D
        # ......... do I want to give Z an attack element? ... like *Drain*? lmao. No, but that'd be wild.
        env.add_binary(address.UnheaderedAddress(0x072497), [0x14, 0x63, 0xC8])
        env.add_binary(address.UnheaderedAddress(0x07249A), [0x12, 0x63, 0xFF])
        # use a different attack index under z_must_nerf:
        if env.options.flags.has('z_must_nerf'):
            stat_changes.append('    attack index $9F\n') # (255, 99, 255)
            env.add_file('scripts/dark_wave_damage.f4c')
        else:
            stat_changes.append('    attack index $5D\n')
        bb014_attack_index = ('$9F' if env.options.flags.has('z_must_nerf') else '$5D')
        bb235_attack_index = ('$9F' if env.options.flags.has('z_must_nerf') else '$5E')

        if env.options.flags.has('z_no_nerfs'):
            bigbang_replacements[0].extend([
                '    chain {\n',
                '        set attack index $5D\n',
                '        chain into\n',
                '        use command #DarkWave\n',
                '        condition 3\n'
                '    }\n',
            ])
            for i in [1, 4]:
                bigbang_replacements[i].extend([
                    '    chain {\n',
                    '        set attack index $5D\n',
                    '        chain into\n',
                    '        use command #DarkWave\n',
                    '    }\n',
                ])
            for i in [2, 3, 5]:
                bigbang_replacements[i].extend([
                    '    chain {\n',
                    '        set attack index $5E\n',
                    '        chain into\n',
                    '        use command #DarkWave\n',
                    '    }\n',
                ])  
        else:
            bigbang_replacements[0].extend([
                '    use command #DarkWave\n',
                '    condition 3\n'
            ])
            for i in [1, 4]:
                bigbang_replacements[i].extend([
                    '    set attack index ' + bb014_attack_index + '\n',
                    '    use command #DarkWave\n',
                ])
            for i in [2, 3, 5]:
                bigbang_replacements[i].extend([
                    '    set attack index ' + bb235_attack_index + '\n',
                    '    use command #DarkWave\n',
                ])

        # Yes, this works, but only because we wrote a bugfix for retargetting spells 
        script_nuke_replacement.extend([
            '    set attack index $5F\n',
            '    use command #Jump\n',
        ])
        script_virus_replacement.extend([
            '    set attack index $41\n',
            '    target all characters\n',
            '    use #spell.Enemy_Needle\n',
        ])
        # already in a chain
        meteo_replacement.extend([
            '    set attack index $4E\n',
            '    pass\n\n',
            '    use command #DarkWave\n',
        ])
        # new Fight counter, intended to allow nerfing of Dark Wave; script 0x4D
        counter_nuke_replacement.extend([ 
            '    set attack index $41\n',
            '    fight\n',
        ])
        # new Dart counter, strong Needle, nerfs Dark Wave a little bit; script 0x4E
        counter_nuke_call_replacement.extend([ 
            '    set attack index $5F\n',
            '    use #spell.Enemy_Counter\n',
        ])
        # new Jump counter, brutally very strong Fight, reverse nerf (like Virus does for normal Big Bang); script 0x4F
        counter_weak_replacement.extend([ 
            '    set attack index $5E\n',
            '    fight \n', 
        ])
        # new Aim counter, intended to allow nerfing of Dark Wave; script 0x58
        counter_virus_replacement.extend([ 
            '    set attack index $41\n',
            '    target all characters\n',
            '    use #spell.Enemy_Counter\n',  
        ])

        # custom react-to-dart condition: 0x16 is Dart, so... add 0xC0 to it? yep, works perfectly. 
        # overwriting index 0x05, which is unused; condition set 0x05 points at condition 0x05, so we just use that
        env.add_binary(address.UnheaderedAddress(0x076700 + (0x05 * 0x4)), [0x07, 0x19, 0xD6, 0x00])
        # custom react-to-aim condition: 0x0C is Aim, so... add 0xC0 to it? yep, works perfectly. overwriting index 0x29, which is unused
        # condition 0x29 is only used in condition set 0x30, so we just use that
        env.add_binary(address.UnheaderedAddress(0x076700 + (0x29 * 0x04)), [0x07, 0x19, 0xCC, 0x00])
        # for reactions: first two are vanilla, third is custom react-to-Dart, fourth is custom react-to-Aim, fifth is react-to-Jump (Land), sixth is react-to-Fight
        # will need to change in the event of writing a compiler for new ai sets/etc.
        env.add_binary(address.UnheaderedAddress(0x0764A1), [0x61, 0x56, 0x18, 0x54, 0x05, 0x4E, 0x30, 0x58, 0x5C, 0x4F, 0x06, 0x4D]) 
    
    elif env.options.flags.has('z_chaos_script'):
        # 2-5 random attacks per phase (or 1-3 for last phase), sometimes with a pass-shake-BB-type pattern (at most floor(n/2) of them), random reactions
        # each phase should have at least one damaging move
        chaos_phases = [[], [], []]
        shake_dict = POSSIBLE_BIGBANG_COMMANDS
        shake_dict.update({'#DarkWave' : (True, 'attack index', 0x5F, 'all characters')})
        potential_shake_attacks = list(shake_dict)
        potential_non_shake_attacks = list(POSSIBLE_CHAOS_COMMANDS)
        potential_reactions = list(POSSIBLE_CHAOS_REACTIONS)
        chaos_spoilers = []
        spoilers_to_add = [[], [], []]

        for i in range(0,3):
            if i < 2:
                max_attacks = env.rnd.randrange(2,6)
            else:
                max_attacks = env.rnd.randrange(1,4)
            max_shakes = max(1,max_attacks // 2)
            num_shakes = 0
            num_damaging = 0
            num_commands = 0
            num_black_hole = 0
            while num_commands < max_attacks:
                black_hole_added = False
                if num_shakes < max_shakes and (env.rnd.random() < 2/5):
                    # add a shake command that can be nerfed (usually), but not during "Meteo" phase
                    attack_to_add = env.rnd.choice(potential_shake_attacks)
                    attack_list = ['    pass\n' + ('\n' if i < 2 else ''), 
                                ('    use #ZeromusShake2\n\n' if i < 2 else '    \n')]
                    if attack_to_add == '#DarkWave':
                        if env.options.flags.has('z_must_nerf'):
                            attack_list.append('    set attack index $9F\n')
                            env.add_file('scripts/dark_wave_damage.f4c')
                        elif env.options.flags.has('z_no_nerfs'):
                            attack_list.append('    set attack index $5F\n')
                        attack_list.append('    use command #DarkWave\n\n')
                    else:
                        if env.options.flags.has('z_no_nerfs') and attack_to_add == '#spell.Meteo':
                            attack_list.append(f'    set spell power 9\n')
                        elif env.options.flags.has('z_no_nerfs') and attack_to_add == '#spell.Enemy_Globe199':
                            attack_list.append(f'    set spell power 20\n')
                        elif env.options.flags.has('z_must_nerf'):
                            attack_list.append(f'    set spell power 253\n')
                        else:
                            attack_list.append(f'    set spell power {shake_dict[attack_to_add][2]}\n')
                        attack_list.extend(['    target all characters\n',
                                            '    use ' + attack_to_add + '\n\n'])
                    if env.options.flags.has('z_no_nerfs'):
                        attack_list[-1] = attack_list[-1][:-1]
                        attack_list[2:] = ['    ' + attack_list[k+2] for k in range(0,len(attack_list[2:]))]
                        attack_list.insert(2, '    chain {\n')
                        attack_list.insert(4, '        chain into\n')
                        attack_list.append('    }\n\n')    

                    # sometimes add a Black Hole afterwards, but not always and no more than 2 per phase and not in "Meteo" phase
                    if i < 2 and num_black_hole < 2 and (env.rnd.random() < 3/5):
                        attack_list.extend([
                            '    use #Enemy_BlkHole\n',
                            '    message $75\n',
                            '    wait\n\n'
                        ])
                        num_black_hole += 1
                        black_hole_added = True    
                    
                    # make sure to add at least one damaging move
                    if not (num_damaging == 0 and num_commands == max_attacks-1 and not shake_dict[attack_to_add][0]):
                        chaos_phases[i].extend(attack_list)
                        num_commands += 1
                        num_shakes += 1
                        if shake_dict[attack_to_add][0]:
                            num_damaging += 1
                        # add to spoilers
                        if i < 2:
                            spoilers_to_add[i].append('Shake')
                        if attack_to_add == '#DarkWave':
                            spoilers_to_add[i].append('Dark Wave')
                        else:
                            spoilers_to_add[i].append(databases.get_spell_spoiler_name(attack_to_add))
                        if black_hole_added:
                            spoilers_to_add[i].append('Blk.Hole')

                else:
                    # add a normal command like the vanilla Nuke or Virus; can sometimes pass like in Nuke phase (a bit more likely than 1/10)
                    if env.rnd.random() < 1/10:
                        attack_to_add = 'pass'
                    else:
                        attack_to_add = env.rnd.choice(potential_non_shake_attacks)
                    attack_list = []

                    if attack_to_add in ['fight', '#Jump', '#Kick']:
                        attack_list.extend(['    set attack index $5F\n',
                            ('    fight\n\n' if attack_to_add == 'fight' else '    use command ' + attack_to_add + '\n\n')
                            ])
                        if attack_to_add == '#Jump':
                            fixjumpflag = True
                    elif attack_to_add == '#Change':
                        attack_list.append('    use command #Change\n\n')
                    elif attack_to_add == 'pass':
                        attack_list.append('    pass\n\n')
                    else:
                        targeting_data = env.rnd.choice(POSSIBLE_CHAOS_COMMANDS[attack_to_add][3].split(' / '))
                        spell_power_index = POSSIBLE_CHAOS_COMMANDS[attack_to_add][3].split(' / ').index(targeting_data)
                        if targeting_data == 'random character':
                            attack_list.extend([
                                f'    set spell power {POSSIBLE_CHAOS_COMMANDS[attack_to_add][2][spell_power_index]}\n',
                                '    use ' + attack_to_add + '\n\n'
                                ])                            
                        else:
                            attack_list.extend([
                                f'    set spell power {POSSIBLE_CHAOS_COMMANDS[attack_to_add][2][spell_power_index]}\n',
                                '    target ' + targeting_data + '\n',
                                '    use ' + attack_to_add + '\n\n'
                                ])
                            
                    # sometimes add a Black Hole afterwards, but not always and no more than 2 per phase and not in "Meteo" phase, less often than after shakes
                    if i < 2 and num_black_hole < 2 and (env.rnd.random() < 1/5):
                        attack_list.extend([
                            '    use #Enemy_BlkHole\n',
                            '    message $75\n',
                            '    wait\n\n'
                        ])
                        num_black_hole += 1
                        black_hole_added = True

                    # make sure to add at least one damaging move
                    if not (num_damaging == 0 and num_commands == max_attacks-1 and not POSSIBLE_CHAOS_COMMANDS[attack_to_add][0]):
                        chaos_phases[i].extend(attack_list)
                        num_commands += 1
                        if POSSIBLE_CHAOS_COMMANDS[attack_to_add][0]:
                            num_damaging += 1                    
                        # add to spoilers
                        if attack_to_add == 'fight':
                            spoilers_to_add[i].append('Fight')
                        elif attack_to_add == '#Change':
                            spoilers_to_add[i].append('Change Rows')
                        elif attack_to_add in ['#Jump', '#Kick']:
                            spoilers_to_add[i].append(attack_to_add[1:])
                        elif attack_to_add == 'pass':
                            pass
                        else:
                            spoilers_to_add[i].append(databases.get_spell_spoiler_name(attack_to_add))
                        if black_hole_added:
                            spoilers_to_add[i].append('Blk.Hole')
            # build spoiler entry for this phase
            chaos_spoilers.append((f'Zeromus script {i+1}', ', '.join(spoilers_to_add[i])))

        if env.options.flags.has('z_must_nerf'):
            statchangeflag = True
            # even with whichbang, we're restricting the opening BB to be magic, so don't change attack
            stat_changes.append('    spell power 255\n')

        for i in range(0,3):
            env.add_substitution(f'chaos phase {i+1}', ''.join(chaos_phases[i]))

        if env.options.flags.has('z_random_bigbangs'):
            single_bb_replacement = env.rnd.choice(list(POSSIBLE_BIGBANG_COMMANDS))
            bigbang_replacements[0].extend([
                '    target all characters\n',
                '    use ' + single_bb_replacement + '\n',
                '    condition 3\n'
            ])
            if env.options.flags.has('z_no_nerfs'):
                bigbang_replacements[0] = ['    ' + bigbang_replacements[0][k] for k in range(0,len(bigbang_replacements[i]))]
                bigbang_replacements[0].insert(0, '    chain {\n')
                bigbang_replacements[0].insert(1, f'        set spell power {bb_spell_powers[0]}\n')
                bigbang_replacements[0].insert(2, '        chain into\n')
                bigbang_replacements[0].append('    }\n')

            chaos_spoilers.insert(0, ("Opening Big Bang replacement", databases.get_spell_spoiler_name(single_bb_replacement)))

        elif env.options.flags.has('z_no_nerfs'):
            bigbang_replacements[0].extend([
                '    chain {\n',
                f'        set spell power {bb_spell_powers[0]}\n',
                '        chain into\n',
                '        use #Enemy_BigBang\n',       
                '        condition 3\n'
                '    }\n'
            ])            

        # build reactions
        reaction_list = []
        reaction_spoiler_labels = ['Counter Nuke replacement', 'Counter Nuke Call replacement', 'Counter Weak replacement', 'Counter Virus replacement']
        for i in range(0,4):
            reaction_to_add = env.rnd.choice(potential_reactions)
            # set both attack and spell power for all reactions, in case of DarkWave
            if reaction_to_add == 'fight':
                reaction_list.append([
                    '    set spell power 14\n',
                    '    set attack index $5F\n',
                    '    fight\n'
                ])
                chaos_spoilers.append((reaction_spoiler_labels[i], 'Fight'))
            elif reaction_to_add == '#Change':
                reaction_list.append([
                    '    set spell power 14\n',
                    '    set attack index $5F\n',
                    '    use command ' + reaction_to_add + '\n'
                ])
                chaos_spoilers.append((reaction_spoiler_labels[i], 'Change Rows'))
            else:
                targeting_data = env.rnd.choice(POSSIBLE_CHAOS_REACTIONS[reaction_to_add][3].split(' / '))
                spell_power_index = POSSIBLE_CHAOS_REACTIONS[reaction_to_add][3].split(' / ').index(targeting_data)
                if targeting_data == 'random character':
                    reaction_list.append([
                        f'    set spell power {POSSIBLE_CHAOS_REACTIONS[reaction_to_add][2][spell_power_index]}\n',
                        '    set attack index $5F\n',
                        '    use ' + reaction_to_add + '\n'
                    ])         
                else:          
                    reaction_list.append([
                        f'    set spell power {POSSIBLE_CHAOS_REACTIONS[reaction_to_add][2][spell_power_index]}\n',
                        '    set attack index $5F\n',
                        '    target ' + targeting_data + '\n',
                        '    use ' + reaction_to_add + '\n'
                    ])
                    if reaction_to_add == '#spell.Enemy_BlkHole':
                        reaction_list[-1].append('    message $75\n')
                chaos_spoilers.append((reaction_spoiler_labels[i], databases.get_spell_spoiler_name(reaction_to_add)))
        counter_nuke_replacement.extend(reaction_list[0])
        counter_nuke_call_replacement.extend(reaction_list[1])
        counter_weak_replacement.extend(reaction_list[2])
        counter_virus_replacement.extend(reaction_list[3])

        env.add_file('scripts/zeromus_chaosscript.f4c')
        env.spoilers.add_table("MISC", chaos_spoilers, public = env.options.flags.has_any('-spoil:all', '-spoil:misc'))        

    elif env.options.flags.has('z_random_scripts'):
        # assign three random scripts from the game, avoiding condition changes
        # mutually exclusive with z_shuffle_scripts/-z:phaseshift
        # requires a patch for Z to load both normal and alternate scripts
        env.add_file('scripts/zeromus_mimicscript.f4c')

        scripts = list(POSSIBLE_SCRIPTS_DICT)
        script_descriptions = POSSIBLE_SCRIPTS_DICT
        if env.options.flags.has('no_free_bosses'):
            scripts.extend(list(POSSIBLE_BNOFREE_SCRIPTS_DICT))
            script_descriptions.update(POSSIBLE_BNOFREE_SCRIPTS_DICT)
        env.rnd.shuffle(scripts)
        env.add_substitution('Virus phase script type', ('#$80' if scripts[0] > 0xFF else '#$00'))
        env.add_substitution('Nuke phase script type', ('#$80' if scripts[1] > 0xFF else '#$00'))
        env.add_substitution('Meteo phase script type', ('#$80' if scripts[2] > 0xFF else '#$00'))
        scripts_lo_bytes = [(scripts[i]-0x100 if scripts[i] > 0xFF else scripts[i]) for i in range(3)]
        env.add_binary(address.UnheaderedAddress(0x076498), [0x15, scripts_lo_bytes[2], 0x14, scripts_lo_bytes[1], 0x13, scripts_lo_bytes[0], 0x00, 0x4B])
        
        # make sure to patch Jump for monsters if necessary
        if 0xDA in scripts[:3]:
            fixjumpflag = True
        # patch Big Bangs for whichbang, nonerfs, mustnerf
        if env.options.flags.has('z_random_bigbangs'):
            whichbangflag = True
        elif env.options.flags.has('z_no_nerfs'):
            replacescriptflag = True
            bigbang_replacements[0].extend([
                '    chain {\n',
                f'        set spell power {bb_spell_powers[0]}\n',
                '        chain into\n',
                '        use #Enemy_BigBang\n',       
                '        condition 3\n',
                '    }\n'
            ])
            if 0x14C in scripts[:3]:
                for i in [1, 2, 3]:
                    bigbang_replacements[i].extend([
                        '    chain {\n',
                        f'        set spell power {bb_spell_powers[i]}\n',
                        '        chain into\n',
                        '        use #Enemy_BigBang\n',
                        '    }\n'
                    ])
            if 0x155 in scripts[:3]:
                for i in [4, 5]:
                    bigbang_replacements[i].extend([
                        '    chain {\n',
                        f'        set spell power {bb_spell_powers[i]}\n',
                        '        chain into\n',
                        '        use #Enemy_BigBang\n',
                        '    }\n'
                    ])
        elif env.options.flags.has('z_must_nerf'):
            replacescriptflag = True
            statchangeflag = True
            stat_changes.append('    spell power 255\n')
            if 0x14C in scripts[:3]:
                for i in [1, 2, 3]:
                    bigbang_replacements[i].extend([
                    '    set spell power 253\n',
                    '    use #Enemy_BigBang\n',
                    ])
            if 0x155 in scripts[:3]:
                for i in [4, 5]:
                    bigbang_replacements[i].extend([
                    '    set spell power 253\n',
                    '    use #Enemy_BigBang\n',
                    ])
        # spoiler log:
        env.spoilers.add_table(
            "MISC", 
            [ ("Zeromus script 1", script_descriptions[scripts[0]]),
            ("Zeromus script 2", script_descriptions[scripts[1]]),
            ("Zeromus script 3", script_descriptions[scripts[2]]) ],
            public = env.options.flags.has_any('-spoil:all', '-spoil:misc')
            )

    else:
        # vanilla script, except with modifications to Big Bangs/nerfs.
        if env.options.flags.has('z_random_bigbangs'):
            whichbangflag = True

        elif env.options.flags.has('z_no_nerfs'): 
            # vanilla script but with chains for the Big Bangs; yes, this will be brutal
            replacescriptflag = True
            bigbang_replacements[0].extend([
                '    chain {\n',
                f'        set spell power {bb_spell_powers[0]}\n',
                '        chain into\n',
                '        use #Enemy_BigBang\n',       
                '        condition 3\n'
                '    }\n'
            ])
            for i in range(1,6):
                bigbang_replacements[i].extend([
                    '    chain {\n',
                    f'        set spell power {bb_spell_powers[i]}\n',
                    '        chain into\n',
                    '        use #Enemy_BigBang\n',
                    '    }\n'
                ])
        
        elif env.options.flags.has('z_must_nerf'):
            # vanilla script except we make the spell power set to 253 (0xFD) for Big Bangs
            # setting 255 at the start via the script-change f4c
            # I *think* using 255 (0xFF) makes the game think it's an opcode... yep. so does 254 (0xFE), so 253 it is.
            replacescriptflag = True
            statchangeflag = True
            stat_changes.append('    spell power 255\n')
            
            for i in range(1,6):
                bigbang_replacements[i].extend([
                    '    set spell power 253\n',
                    '    use #Enemy_BigBang\n',
                ])  

    if whichbangflag:
        # vanilla script except we replace Big Bangs with other spells
        replacescriptflag = True
        commands = list(POSSIBLE_BIGBANG_COMMANDS)
        replacement_commands = []
        for i in range(0,5):
            replacement_commands.append(env.rnd.choice(commands))
        # the last Big Bang can have some funnier commands
        commands.extend(list(BIGBANG_5_COMMANDS))
        replacement_commands.append(env.rnd.choice(commands))

        # use a different spell power under z_must_nerf:
        # setting 255 at the start via the f4c, 253 for scripted changes because 254/255 break things
        if env.options.flags.has('z_must_nerf'):
            statchangeflag = True
            stat_changes.append('    spell power 255\n')
        for i in range(0,6):
            if env.options.flags.has('z_no_nerfs') and replacement_commands[i] == '#spell.Meteo':
                bb_spell_powers[i] = 9
            elif env.options.flags.has('z_no_nerfs') and replacement_commands[i] == '#spell.Enemy_Globe199':
                bb_spell_powers[i] = 20
            elif env.options.flags.has('z_must_nerf'):
                bb_spell_powers[i] = 253

        bigbang_replacements[0].extend([
            '    target all characters\n',
            '    use ' + replacement_commands[0] + '\n',
            '    condition 3\n'
        ])
        for i in range(1,6):
            bigbang_replacements[i].extend([
                f'    set spell power {bb_spell_powers[i]}\n',
                '    target all characters\n',
                '    use ' + replacement_commands[i] + '\n',
            ])

        if env.options.flags.has('z_no_nerfs'):
            for i in range(0,6):
                bigbang_replacements[i] = ['    ' + bigbang_replacements[i][k] for k in range(0,len(bigbang_replacements[i]))]
            bigbang_replacements[0].insert(0, '    chain {\n')
            bigbang_replacements[0].insert(1, f'        set spell power {bb_spell_powers[0]}\n')
            bigbang_replacements[0].insert(2, '        chain into\n')
            bigbang_replacements[0].append('    }\n')
            for i in range(1,6):
                bigbang_replacements[i].insert(0, '    chain {\n')
                bigbang_replacements[i].insert(2, '        chain into\n')
                bigbang_replacements[i].append('    }\n')

        # build spoiler log
        env.spoilers.add_table(
            "MISC", 
            [ ("Opening Big Bang replacement", databases.get_spell_spoiler_name(replacement_commands[0])),
            ("Virus phase Big Bang replacements", ', '.join([databases.get_spell_spoiler_name(replacement_commands[i]) for i in range(1,4)])),
            ("Nuke phase Big Bang replacements", ', '.join([databases.get_spell_spoiler_name(replacement_commands[i]) for i in range(4,6)])) ],
            public = env.options.flags.has_any('-spoil:all', '-spoil:misc')
            )

    if env.options.flags.has('z_random_phases'):
        # mutually exclusive with -z:lavosshell and -z:chaos; handled by flagsetcore
        phases = [0x4C, 0x55, 0x57]
        env.rnd.shuffle(phases)
        # manual bytes for attack phase shuffle:
        env.add_binary(address.UnheaderedAddress(0x076498), [0x15, phases[2], 0x14, phases[1], 0x13, phases[0], 0x00, 0x4B])
        # build spoiler log entry
        phases_name_dict = ( {0x46 : 'Needle', 0x55 : 'Jump', 0x57 : 'Dark Wave'} if physicalflag 
                            else {0x46 : 'Virus', 0x55 : 'Nuke', 0x57 : 'Meteo'} )
        env.spoilers.add_table(
            "MISC", 
            [ ("Zeromus phase order", ', '.join([phases_name_dict[p] for p in phases])) ],
            public = env.options.flags.has_any('-spoil:all', '-spoil:misc')
            )        

    # now add the script changes as substitutions, and add any remaining f4c files
    for i in range(0,6):
        if bigbang_replacements[i]:
            env.add_substitution(f'big bang {i+1} replacement', ''.join(bigbang_replacements[i]))
    if script_nuke_replacement:
        env.add_substitution('script virus replacement', ''.join(script_virus_replacement))
        env.add_substitution('script nuke replacement', ''.join(script_nuke_replacement))
    if meteo_replacement:
        env.add_substitution('meteo replacement', ''.join(meteo_replacement))
    if counter_nuke_replacement:
        env.add_substitution('counter nuke replacement', ''.join(counter_nuke_replacement))
        env.add_substitution('counter virus replacement', ''.join(counter_virus_replacement))
        env.add_substitution('counter weak replacement', ''.join(counter_weak_replacement))
        env.add_substitution('counter nuke call replacement', ''.join(counter_nuke_call_replacement))
    if replacescriptflag:
        env.add_file('scripts/zeromus_replacescript.f4c')
    if statchangeflag:
        stat_changes.append('}\n')
        env.add_substitution('Z base stat changes', ''.join(stat_changes))
    if fixjumpflag:
        env.add_file('scripts/fix_jump_retargeting.f4c')