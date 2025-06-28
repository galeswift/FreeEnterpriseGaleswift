from . import databases

POSSIBLE_GOLBEZ_COMMANDS = [
    '#spell.Drain',
    '#spell.Fire2',
    '#spell.Fire3',
    '#spell.Ice2',
    '#spell.Ice3',
    '#spell.Lit2',
    '#spell.Lit3',
    '#spell.Virus',
    '#spell.Weak'
    ]

UNSAFE_GOLBEZ_COMMANDS = [
    '#spell.Enemy_Glare',
    '#spell.Enemy_Globe199',
    '#spell.Enemy_Laser',
    '#spell.Nuke'
    ]

POSSIBLE_SHADOW_COMMANDS = [
    '#spell.Enemy_Beak',
    '#spell.Enemy_Bluster',
    '#spell.Enemy_Breath',
    '#spell.Enemy_Count',
    '#spell.Enemy_Crush',
    '#spell.Enemy_Demolish',
    '#spell.Enemy_Disrupt2', # the instant-kill, not the status removal
    '#spell.Fatal',
    '#spell.Enemy_Gas',
    '#spell.Enemy_Hug',
    '#spell.Mute',
    '#spell.Enemy_Petrify',
    '#spell.Piggy',
    '#spell.Enemy_Ray',
    '#spell.Enemy_Search',
    '#spell.Size',
    '#spell.Enemy_Slap',
    '#spell.Stone',
    '#spell.Toad',
    '#spell.Enemy_Whisper'
    ]

def apply(env):
    if env.options.flags.has('golbez_no_shadow') and not env.options.flags.has('golbez_random_spells'):
        env.add_file('scripts/golbez_no_shadow.f4c')

    if env.options.flags.has('golbez_random_spells'):
        golbez_commands = POSSIBLE_GOLBEZ_COMMANDS
        if env.options.flags.has('bosses_unsafe'):
            golbez_commands = golbez_commands + UNSAFE_GOLBEZ_COMMANDS
        env.rnd.shuffle(golbez_commands)
        golbez1 = f'use {golbez_commands[0]}'
        golbez2 = f'use {golbez_commands[1]}'
        golbez3 = f'use {golbez_commands[2]}'
        env.add_substitution('golbez spell 1 replacement', golbez1)
        env.add_substitution('golbez spell 2 replacement', golbez2)
        env.add_substitution('golbez spell 3 replacement', golbez3)
        env.spoilers.add_table(
            "MISC", 
            [["Golbez spell 1", databases.get_spell_spoiler_name(golbez_commands[0])],
             ["Golbez spell 2", databases.get_spell_spoiler_name(golbez_commands[1])],
             ["Golbez spell 3", databases.get_spell_spoiler_name(golbez_commands[2])]],
            public = env.options.flags.has_any('-spoil:all', '-spoil:misc')
            )
        if env.options.flags.has('golbez_no_shadow'):
            env.add_file('scripts/golbez_no_shadow_spells.f4c')
        else:
            shadow_commands = POSSIBLE_SHADOW_COMMANDS
            env.rnd.shuffle(shadow_commands)
            shadow1 = f'use {shadow_commands[0]}'
            shadow2 = f'use {shadow_commands[1]}'
            shadow3 = f'use {shadow_commands[2]}'
            env.add_substitution('shadow spell 1 replacement', shadow1)
            env.add_substitution('shadow spell 2 replacement', shadow2)
            env.add_substitution('shadow spell 3 replacement', shadow3)
            env.add_file('scripts/golbez_shadow_spells.f4c')
            env.spoilers.add_table(
                "MISC", 
                [["Shadow spell 1", databases.get_spell_spoiler_name(shadow_commands[0])],
                 ["Shadow spell 2", databases.get_spell_spoiler_name(shadow_commands[1])],
                 ["Shadow spell 3", databases.get_spell_spoiler_name(shadow_commands[2])]],
                public = env.options.flags.has_any('-spoil:all', '-spoil:misc')
                )
