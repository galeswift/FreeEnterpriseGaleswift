from .address import *
from . import databases

DWARF_CASTLE_WHITE_POOL = ['Mute', 'Charm', 'Blink', 'Slow', 'Fast', 'Bersk', 'Wall', 'Peep', 'Cure3', 'Size', 'Exit', 'Float']

def apply(env):
    # misc/creative tweaks
    if env.options.flags.has('kainmagic'):
        env.add_file('scripts/give_kain_magic.f4c')
        mp_script = '\n'
        for level in range(1,51):
            mp_script = mp_script + f'patch (${(0x0FB65E + (0x05 * (level-1))):06X} bus) {{ {2:02X} }}\n'
        env.add_substitution('kain mp script', mp_script)
    elif env.options.flags.has('harmspell'):
        env.add_file('scripts/harm_spell.f4c')

    if env.options.flags.has('edwardheal'):
        env.add_file('scripts/improve_edward_heal.f4c')

    if env.options.flags.has_any('edwardsing','edwardsing_better'):
        env.add_file('scripts/edward_sing_upgrade.f4c')
        sing_text_options = [
            'Song of Molbols',
            'Song of Ruin',
            'Sick Beats',
            'Samba de Status',
            'Debuff Dirge',
            'Evil Chorus',
            'Vogon Poetry'
            ]
        env.rnd.shuffle(sing_text_options)
        env.add_substitution('song of silence replacement text', sing_text_options[0])
        if env.options.flags.has('edwardsing_better'):
            env.add_substitution('edward sing status options', '#$bcff')
        else:
            env.add_substitution('edward sing status options', '#$1804')

    if env.options.flags.has('cidairship'):
        env.add_file('scripts/cidairship.f4c')

    if env.options.flags.has('cidpeep'):
        env.add_file('scripts/improve_cid_peep.f4c')

    if env.options.flags.has('twinmeteo'):
        env.add_file('scripts/twin_meteo_stone.f4c')

    if env.options.flags.has('bigchocobosummon'):
        env.add_file('scripts/big_chocobo_summon.f4c')
        if 'saveusbigchocobo' in env.meta.get('wacky_challenge',[]):
            env.add_toggle('save us big chocobo summon')

    if env.options.flags.has('darkpaladin'):    
        # apply stat changes, gear changes, and extra scripting
        # some names are changed in character_rando
        dp_initial_stats_script = ('\n' + 'patch ($0FAA27 bus) { 90 01 90 01 }\n' + # 400 HP
            'patch ($0FAA2F bus) { 0F 0F 0A 07 04 }\n' + # 15 Str/Agi, 10 Vit, 7 Wis, 4 Wil
            'patch ($0FAA34 bus) { 0A 32 }\n' # crit rate 10 (from 3), bonus 50 (from 30)
        )
        env.add_script(dp_initial_stats_script)

        dp_level_up_stats_script = '\n'
        for level in range(1,70):
            str_bit = (1 if (level % 7) in [0,1,2,4,5] else 0) + (1 if (level % 7) in [3,6] and (level > 25) else 0)
            agi_bit = (1 if (level > 15) and (level % 2) == 0 else 0)
            vit_bit = (1 if ((level+1) % 5) == 0 else 0)
            wis_bit = (1 if (level % 5) in [0,2]  else 0) + (1 if (level % 5) in [1,3] and (level in range(30,45)) else 0)
            wil_bit = (1 if ((level+1) % 6) == 0 else 0)
            incr_bits = (2 if (level % 7) == 0 else 1) + (1 if (level % 3) == 0 and (level in range(40,60)) else 0) 
            stats_byte = (0x80 * str_bit) + (0x40 * agi_bit) + (0x20 * vit_bit) + (0x10 * wis_bit) + (0x08 * wil_bit) + incr_bits
            hp_byte = 12 + 6 * (level // 8) + 4 * max(0,min(level-30, 13))
            dp_level_up_stats_script = dp_level_up_stats_script + f'patch (${(0x0FC010 + (0x05 * (level-1))):06X} bus) {{ {stats_byte:02X} {hp_byte:02X} }}\n'
        env.add_script(dp_level_up_stats_script)
        
        if not 'whatsmygear' in env.meta.get('wacky_challenge',[]):
            env.add_script('\n'+ 
                'patch ($0f91d7 bus) { 90 }\n' + # Str/Wis +3 for Light/Chaos Sword
                'patch ($0f92ff bus) { B3 }\n' # Str/Vit/Wis +15 for Crystal/Hades Sword
                )
            wis_wil_swap = '\n'
            for gear_id in [0x64, 0x6C, 0x71, 0x76, 0x85, 0x8C, 0xA0, 0xA6]:
                wis_wil_swap += f'patch (${(0x0F9100 + (0x08 * gear_id) + 0x07):06X} bus)' + ' { 10 }\n' # Wis+3 for all Pally/Ancient and Crystal/Hades gear
            env.add_script(wis_wil_swap)

        env.add_file('scripts/darkpaladin.f4c')

    elif env.options.flags.has('rosapaladin'):
        env.add_file('scripts/rosa_paladin.f4c')
        env.add_substitution('auto cover job class', '#$05')

    if env.options.flags.has('rosapray'):
        env.add_file('scripts/improve_rosa_pray.f4c')

    if env.options.flags.has('fusoyaregen'):
        if 'tellahmaneuver' in env.meta.get('wacky_challenge',[]):
            env.add_binary(BusAddress(0x03E3FE), [0x32]) # 50 HP regen instead of 10 HP
        else:
            env.add_file('scripts/improve_fusoya_regen_mp.f4c')
            env.add_toggle('fusoya_regen_mp')
            if '3point' in env.meta.get('wacky_challenge',[]):
                env.add_binary(BusAddress(0x03E3FE), [0x01]) # 1 MP regen instead of 10 MP
                env.add_binary(BusAddress(0x03AAA7), [0x14]) # counter needs to hit 20 ticks instead of 5 ticks 
                env.add_binary(BusAddress(0x13FEAB), [0x99]) # regen duration should be 25*RA ticks

    if env.options.flags.has('yanghp'):
        # allow Yang to get 152-171 HP from level 61-69 (and 60), and 160-180 on levels 70+
        for lvl in range(61,70):
            env.add_binary(BusAddress(0x0FBD6F + (0x05) * (lvl-61)), [0x98])
        env.add_binary(BusAddress(0x0FBD9C), [0xA0])

    if env.options.flags.has('tellahrecall'):
        # flatten the Recall distribution, remove failure, tier1 -> tier3
        env.add_binary(BusAddress(0x03EA1D), [0x9F])
        for i in range(8):
            env.add_binary(BusAddress(0x03EA22 + (i * 0x08)), [(i+1) * 0x14])
        for i in range(3):
            env.add_binary(BusAddress(0x03EA46 + (i * 0x08)), [0x1F + (i * 0x03)])

    if env.options.flags.has('edgedart'):
        env.add_file('scripts/edgedart.f4c')

    if env.options.flags.has('magicwhips'):
        env.add_file('scripts/whip_summon_bonus.f4c')

    if env.options.flags.has('rydiaredmage'):
        # Rydia gets Life1, Heal... and the vanilla game already gives her Cure2. Funny that. She gets Harm if it's available.
        fixed_white_to_add = ['Life1', 'Heal'] + (['Harm'] if env.options.flags.has('harmspell') else [])
        # identify the 5 random spells Rydia gets at Dwarf Castle
        if env.options.flags.has('japanese_spells'):
            DWARF_CASTLE_WHITE_POOL.extend(['Armor', 'Shell', 'Dspel'])
        random_white_to_add = env.rnd.sample(DWARF_CASTLE_WHITE_POOL, (4 if env.options.flags.has('harmspell') else 5))
        spell_names = (fixed_white_to_add + random_white_to_add)[2:]
        spoiler_names = ['Cure2'] + fixed_white_to_add + random_white_to_add
        
        dwarf_white_script_lines = (
            [f'give spell #RydiaWhite #{spell}' for spell in fixed_white_to_add + random_white_to_add]
            + [f'[#B #Text_LoadSpellName {index} #spell.{spell}]' for index,spell in enumerate(spell_names)]
            + ['message $11d']
            )
    
        env.add_substitution('dwarf summon rando', '\n'.join(dwarf_white_script_lines))

        env.spoilers.add_table("MISC", 
            [["Dwarf castle white magic", ', '.join([databases.get_spell_spoiler_name(f"#spell.{spell}") for spell in spoiler_names])]], 
            public=env.options.flags.has_any('-spoil:all', '-spoil:misc'))
        
        env.add_file('scripts/rydiaredmage.f4c')