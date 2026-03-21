from . import databases
from .address import *

def spell_data(env):
    spells_dbview = databases.get_spells_dbview()
    update_spells_dbview = databases.get_update_spells_dbview()

    # first, handle the changes to spell data from Cspells:anti, which is only cast time (in byte 0)
    if env.options.flags.has('antidale_spells_progression'):
        for update in update_spells_dbview:
            matching_spell = spells_dbview.find_one(lambda sp: sp.code == update.code)
            # update casting time/targeting data
            env.add_binary(
                BusAddress(0xF97A0 + (0x06 * matching_spell.code)),
                [(update.data[0])],
                as_script=True
            )

    # next, handle changes to MP costs arising from -tweak:harmspell/kainmagic,
    # -tweak:twinmeteo, and -tweak:chocobosummon (if 3point and misspelled 
    # don't already handle them)
    if '3point' not in env.meta.get('wacky_challenge', []):
        # W.Meteo is not Misspelled, so just give it 99 MP
        if env.options.flags.has('twinmeteo'):
            spell = spells_dbview.find_one(lambda sp: sp.code == 0x5E)
            env.add_binary(
                BusAddress(0xF97A5 + (0x06 * 0x5E)),
                [(spell.data[5] & 0x80) | 0x63],
                as_script=True
            )   

        if 'misspelled' not in env.meta.get('wacky_challenge', []):
            # set values for spell 0x17's MP cost/wall bit; 
            # it's 15 MP if it's actually Harm or Lance, and Lance ignores walls
            sight_mp = (0x0F if env.options.flags.has_any('kainmagic','harmspell') else 0x02)
            sight_hi_bit = (0x08 if env.options.flags.has('kainmagic') else 0x00)  

            if env.options.flags.has('bigchocobosummon'):
                env.add_binary(
                    BusAddress(0xF97A5 + (0x06 * 0x5F)),
                    [0x87],
                    as_script=True
                )        
            if env.options.flags.has_any('kainmagic','harmspell'):
                spell = spells_dbview.find_one(lambda sp: sp.code == 0x17)
                env.add_binary(
                    BusAddress(0xF97A5 + (0x06 * 0x17)),
                    [sight_hi_bit | sight_mp],
                    as_script=True
                )                    

