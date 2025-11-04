def command_lists(env):
    # updates command lists based on flags
    # situations to care about:
    # -- command changes wackies (Darts, Musical, Klepto)
    # -- j-abilities
    # -- added abilities from e.g. -tweak flags, -fusoya:omnimage
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

    if env.options.flags.has('cidairship'):
        # give Cid his Raid command
        commands['Cid'].append('#Raid')

    if env.options.flags.has('kainmagic'):
        # give Kain White and Black commands
        commands['Kain1'].extend(['#White', '#Black'])

    if env.options.flags.has('add_spells_fusoya'):
        # replace Regen with Omni if necessary, or just add it
        # doing some funky indexing in case this ability gets moved
        if '#Regen' in commands['Fusoya']:
            commands['Fusoya'][commands['Fusoya'].index('#Regen')] = '#Omni'
        else:
            commands['Fusoya'].append('#Omni')

    wackies = env.meta.get('wacky_challenge', [])
    if 'darts' in wackies:
        # Dart replaces Fight
        for cl in commands:
            commands[cl][0] = '#Dart'
        commands['Edge'].pop(0) # Edge already has Dart
    elif 'musical' in wackies:
        # Sing replaces Fight
        for cl in commands:
            commands[cl][0] = '#Sing'
        commands['Edward'].pop(0) # Edward already has Sing
    elif 'kleptomania' in wackies:
        # Sneak is added to all command lists, usually at the bottom (except Edge)
        # various less-useful-ish commands are removed to make space
        for cl in commands:
            if cl != 'Edge':
                commands[cl].append('#Sneak')
        commands['CRydia'].remove('#White')
        if env.options.flags.has('kainmagic'):
            commands['Kain1'].remove('#Black')
        if env.options.flags.has('add_spells_fusoya'):
            commands['Fusoya'].remove('#Fight')        
        if env.options.flags.has('japanese_abilities'):
            commands['Tellah1'].remove('#Recall')
            commands['Edward'].remove('#Medicine')
            commands['Rosa1'].remove('#Pray')
            commands['Yang1'].remove('#Fortify')
            commands['Palom'].remove('#Twin')
            commands['Porom'].remove('#Twin')
            if not env.options.flags.has('add_spells_fusoya'):
                commands['Fusoya'].remove('#Regen')

    if env.options.flags.has('rosapaladin'):
        # swap Rosa and PCecil's command lists; needs to happen last
        commands['Rosa1'], commands['PCecil'] = commands['PCecil'], commands['Rosa1']

    # add #Item at the end
    for cl in commands:
        commands[cl].append('#Item')

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
    
    env.add_script('\n'.join(commands_script))