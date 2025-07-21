# Free Enterprise 4 All: The Bad Ideas Fork

This fork of [the v4.6.0 FE repository](https://github.com/HungryTenor/FreeEnterprise4) is intended to collect a variety of contributions from community members into one fork, providing players the options for... Bad Ideas.

This page lists out, in some detail, the new/non-vanilla flags offered by the fork, arranged roughly by where they are on the generator page. Each description will credit the flag creator/designer (possibly multiple people) and point to the main point(s) in the repository codebase where the flag is implemented.

[TOC]

## Objective Flags

### `Omode:bosscollector[N]` {: .h6 }

- Idea: sgrunt
- Design/Programming: Galeswift
- Locations: objective_rando.py, flagsetcore.py, objectives.f4c, eventextensions_randomizer.f4c

This flag requires you to defeat some number of bosses to complete the objective (independent of any boss hunt objectives).

### `Omode:goldhunter[N]` {: .h6 }

- Idea: Galeswift
- Design/Programming: Galeswift:
- Locations: goldhunt.f4c, objective_rando.py, eventextensions(_if, _misc).f4c, objectives.f4c 

This flag requires you to turn in a certain amount of GP to Tory in Agart to complete the objective. You lose the GP afterwards. 

### `Omode:dkmatter[N]` {: .h6 }

- Idea: b0ardface, sgrunt
- Design/Programming: sgrunt
- Locations: objective_rando.py, dark_matter_hunt.f4c

Vanilla FE requires you to obtain 30 DkMatters out of 45; this flag expansion by sgrunt allows you to configure the number of required DkMatters in multiples of 5.

### `Omode:ki[N]`

- Idea: sgrunt
- Design/Programming: sgrunt
- Locations: bank00_extensions.f4c, rewards.f4c, objective_rando.py 

This flag requires you to obtain a certain number of key items to complete the objective. `Omode:ki17` is incompatible with `Owin:crystal`, of course. 

### `Omode:external` {: .h6 }

- Idea: warlink05
- Design/Programming: ScytheMarshall
- Locations: objective_rando.py, external_objective.f4c

An objective that is completed upon the usage of the EagleEye item (instead of it casting Sight), which is given to you at the start of the seed and is impossible to lose. This objective is intended for handling "external" objectives, meaning things like bingo cards, meta objectives, and so on.

### `Orandom[N]` {: .h6 }

- Idea: Galeswift (but probably others)
- Design/Programming: Galeswift
- Locations: uispec.txt, objective_rando.py

Up to three "buckets" of randomized objectives are now available, allowing individual configuration of each bucket.

### `Orandom:only[char]` {: .h6 }

- Idea: Galeswift
- Design/Programming: Galeswift
- Locations: uispec.txt, objective_rando.py

Random character quests for objectives can now be specified to only be for certain characters.

### `Ogated:[N]` {: .h6 }

- Idea: Galeswift
- Design/Programming: Galeswift
- Locations: eventextensions_if.f4c, objectives.f4c, rewards.f4c, objective_rando.py, core_rando.py, tracker.f4c, rosas_mom_hints.f4c

This flag allows some tiering of objectives. A gated objective means that you will only get the reward needed for completion of that objective upon completion of all other required objectives. For example, if you set "Complete the Tower of Zot" as a gated objective, you will be granted the Earth Crystal automatically upon completion of the other objectives.

### `Ohardreq:[N]` {: .h6 }

- Idea: Antidale (but probably others)
- Design/Programming: Galeswift
- Locations: objectives.f4c, tracker.f4c, objective_rando.py

This flag forces you to complete certain objectives to complete the seed. For example, if you require 4 out of 5 objectives, and 1 hard required, the hard objective must be included as part of the 4; if you complete the other 4 objectives, you will not obtain the objective reward until you complete the hard required objective.

## Key Item Flags

### `Knofree[dwarf,package]` {: .h6 }

- Idea: sgrunt (probably others)
- Design/Programming: sgrunt
- Locations: 

### `Kmiab:[standard,all,above,below,lst]` {: .h6 }

- Idea: various (including Skarcerer, ScytheMarshall)
- Design/Programming: ScytheMarshall
- Locations: core_rando.py

The v4.6.0 `Kmiab` flag includes all of the non-LST miabs in the key item pool, or all miabs if `Kmoon` or `Kunsafe` is on. Now, there are three subgroups of miabs: "above-ground" (Zot, Eblan, Hook route, Lunar Path, Giant), "below-ground" (Feymarch, Sylph Cave, Lower Bab-il), and the LST miabs. These subgroups can be specified separately, the vanilla `Kmiab` behaviour with safety checks can be selected using `Kmiab:standard`, and all miabs (ignoring the safety checks, so the pre-v.4.6.0 behaviour) can be selected using Kmiab:all or just specifying all three subgroups. 

### `Kforge` {: .h6 }

- Idea: sgrunt (but probably others, and b0ardface for the original "Forge the Crystal")
- Design/Programming: sgrunt
- Locations: custom_weapon_rando.py, core_rando.py

This flag adds Kokkol's forge item to the available key item slots. The vanilla Excalibur is added to the key item rewards pool, just like v4.6.0 `Omode:classicforge` does. This setting overrides any supersmith reward.

### `Kpink` {: .h6 }

- Idea: sgrunt (but probably others)
- Design/Programming: sgrunt
- Locations: core_rando.py

This flag adds the Pink Tail trade reward to the available key item slots. The vanilla Adamant armor is added to the key item rewards pool, unless Adamants have been removed via `-noadamants`. 

### `Kunsafer` {: .h6 }

- Idea: Milkode (but probably others)
- Design/Programming: sgrunt
- Locations: core_rando.py

Under this flag, you will be _required_ to obtain moon access prior to obtaining underground access, meaning you will find your underground access somewhere accessible using the Darkness crystal (either on the moon somewhere or via the Giant).

### `Klatedark`, `Kunreliabledark` {: .h6 }

- Idea: sgrunt, Antidale
- Design/Programming: sgrunt (for `Klatedark`), Antidale, ScytheMarshall (for `Kunreliabledark`)
- Locations: core_rando.py

The `Klatedark` flag forces the Darkness crystal to be gated by underground access, meaning you will find it somewhere beyond the Magma Key or the Hook. The `Kunreliabledark` flag implements Antidale's weighting suggestion that Darkness should be gated by underground access about 66% of the time on the usual flagsets as long as `Kunsafe/r` is not on, which amounts to forcing it to be gated 25% of the time.

### `Kstart:[item]` {: .h6 }

- Idea: various
- Design/Programming: sgrunt, Galeswift, ScytheMarshall (for `Kstart:zonk`)
- Locations: core_rando.py, flagsetcore.py

The starting key item check will be the item specified in the flag, or a non-key-item in the case of `Kstart:zonk`. This flag is incompatible with `Kvanilla`, for obvious reasons.

When operating with minimal key item checks, `Kstart:zonk` will take priority over placing the Spoon and/or the Pink Tail at the starting slot, and therefore can remove one (or both!) of those items from the game. This situation will often occur when the Pass and the Crystal are both in the key item pool (e.g. on `Onone Pkey`). On `Tvanilla` or `Tshuffle`, you may get literally nothing (like the Baron Castle check does on `Kvanilla Pnone`) or a Cure1 in a random MIAB if the Spoon or Pink Tail cannot be placed in the starting slot.

### `Kunweighted` {: .h6 }

- Idea: various (including CoffeeAndChocobos, ScytheMarshall)
- Design/Programming: ScytheMarshall
- Locations: core_rando.py

FE normally has a weighted Key Item placement algorithm, that prioritizes `Kmain` checks over every other check; basically only half (or a few more) of the flags-possible `Ksummon`/`Kmoon` checks actually get added to the slots to which key items are assigned, and similarly for each area with monster boxes under Kmiab, where the first two are added and then maybe more, randomly. This flag removes that weighting, so that every check has the same chance of having a key item. 

## Character Flags

### `Cthrift[n]` {: .h6 }

- Idea: FirebirdLover
- Design/Progamming: ScytheMarshall
- Locations: character_rando.py

Under `Cthrift[n]`, where `n` can be from 2 to 5, characters will start with a full set of gear: one of each armour piece, a primary-hand weapon, and either a shield (for characters that get them who are not getting a two-handed weapon), a second weapon (for Yang/Edge), or nothing in their off-hand. The gear is selected from items with tier at most `n`. Cursed Rings are excluded, for balance/softlock-avoidance/flagset-design reasons. 

### `Cspells:[j,anti]` {: .h6}

- Idea: Antidale
- Design/Programming: Antidale (with some tweaks by ScytheMarshall)
- Locations: reordered_spells.f4c, update_spells.py, updated_spells.csvdb, fusoya_rando.py, mtordeals.f4c

These flags modify the flag name for enabling the J spells list, which changes from `Cj:spells` to `Cspells:j`, and add a new spells list modification. The syntax change is to make it clearer that there are now two different ways that spells can change from the vanilla US lists and properties. `Cspells:j` has not changed at all, while `Cspells:anti` has a goal of improving the mid-game of most mages, while also delaying their ultimate damaging spells. It aims to achieve this by speeding up the cast times of the elemental spells, and also generally lowering the level that mages learn spells in the mid-game, and pushing learning Nuke and White to somewhere around 1,300,000 experience for the four characters who learn it via levels. In addition, FuSoYa and Tellah will now learn Weak by level-up, not by the usual method; that happens for FuSoYa at level 53 and for Tellah at level 33. The other details of the changes are as follows:

Rosa
:   White 48 -> 55

Porom
:   Blink 23 -> 22
:   Charm 25 -> 24
:   Size 31 -> 29
:   Cure3 33 -> 30
:   Float 40 -> 32
:   Fast 38 -> 34
:   Wall 44 -> 38
:   Cure4 48 -> 40
:   Life2 56 -> 46
:   White 52 -> 57

Rydia
:   Virus 26 -> 24
:   Psych 32 -> 29
:   Ice3 38 -> 30
:   Fire3 40 -> 30
:   Lit3 42 -> 30
:   Drain 35 -> 33
:   Stone 46 -> 36
:   Quake 44 -> 38
:   Fatal 49 -> 42
:   Weak 48 -> 46
:   Nuke 50 -> 54
:   Meteo 60 -> 56

Palom
:   Ice3 32 -> 30
:   Fire3 33 -> 30
:   Lit3 34 -> 30
:   Fatal 46 -> 42
:   Weak 48 -> 44
:   Nuke 52 -> 57

Tier 1 spells are now instant cast (previously ATB Delay of 2), tier 2 have an ATB delay of 2 (previously 6), and tier 3 have an ATB delay of 4 (previously 8).

### `Cmostlydead`, `Cbrieflydead` {: .h6 }

- Idea: warlink05
- Design/Programming: ScytheMarshall
- Locations: swoon_to_wishes.f4c, post_battle.f4c, rewards.f4c, character_rando.py

These new "permadeath" options allow for characters to leave your party when they end a battle swooned without being inaccessible for the rest of the game. Under `Cbrieflydead`, a swooned character will simply be available in the Tower of Wishes after they leave the party, with their equipment and stats as-is (including still being swooned when you pick them up). Under `Cmostlydead`, a swooned character will be sent to the Tower of Wishes and be _reinitialized_, to base level and equipment. 

Under `Cbye`, both options operate as the usual permadeath. When a character's equipment would be otherwise inaccessible, the Legend Sword (if equipped) will be forcibly placed into your inventory.

### `Csuperhero` {: .h6 }

- Idea: Jokermage
- Design/Programming: Galeswift
- Locations: eventextensions_misc.f4c, rewards.f4c, zot_top.f4c, places where the hero challenge is checked for

This flag acts the same as `Chero`, except that your starting character will obtain incredible stat boosts (+50 to each of the five stats) until finding the Earth crystal (their one weakness). After returning the crystal to the boss at the top of Zot, the character gains their stat boosts back.

### `Cnopartner` {: .h6 }

- Idea: Guerin
- Design/Programming: Galeswift
- Locations: character_rando.py, opening.f4c

The starting partner character (who meets your starting/pre-game screen character in the opening cutscene) will not join your party, nor will be in the Tower of Wishes.

### `Ctreasure:[free,earned,relaxed,unsafe]` {: .h6 }

- Idea: Galeswift (but potentially others)
- Design/Programming: Galeswift
- Locations: core_rando.py, character_rando.py, rewards.f4c, treasure_rando.py

These flags take characters from the usual axtor reward slots and place them into treasure chests. `Ctreasure:free/earned` are linked to `Cnofree/noearned`, so free characters are placed in boxes separately from earned characters. Restricted characters will be found in MIABs, which doesn't normally do anything on `Ctreasure:free` unless you force the generator to roll `Crelaxed/restrict:[chars]/nofree/treasure:free` (which is not normally possible with just the UI on the generator page).

Free characters will normally all be placed in treasures in the overworld only. Under `Ctreasure:unsafe`, they can go anywhere. Under `Ctreasure:relaxed`, restricted charaacters will be placed in non-MIAB boxes as well.

!!! info "Linked Flags"
    In order to enable any of the `Ctreasure` flags, you must select treasure settings that randomize chest contents. The flag validation will remove your `Ctreasure` flags when any of `Tvanilla`, `Tshuffle`, and `Tempty` are set.

    * Enabling `Ctreasure:free` enables `C:nofree`.
    * Enabling `Ctreasure:earned` enables `C:noearned`. Unlike the main site, character sprites at overworld locations are not replaced by piggy sprites.
    * Enabling either `Ctreasure:unsafe` or `Ctreasure:relaxed` will enable both `Ctreasure:free` and `Ctreasure:earned`, if neither `Ctreasure:free` nor `Ctreasure:earned` are explicitly set.


### `Chi` {: .h6 }

- Idea: Galeswift
- Design/Programming: Galeswift
- Locations: character_expansion.f4c, join_full_party_menu.f4c

Under this flag, new characters are required to join the party, even if your party is full. This flag cannot be set under `Chero/party:1`. 

### `Cfifo` {: .h6 }

- Idea: FirebirdLover
- Design/Programming: Galeswift
- Locations: join_full_party_menu.f4c

Under this flag, when you are dismissing a character, you must dismiss the character that has been in your party the longest, excluding the hero character if there is one.

### `Cpaladin` {: .h6 }

- Idea: various, probably
- Design/Programming: Galeswift, ScytheMarshall (pre-game sprites and bugfixes)
- Locations: mtordeals.f4c, character_rando.py, paladin_start_sprite.f4c, opening.f4c, pregame_screen.f4c, generator.py, standing_characters_paladin.bin

Cecil starts as a paladin on this flag, at the same stats as he normally would after his class change. Ordeals is still available as a key item check/etc. as usual and will restore Tellah's spells. Multiple files are changed in order to handle the class change, or lack thereof, under `Csuperhero`.

## Treasure Flags

Courtesy of Antidale, the `Tpro` weights have been modified slightly, to reduce the chance of the lowest tiers in some areas and up the chance of the highest tier(s). The list of changes is as follows.

Baron Town
:   from: 40,20,20,18,2,0,0,0 
:   to:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;35,22,20,18,5,0,0,0

Damcyan
:   from: 40,20,20,18,2,0,0,0 
:   to:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;35,22,20,18,5,0,0,0

Village Mist
:   from: 20,30,30,18,2,0,0,0 
:   to:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;17,30,30,18,5,0,0,0

Bahamut Cave
:   from: 20,30,30,18,2,0,0,0 
:   to:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0,10,25,30,20,10,5,0

Lunar Path
:   from: 8,12,30,30,18,2,0,0 
:   to:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0,10,30,30,20,10,0,0

Waterfall
:   from: 0,0,35,40,23,2,0,0 
:   to:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0,0,0,50,28,17,5,0

Mist Cave
:   from: 0,0,35,40,23,2,0,0 
:   to:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0,0,35,40,20,5,0,0

Tomra
:   from: 10,20,40,28,2,0,0,0 
:   to:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;5,15,40,28,7,5,0,0

Giant (MIAB)
:   from: 0,0,0,0,30,35,35,0 
:   to:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0,0,0,0,25,35,35,5

### `Tsparsey:[underground,moon,overworld]` {: .h6 }

- Idea: Galeswift
- Design/Programming: Galeswift
- Locations: treasure_rando.py, flagsetcore.py

This flag restricts the `Tsparse` settings to only the chosen areas. Cave Eblana and Upper Bab-il count as the underworld for the purposes of this flag, and the Giant counts as the moon.

### `Tunrestrict:[treasury,moon,underworld,overworld]` {: .h6 }

- Idea: Galeswift (potentially others)
- Design/Programming: Galeswift
- Locations: treasure_rando.py

This flag causes the specified areas to ignore the restrictions imposed on non-MIAB chests by `Tmaxtier` and `Tmintier`. 

### `Tstandardish` {: .h6 }

- Idea: Antidale
- Design/Programming: Antidale
- Locations: treasure_rando.py, core_rando.py, util.py

Under `Tstandardish` you get boosted treasure tiers compared to `Tpro`, but the boosts are more targeted towards tier 5 and tier 6 treasures. The Last Arm miab can have tier 8, unlike on `Tpro`.

### `Tvanillaish` {: .h6 }

- Idea: sgrunt
- Design/Programming: sgrunt
- Locations: treasure_rando.py, core_rando.py, tvanillaish.csvdb

`Tvanillaish` is a weighted treasure distribution. The weights for non-MIAB chests in each area are given by the number of non-MIAB items of each tier in vanilla FF4 (the Japanese version, not the US version FF2). The weights for MIAB rewards in each area are given similarly, but for vanilla MIAB rewards in that area (meaning if there is only one MIAB reward, then then the reward for that MIAB will be exactly that tier). The weights for the three categories of quest rewards are the `Tpro` weights.

### `Tsemipro` {: .h6 }

- Idea: sgrunt
- Design/Programming: sgrunt
- Locations: treasure_rando.py, core_rando.py, util.py

`Tsemipro` is a weighted treasure distribution between `Tpro` and `Twildish`. Similarly to `Twildish`, it uses a matrix (found in util.py) to shift weight up to the next tier.

### `Tplayable` {: .h6 }

- Idea: gameboyf9 (creator of FF4PR's Falcon Dive)
- Design/Programming: ScytheMarshall
- Locations: treasure_rando.py, character_rando.py

Under this flag, all chests will contain items that at least one character available in the seed will be able to use. Under Omnidextrous, this flag does nothing. Under Fist Fight, the only weapons available are claws. This flag does not apply to KI check zonk rewards or MIABs. Summon orbs are consumables, so are treated like any other consumable item (so will appear even if Rydia doesn't; this choice is for tier restriction purposes).

With mystery flags, you can tell who the characters are in the seed by looking at the gear you get.

### `Tadjmiabareas` {: .h6 }

- Idea: ScytheMarshall
- Design/Programming: ScytheMarshall
- Locations: util.py, treasure_rando.py

This flag scales down weights for non-MIAB treasures in areas where there are MIABs, similarly to how `Twildish` scales up `Tpro` weights. The goal is to allow some fine-tuning of weighted treasure to make `-vanilla:miabs` a bit more balanced in the early game.

## Shop Flags

### `Ssingles` {: .h6 }

- Idea: Skarcerer (via jokes from #newbies-corner)
- Design/Programming: Galeswift
- Locations: shop_rando.py

Under `Ssingles`, each shop only sells a single item which can be different between the shops, but otherwise follow the standard randomization rules and safety checks (unless disabled).

### `Swildish` {: .h6 }

- Idea: Too many community members to count
- Design: ScytheMarshall/Xenocat823543 (this version)
- Programming: sgrunt
- Locations: shop_rando.py

This flag provides a higher-powered shops setting without the full randomness of `Swild`.

!!! info "`Swildish` Description"
    - Kokkol's shop contains tier 6-7 items/gear.
    - Gated shops are up to tier 6.
    - Ungated weapon/armor shops are up to tier 5.
    - Ungated item shops are up to tier 4.
    - Pick two of Siren, Coffin, HrGlass2, Bacchus, Elixir, and Levia; pick 1-2 of the damage "wild" items. Distribute these items to free shops.

### `Svanillaish` {: .h6 }

- Idea: sgrunt
- Design/Programming: sgrunt
- Locations: shop_rando.py

Under this flag, shops will contain items of similar quality and quantity as their vanilla counterparts. In particular, a shop will have exactly the same number of items in each tier as the vanilla game; the flag interacts with `Sno:j` by basing the quantities of each tier on the US version.

### `Ssame` {: .h6 }

- Idea: Galeswift
- Design/Programming: Galeswift
- Locations: shop_rando.py

Shops only sell a single item, where all shops in the game are the same. The item chosen uses the same rules as `Swild`.

### `Smixed:[shaken,stirred]` {: .h6 }

- Idea: Skarcerer, ScytheMarshall (for `stirred` only)
- Design/Programming: Galeswift, ScytheMarshall (for `stirred` only)
- Locations: compile_item_prices.py

This flag shuffles the prices of all of the items in the game (under `shaken`) or all of the normal buy/sellable items (under `stirred`). In particular, `Smixed:shaken` mixes in the prices of key items and non-items like no-weapon, no-armor, Sort, and the TrashCan, so some normal items will just be worth 0 GP. `Smixed:stirred` only shuffles the prices of items that you can normally possibly buy in shops on `Swild`.

Under `-wacky:mysteryjuice`, the 1000 GP prices will be shuffled into other items (rather than randomized prices being overwritten by 1000 GP). Under `Sprice:[n]/pricey:[]`, the price increase/decrease applies to the new shuffled price (in case only some items are more/less expensive).

### `Salways:[item]` {: .h6 }

- Idea: Galeswift (probably others)
- Design/Programming: Galeswift
- Locations: shop_rando.py

Each of the specified items will be in at least one shop somewhere, according to the usual restrictions.

### `Sno:[item]` {: .h6 }

- Idea: Galeswift (probably others)
- Design/Programming: Galeswift
- Locations: shop_rando.py

The `Sno:` family of flags has been expanded to include many other items and classes of items.

### `Sprice/pricey:[N]` {: .h6 }

- Idea: Galeswift
- Design/Programming: Galeswift
- Locations: compile_item_prices.py

These flags change the prices of the items specified by `Spricey`, which can be armor/weapons/items separately.

### `Splayable` {: .h6 }

- Idea: ScytheMarshall
- Design/Programming: ScytheMarshall
- Locations: shop_rando.py, character_rando.py

Similarly to `Tplayable`, this flag limits shop items to those usable to characters you can actually find in the seed, with the same exceptions.

## Boss Flags

For bosses with scripted stat changes in battle, instead of simply scaling the stat changes multiplicatively (which does not handle changes where one of the stats starts at zero), we now scale the original difference between the stats, and add to get the new scripted stat change. In this way we correct Valvalis having zero defense at the vanilla Zot 2 spot (even in tornado form) and Kainazzo not gaining defense at various spots. This change is not what v5.0 uses to handle vanilla Val; the scaling is unchanged, it's just that vanilla bosses don't have their stats changed (because the scaling to other bosses happens on the fly now).

### `Bstats:[j/et]` {: .h6 }

- Idea: harumph (probably others)
- Design: harumph, original FF4 devs
- Programming: ScytheMarshall, with some original work from harumph
- Locations: boss_rando.py, japanese_bosses.f4c, easy_type_bosses.f4c, zeromus_jscript.f4c, zeromus_etscript.f4c, boss_rando_formation_data.py (and _j, _et versions), zeromus_rando.py

These flags change all bosses, including Zeromus, to have stats and attack/reaction scripts based on the original Japanese version of FF4 or the Easy Type version (an "easier" version of the game for the Japanese audience based on the US version). Non-boss monsters are not changed, including any Alt Gauntlet monsters, excepting that Tricker and Red D are significantly faster in the J version, due to speed table changes.

The `-z` flags interact with these flags in the following ways: 

- Any time the original spell powers for Big Bangs are used, they will be the numbers found in the J/ET versions.
- Any "made-up" spell powers or similar are scaled up by 5/4 on the J version and down by 5/6 on the ET version.
- If Zeromus's original scripts show up, then they will be based on the J/ET versions.
- The ET version changes the HP threshold for Meteo phase regardless of `-z` flags.

### `Brestrict:[location]` {: .h6 }

- Idea: sgrunt (probably others)
- Design/Programming: sgrunt
- Locations: core_rando.py, objective_rando.py

This flag limits where objective bosses (and D.Mist, if `Knofree` is on) can appear.

### `Bitburns` {: .h6 }

- Idea: xPankraz
- Design/Programming: Galeswift (with advice from folks in the Discord thread)
- Locations: wyvern_rando.py

Like `Bwhichburn`, but the replacement attack will be _very_ unsafe, regardless of the `Bunsafe` flag.

!!! warn "`Bitburns` Options"
    The replacement attack will be one of:

    - MegaNuke
    - Big Bang
    - Zantetsuken/Odin
    - Meteo
    - Quake
    - Globe199 by row
    - Full party non-reflectable Charm/Glance
    - Magnet/Stop/Stone/Fatal/Gaze/Bluster by row

    If the boss slot has 40,000 HP or more (D.Lunars, Elements), then the attack could be one of:

    - Full-party Laser
    - Blizzard
    - Wave
    - Tornado

    If the boss slot has 127 spell power (CPU, Ogopogo), then the attack could be one of:

    - Heat Ray
    - Glare
    - White

### `Bflatvern` {: .h6 }

- Idea: ScytheMarshall
- Design/Programming: ScytheMarshall
- Locations: boss_rando.py

In vanilla FE (before v5.0), Wyvern's scripted spell power changes for the reflected Nukes and the counter MegaNuke did not get scaled, due to a typo in the code. That bug has been fixed in this fork, but this flag will restore the vanilla FE spell power for those attacks, to allow for the vanilla pre-v5.0 FE Wyvern experience.

### `Bwoahdin` {: .h6 }

- Idea: CoffeeAndChocobos
- Design/Programming: ScytheMarshall
- Locations: odin_replace_two_zantetsukens.f4c

In some other FF games, Odin has both the target-all instant death attack and a single-target damaging attack (usually "Gungnir"). Under this flag, Odin's script is changed so that the first two Odin attacks are replaced with a random single-target spell. Odin will also not raise the sword until the point where you can trigger the Thunderstruck script. 

### `Bwhybez/whichbez` {: .h6 }

- Idea: sgrunt (probably others)
- Design/Programming: sgrunt
- Locations: golbez_rando.py

Golbez's attack script will change similarly to Wyvern's script under `Bwhyburn` and `Bwhichburn`. `Bwhybez` removes the HoldGas/Shadow phase of the fight and proceeds directly to cycling the three spells (with a bit of comedy added in). `Bwhichbez` randomizes what Golbez's three spells are, as well as Shadow's three spells if `Bwhybez` is not on. 

Golbez's spells are single-target damaging spells (and Weak), and can be worse if `Bunsafe` is on. Shadow's spells are single-target status spells that incapacitate your characters.

!!! warning "Don't reflect Shadow's spells!"
    Some of Shadow's spells can be bounced off Wall... which sounds great, until you reflect Beak onto Golbez and softlock the fight because Beak bypasses the boss bit.

### `Bspellpower` {: .h6 }

- Idea: various (including Alchemie, ScytheMarshall)
- Design/Programming: ScytheMarshall
- Locations: boss_rando.py

Under `Bspellpower`, all bosses are treated as having at least 1 spell power. That means all bosses are assigned the spell power of the spot (or just 1 if the spot normally doesn't have spell power). This change removes the level-based scaling for spell power and allows some bosses (Antlion, KQ Eblan) to do more damage while nerfing some bosses going into low spell power slots. This change also impacts scripted stat changes (for Wyvern, so that the bounced Nukes also change in damage).

### `Bremove[officer_slot,kingqueen_slot]` {: .h6 }

- Idea: various (including Fleury, Inven)
- Design/Programming: ScytheMarshall
- Locations: boss_rando.py, kaipo_rydia.f4c, babil_rubicant.f4c

These flags will remove the specified boss slot from the game entirely. No objective bosses will be placed there, FuSoYa will not learn spells, etc.

## Encounter Flags

The default `E` flag is now `Etoggle`.

******* remember to get ap7's encounter shuffle flags?

### `Enogp` {: .h6 }

- Idea: sgrunt
- Design/Programming: sgrunt
- Locations: encounter_no_gp.f4c, encounter_rando.py

This flag removes GP from random encounters.

### `Enodmachin` {: .h6 }

- Idea: sgrunt (probably others)
- Design/Programming: sgrunt
- Locations: encounter_no_dmachin.f4c, encounter_rando.py

This flag replaces the D.Machin in the repeatable D.Machin grind encounter with a Horseman.

### `Enomacgiant` {: .h6 }

- Idea: various (including ScytheMarshall)
- Design/Programming: sgrunt, effectively (ScytheMarshall repurposed sgrunt's `Enodmachin` code)
- Locations: encounter_no_macgiant.f4c, encounter_rando.py

This flag replaces the MacGiant in the repeatable MacGiant grind encounter with a Machine.

### `Etable:[shuffle7,shuffle8,relocatedish,relocated,wildish,wild,chaos,uniquelygood]` {: .h6 }

- Idea: leggystarscream, ap7, ScytheMarshall, probably others
- Design: leggystarscream (`shuffle8`), ap7 (`shuffle7`, `wildish`, `wild`), ScytheMarshall (the rest)
- Programming: ScytheMarshall (for this implementation)
- Locations: encounter_rando.py

These flags change the encounter tables; namely, which encounters are in which group. The "map ID to group" association is left unchanged (because that is patched by the Something Worth Fighting For wacky flag). The `shuffle` flags only shuffle the encounters within each group. The `relocated` flags shuffle the groups around, within certain zones. The `wild` flags shuffle the encounters around with no regard for group, only for zones or map plane. The `chaos` flag randomly assigns valid encounters with no regard for ensuring encounters are still there. The `uniquelygood` flag chooses one encounter from each group to be the only encounter that group has; the encounter will be a grind fight, an otherwise useful encounter, or a notable fight, without repeating an encounter from another group (e.g. double King-Ryus are in multiple groups, they will only show up once here).

## Harp Flags

harumph, the leader of the #FadeHarp community, made some flags to change the TwinHarp behaviour. In vanilla FE, you will always get a randomized song instead of the vanilla Melody of Lute (Edward's theme) during the TwinHarp cutscene and subsequent fight. These flags change that behaviour.

### `Hrandom` {: .h6 }

- Idea: b0ardface
- Design/Programming: b0ardface, music by b0ardface, Calmlamity, Xenocat823543, and others
- Locations: midiharp.f4c, the compiled_songs folder, the harp tools in fetools 

This flag replicates vanilla FE behaviour (up to the songs available on this fork). The random song will never be Melody of Lute.

### `Hvanilla` {: .h6 }

- Idea: harumph
- Design/Programming: harumph, ScytheMarshall (this particular implementation)
- Locations: vanilla_harp.f4c

This flag forces Edward to play Melody of Lute. The song credits will still display.

### `Hnone` {: .h6 }

- Idea: harumph, others
- Design/Programming: harumph, ScytheMarshall (this particular implementation)
- Locations: no_harp.f4c

This flag forces Edward to play nothing. The track used is a "silence" audio track in the game's data.

## Other Flags

### `-doorsrando:[category]` {: .h6 }

- Idea: various
- Design/Programming: jayp12323, Wylem
- Locations: doors_rando.py, map_history_extension.f4c, doorsrando.f4c, generator.py

Most doors in the game are randomized, including entrances to field maps from overworld maps, within the given categories. The doors that aren't include connectors between floors of the same dungeon and every Training Room in the game. Dungeons which, in vanilla, chain into other dungeons have their "exits" also randomized, so Cave Eblana will exit out into a map that is probably not the normal connection to Upper Bab-il, and so on.

The doors in Baron Town that are locked by the Baron Key are now open by default; the Baron Key check is now placed in the water outside of Baron Castle, so you can still Push B to Jump past it but it will block your progression otherwise. 

Many return triggers have been reworked into teleport triggers, to prevent unusual behaviour. Be very careful to not follow chains forever, though, because the map stack will not appreciate it. Some teleports have been removed, for example the teleport in the Sylph Cave house and one of the teleports on the treasure floor of the Feymarch town.

The Tower Key is now a logical way underground, if you can access Lower Bab-il from the overworld. Sylph Cave MIABs can still be in Yang's room in Sylph Cave, even though the room is disconnected from the rest of Sylph.

### `-entrancesrando:[category]` {: .h6 }

- Idea: various
- Design/Programming: jayp12323, Wylem
- Locations: doors_rando.py, map_history_extension.f4c, doorsrando.f4c, generator.py

Entrances to field maps from the various overworld maps are randomized within the given categories; for example, under `all` the entrance to Baron Town might lead to Dwarf Castle and the entrance to Baron Castle might lead to Cave Bahamut. Doors within field maps, for example doors to buildings inside of towns or connectors to different parts of a dungeon, remain intact.

### `-calmness` {: .h6 }

- Idea: jayp12323
- Design/Programming: jayp12323
- Locations: doorsrando.f4c

When doors or entrances are randomized, pressing Select and R at the same time while you have movement control in a field map triggers an event that puts you on the Enterprise in the air above Mysidia, and if you have the Hovercraft and/or the Big Whale, they will also be warped to that peninsula. This maneuver is colloquially called the "Panic button".

This flag _removes_ the Select+R functionality.

### `-forcesealed` {: .h6 }

- Idea: rejakdylle
- Design/Programming: jayp12323
- Locations: doorsrando.f4c

Normally, with the Panic button you can simply warp out of Sealed Cave after picking up the item at the bottom without fighting the boss. This flag triggers the boss fight on the way into the crystal room, not out of it. You can, of course, still skip the fight on Push B to Jump.

### `-kit:atb` {: .h6 }

- Idea: ScytheMarshall
- Design/Programming: ScytheMarshall
- Locations: kit_rando.py

This kit gives 2-3 SilkWebs, 4-5 Hermes, 1 HrGlass1, and 3-4 Heals (since they reset the speed modifier).

### `-kit:adamant` {: .h6 }

- Idea: tons of folks
- Design/Programming: sgrunt
- Locations: kit_rando.py

This kit gives you an Adamant armor, regardless of `-noadamants`.

### `-kit:cursed` {: .h6 }

- Idea: also tons of folks
- Design/Programming: sgrunt
- Locations: kit_rando.py

This kit gives you a Cursed ring, regardless of `-nocursed`.

### `-kit:hero` {: .h6 }

- Idea: sgrunt
- Design/Programming: sgrunt
- Locations: kit_rando.py

This kit gives you one tier 4-5 weapon, body armor, headgear, and ring/gauntlet for your starting character. If the weapon is a bow, it will come with arrows; if the starting character is Edge or the Omnidextrous flag is enabled, there will also be a second weapon.

### `-kit:exit` {: .h6 }

- Idea: JudgeJoe, Fleury14
- Design/Programming: jayp12323
- Locations: kit_rando.py

This kit gives you 5-10 Exits.

### `-kit:egg` {: .h6 }

- Idea: ScytheMarshall, Deathlike, Skarcerer
- Design/Programming: ScytheMarshall
- Locations: kit_rando.py

This kit gives you one Siren and a selection of items that your starting character can use to successfully defeat a Yellow D egg. It's possible that resets are necessary or that the fights will be very long. Depending on the starting character, there may be many possible selections of items or only a few. The probability of a specific selection of items is smaller if the Yellow D fight will be long/etc. or if the items contribute to your party's power afterwards.

### `-monsterevade`, `-monsterflee` {: .h6 }

- Idea: ScytheMarshall (but also probably others)
- Design/Programming: ScytheMarshall (with help from Aexoden and the disassembly)
- Locations: give_monsters_evade.f4c, monster_flee.f4c

These flags restore functionality to monsters that the original devs removed before the game released. `-monsterevade` allows monsters to correctly load their physical and magical evade stats at the start of battle (instead of just when those stats change, like for Valvalis). Be warned: monsters will take a lot less damage, and will dodge Life pots/casts! `-monsterflee` builds on the evade functionality and restores the ability for monsters to flee from battle (which requires them to have non-zero evade). Monsters can flee from non-boss-bit battles.

### `-miscbugfixes` {: .h6 }

- Idea: ScytheMarshall, cassidy (for Hermes/Berserk)
- Design/Programming: ScytheMarshall, cassidy/Wylem (for Hermes/Berserk)
- Locations: fix_hermes_berserk.f4c, fix_victim_history.f4c, fix_wisdom_will_timers.f4c

This flag includes fixes for four vanilla FF4 bugs: 

- The Hermes/Berserk glitch, where if you use a Hermes and then berserk that character before they take another action, they can hit swooned chararcters (because the game checks the subcommand for "can this actor hit swooned actors with their command?" and Hermes has the same subcommand as a monster spell that's used in the Zeromus cutscene to revive your party). The fix is to first check if the actor's command is magic; if it is, then load the subcommand, and if it isn't, put `FF FF` into the (16-bit) accumulator instead (preventing the check from ever succeeding).
- The monster victim history bug, where multi-target spells do not update a monster's victim history except when the monster is in the lowest slot. The fix is to rewrite a loop in-place.
- The (Wisdom+Will)-based timer issue, where the code loads a garbage byte instead of the correct byte, causing Sap timers to be effectively random. The fix is to load the correct byte.
- The Will-based timer overflow issue, where the code does not multiply by 4 correctly (losing upper bits if the value is greater than 64). The fix is to write a better loop. This fix impacts Sleep/Paralyze/gradual petrification (only from the dummied-out Medusa Sword); in particular, some high-level monsters will not sleep way longer than intended, now.

### `-smith:playable` {: .h6 }

- Idea: various (perhaps mostly ScytheMarshall)
- Design/Programming: ScytheMarshall
- Locations: custom_weapon_rando.py

Under this flag, the forge item will be usable by one of the characters you can get in the seed, whether it's an FF4A weapon or a regular tier 7-8 item. This flag does nothing when it's just the vanilla Excalbur (and on `Omode:classicforge`) or if it would otherwise give nothing (only Yang and no j-items or Adamants). 

### `-smith:omni` {: .h6 }

- Idea: CoffeeAndChocobos
- Design/Programming: CoffeeAndChocobos, ScytheMarshall
- Locations: custom_weapon_rando.py, flagsetcore.py

This flag allows every character in the seed to equip the FF4A weapon, if there is one. It will not, however, also allow anyone who cannot equip bows or arrows to equip the other hand to use Rosa's weapons.

### `-starting:blackchocobo,underground` {: .h6 }

- Idea: Deathlike, Skarcerer, others in the past
- Design: Deathlike, Skarcerer, Marshal, ScytheMarshall, others
- Programming: ScytheMarshall
- Locations: opening_[blackchocobo/underground].f4c, guided_intro.f4c, core_rando.py, generator.py, doors_rando.py, doorsrando.f4c, panic_button.f4c, many area f4c files, randomizer_keyitems.f4c, eventextensions[_misc].f4c, tracker.f4c, treasure_rando.py

These flags provide alternate starting conditions for the seed: either starting without an airship but with Black Chocobos, or starting underground with the Falcon (without the Drill). Logic is included to ensure that not having the Enterprise does not softlock the seed, though no logic is included to ensure that your party can win any fights. Some cutscenes are modified to not give you the Enterprise afterwards if you do not have it, instead giving a different vehicle (or no vehicle). Baron Castle now gives the Enterprise. Mist does not get locked from the right side after the Package cutscene.

## FuSoYa Flags

- Idea: ScytheMarshall (except `-fusoya:slowstart`, `-fusoya:unlearn`, `-fusoya:omnimage`)
- Design/Programming: ScytheMarshall
- Locations: fusoya_rando.py, fusoya_challenge.f4c; some wacky f4c files where command menus change

These flags are intended to change how FuSoYa's spell-learning works, with the goal of making the character more balanced and less of an instant exclusion from "competitive" flagsets. 

### `-fusoya:vanilla` {: .h6 }

This flag is just the `-vanilla:fusoya` flag but renamed; Fu starts at full power with all spells learned.

### `-fusoya:sequential_p` {: .h6 }

Under this flag, FuSoYa learns spells in a fixed order: the order in which Porom and Palom learn their spells by level-up. If spells are learned at the same level, there is an arbitrary choice for which spells come first (mostly for minor balancing).

### `-fusoya:sequential_r` {: .h6 }

- Idea: Deathlike

Under this flag, FuSoYa learns spells in a fixed order: the order in which Rosa and Rydia learn their spells by level-up. If spells are learned at the same level, there is an arbitrary choice for which spells come first (mostly for minor balancing). Since Rosa and Rydia don't learn all of their spells by level-up (no Exit, Fire1, Fire/Ice/Lit2), FuSoYa will not learn the missing spells.

### `-fusoya:location` {: .h6 }

Under this flag, FuSoYa will learn three spells after every boss, but the spells learned depend on the boss location. Stronger/gated boss spots are weighted to provide more powerful spells.

Spells are broken into four tiers based on power/usefulness and boss spots are divided into eight tiers based on strength/out-of-the-way-ness. Each spell tier has a weighting for which boss spots spells can go; the stronger spells are weighted to go in the more powerful boss spots. Each spell is then assigned to a boss spot until all the spells are used up, and then it repeats, going until all the boss spots are assigned three spells (skipping spells that cannot be placed into a remaining boss spot due to weighting restrictions).

### `-fusoya:nerfed` {: .h6 }

FuSoYa will start with a fixed pool of 14 black magic and 14 white magic spells (17 with j-spells), mostly tier 2 and below, but will not learn any spells over the course of the game. He will still gain HP as usual. The spells chosen are the same as the spells that FuSoYa would start with on the old F1 FuSoYa challenge flag (where he would get the rest of his spells at Ordeals).

### `-fusoya:maybe` {: .h6 }

FuSoYa will not necessarily learn every spell. Each spell is independently kept with a probability of 85%. Vanilla and nerfed FuSoYa will have possibly fewer starting spells and other FuSoYas will learn fewer spells/learn some spells a bit earlier.

### `-fusoya:uncapped` {: .h6 }

FuSoYa will gain, or start with, up to 3900 HP (500 plus 100 HP for every boss in the seed). This flag interacts with `Bremove` and `-fusoya:omnimage` to lower the total HP threshold.

### `-fusoya:slowstart` {: h6 }

- Idea: Guerin

FuSoYa will skip learning spells and gaining HP after three of the first six and two of the next six boss fights. The boss fight numbers are random each seed. Fu will eventually learn all available spells, just five bosses later than usual.

### `-fusoya:randomhp` {: h6 }

FuSoYa will gain the same amount of HP in the same amount of levels, but will possibly not gain any HP after some bosses and more than 100 HP after some bosses. The HP gains will be integer multiples of 100. 

### `-fusoya:unlearn` {: h6 }

- Idea: Galeswift

FuSoYa will start with all possible spells and then lose spells after each boss fight until he's down to six spells. Spell loss happens in reverse order of the usual spell learning, so he will lose more powerful spells earlier; the exception is under `-fusoya:location`, where he loses the spells he would gain at those bosses (meaning he loses more powerful spells after more powerful boss spots).

### `-fusoya:omnimage` {: h6 }

- Idea: Guerin

FuSoYa is given a third spellset potentially containing every non-Black/White spell available to playable characters (except Lance if `-tweak:kainmagic` is on). These spells are included in the spell randomization and interact with the other flags.

## Agility Flags

- Idea: ScytheMarshall (except `-agility:random`, `-agility:750formula`, and `-speedmodbalance`)
- Design/Programming: ScytheMarshall (except for the above)
- Locations: agility.f4c (mostly)

These flags are for changing how the agility system works. Some flags choose different characters to be the anchor, some flags change how the anchor agility is chosen, and some flags scale the "base" ATB up or down. The speed modifier balance flag changes the range of the speed modifier and how much items will change it.

For agility flags that tend to increase the base ATB, the Count spell duration is lengthened to make it significantly more reasonable (otherwise back attack Plague is nearly impossible). 

### `-agility:vanilla` {: .h6 }

This flag is simply `-vanilla:agility` renamed (so your anchor will always be the Cecil in the earliest slot, or else the character in the earliest slot).

### `-agility:slowest` {: .h6 }

The character with the lowest agility stat is chosen as the anchor (including 0 Agility, which could potentially be advantageous).

### `-agility:fastest` {: .h6 }

The character with the largest agility stat is chosen as the anchor. This flag doubles the Count timer.

### `-agility:average` {: .h6 }

The average agility of your party (rounded down, of course) is the value used for anchoring. Empty slots do not count.

### `-agility:median` {: .h6 }

The median agility of your party (the agility stat in the middle, or the lower of the two in the middle for an even number of characters) is the value used for anchoring. Empty slots do not count.

### `-agility:random` {: .h6 }

- Idea: Found in rivers's dev ideas document

The anchor slot is randomly determined (like Afflicted, it is fixed for each formation); for that battle, the agility anchor is chosen by taking the first non-empty party slot starting at the randomly determined slot, cycling around to lower party slots if necessary.

### `-agility:monster` {: .h6 }

The average agility of the _monsters_ in the battle (including pre-swooned/hidden monsters) is the value used for anchoring. This flag is incredibly dangerous, because most later-game monsters are much faster than your party members.

### `-agility:flat` {: .h6 }

Every character and monster will have the same base ATB (5 ticks, unless scaled by another flag), regardless of their agility stat. 

### `-agility:750formula` {: .h6 }

- Idea: S3
- Design: S3
- Programming: S3 (and ScytheMarshall converted it to f4c code)
- Locations: agility.f4c

The agility formula is completely reworked to be dependent on the absolute speed stat instead of relative to an anchor. The base ATB is now (15 * 5 * 10) / (Agi + 32) ticks, where the 5 can be scaled up to 10 or down to 1 by another flag (the 750 in the flag name comes from the numerator). This flag will tend to increase the number of empty ticks/ticks between actions. This flag triples the Count timer.

### `-agility:anchor[7/27/28/41/42]` {: .h6 }

The specified value will be the agility value used for anchoring. The values are chosen to either let most characters at endgame level be RA1 (via 7), force Zeromus to be RA2 or RA3 (28, 42), or force Zeromus to be the worst possible RA1 or RA2 (27, 41). Other fights, especially at lower levels, may be very slow or difficult. The Count timer is doubled for 27/28 and tripled for 41/42.

### `-agility:scale[1/10]` {: .h6 }

This flag will scale the base ATB for the anchor up to 10 ticks or down to 1 tick (which also impacts flat agility and the 750formula agility). Battles will either feel very slow or very fast. Under 10 tick scaling, the Count timer is doubled.

### `-speedmodbalance` {: .h6 }

- Idea: S3
- Design/Programming: S3, ScytheMarshall
- Locations: speed_modifier.f4c

This flag changes the speed modifier range to be 8-32 (from 12-32). Slow now increases the speed modifier by 4 instead of 8, SilkWebs increase by 8 instead of 16, Fast decreases the speed modifier by 4 instead of 3, and Hermes is left alone because it already decreased by 8. S3's original idea had a range of 8-24.

## Experience Flags

- Idea: various (everyone in the relevant Discord thread!)
- Design/Programming: ScytheMarshall
- Locations: experience_acceleration.f4c, generator.py

These flags adjust the experience earned from battle, in ways different/similar to the pre-existing `-exp:` flags. As with those flags, all of the bonuses are multiplicative with each other, meaning if you slingshot a character with 10 KI while `-exp:crystalbonus` is on and you have the Crystal, then that character will receive 8 (2x2x2) times the usual experience. 

### `-exp:crystalbonus` {: .h6 }

Earn double experience after obtaining the Crystal.

### `-exp:objectivebonus[25/10/_num]` {: .h6 }

Earn extra experience based on how many objectives you have completed up until the end of the battle (not including any potential objectives you complete _after_ the battle ends). The options are 25% per objective (25), 10% per objective (10), and a percentage depending on the percentage of the available objectives you have completed (_num). For example, if there are 7 objectives in the seed and you complete 3 of them, then you will earn 42% bonus experience (no matter how many objectives you need to complete to get the objective completion reward). This flag is forced off if there are no objectives,

### `-exp:kicheckbonus[10/5/2/_num]` {: .h6 }

Earn extra experience based on how many key item checks you have completed up until the end of the battle (not including the potential check(s) the battle is for). The options are 10% (10), 5% (5), 2% (2), and a percentage depending on the percentage of available key item checks you have completed (_num), not counting the starting key item check. The number of key item checks depends on the `K` flags. If the seed has mystery flags, then every key item check is assumed to be available.

### `-exp:zonkbonus[10/5/2]` {: .h6 }

A "zonk" is when you get a non-key-item reward from a key item check. Under this flag, you earn extra experience based on the number of zonks you have had, not counting what happens with the starting key item. The options are 10% (10), 5% (5), and 2% (2) (no flag-dependent option, because on mystery flags you would be able to identify the `K` flag immediately). If a check cannot potentially reward a key item, then it does not count for the zonk count, unless the seed has mystery flags.

### `-exp:miabbonus[100/50]` {: .h6 }

Under this flag, MIAB encounters award double or 1.5 times the usual EXP.

### `-exp:moonbonus[200/100]` {: .h6 }

Under this flag, encounters on the moon (the surface, Cave Bahamut, or LST) award double or triple the usual EXP.

### `-exp:maxlevelbonus` {: .h6 }

Under this flag, if 5 plus twice the largest level in your party is less than the smallest monster level in the encounter, then the encounter awards 20% bonus EXP (and another 20% for each additional deficit of 5). For example, a pack of 3 Warlocks has smallest monster level 73, so if your largest level is 25 (base level Edge), then we compute 5 + 2*25 = 55, and take 73-55 = 18. 18 divided by 5 is 3.6, so there are 3 deficits of 5, so you would receive 3 * 20% = 60% bonus experience.

### `-exp:smallparty` {: .h6 }

Under this flag, encounters give more EXP when your party is not full. If you can have `N` characters and you don't, then you get `6-N` bonuses of 10%, which sums over `N` from 1 to the maximum party size. For example, if you have 2 characters but you could have 5, then you get 1+2+3 = 6 bonuses of 10% (with contributions from `N` being 5,4,3), for 60% total bonus EXP. 

Since the battle spoils function runs after permadeath/etc. occurs, any characters that leave your party do not count as being part of your party for the purposes of this calculation.

### `-exp:geometric[90/80/.../10/0]` {: .h6 }

In vanilla FF4, each instance of a monster type killed in battle gives the same amount of EXP; there are at most three monster types, and their exp gains get added up separately. (Meaning that the graphical position of the monster doesn't matter; e.g. if there are three Warlocks on screen, they are all just Warlocks, independent of "which" Warlocks they are.) Under this flag, each monster of the same type defeated in the same battle will yield a scaled amount of the EXP of the previous monster of that type, giving diminishing returns for repeated monster kills. Note that the reduction is per monster type and not per graphical position in battle (as above).

The options are multiples of 10 from 90 down to 0, resulting in 90% exp scaling, 80% scaling, etc., down to 0% scaling. Analysis of the geometric series `a(1+r+r^2+...)`, where `a` is the base exp for that monster type and `r` is the scale factor (the parameter divided by 100), shows that exp per monster type is bounded above by `a/(1-r)`, meaning that arbitrarily large grinds are now not possible. For examble, if `r` is 0.5, then at most you can get double the base experience from defeating monsters of a given type (e.g. in a D$ grind). Thus, life glitching is not as effective, and on 0% scaling is completely worthless. Moreover, on 0% scaling it is more effective to fight encounters where all of the monsters are different, since duplicate monsters do not give extra exp.

## PRNG Flags

- Idea: various, including ScytheMarshall and cassidy (for `-prng:random`)
- Design/Programming: ScytheMarshall
- Locations: generator.py

These flags change the PRNG table for the game (a table of 256 bytes from 0-255, shuffled).

### `-prng:shuffle` {: .h6 }

This flag provides a differently shuffled table of the bytes 0-255.

### `-prng:random` {: .h6 }

This flag independently randomizes each of the 256 bytes of the table, so that there is no guarantee that every number shows up and there are probably repeats. There is a safety check made to ensure that the table allows for every battle slot to be selected. Otherwise, the game will softlock in battle because it cannot choose a valid target.

### `-prng:consecutive` {: .h6 }

This flag replaces the table with the numbers 0-255 in ascending order.

### `-prng:mostlysingle` {: .h6 }

This flag replaces the PRNG table with one random integer chosen from 0 to 255. However, as a safety, 12 of the entries are replaced with 12 numbers near the random integer in order to allow every battle slot to be targettable. (Hence, "mostly single".) 

## Zeromus Flags

- Idea: various folks over the years, surely
- Design/Programming: ScytheMarshall (with many thanks to Wylem)
- Locations: zeromus_rando.py, zeromus_chaosscript.f4c, zeromus_mimicscript.f4c, zeromus_replacescript.f4c, fix_jump_retargeting.f4c, dark_wave_damage.f4c

These flags handle the randomization of Zeromus and the relevant battle scripts. The intent is to refresh the Zeromus fight experience, so that there's something new to experience at the end of the game.

There are four main script change flags: `-z:physical`, `-z:physmag`, `-z:chaos`, and `-z:lavosshell`. Within those flags are two other flags that modify the scripts: `-z:whichbang` and `-z:phaseshift`. Additional to those flags are flags that modify nerfing of Big Bang/similar attacks: `-z:nonerfs` and `-z:mustnerf`.

### `-z:physical` {: .h6 }

Replaces Big Bang and Meteo with Dark Wave, direct Virus with Needle-all, and direct Nuke with Jump. Yes, thanks to the Kain cutscene fight in vanilla, monsters can Jump. The counter attacks are changed so that Fight, Aim, Jump, and Dart are countered by Fight, Counter-all, a very strong Fight, and a very strong single-target Counter; the latter two do not nerf Dark Wave but the first two do. Zeromus's attack stats are set/changed so that damage is roughly equivalent to the vanilla damage, but since Dark Wave is unblockable, it's possibly much more dangerous.

It turns out that spells do not correctly retarget when the only monsters left in the battle are in the back row, so the game softlocks. Normally this isn't an issue, since monsters can't temporarily disappear from battle (and Cecil does not have spells in the cutscene fight), but since Zeromus is Jumping, we need to patch this behaviour.

### `-z:physmag` {: .h6 }

50% of the time, this flag does nothing. The other 50% of the time, Zeromus gets the physical scripting from `-z:physical`. The point of this flag is to introduce uncertainty as to what Zeromus is going to do.

### `-z:chaos` {: .h6 }

This flag replaces Zeromus's three main attack phases with three new phases consisting of 2-5 attacks (1-3 for the third phase), floor(n/2) of which are "shake" attacks (stronger target-all nerfable attacks preceded by a shake, just like Big Bang; no shakes in third phase), and at most two Black Holes potentially following some attacks. Each phase has at least one damaging move, so that you will eventually lose the battle if you do nothing. The counter attacks are chosen at random, though the triggers for those counters are unchanged.

The flag is named after Chaos, the final boss of FF1 and notorious casino simulator in speedruns.

### `-z:lavosshell` {: .h6 }

This flag replaces Zeromus's three main attack phases with three random scripts from other monsters (or their reactions), as long as those phases do not modify condition/reaction flags and do not automatically end the battle (among other things). These scripts will be able to defeat you if you do nothing. Some of these scripts are _significantly_ more dangerous than others.

The flag is named after the Lavos Shell, the first form of the final boss of Chrono Trigger (which copies bosses in increasing order of power throughout the game before swapping to its own attack script).

### `-z:whichbang` {: .h6 }

For Z scripts that include Big Bangs, this flag replaces each instance Big Bang with a similar target-all spell chosen from a small list (including Big Bang itself). It could be a different spell for each Big Bang instance.

### `-z:phaseshift` {: .h6 }

For the non-random-phase scripts, this flag shuffles the order of the three attack phases, so you could see Meteo phase first, then Virus phase, then Nuke phase. The HP thresholds and reactions do not change.

### `-z:nonerfs` {: .h6 }

This flag places chains around every Big Bang type attack that Zeromus does, so that you cannot modify the stat used for the attack (i.e. you cannot nerf Big Bangs). No extra turns have been added, so Zeromus will be significantly more dangerous.

### `-z:mustnerf` {: .h6 }

This flag changes Zeromus's base spell power to 255 (or attack stats to (255,99,255), if physical scripting is enabled) and changes the scripted stat changes for Big Bang type attacks to be 253 for spell power and (255,99,255) for physical scripting. In this way, Zeromus will do 9999 damage almost guaranteed, unless you nerf the Big Bangs/Dark Waves.

Dark Wave is normally bugged; it does not cap its damage, so it breaks the graphical display/can heal by overflowing 14-bit damage. So, we need to patch that issue.

### `-z:vanillasprite` {: .h6 }

This flag is just `-vanilla:z` renamed.

## Wacky Flags

Wylem reworked the wacky challenge framework to allow for multiple wackies to be present at once, in his multi-wacky fork. Thanks, Wylem!

### `-wacky:mirrormirror` - Mirror, Mirror, On the Wall {: .h6 }

- Idea: ScytheMarshall
- Design/Programming: Wylem
- Locations: wacky_rando.py, wacky/mirrormirror.f4c

This wacky flag forces all actors in battle to start with Wall (except summoned monsters).

### `-wacky:dropitlikeitshot` - Drop It Like It's Hot {: .h6 }

- Idea: ScytheMarshall
- Design/Programming: ScytheMarshall
- Locations: wacky_rando.py, wacky/dropitlikeitshot.f4c

This wacky flag changes the drop rate for monsters that sometimes drop items to 100% and makes the drop table probabilities uniform (25% for each of common, uncommon, rare, mythic). 

### `-wacky:scrambledstats` - Scrambled Stats {: .h6 }

- Idea: CoffeeAndChocobos
- Design/Programming: ScytheMarshall (with documentation from Wylem)
- Locations: wacky_rando.py, wacky/scrambledstats.f4c, agility.f4c

This wacky flag shuffles the roles of the five main stats (Str, Agi, Vit, Wis, Wil) in battle for your characters (and Vit for monsters). Your derived stats like attack/defense depend on the new stats. 

### `-wacky:advertising` - Truth in Advertising {: .h6 }

- Idea: Antidale
- Design: everyone in the relevant Discord thread
- Programming: ScytheMarshall
- Locations: wacky_rando.py, wacky/advertising.f4c, custom_weapon_rando.py

This wacky flag makes widespread changes to equipment, spells, and monsters in order to make them "more true to what they seem like". For example, all ice weapons now hit reptile weakness, all bolt weapons now hit robot weakness (and robots are weak to bolt as well), Dwarf Axe now hits air weakness, monsters are weak to air if and only if they are visibly floating, the Quake enemy spell is now also 200 power, the Gigant Axe hits giant weakness, etc. The full list is split up between wacky_rando.py and advertising.f4c.

### `-wacky:whatsmygear` - What's My Gear Again? {: .h6 }

- Idea: Alchemie, ScytheMarshall
- Design/Programming: ScytheMarshall
- Locations: wacky_rando.py, generator.py

This wacky flag fully randomizes the stat bonuses that equipment items give (and changes the select button descriptions to show what the new stat bonuses are). "Unarmed" is not modified.

## Tweak Flags

The "Tweak" flags are miscellaneous flags that modify the game in fairly large ways, to try out different mechanics, do proof-of-concepts for code changes or f4c usage, and so on.

### `-tweak:kainmagic` {: .h6 }

- Idea: various, often joking ("Give Kain MP!")
- Design/Programming: ScytheMarshall
- Locations: give_kain_magic.f4c

This flag gives Kain a relatively small amount of MP and MP growth up to around level 50, a set of black magic based roughly on what his spears can do (Fire2, Ice2, Lit2, and can learn Weak), and a set of white magic (Cure2, Heal, a new spell "Lance", and can learn Blink, Bersk, White). Lance is a fairly strong holy elemental drain spell that replaces Sight. Because Lance is scaled more to Kain's Will instead of an actual white mage's stats, every character that gets Sight will have Lance removed from their spell list because the spell is too strong. 

### `-tweak:harmspell` {: .h6 }

- Idea: ScytheMarshall
- Design/Programming: ScytheMarshall
- Locations: harm_spell.f4c; fusoya_rando.py for spoiler log changes, japanese_spells.f4c for spellset changes

This flag replaces Sight with Harm, a holy-elemental damage-dealing spell slightly weaker than Virus with similar targetting, MP cost, and cast time (with the same HP leak effect that White has). The goal is to provide white mages with an offensive magic option before White.

### `-tweak:edwardheal` {: .h6 }

- Idea: ScytheMarshall
- Design/Programming: ScytheMarshall
- Locations: improve_edward_heal.f4c

This flag modifies Edward's Heal J-ability to use the best of Cure1, Cure2, Cure3 in your inventory instead of only Cure1s. 

### `-tweak:darkpaladin` {: .h6 }

- Idea: various, but initial inspiration from PinkPuff (via Unprecedented Chaos) and F&I thread from Kindron Darkfire
- Design/Programming: ScytheMarshall (taking cues from UC)
- Locations: darkpaladin.f4c, character_rando.py; spoiler logs from core_rando.py, treasure.py, shop_rando.py, custom_weapon_rando.py

This flag makes widespread changes to Paladin Cecil's stats, equipment, and abilities, based loosely on the stronger DKC in Unprecedented Chaos. He retains Dark Wave upon class-change, as well as DKC equipment, and loses command Cover (but will still Cover low-HP characters). His stats become more attack-focused/Wisdom-heavy and his gear now boosts Wis instead of Wil. His white magic set is replaced with a black magic set that mostly has status spells and single-target magic. His equipment is renamed for thematic reasons. Holy swords are now dark elemental, and the Lightbringer (now "Deathbringer") specifically hits dragon weakness. Spoiler logs are updated to match the new names, as are the select button descriptions.

### `-tweak:cidairship` {: .h6 }

- Idea: CoffeeAndChocobos, though the original FF4 devs may have considered doing something like this
- Design/Programming: ScytheMarshall (design, programming), CoffeeAndChocobos (design)
- Locations: cidairship.f4c; some wacky f4c files where command menus change

This flag gives Cid a new target-all command called Raid, using command ID `$15` (which was dummied out in vanilla FF4, but in the Japanese version this command still had a name in the code, "Airship"). The command does damage based on Cid's agility and the furthest airship you've acquired; the Falcon does more damage than the Enterprise, and the Big Whale does more damage than the Falcon. The command ignores defense/magic defense, so Cid can use it to fight Valvalis/etc.

### `-tweak:twinmeteo` {: .h6 }

- Idea: ScytheMarshall
- Design/Programming: ScytheMarshall
- Locations: twin_meteo_stone.f4c

This flag allows Twin to cast W.Meteo or self-target Stone, in addition to Flare and Comet, but only if the casting twins have a combined level of 70 or greater. The probabilities become 143/256 for Flare, 1/4 for Comet (remains the same), 1/8 for W.Meteo, 1/16 for self-target Stone, and 1/256 for failing. Stone will only target the casting twins.

### `-tweak:chocobosummon` {: .h6 }

- Idea: CoffeeAndChocobos
- Design/Programming: CoffeeAndChocobos (design), ScytheMarshall (design and programming), others in the Discord thread
- Locations: big_chocobo_summon.f4c

This flag turns the Chocobo summon into a spell somewhat like Asura, in that sometimes it will instead Call the Big Chocobo to attack. The chance of the Big Chocobo attacking is 4% plus 2% for each distinct item stored with the Big Chocobo, maxing out at 100% at 48 distinct items. The spell power is described in the following way. The base spell power is 40. For each distinct item stored with the Big Chocobo, the spell power increases by 8, plus its item price (prices larger than 112000 GP count as 112000) divided by 16000, times 8. The largest increase per item is 64 points of spell power (e.g. Crystal Sword, Avenger, Adamant). The maximum total spell power is 2040. Carrots give +16 spell power instead of +8, and Whistles give +32 spell power instead of +16. The Grimoire's Chocobo summon is replaced with Big Chocobo.

Since the Big Chocobo menu cannot be accessed with the Save Us Big Chocobo wacky active, the probability is a static 20% with 232 spell power (as if you stored 8 different items with an average of 24 bonus spell power each).