def spellset_data(env):
    # collect all changes to all spellsets except for FuSoYa, 
    # and add one script for all changes

    # potential changes:
    #   Sight -> Harm with level change (-tweak:harmspell)
    #   Sight -> Lance (removed from non-Kain white spellsets) (-tweak:kainmagic)
    #   Add two spellsets for Kain (-tweak:kainmagic)
    #   Change Cecil's spellset to Black magic (-tweak:darkpaladin)
    #   Remove/Add Exit (-tweak:rosadin)
    #   Japanese spells (Cspells:j)
    #   Antidale's spell progression changes (Cspells:anti)
    
    # start with vanilla spellset data
    spellsets = {}
    spellsets['PCecil'] = { # $00
        '#Cure1' : 0,
        '#Sight' : 3,
        '#Peep'  : 8,
        '#Cure2' : 15,
        '#Exit'  : 19,
        '#Heal'  : 24
    }
    spellsets['KainBlack'] = {} # $01
    spellsets['RydiaWhite'] = { # $02
        '#Cure1' : 3,
        '#Sight' : 4,
        '#Hold'  : 7
    }
    spellsets['RydiaBlack'] = { # $03
        '#Ice1'  : 2,
        '#Lit1'  : 5,
        '#Sleep' : 8,
        '#Venom' : 10,
        '#Warp'  : 12,
        '#Toad'  : 13,
        '#Stop'  : 15,
        '#Piggy' : 20,
        '#Virus' : 26,
        '#Psych' : 31,
        '#Drain' : 35,
        '#Ice3'  : 38,
        '#Fire3' : 40,
        '#Lit3'  : 42,
        '#Quake' : 44,
        '#Stone' : 46,
        '#Weak'  : 48,
        '#Fatal' : 49,
        '#Nuke'  : 50,
        '#Meteo' : 56
    }
    spellsets['RydiaCall'] = { # $04
        '#Chocb' : 0
    }
    spellsets['TellahWhite'] = { # $05
        '#Cure2' : 0,
        '#Charm' : 0,
        '#Blink' : 0,
        '#Heal'  : 0,
        '#Life1' : 0,
        '#Exit'  : 0
    }
    spellsets['TellahBlack'] = { # $06
        '#Fire1' : 0,
        '#Ice1'  : 0,
        '#Lit1'  : 0,
        '#Stop'  : 0,
        '#Psych' : 0
    }
    spellsets['Rosa'] = { # $07
        '#Cure1' : 0,
        '#Hold'  : 0,
        '#Peep'  : 0,
        '#Slow'  : 0,
        '#Sight' : 0,
        '#Life1' : 11,
        '#Cure2' : 13,
        '#Mute'  : 15,
        '#Heal'  : 18,
        '#Bersk' : 20,
        '#Blink' : 23,
        '#Charm' : 24,
        '#Cure3' : 28,
        '#Size'  : 29,
        '#Fast'  : 30,
        '#Float' : 32,
        '#Wall'  : 34,
        '#Cure4' : 38,
        '#Life2' : 42,
        '#White' : 48
    }
    spellsets['Palom'] = { # $08
        '#Fire1' : 0,
        '#Ice1'  : 0,
        '#Lit1'  : 0,
        '#Sleep' : 0,
        '#Venom' : 0,
        '#Ice2'  : 11,
        '#Piggy' : 11,
        '#Fire2' : 12,
        '#Lit2'  : 13,
        '#Stop'  : 14,
        '#Virus' : 19,
        '#Toad'  : 22,
        '#Quake' : 23,
        '#Drain' : 26,
        '#Warp'  : 29,
        '#Ice3'  : 32,
        '#Fire3' : 33,
        '#Lit3'  : 34,
        '#Stone' : 36,
        '#Psych' : 40,
        '#Fatal' : 46,
        '#Weak'  : 48,
        '#Meteo' : 50,
        '#Nuke'  : 52
    }
    spellsets['Porom'] = { # $09
        '#Cure1' : 0,
        '#Hold'  : 0,
        '#Peep'  : 0,
        '#Slow'  : 0,
        '#Sight' : 0,
        '#Life1' : 11,
        '#Cure2' : 13,
        '#Mute'  : 15,
        '#Bersk' : 18,
        '#Exit'  : 19,
        '#Heal'  : 20,
        '#Blink' : 23,
        '#Charm' : 25,
        '#Size'  : 31,
        '#Cure3' : 33,
        '#Fast'  : 38,
        '#Float' : 40,
        '#Wall'  : 44,
        '#Cure4' : 48,
        '#White' : 52,
        '#Life2' : 56
    }
    # spellsets['FusoyaWhite'] = {...} # $0A
    # spellsets['FusoyaBlack'] = {...} # $0B
    spellsets['Edge'] = { # $0C
        '#Flame' : 0,
        '#Pin'   : 27,
        '#Smoke' : 33,
        '#Image' : 38
    }
    spellsets['KainWhite'] = {} # $0D
    # spellsets['FusoyaOmni'] = {...} # $0E

    if env.options.flags.has('japanese_spells'):
        # add in J-spells, update spell learn levels
        spellsets['RydiaBlack'].update({
            '#Psych' : 32,
            '#Drain' : 36,
            '#Ice3'  : 39,
            '#Fire3' : 42,
            '#Lit3'  : 45,
            '#Quake' : 47,
            '#Stone' : 49,
            '#Weak'  : 51,
            '#Fatal' : 52,
            '#Nuke'  : 55,
            '#Meteo' : 60
        })
        spellsets['Rosa'].update({
            '#Armor' : 12,
            '#Shell' : 29,
            '#Cure3' : 30,
            '#Size'  : 30,
            '#Dspel' : 31,
            '#Fast'  : 33,
            '#Float' : 35,
            '#Wall'  : 36,
            '#Life2' : 45,
            '#White' : 55
        })
        spellsets['Porom'].update({
            '#Armor' : 12,
            '#Shell' : 29,
            '#Dspel' : 31
        })
    elif env.options.flags.has('antidale_spells_progression'):
        # change spell learn levels
        spellsets['RydiaBlack'].update({
            '#Virus' : 24,
            '#Psych' : 29,
            '#Ice3'  : 30,
            '#Fire3' : 30,
            '#Lit3'  : 30,
            '#Drain' : 33,
            '#Stone' : 36,
            '#Quake' : 38,
            '#Fatal' : 42,
            '#Weak'  : 46,
            '#Nuke'  : 54
        })
        spellsets['TellahBlack'].update({
            '#Weak' : 33
        })
        spellsets['Rosa'].update({
            '#White' : 55
        })
        spellsets['Palom'].update({
            '#Ice3'  : 30,
            '#Fire3' : 30,
            '#Lit3'  : 30,
            '#Fatal' : 46,
            '#Weak'  : 48,
            '#Nuke' : 57
        })
        spellsets['Porom'].update({
            '#Blink' : 22,
            '#Charm' : 24,
            '#Size'  : 29,
            '#Cure3' : 30,
            '#Float' : 32,
            '#Fast'  : 34,
            '#Wall'  : 38,
            '#Cure4' : 40,
            '#Life2' : 46,
            '#White' : 57
        })

    if env.options.flags.has('rosapaladin'):
        # Remove Exit from Cecil's spellset
        # and give it to Rosa's, since those are swapped
        # Also update Sight/Peep to be pre-learned by Rosa,
        # since she starts at a level beyond where Cecil would learn them,
        # and update the non-Cure1 initial spells so that Cecil gradually learns them
        spellsets['PCecil'].pop('#Exit')
        spellsets['PCecil'].update({
            '#Sight' : 0,
            '#Peep'  : 0,
        })
        spellsets['Rosa'].update({
            '#Sight' : 3,
            '#Hold'  : 7,
            '#Peep'  : 8,
            '#Slow'  : 10,
            '#Exit'  : 19
        })
        if env.options.flags.has('antidale_spells_progression'):
            spellsets['Rosa'].update({
                '#White' : 56
            })
    elif env.options.flags.has('darkpaladin'):
        # Change PCecil's spellset to a black magic set
        spellsets['PCecil'].clear()
        spellsets['PCecil'].update({
            '#Venom' : 0,
            '#Sleep' : 3,
            '#Piggy' : 5,
            '#Drain' : 8,
            '#Psych' : 12,
            '#Toad'  : 15,
            '#Warp'  : 19,
            '#Stop'  : 22,
            '#Virus' : 25,
            '#Weak'  : 33,
            '#Fatal' : 37,
            '#Nuke'  : 40
        })
        if env.options.flags.has('antidale_spells_progression'):
            spellsets['PCecil'].update({
                '#Weak'  : 38,
                '#Fatal' : 45,
                '#Nuke'  : 57
            })
    rosa_exit_replacement = env.meta['zot_spell']
    if not env.options.flags.has('rosapaladin') and rosa_exit_replacement != '#Exit':
        # swap #Exit into the replacement spell's level-up slot
        # if Rosa is learning something else
        spellsets['Rosa'].update({
            '#Exit'  : spellsets['Rosa'][rosa_exit_replacement]
        })
        spellsets['Rosa'].pop(rosa_exit_replacement)

    if env.options.flags.has('harmspell'):
        # move '#Sight' (i.e. '#Harm') to be learned via level-up
        # removing #Sight and adding #Harm to be very clear
        if not env.options.flags.has('darkpaladin'):
            spellsets['PCecil'].pop('#Sight')
            spellsets['PCecil'].update({
                '#Harm' : 17
            })
        spellsets['RydiaWhite'].pop('#Sight')
        spellsets['Rosa'].pop('#Sight')
        spellsets['Rosa'].update({
            '#Harm' : 14
        })
        spellsets['Porom'].pop('#Sight')
        spellsets['Porom'].update({
            '#Harm' : 14
        })
    elif env.options.flags.has('kainmagic'):
        # remove #Sight, give Kain #Lance and filled out spellsets
        spellsets['PCecil'].pop('#Sight')
        spellsets['RydiaWhite'].pop('#Sight')
        spellsets['Rosa'].pop('#Sight')
        spellsets['Porom'].pop('#Sight')
        spellsets['KainBlack'].update({
            '#Fire2' : 0,
            '#Ice2'  : 0,
            '#Lit2'  : 0,
            '#Weak'  : 25
        })
        spellsets['KainWhite'].update({
            '#Cure2' : 0,
            '#Heal'  : 0,
            '#Lance' : 0,
            '#Blink' : 15,
            '#Bersk' : 17,
            '#White' : 30
        })
        if env.options.flags.has('antidale_spells_progression'):
            spellsets['KainBlack'].update({
                '#Weak'  : 38
            })            
            spellsets['KainWhite'].update({
                '#White' : 56
            })      

    if env.options.flags.has('call_level_up'):
        spellsets['RydiaCall'].update({
            '#spell.Imp'   : 3,
            '#spell.Bomb'  : 10,
            '#spell.Mage'  : 15,
            '#spell.Odin'  : 23,
            '#spell.Sylph' : 27,
            '#spell.Shiva' : 28,
            '#spell.Jinn'  : 29,
            '#spell.Indra' : 30,
            '#spell.Titan' : 32,
            '#spell.Mist'  : 34,
            '#spell.Asura' : 39,
            '#spell.Levia' : 46,
            '#spell.Baham' : 53,
        })
        if env.options.flags.has('japanese_spells'):
            spellsets['RydiaCall'].update({
                '#spell.Cocka' : 21,
                '#spell.Levia' : 49,
                '#spell.Baham' : 57,
            })
        elif env.options.flags.has('antidale_spells_progression'):
            spellsets['RydiaCall'].update({
            '#spell.Shiva' : 26,
            '#spell.Jinn'  : 26,
            '#spell.Indra' : 26,
            })            
    elif env.options.flags.has('call_start_all'):
        spellsets['RydiaCall'].update({
            '#spell.Imp'   : 0,
            '#spell.Bomb'  : 0,
            '#spell.Mage'  : 0,
            '#spell.Odin'  : 0,
            '#spell.Sylph' : 0,
            '#spell.Shiva' : 0,
            '#spell.Jinn'  : 0,
            '#spell.Indra' : 0,
            '#spell.Titan' : 0,
            '#spell.Mist'  : 0,
            '#spell.Asura' : 0,
            '#spell.Levia' : 0,
            '#spell.Baham' : 0,
        })       
        if env.options.flags.has('japanese_spells'):
            spellsets['RydiaCall'].update({
                '#spell.Cocka' : 0,
            })

    spells_script = []
    # set up spell name consts for #Lance and #Harm
    spells_script.extend([
        'consts(spell) {',
        '    $17    Harm',
        '    $17    Lance',
        '}\n'
    ])
    # set up spellset name consts for #KainBlack and #KainWhite
    spells_script.extend([
        'consts(spellset) {',
        '    $01    KainBlack',
        '    $0d    KainWhite',
        '}\n'
    ])

    for spellset in spellsets:
        # build f4c script for each 
        initial_spells = ['    initial {']
        learned_spells = ['    learned {']
        for sp in spellsets[spellset]:
            if not spellsets[spellset][sp]:
                initial_spells.append('         ' + sp)
            else:
                learned_spells.append('         ' + f'{spellsets[spellset][sp]}' + '  ' + sp)
        initial_spells.append('    }')
        learned_spells.append('    }')
        spset_script = [
            'spellset(#' + spellset + ') {',
        ]
        spset_script.extend(initial_spells)
        spset_script.extend(learned_spells)
        spset_script.append('}\n')
        spells_script.extend(spset_script)

    #print('\n'.join(spells_script))
    env.add_script('\n'.join(spells_script))
    
