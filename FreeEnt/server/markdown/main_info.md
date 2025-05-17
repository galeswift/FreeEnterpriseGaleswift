# Free Enterprise 4 All: The Bad Ideas Fork

This fork of [the v4.6.0 FE repository](https://github.com/HungryTenor/FreeEnterprise4) is intended to collect a variety of contributions from community members into one fork, providing players the options for... Bad Ideas.

This page lists out, in some detail, the new/non-vanilla flags offered by the fork, arranged by flag name. Each description will credit the flag creator/designer (possibly multiple people) and point to the main point(s) in the repository codebase where the flag is implemented.

[TOC]

## Objective Flags

### `Omode:external` {: .h6 }

- Idea: warlink05
- Design/Programming: ScytheMarshall
- Locations: objective_rando.py, external_objective.f4c

An objective that is completed upon the usage of the EagleEye item (instead of it casting Sight), which is given to you at the start of the seed and is impossible to lose. This objective is intended for handling "external" objectives, meaning things like bingo cards, meta objectives, and so on.

## Key Item Flags

### `Kmiab:[standard,all,above,below,lst]` {: .h6 }

- Idea: various (including Skarcerer, ScytheMarshall)
- Design/Programming: ScytheMarshall
- Locations: core_rando.py

The v4.6.0 `Kmiab` flag includes all of the non-LST miabs in the key item pool, or all miabs if `Kmoon` or `Kunsafe` is on. Now, there are three subgroups of miabs: "above-ground" (Zot, Eblan, Hook route, Lunar Path, Giant), "below-ground" (Feymarch, Sylph Cave, Lower Bab-il), and the LST miabs. These subgroups can be specified separately, the vanilla `Kmiab` behaviour with safety checks can be selected using `Kmiab:standard`, and all miabs (ignoring the safety checks, so the pre-v.4.6.0 behaviour) can be selected using Kmiab:all or just specifying all three subgroups. 

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

### `Cmostlydead`, `Cbrieflydead` {: .h6 }

- Idea: warlink05
- Design/Programming: ScytheMarshall
- Locations: swoon_to_wishes.f4c, post_battle.f4c, rewards.f4c, character_rando.py

These new "permadeath" options allow for characters to leave your party when they end a battle swooned without being inaccessible for the rest of the game. Under `Cbrieflydead`, a swooned character will simply be available in the Tower of Wishes after they leave the party, with their equipment and stats as-is (including still being swooned when you pick them up). Under `Cmostlydead`, a swooned character will be sent to the Tower of Wishes and be _reinitialized_, to base level and equipment. 

Under `Cbye`, both options operate as the usual permadeath. When a character's equipment would be otherwise inaccessible, the Legend Sword (if equipped) will be forcibly placed into your inventory.

## Treasure Flags

### `Tplayable` {: .h6 }

- Idea: gameboyf9 (creator of FF4PR's Falcon Dive)
- Design/Programming: ScytheMarshall
- Locations: treasure_rando.py, character_rando.py

Under this flag, all chests will contain items that at least one character available in the seed will be able to use. Under Omnidextrous, this flag does nothing. Under Fist Fight, the only weapons available are claws. This flag does not apply to KI check zonk rewards or MIABs. Summon orbs are consumables, so are treated like any other consumable item (so will appear even if Rydia doesn't; this choice is for tier restriction purposes).

With mystery flags, you can tell who the characters are in the seed by looking at the gear you get.

## Shop Flags

### `Splayable` {: .h6 }

- Idea: ScytheMarshall
- Design/Programming: ScytheMarshall
- Locations: shop_rando.py, character_rando.py

Similarly to `Tplayable`, this flag limits shop items to those usable to characters you can actually find in the seed, with the same exceptions.

## Boss Flags

### `Bwoahdin` {: .h6 }

- Idea: CoffeeAndChocobos
- Design/Programming: ScytheMarshall
- Locations: odin_replace_two_zantetsukens.f4c

In some other FF games, Odin has both the target-all instant death attack and a single-target damaging attack (usually "Gungnir"). Under this flag, Odin's script is changed so that the first two Odin attacks are replaced with a random single-target spell. Odin will also not raise the sword until the point where you can trigger the Thunderstruck script. 

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

### `Enomacgiant` {: .h6 }

- Idea: various (including ScytheMarshall)
- Design/Programming: sgrunt, effectively (ScytheMarshall repurposed sgrunt's `Enodmachin` code)
- Locations: encounter_no_macgiant.f4c, encounter_rando.py

This flag replaces the MacGiant in the repeatable MacGiant grind encounter with a Machine.

## Other Flags

### `-kit:atb` {: .h6 }

- Idea: ScytheMarshall
- Design/Programming: ScytheMarshall
- Locations: kit_rando.py

This kit gives 2-3 SilkWebs, 4-5 Hermes, 1 HrGlass1, and 3-4 Heals (since they reset the speed modifier).

### `-monsterevade`, `-monsterflee` {: .h6 }

- Idea: ScytheMarshall (but also probably others)
- Design/Programming: ScytheMarshall (with help from Aexoden and the disassembly)
- Locations: give_monsters_evade.f4c, monster_flee.f4c

These flags restore functionality to monsters that the original devs removed before the game released. `-monsterevade` allows monsters to correctly load their physical and magical evade stats at the start of battle (instead of just when those stats change, like for Valvalis). Be warned: monsters will take a lot less damage, and will dodge Life pots/casts! `-monsterflee` builds on the evade functionality and restores the ability for monsters to flee from battle (which requires them to have non-zero evade). Monsters can flee from non-boss-bit battles.

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

- Idea: ScytheMarshall (except `-agility:750formula` and `-speedmodbalance`)
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

This flag gives Kain 255 MP, a set of black magic based roughly on what his spears can do (Fire2, Ice2, Lit2, and can learn Weak), and a set of white magic (Cure2, Heal, a new spell "Lance", and can learn Blink, Bersk, White). Lance is a fairly strong holy elemental drain spell that replaces Sight. Every character that gets Sight will also get Lance because the spell just hasn't been removed from their spell lists yet (but also, white mages having an offensive spell before White is nice). 

### `-tweak:edwardheal` {: .h6 }

- Idea: ScytheMarshall
- Design/Programming: ScytheMarshall
- Locations: improve_edward_heal.f4c

This flag modifies Edward's Heal J-ability to use the best of Cure1, Cure2, Cure3 in your inventory instead of only Cure1s. 

### `-tweak:darkpaladin` {: .h6 }

- Idea: various, but initial inspiration from PinkPuff (via Unprecedented Chaos)
- Design/Programming: ScytheMarshall (taking cues from UC)
- Locations: darkpaladin.f4c, character_rando.py; spoiler logs from core_rando.py, treasure.py, shop_rando.py, custom_weapon_rando.py

This flag makes widespread changes to Paladin Cecil's stats, equipment, and abilities, based loosely on the stronger DKC in Unprecedented Chaos. He retains Dark Wave upon class-change, as well as DKC equipment, and loses command Cover (but will still Cover low-HP characters). His stats become more attack-focused/Wisdom-heavy and his gear now boosts Wis instead of Wil. His white magic set is replaced with a black magic set that mostly has status spells and single-target magic. His equipment is renamed for thematic reasons. Holy swords are now dark elemental, and the Lightbringer (now "Deathbringer") specifically hits dragon weakness. Spoiler logs are updated to match the new names, as are the select button descriptions.

### `-tweak:cidairship` {: .h6 }

- Idea: CoffeeAndChocobos, though the original FF4 devs may have considered doing something like this
- Design/Programming: ScytheMarshall (design, programming), CoffeeAndChocobos (design)
- Locations: cidairship.f4c; some wacky f4c files where command menus change

This flag gives Cid a new target-all command called Raid, using command ID `$15` (which was dummied out in vanilla FF4, but in the Japanese version this command still had a name in the code, "Airship"). The command does damage based on Cid's agility and the furthest airship you've acquired; the Falcon does more damage than the Enterprise, and the Big Whale does more damage than the Falcon. The command ignores defense/magic defense, so Cid can use it to fight Valvalis/etc.

### `-tweak:harmspell` {: .h6 }

- Idea: ScytheMarshall
- Design/Programming: ScytheMarshall
- Locations: harm_spell.f4c; fusoya_rando.py for spoiler log changes, japanese_spells.f4c for spellset changes

This flag replaces Sight with Harm, a holy-elemental damage-dealing spell slightly weaker than Virus with similar targetting, MP cost, and cast time (with the same HP leak effect that White has). The goal is to provide white mages with an offensive magic option before White.