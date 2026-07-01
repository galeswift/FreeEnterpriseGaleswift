ABILITIES_TO_HEX = {
    '#Fight'    : 0x00,
    '#Item'     : 0x01,
    '#White'    : 0x02,
    '#Black'    : 0x03,
    '#Call'     : 0x04,
    '#DarkWave' : 0x05,
    '#Jump'     : 0x06,
    '#Recall'   : 0x07,
    '#Sing'     : 0x08,
    '#Hide'     : 0x09,
    '#Medicine' : 0x0A,
    '#Pray'     : 0x0B,
    '#Aim'      : 0x0C,
    '#Focus'    : 0x0D,
    '#Kick'     : 0x0E,
    '#Fortify'  : 0x0F,
    '#Twin'     : 0x10,
    '#Bluff'    : 0x11,
    '#Cry'      : 0x12,
    '#Cover'    : 0x13,
    '#Peep'     : 0x14,
    '#Raid'     : 0x15,
    '#Dart'     : 0x16,
    '#Sneak'    : 0x17,
    '#Ninja'    : 0x18,
    '#Regen'    : 0x19,
    '#Omni'     : 0x19,
}

def command_lists(env):
    # updates command lists based on flags
    # situations to care about:
    # -- command changes wackies (Darts, Musical, Klepto)
    # -- j-abilities
    # -- added abilities from e.g. -tweak flags, Fomnimage
    # -- other flags that give/change ability lists

    # start with vanilla (non-J) command lists, minus #Item
    # note that we need actor constants here (to do actor(#const) { ... })
    commands = {}
    commands['DKCecil'] = [
        '#Fight'
    ]
    commands['Kain1'] = [
        '#Fight',
        '#Jump'
    ]
    commands['CRydia'] = [
        '#Fight',
        '#White',
        '#Black',
        '#Call'
    ]
    commands['Tellah1'] = [
        '#Fight',
        '#White',
        '#Black'
    ]
    commands['Edward'] = [
        '#Fight',
        '#Sing',
        '#Hide'
    ]
    commands['Rosa1'] = [
        '#Fight',
        '#White',
        '#Aim'
    ]
    commands['Yang1'] = [
        '#Fight',
        '#Kick'
    ]
    commands['Palom'] = [
        '#Fight',
        '#Black',
        '#Twin'
    ]
    commands['Porom'] = [
        '#Fight',
        '#White',
        '#Twin'
    ]
    commands['PCecil'] = [
        '#Fight',
        '#White',
        '#Cover'
    ]
    commands['Tellah3'] = [
        '#Fight',
        '#White',
        '#Black'
    ]
    commands['Cid'] = [
        '#Fight',
        '#Peep'
    ]
    commands['ARydia'] = [
        '#Fight',
        '#Black',
        '#Call'
    ]
    commands['Edge'] = [
        '#Fight',
        '#Dart',
        '#Sneak',
        '#Ninja'
    ]
    commands['Fusoya'] = [
        '#Fight',
        '#White',
        '#Black'
    ]

    if env.options.flags.has('darkpaladin'):
        # Paladin -> Dark Paladin commands
        commands['PCecil'] = [
            '#Fight',
            '#Black'
        ]

    if env.options.flags.has('japanese_abilities'):
        # add in J-abilities
        commands['DKCecil'].append('#DarkWave')
        commands['Tellah1'].append('#Recall')
        commands['Edward'].append('#Medicine')
        commands['Rosa1'].append('#Pray')
        commands['Yang1'].extend(['#Focus', '#Fortify'])
        commands['Palom'].append('#Bluff')
        commands['Porom'].append('#Cry')
        if env.options.flags.has('darkpaladin'):
            commands['PCecil'].insert(1,'#DarkWave')
        commands['Fusoya'].append('#Regen')

    elif env.options.flags.has('all_good_abilities'):
        # set up "good" command lists
        commands['DKCecil'].extend(['#DarkWave', '#Hide', '#Dart'])
        commands['Kain1'].extend(['#DarkWave', '#Sneak'])
        commands['Tellah1'].append('#Recall')
        if not env.options.flags.has_any('edwardsing', 'edwardsing_better'):
            # Sing is good if we've buffed it
            commands['Edward'].remove('#Sing')
            commands['Edward'].append('#Cry')
        if env.options.flags.has('edwardheal'):
            # Heal is good if we've buffed it
            commands['Edward'].append('#Medicine')
        else:
            commands['Edward'].append('#Aim')
        if env.options.flags.has('rosapray'):
            # Pray is good if we've buffed it
            commands['Rosa1'].append('#Pray')
        else:
            commands['Rosa1'].append('#Cover')
        commands['Yang1'].extend(['#Focus', '#Fortify'])
        commands['Palom'].append('#Bluff')
        commands['Porom'].append('#Cry')
        if env.options.flags.has('darkpaladin'):
            # Dark Pally gets Power, Paladin gets Bear
            commands['PCecil'].append('#Focus')
        else:
            commands['PCecil'].append('#Fortify')
        commands['Cid'].extend(['#Focus', '#Aim', '#Fortify'])
        if not env.options.flags.has('rydiaredmage'):
            commands['ARydia'].append('#Bluff')
        if env.options.flags.has('fusoyaregen'):
            # Fu gets Regen (for now), as does post-Ordeals Tellah
            commands['Tellah3'].append('#Regen')
            commands['Fusoya'].append('#Regen')
        else:
            # Fu gets Bluff, and Tellah gets Pray if it's good or Bluff if not
            if env.options.flags.has('rosapray'):
                commands['Tellah3'].append('#Pray')
            else:
                commands['Tellah3'].append('#Bluff')
            commands['Fusoya'].append('#Bluff')

    if env.options.flags.has('cidairship'):
        # give Cid his Raid command
        if env.options.flags.has('all_good_abilities'):
            commands['Cid'].remove('#Peep')
            commands['Cid'].remove('#Fortify')
            # ... and Kain, if he needs it
            commands['Kain1'].remove('#DarkWave')
            commands['Kain1'].insert(2,'#Raid')
        commands['Cid'].append('#Raid')
    elif env.options.flags.has('all_good_abilities'):
        if env.options.flags.has('cidpeep'):
            # Peep is better now, so we'll keep it (even if Bear might still be better)
            commands['Cid'].remove('#Fortify')
        else:
            commands['Cid'].remove('#Peep')

    if env.options.flags.has('kainmagic'):
        # give Kain White and Black commands
        commands['Kain1'].extend(['#White', '#Black'])
        if env.options.flags.has('all_good_abilities'):
            if not env.options.flags.has('cidairship'):
                commands['Kain1'].remove('#DarkWave')
            commands['Kain1'].remove('#Sneak')

    if env.options.flags.has('rydiaredmage'):
        commands['ARydia'].insert(1,'#White')

    if env.options.flags.has('add_spells_fusoya'):
        # replace Regen with Omni if necessary, or just add it
        if len(commands['Fusoya']) > 3:
            # remove either Regen or Bluff if necessary
            commands['Fusoya'].pop()
        commands['Fusoya'].append('#Omni')

    wackies = env.meta.get('wacky_challenge', [])
    if 'darts' in wackies:
        # Dart replaces Fight
        for cl in commands:
            commands[cl][0] = '#Dart'
        commands['Edge'].pop(0) # Edge already has Dart
        if env.options.flags.has('all_good_abilities'):
            # ... so, let's give him Bluff to fill in the gap
            commands['Edge'].append('#Bluff')
            # DKC also has Dart, so we sub in the thematic Sneak
            commands['DKCecil'].pop(0)
            commands['DKCecil'].append('#Sneak')
    elif 'musical' in wackies:
        # Sing replaces Fight
        for cl in commands:
            commands[cl][0] = '#Sing'
        if not (env.options.flags.has('all_good_abilities')) or env.options.flags.has_any('edwardsing', 'edwardsing_better'):
            commands['Edward'].pop(0) # Edward already has Sing
            if env.options.flags.has('all_good_abilities'):
                # ... so, let's give him Aim if he already has Heal, and Cry otherwise
                if env.options.flags.has('edwardheal'):
                    commands['Edward'].append('#Aim')
                else:
                    commands['Edward'].append('#Cry')
    elif 'kleptomania' in wackies:
        # Sneak is added to all command lists, usually at the bottom (except Edge)
        # various less-useful-ish commands are removed to make space
        for cl in commands:
            if cl != 'Edge':
                commands[cl].append('#Sneak')
        commands['CRydia'].remove('#White')
        if env.options.flags.has('kainmagic'):
            commands['Kain1'].remove('#Black')
        elif len(commands['Kain1']) > 4:
            # in this case, Kain already has Sneak due to all_good_abilities
            commands['Kain1'].pop()
        if env.options.flags.has('add_spells_fusoya'):
            commands['Fusoya'].remove('#Fight')
        if env.options.flags.has('rydiaredmage'):
            commands['ARydia'].remove('#White')
        if env.options.flags.has('japanese_abilities'):
            commands['Tellah1'].remove('#Recall')
            commands['Edward'].remove('#Medicine')
            commands['Rosa1'].remove('#Pray')
            commands['Yang1'].remove('#Fortify')
            commands['Palom'].remove('#Twin')
            commands['Porom'].remove('#Twin')
            if not env.options.flags.has('add_spells_fusoya'):
                commands['Fusoya'].remove('#Regen')
        elif env.options.flags.has('all_good_abilities'):
            commands['DKCecil'].remove('#Dart')
            commands['Tellah1'].remove('#Recall')
            # remove whichever of Heal/Aim Edward has
            commands['Edward'].pop(-2)
            # remove whichever of Pray/Cover Rosa has
            commands['Rosa1'].pop(-2)
            commands['Yang1'].remove('#Fortify')
            commands['Palom'].remove('#Twin')
            commands['Porom'].remove('#Twin')
            # remove whichever of Regen/Pray/Bluff post-Ordeals Tellah has
            commands['Tellah3'].pop(-2)
            # remove whichever of Bear/Power PCecil has
            commands['PCecil'].pop(-2)
            # remove Power if Cid has Raid, or Peer/Bear otherwise
            if env.options.flags.has('cidairship'):
                commands['Cid'].remove('#Focus')
            else:
                commands['Cid'].pop(-2)
            # remove White above if Rydia's kept her spells, Bluff otherwise
            if not env.options.flags.has('rydiaredmage'):
                commands['ARydia'].remove('#Bluff')
            # remove whichever of Regen/Bluff FuSoYa has
            if not env.options.flags.has('add_spells_fusoya'):
                commands['Fusoya'].pop(-2)

    if env.options.flags.has('rosapaladin'):
        # swap Rosa and PCecil's command lists; needs to happen last
        commands['Rosa1'], commands['PCecil'] = commands['PCecil'], commands['Rosa1']

    # add #Item at the end
    for cl in commands:
        commands[cl].append('#Item')

    if 'skillissue' in wackies:
        # need to find which abilities are in use, and then pass that to wacky_rando.py
        env.meta['available_abilities'] = set().union(*[set([ABILITIES_TO_HEX[c] for c in commands[cl]]) for cl in commands])

    # set up alternative command constants
    commands_script = []
    commands_script.extend([
        'consts(command)',
        '{',
        '    $15   Raid',
        '    $19   Omni',
        '}\n'
    ])

    for cl in commands:
        # build f4c scripts for each command script
        cl_script = [
            'actor(#' + cl + ')',
            '{',
            '    commands {',
        ]
        cl_script.extend(['        ' + c for c in commands[cl]])
        cl_script.extend(['    }', '}\n'])
        commands_script.extend(cl_script)
    
    #print('\n'.join(commands_script))
    env.add_script('\n'.join(commands_script))