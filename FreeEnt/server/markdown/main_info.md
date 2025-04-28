
## Implemented flags

#### Objectives
- [Omode:bosscollector]: Kill X number of bosses as an objective
{: #bosscollector }
- [Omode:goldhunter]: Turn in a certain amount of gold to Tory in Agart as an objective
{: #goldhunter }
- Random pools: Added 2 extra 'buckets' of randomized objectives, allowing individual configuration of them
{: #objective-pools }
- Random:only chars: Added ability to specify that random character quests for an objective are only for certain characters
{: #objective-character-restrictions }
- Gated objectives: A gated objective means that you will only get the reward for that objective upon completion of all required other objectives.  So if you set "Complete the Tower of Zot" as a gated objective, you will be granted the earth crystal automatically upon completion of the other objectives.
{: #objectives-gated }
- Hard required objectives: Hard required objectives are a # of objectives that must be completed in order to consider all objectives completed.  So if you require 4 out of 5 objectives, and 1 hard required, the hard objective must be included as part of the 4.
{: #objectives-required }

#### Key Items
- [KStart]: Added ability to specify key items as the starting item granted
{: #kstart }

#### Characters
- [CNopartner]: Disables your starting partner.
{: #nopartner }
- [Cpaladin]: Cecil starts as a paladin.  Ordeals is still available as an objective as usual.
{: #cpaladin }
- [Chi]: New characters are required to join the party, even if your party is full.
{: #chi }
- [Cfifo]: When dismissing a character, you must dismiss the character that has been in your party the longest.
{: #cfifo}
- [Csuperhero]: This flag acts the same as Chero, except your starting character will obtain incredible stat boosts, until finding the earth crystal (their one weakness). Trading in the Earth Crystal to the boss in the Tower of Zot removes the Earth Crystal from your inventory and restores the stat boosts.
{: #superhero }
- Ctreasure
    - [Ctreasure-free] Free characters will instead be found in treasure chests in the overworld. Restricted characters will be found in MIABs
{: #ctreasure-free  }
    - [Ctreasure-earned] Earned characters will instead be found in treasure chests in the overworld. Restricted characters will be found in MIABs
{: #ctreasure-earned  }
    - [Ctreasure-unsafe] Free characters will normally all be placed in treasures in the overworld only.  With this flag however, characters will be distributed throughout the underworld,overworld and moon.  This means you may end up with no characters in chests in the overworld.
{: #ctreasure-unsafe  }
    - [Ctreasure-relaxed] Restricted characters will be found in all chests.  No characters will be placed in MIAB chests.
{: #ctreasure-relaxed }

!!! info "Linked Flags"
    In order to enable any of the Ctreasure flags, you must select treasure settings that randomize chest contents. The flag validation will remove your Ctreasure flags when any of Tvanilla, Tshuffle, and Tempty are set.

    * Enabling Ctreasure:free enables C:nofree.
    * Enabling Ctreasure:earned enables C:noearned. Unlike the main site, character sprites at overworld locations are not replaced by piggy sprites.
    * Enabling either Ctreasure:unsafe or Ctreasure:relaxed will enable both Ctreasure:free and Ctreasure:earned, if neither Ctreasure:free nor Ctreasure:earned are explicitly set.

#### Treasures
- [Tunrestrict]: Allows ignoring the restrictions placed on tiers in the treasury/moon/underworld/overworld
{: #tunrestrict }

#### Shops
- [Sprice]/[Spricey]: Changes the price of items in shops.  Can target armor/weapons/items individually
{: #sprice  }
- [Salways]: Items are forced to be guaranteed in shops
{: #salways  }
- [Sno]: More options added to exclude items such as bacchus, coffin, etc.
{: #sno  }
- [Smixed]: Shop prices are randomized
{: #smixed }
- [Ssame]: Shops only sell a single item, and all shops in the game are the same. The item chosen uses the same rules as Swild.
{: #ssame  }
- [Ssingles]: Shops only sell a single item, but follow the standard randomization rules and safety checks (unless disabled).
{: #ssingles  }

#### Bosses
- [Bitburns]: The replacement attack will include Meganuke, Big Bang, Zanteksuken, Full party charm, and Meteo
{: #bitburns  }

#### Flags from other forks
- This branch includes the entrance/door randomization work from jayp [here](https://github.com/jayp12323/FreeEnterprise4)
{: #jayp12323  }
- Also includes all changes from scythe's fork/branch [here](https://github.com/ScytheMarshall/FreeEnterprise4All/tree/scythe-changes)
{: #scythe-marshall  }


# FreeEnterprise4

This is a fork of [the v4.6.0 FE repository](https://github.com/HungryTenor/FreeEnterprise4) 

Please see the original repo for its README information.

## v4.6.0 Contributors
Free Enterprise was made possible using the extensive technical research and knowledge of PinkPuff, Grimoire LD, Chillyfeez, and Aexoden. This repo contains code written and designed by b0ardface/HungryTenor, Crow, Myself086, Myria, mxzv, and Wylem. It also contains the graphic design work of SchalaKitty and Steph Sybydlo. It is based on the game design work of riversmccown and mxzv. And while their specific assets are not included in this repo, the musical work of Xenocat and Calmlamity contributes extensively to Free Enterprise, and was formative in the development of tools contained here.

## Community Contributors:

This repository contains other code written by community members who are not (necessarily) part of the formal "Green Names" FE development team, including:

- Antidale
- cassidy
- Galeswift (that's me!)
- harumph
- S3
- ScytheMarshall
- sgrunt
- Wylem

Some of the code is based on design work done by community members who aren't listed above. They are... (to be filled in).

Many of the ideas are due to other community members asking questions or requesting features for the randomizer. You know who you are (and if not, check out the Discord server!).

### License

This repo is distributed under the MIT License.
