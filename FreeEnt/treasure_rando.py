from . import core_rando
from .crosspolinate import crosspolinate
from . import databases
from .address import *
from . import rewards
from . import util
from . import spoilers
from . import character_rando
from .rewards import AxtorChestReward
import random
from random import shuffle
from dataclasses import dataclass

FIGHT_SPOILER_DESCRIPTIONS = {
    0x1C0 : "Staleman/Skulls",
    0x1C1 : "BlackCats/Lamia",
    0x1C2 : "Mad Ogre x3",
    0x1C3 : "FlameDog",
    0x1C4 : "Mad Ogre x4",
    0x1C5 : "Green D.",
    0x1C6 : "Staleman x2",
    0x1C7 : "Last Arm",
    0x1E0 : "Alert (Chimera)",
    0x1E1 : "Alert (Stoneman)",
    0x1E2 : "Alert (Naga)",
    0x1E3 : "Alert (FlameDog)",
    0x1E4 : "Warrior x5",
    0x1E5 : "ToadLady/TinyToads",
    0x1E6 : "Ghost x6",
    0x1E7 : "DarkTrees/Molbols",
    0x1E8 : "Molbol x2",
    0x1E9 : "Centpede x2",
    0x1EA : "Procyotes/Juclyotes",
    0x1EB : "RedGiant x2",
    0x1EC : "Warlock x2/Kary x2",
    0x1ED : "Warlock/Kary x3",
    0x1EE : "Red D./Blue D.",
    0x1EF : "Blue D. x2",
    0x1F0 : "Behemoth",
    0x1F1 : "Red D. x2",
    0x1F2 : "D.Fossil/Warlock",
    0x1F3 : "Behemoth",
    0x1F4 : "Behemoth"
}

# needed tool for Tspecific
_CHARACTER_TO_USERS = {
    'cecil' : ['dkcecil', 'pcecil'],
    'rydia' : ['crydia', 'arydia']
}

def _round_gp(amount):
    if amount < 1280:
        return int(amount / 10) * 10
    else:
        return int(min(127000, amount) / 1000) * 1000

def _slug(treasure):
    if type(treasure) is str:
        return treasure
    else:
        return f"{treasure.map} {treasure.index}"

@dataclass
class TreasureData:
    contents: str
    fight: str
    t: any
    character_reward_slot_index: int
    character_reward_treasure_index: int

