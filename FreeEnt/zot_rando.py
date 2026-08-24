from . import databases

ZOT_SPELLS = ['Bersk', 'Blink', 'Cure3', 'Cure4', 'Exit', 'Fast', 'Float', 'Life2', 'Size', 'Wall', 'White']

def apply(env):
    if not env.options.flags.has('random_zot_spell'):
        spell_name = 'Exit'
    else:
        spell_name = env.rnd.choice(ZOT_SPELLS)

    if env.options.flags.has('rosapaladin'):
        # Rosa is using PCecil's spellset
        spellset_name = 'PCecil'
    else:
        spellset_name = 'Rosa'

    zot_spell_script = [f'give spell #{spellset_name} #{spell_name}']
    if env.options.flags.has('random_zot_spell'):
        zot_spell_script.extend([f'[#B #Text_LoadSpellName 2 #spell.{spell_name}]',
                                 'sound #WhiteMagic',
                                 'message $10D'])
    env.add_substitution('zot spell rando', '\n'.join(zot_spell_script))

    env.meta['zot_spell'] = f'#{spell_name}'

    # spoiler
    if env.options.flags.has('random_zot_spell'):
        env.spoilers.add_table("MISC", 
            [["Zot spell", databases.get_spell_spoiler_name(f"#spell.{spell_name}")]], 
            public=env.options.flags.has_any('-spoil:all', '-spoil:misc'))