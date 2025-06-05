## Spells
This adds a new flag **Cspells:anti** and also modifies the flag name for enabling the J spells list, which changes from **Cj:spells** to **Cspells:j**. The syntax change is to make it clearer that there are now two different ways that spells can change from the vanilla US lists and properties, and while **j:abilities** and **spells:j** are related, the fact that they're not in opposition makes this feel correct to me. **Cspells:j** has not changed at all. [Cspells:anti](</fork_info?md_file=anti_spells_detail>) has a goal of improving the mid-game of most mages, while also delaying their ultimate damaging spells. It aims to achieve this by speeding up the cast times of the elemental spells, and also generally lowering the level that mages learn spells in the mid-game, and pushing learning Nuke and White to somewhere around 1,300,000 xp for the four characters who learn it via levels. See [Cspells:anti](</fork_info?md_file=anti_spells_detail>) for the full details.

## Treasures
There are two changes to treasures in this fork: adding a new **Tstandardish** flag, which is something in between **Tpro** and **Twildish**, and a change to the base treasure distribution in some locations.

### Tstandardish
Under **Tstandardish** you get boosted treasure tiers, but the boosts are more targeted towards tier 5 and tier 6 treasures. Here is the boost matrix straight from the code: 

STANDARDISH_BOOST_MATRIX = {
:   1: [(1, 6/8)],
:   2: [(1, 2/8), (2, 6/8)],
:   3: [(2, 2/8), (3, 5/8)],
:   4: [(3, 3/8), (4, 4/8)],
:   5: [(4, 4/8), (5, 5/8)],
:   6: [(5, 3/8), (6, 6/8)],
:   7: [(6, 2/8), (7, 7/8)],
:   8: [(7, 1/8), (8, 1)],
}


### Updated base treasure curves for some locations:
These changes serve mostly to reduce how ofen you get the lowest tier treasures for a locatoin, and boost the top tier for that location a smidge. Note that this does include allowing tier 8 drops from the Last Arm chest in the Giant.

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