class TreasureAssignment:
    def __init__(self, autosells, env):
        self._autosells = autosells
        self._assignments = {}
        self._remaps = {}
        self._env = env
        
    def get_remap(self, t):
        slug = _slug(t)        
        if slug in self._remaps:
            slug = self._remaps[slug]
        return slug
    
    def remap(self, old, new):
        self._remaps[_slug(old)] = _slug(new)    

    def assign(self, t, contents, fight=None, remap=True):
        slug = _slug(t)        
        if remap: 
            slug = self.get_remap(t)
        if contents in self._autosells and fight is None:
            contents = '{} gp'.format(self._autosells[contents])        
            
        character_reward_slot_index = -1   
        character_reward_treasure_index = t.index    
        #translate either a reward slot or item into a reward index
        if contents != None and contents.startswith('#reward_slot.'):            
            slot = rewards.RewardSlot[contents[len('#reward_slot.'):]]
            reward = self._env.meta['rewards_assignment'][slot]
            if type(reward) is AxtorChestReward:
                character_reward_slot_index = reward.reward_index             
        elif contents != None and '#item.fe_CharacterChestItem' in contents:
            split_contents = contents.split("&")
            character_reward_slot_index = split_contents[1]
            character_reward_treasure_index = split_contents[2]
            contents = '#item.NoArmor'
        
        # if slug in self._assignments and contents != None:
        #     (ocontents, ofight, ot, ocharacter_reward_slot_index) = self._assignments[slug]
        #     if ocontents == "#item.NoArmor":
        #         print(f'Re-assigning {slug} to something already assigned, with contents {contents} with prev contents {self._assignments[slug]}')

        # if character_reward_slot_index != -1 and remap and slug in self._remaps:
        #     print(f'Added character to remapped chest')

        #print(f'Assigning treasure with {contents}:{fight}:{t}:{character_reward_slot_index}')
        newEntry = TreasureData(contents=contents, fight=fight, t=t, character_reward_slot_index=int(character_reward_slot_index), character_reward_treasure_index = int(character_reward_treasure_index))
        self._assignments[slug] = newEntry

    def get(self, t, remap=True):
        slug = _slug(t)
        if remap:
            slug = self.get_remap(t)

        return self._assignments.get(slug, (None, None))

    def get_assignments(self):
        return self._assignments

    def do_substitution(self, env):
        treasure_list = [ ]
        slot_list = []
        for slug in self._assignments:
            treasureEntry = self._assignments[slug]            
            if treasureEntry.contents is None:
                treasureEntry.contents = '$00'
            if treasureEntry.character_reward_slot_index != -1 and type(treasureEntry.t) is not str:                
                worldId = 0
                if treasureEntry.t.flag & (0xff00) > 0:
                    worldId = 1      
                mapIdStr = f'{int(treasureEntry.t.mapid,16):04X}'
                treasure_list.append(f'{worldId:02x}')
                treasure_list.append(mapIdStr[-2:])
                treasure_list.append(f'{treasureEntry.character_reward_treasure_index:02X}')
                slot_list.append(treasureEntry.character_reward_slot_index)
                
                char_name = "unknown"
                for char in character_rando.SLOTS:
                    if character_rando.SLOTS[char] == treasureEntry.character_reward_slot_index:
                        char_name = char
                print(f'Assigning fight:{treasureEntry.fight} {char_name} to {treasureEntry.t.spoilerarea} - {treasureEntry.t.spoilersubarea} - {treasureEntry.t.spoilerdetail}')

        env.add_substitution(f'character treasure rewards', ' '.join(treasure_list))
        env.add_substitution(f'character treasure slots', ' '.join([f'{s:02X}' for s in slot_list]))
            
    def get_script(self):
        lines = []
        for slug in self._assignments:
            treasureEntry = self._assignments[slug]
            contents = treasureEntry.contents     
            if contents is None:
                contents = '$00'
            # if fight is not None:
            #     trigger = f'{t.map} {t.index}'
            line = f"trigger({slug}) {{ treasure {contents} "
            fight = treasureEntry.fight
            if fight is not None:
                if fight >= 0x1E0:
                    fight -= 0x1E0
                else:
                    fight -= 0x1C0
                line += f"fight ${fight:02X} "
            line += "}"                      
            lines.append(line)
        return '\n'.join(lines)

def refineItemsView(dbview, env):    
    dbview.refine(lambda it: it.tier > 0)
    if env.options.flags.has('treasure_no_j_items'):
        dbview.refine(lambda it: not it.j)
    if env.options.flags.has('no_adamants'):
        dbview.refine(lambda it: it.const != '#item.AdamantArmor')
    if env.options.flags.has('no_cursed_rings'):
        dbview.refine(lambda it: it.const != '#item.Cursed')
    if 'kleptomania' in env.meta.get('wacky_challenge',[]):
        dbview.refine(lambda it: (it.category not in ['weapon', 'armor']))   
    if env.meta.get('wacky_challenge') == '3point':
        dbview.refine(lambda it: it.const != '#item.SomaDrop')

    # In Omnidextrous, everyone can equip anything, hence can use everything, so this flag does nothing.
    if env.options.flags.has('treasure_playable') and not 'omnidextrous' in (env.meta.get('wacky_challenge',[])):
        user_set = expand_characters_to_users(env.meta['available_characters'])
        # In Fist Fight, the only weapons are claws, which are equippable by everyone, so need more complex logic
        if 'fistfight' in env.meta.get('wacky_challenge',[]):
            dbview.refine(lambda it: it.category == 'item' or (it.category != 'weapon' and not set(it.equip).isdisjoint(user_set)) or (it.subtype == 'claw'))
        else:
            dbview.refine(lambda it: it.category == 'item' or not set(it.equip).isdisjoint(user_set))       

def expand_characters_to_users(char_set):
    user_set = set()
    for char in char_set:
        if char in _CHARACTER_TO_USERS:
            for user in _CHARACTER_TO_USERS[char]:
                user_set.add(user)
        else:
            user_set.add(char)
    return user_set

