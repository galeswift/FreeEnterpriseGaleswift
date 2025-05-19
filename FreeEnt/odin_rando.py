from . import databases

POSSIBLE_ODIN_COMMANDS = [
    '#spell.Drain',
    '#spell.Psych',
    '#spell.Toad',
    '#spell.Fire2',
    '#spell.Fire3',
    '#spell.Ice2',
    '#spell.Ice3',
    '#spell.Lit2',
    '#spell.Lit3',
    '#spell.Virus',
    '#spell.Weak',
    '#spell.Enemy_Magnet',
    '#spell.Enemy_Gas',
    '#spell.Enemy_Whisper',
    '#spell.Enemy_Bluster',
    '#spell.Enemy_Breath',
    '#spell.Enemy_Glance',
    '#spell.Enemy_Blast',
    '#spell.Enemy_Needle',
    '#spell.Enemy_Counter'
    ]

UNSAFE_ODIN_COMMANDS = [ 
    '#spell.Enemy_Glare',
    '#spell.Enemy_Globe199',
    '#spell.Enemy_Laser',
    '#spell.Nuke',
    '#spell.White',
    '#spell.Stone',
    '#spell.Enemy_Hug',
    '#spell.Fatal'
    ]

def apply(env):
    if env.options.flags.has('odin_random_spell'):
        odin_commands = list(POSSIBLE_ODIN_COMMANDS)
        if env.options.flags.has('bosses_unsafe'):
             odin_commands.extend(UNSAFE_ODIN_COMMANDS)
        cmd = env.rnd.choice(list(odin_commands))
        script = f'use {cmd}'
        env.add_substitution('odin spell replacement', script)
        if env.meta.get('wacky_challenge') == 'advertising':
            env.add_file('scripts/wacky/odin_advertising.f4c')
        else:
            env.add_file('scripts/odin_replace_two_zantetsukens.f4c')
        
        env.spoilers.add_table(
            "MISC",
            [["Odin spells 1+2", databases.get_spell_spoiler_name(cmd)]],
            public = env.options.flags.has_any('-spoil:all','-spoil:misc')
            )
    elif env.meta.get('wacky_challenge') == 'advertising':
        env.add_file('scripts/wacky/odin_advertising.f4c')