def apply(env):       
    treasure_dbview = databases.get_treasure_dbview()

    treasure_dbview.refine(lambda t: not t.exclude)
    plain_chests_dbview = treasure_dbview.get_refined_view(lambda t: t.fight is None)

    items_dbview = databases.get_items_dbview()
    refineItemsView(items_dbview, env)        

    maxtier = env.options.flags.get_suffix('Tmaxtier:')
    if maxtier:
        maxtier = int(maxtier)
        items_dbview.refine(lambda it: it.tier <= maxtier)

    mintier = env.options.flags.get_suffix('Tmintier:')
    if mintier:
        mintier = int(mintier)
        items_dbview.refine(lambda it: it.tier >= mintier)

    if 'kleptomania' in env.meta.get('wacky_challenge', []):
        items_dbview.refine(lambda it: (it.category not in ['weapon', 'armor']))

    autosells = {}
    if env.options.flags.has('treasure_money'):
        autosell_items = items_dbview.find_all()
    elif not env.options.flags.has_any('treasure_vanilla', 'treasure_shuffle', 'treasure_junk'):
        autosell_items = items_dbview.find_all(lambda it: it.tier == 1)
    else:
        autosell_items = []

    for item in autosell_items:
        if env.options.flags.has('shops_sell_zero'):
            autosells[item.const] = 0
        else:
            multiplier = (10 if item.subtype == 'arrow' else 1)
            divisor = (4 if env.options.flags.has('shops_sell_quarter') else 2)
            autosells[item.const] = max(10, _round_gp(int(item.price * multiplier / divisor)))

    treasure_assignment = TreasureAssignment(autosells, env)

    fight_chest_locations = ['{} {}'.format(*env.meta['miab_locations'][slot]) for slot in env.meta['miab_locations']]
    fight_treasure_areas = list(set([t.area for t in treasure_dbview.find_all(lambda t: t.fight is not None)]))
    for area in fight_treasure_areas:
        # find the differences between the lists of:
        #  - chest locations that were originally not MIABs
        #  - chest locations that are now not MIABs
        # 
        treasures = treasure_dbview.find_all(lambda t: t.area == area)
        original_chests = [_slug(t) for t in treasures if t.fight is None]
        new_chests = [_slug(t) for t in treasures if _slug(t) not in fight_chest_locations]
        remapped_original_chests = sorted(set(original_chests) - set(new_chests))
        remapped_new_chests = sorted(set(new_chests) - set(original_chests))
        if len(remapped_original_chests) != len(remapped_new_chests):
            print('---')
            print('\n'.join(original_chests))
            print('---')
            print('\n'.join(new_chests))
            print('---')
            print('\n'.join(remapped_original_chests))
            print('---')
            print('\n'.join(remapped_new_chests))
            print('---')
            raise Exception("Ok things are fuckered")
        for old,new in zip(remapped_original_chests, remapped_new_chests):
            treasure_assignment.remap(old, new)

    character_in_chest_slots = []
    max_overworld_chests = 0
    put_characters_in_chests = False

    if env.options.flags.has('characters_in_treasure_free'):
        character_in_chest_slots = character_rando.FREE_SLOTS
        max_overworld_chests = len(character_rando.FREE_SLOTS) if not env.options.flags.has('characters_in_treasure_unsafe')  else max_overworld_chests
        put_characters_in_chests = True

    if env.options.flags.has('characters_in_treasure_earned'):
        character_in_chest_slots += character_rando.EARNED_SLOTS         
        put_characters_in_chests = True

    if not env.options.flags.has('characters_in_treasure_relaxed'):
        for slot in character_rando.RESTRICTED_SLOTS:
            if slot in character_in_chest_slots:
                character_in_chest_slots.remove(slot)

    assigned_ids= []
    if put_characters_in_chests:
        character_treasure_chests = treasure_dbview.get_refined_view(lambda t: t.fight == None)
        for slot_name in character_in_chest_slots:

            t = None
            if max_overworld_chests <= 0:
                t = env.rnd.choice(character_treasure_chests.find_all(lambda t: t.ordr not in assigned_ids))        
            else:
                t = env.rnd.choice(character_treasure_chests.find_all(lambda t: t.ordr not in assigned_ids and t.world == "Overworld"))
                max_overworld_chests -= 1            
           
            character_dummy = env.assignments[character_rando.SLOTS[slot_name]]           

            treasure_slug = treasure_assignment.get_remap(t)
            treasure_map = treasure_slug.split(" ")[0]
            treasure_idx = treasure_slug.split(" ")[1]
            final_treasure = treasure_dbview.find_one(lambda t: t.map == treasure_map and t.index == int(treasure_idx))
            treasure_assignment.assign(final_treasure, '#item.fe_CharacterChestItem'+"&{:02d}".format(character_rando.SLOTS[slot_name]) + "&{:02d}".format(int(treasure_idx)))
            print(f'Putting character {env.assignments[character_rando.SLOTS[slot_name]]} into chest {final_treasure.spoilerarea} - {final_treasure.spoilersubarea} - {final_treasure.spoilerdetail}')            
            assigned_ids.append(final_treasure.ordr)
            assigned_ids.append(t.ordr)
    
            # update the plain chests to remove the character assigned ones
        plain_chests_dbview.refine(lambda t: t.ordr not in assigned_ids)

    if env.options.flags.has('treasure_vanilla'):
        # for various reasons we really do need to assign every treasure chest still
        for t in treasure_dbview:
            if t.fight is None:
                contents = (t.jcontents if (t.jcontents and not env.options.flags.has('treasure_no_j_items')) else t.contents)
                treasure_assignment.assign(t, contents)
    elif env.options.flags.has('treasure_empty'):
        # all treasures contain nothing
        for t in treasure_dbview:
            treasure_assignment.assign(t, None)
    elif env.options.flags.has('treasure_shuffle'):
        tiers = []

        # split into two tiers
        src_tiers = [
            plain_chests_dbview.find_all(lambda t: t.world == 'Overworld'),
            plain_chests_dbview.find_all(lambda t: t.world != 'Overworld')
            ]

        for src_tier in src_tiers:
            tier = {'chests' : [], 'pool' : []}
            for t in src_tier:
                tier['chests'].append(t)
                tier['pool'].append(t.jcontents if (t.jcontents and not env.options.flags.has('treasure_no_j_items')) else t.contents)
            tiers.append(tier)

        if len(tiers) > 1:
            # crosspolinate the two pools
            crosspolinated_pools = crosspolinate(tiers[0]['pool'], tiers[1]['pool'], 0.5, 0.5, env.rnd)
            tiers[0]['pool'] = crosspolinated_pools[0]
            tiers[1]['pool'] = crosspolinated_pools[1]

        for tier in tiers:
            env.rnd.shuffle(tier['pool'])
            for i,t in enumerate(tier['chests']):
                treasure_assignment.assign(t, tier['pool'][i])
    elif env.options.flags.has('treasure_wild') or env.options.flags.has('treasure_standard'):
        max_item_tier = (99 if env.options.flags.has('treasure_wild') else (mintier if (mintier and (mintier > 5)) else 5))
        # exclude HrGlass1 and HrGlass3 from Twild gen if HrGlass2 can't spawn
        if (max_item_tier == 99 and mintier and mintier > 5):
            max_item_tier = 98
        item_pool = items_dbview.get_refined_view(lambda it: it.tier <= max_item_tier).find_all()
        for t in plain_chests_dbview.find_all():
            treasure_assignment.assign(t, env.rnd.choice(item_pool).const)
    else:
        # revised rivers rando
        items_by_tier = {}
        items_by_tier_unrestricted = {}
        for item in items_dbview:
            items_by_tier.setdefault(item.tier, []).append(item.const)
            items_by_tier_unrestricted.setdefault(item.tier, []).append(item.const)
        distributions = {}
        distributions_unrestricted = {}
        curves_dbview = databases.get_tvanillaish_dbview() if (env.options.flags.has('treasure_vanillaish')) else databases.get_curves_dbview()
        for row in curves_dbview:
            weights = {i : getattr(row, f"tier{i}") for i in range(1,9)}
            if env.options.flags.has('treasure_wild_weighted'):
                weights = util.get_boosted_weights(weights)
            if env.options.flags.has('treasure_semipro'):
                weights = util.get_semiboosted_weights(weights)
            if mintier:
                for tier in range(1,mintier):
                    weights[mintier] += weights[tier]
                    weights[tier] = 0

            distributions_unrestricted[row.area] = util.Distribution(weights)

            # null out distributions for empty item tiers
            for i in range(1,9):
                if not items_by_tier.get(i, None):
                    weights[i] = 0
            distributions[row.area] = util.Distribution(weights)                      
        for t in plain_chests_dbview.find_all():
            tier = -1
            tries = 100
            target_distribution = distributions
            if ((t.area == 'ToroiaTreasury' and env.options.flags.has('Tunrestrict:treasury')) or
                (t.world == 'Overworld' and env.options.flags.has('Tunrestrict:overworld')) or
                (t.world == 'Underworld' and env.options.flags.has('Tunrestrict:underworld')) or
                (t.world == 'Moon' and env.options.flags.has('Tunrestrict:moon')) ):
                target_distribution = distributions_unrestricted
            
            while tier not in items_by_tier and tries > 0:
                tier = min(8, target_distribution[t.area].choose(env.rnd))
                tries -= 1

            if tier in items_by_tier:
                treasure_assignment.assign(t, env.rnd.choice(items_by_tier[tier]))

    # apply sparsity
    sparse_level = env.options.flags.get_suffix('Tsparse:')
    if sparse_level:
        sparse_level = int(sparse_level)
        target_worlds = []
        if env.options.flags.has('treasure_sparse_underground'):
            target_worlds.append('Underworld')            
        if env.options.flags.has('treasure_sparse_moon'):
            target_worlds.append('Moon')
        if env.options.flags.has('treasure_sparse_overworld'):
            target_worlds.append('Overworld')
        sparse_db_view = plain_chests_dbview.find_all(lambda t: t.world in target_worlds)
        empty_count = (len(sparse_db_view) * (100 - sparse_level)) // 100
        for t in env.rnd.sample(sparse_db_view, empty_count):
            treasure_assignment.assign(t, None)

    # apply passes if Pt flag
    if env.options.flags.has('pass_in_chests'):
        remaining_chests = plain_chests_dbview.get_refined_view(lambda t: t.world != 'Moon')
        pass_chest = env.rnd.choice(remaining_chests.find_all())
        treasure_assignment.assign(pass_chest, '#item.Pass')
        remaining_chests.refine(lambda t: t.world != 'Overworld' and t.area != pass_chest.area)
        pass_chest = env.rnd.choice(remaining_chests.find_all())
        treasure_assignment.assign(pass_chest, '#item.Pass')
        remaining_chests.refine(lambda t: t.area != pass_chest.area)
        pass_chest = env.rnd.choice(remaining_chests.find_all())
        treasure_assignment.assign(pass_chest, '#item.Pass')

    # apply required objective treasures
    if env.meta['required_treasures']:
        area_use_count = {}
        remaining_chests = []
        for t in plain_chests_dbview.find_all():
            treasureEntry = treasure_assignment.get(t)
            if treasureEntry.contents != '#item.Pass':
                remaining_chests.append(treasureEntry.t)
                area_use_count[treasureEntry.t.area] = 0

        for item_const in env.meta['required_treasures']:
            remaining_count = env.meta['required_treasures'][item_const]
            while remaining_count > 0:
                chest = env.rnd.choice(remaining_chests)

                # apply coin flip checks against repeated areas
                passed_repeat_check = True
                for i in range(area_use_count[chest.area]):
                    if env.rnd.random() < 0.7:
                        passed_repeat_check = False
                        break
                if not passed_repeat_check:
                    continue

                remaining_chests.remove(chest)
                treasure_assignment.assign(chest, item_const)
                remaining_count -= 1
                area_use_count[chest.area] += 1
    
    #map the fight treasures to the rewards table
    for chest_slot in core_rando.CHEST_ITEM_SLOTS:
        chest_number = env.meta['miab_locations'][chest_slot]
        orig_chest_number = core_rando.CHEST_NUMBERS[chest_slot]
        reward_slot_name =  f'#reward_slot.{chest_slot.name}'        
        orig_chest = treasure_dbview.find_one(lambda t: t.map == orig_chest_number[0] and t.index == orig_chest_number[1])
        target_chest = treasure_dbview.find_one(lambda t: t.map == chest_number[0] and t.index == chest_number[1])
        treasure_assignment.assign(            
            target_chest, 
            reward_slot_name,             
            orig_chest.fight,
            remap = False)

    env.add_script(treasure_assignment.get_script())
    all_treasure_assignments = treasure_assignment.get_assignments()
    treasure_index = 0
    for slug in all_treasure_assignments:
        treasure_index +=1
    
    # write the pre-opened chest values
    chest_init_flags = [0x00] * 0x40
    empty_count = 0
    for t in treasure_dbview.find_all():
        treasureEntry = treasure_assignment.get(t,remap=False)
        if treasureEntry.contents is None:            
            byte_index = t.flag >> 3
            bit_index = t.flag & 0x7
            chest_init_flags[byte_index] |= (1 << bit_index)
            empty_count += 1
    env.add_binary(BusAddress(0x21d9a0), chest_init_flags, as_script=True)

    nonempty_count = 399 - empty_count
    env.add_binary(BusAddress(0x21f0fa), [nonempty_count & 0xFF, (nonempty_count >> 8)], as_script=True)

    # generate spoilers
    treasure_spoilers = []
    treasure_spoiler_order = sorted(treasure_dbview.find_all(), key=lambda t: (t.spoilerarea, t.spoilersubarea))
    all_treasure_public = env.options.flags.has_any('-spoil:all', '-spoil:treasure')
    miabs_public = all_treasure_public or env.options.flags.has('-spoil:miabs')
    for t in treasure_spoiler_order:
        treasureEntry = treasure_assignment.get(t,remap=False)
        contents = treasureEntry.contents
        if contents is None:
            contents = "  (nothing)"
        elif treasureEntry.character_reward_slot_index != -1:
            contents = rewards.REWARD_SLOT_SPOILER_NAMES[rewards.RewardSlot(int(treasureEntry.character_reward_slot_index))]
        elif contents.startswith('#reward_slot.'):
            slot = rewards.RewardSlot[contents[len('#reward_slot.'):]]
            try:
                item = env.meta['rewards_assignment'][slot].item
                contents = databases.get_item_spoiler_name(item)
            except KeyError:
                contents = 'DEBUG'
        elif not contents.endswith(' gp'):
            contents = databases.get_item_spoiler_name(contents)

        if treasureEntry.fight is not None:
            miab = f" (MIAB: {FIGHT_SPOILER_DESCRIPTIONS[treasureEntry.fight]})"
            treasure_spoilers.append( spoilers.SpoilerRow(
                treasureEntry.t.spoilerarea, contents, f"{treasureEntry.t.spoilersubarea} - {treasureEntry.t.spoilerdetail}", miab, 
                public = miabs_public,
                obscurable=True,
                obscure_mask=("NYN!" if all_treasure_public else "NYNY")
                ) )
        else:
            treasure_spoilers.append( spoilers.SpoilerRow(
                treasureEntry.t.spoilerarea, contents, f"{treasureEntry.t.spoilersubarea} - {treasureEntry.t.spoilerdetail}", 
                public = all_treasure_public,
                obscurable=True,
                obscure_mask="NYN"
                ) )
    treasure_assignment.do_substitution(env)
    env.spoilers.add_table("TREASURE", treasure_spoilers, public=(all_treasure_public or miabs_public), ditto_depth=1)


if __name__ == '__main__':
    import FreeEnt
    import random
    import argparse

    parser = argparse.ArgumentParser();
    parser.add_argument('flags', nargs='?')
    args = parser.parse_args();

    options = FreeEnt.FreeEntOptions()
    options.flags.load(args.flags if args.flags else 'Tpro')

    env = FreeEnt.Environment(options)
    env.meta['miab_locations'] = {}
    env.meta['required_treasures'] = {}
    env.meta['rewards_assignment'] = rewards.RewardsAssignment()
    if env.options.flags.get_suffix('Omode:dkmatter'):
        env.meta['required_treasures']['#item.DkMatter'] = 12

    for slot in core_rando.CHEST_NUMBERS:
        env.meta['miab_locations'][slot] = core_rando.CHEST_NUMBERS[slot]
        env.assignments[slot] = ''

    apply(env)
    print(env.scripts[0])

