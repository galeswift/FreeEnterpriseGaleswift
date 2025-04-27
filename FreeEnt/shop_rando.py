import random

from . import databases
from .crosspolinate import crosspolinate

from . import character_rando
from .address import *
from . import util
from .spoilers import SpoilerRow

CATEGORY_QTYS = {'weapon' : 63, 'armor' : 48, 'item' : 30}
WHITE_MAGES = set(['tellah', 'rosa', 'porom', 'fusoya'])

SHOP_SPOILER_ORDER = ["Baron", "Mist", "Kaipo", "Fabul", "Mysidia", "Toroia", "Silvera", "Agart", "Cave Eblan", "Dwarf Castle", "Tomra", "Feymarch", "Smithy", "Moon"]

class ShopAssignment:
    def __init__(self, shop):
        self._shop = shop
        self._manifest = []

    @property
    def shop(self):
        return self._shop

    @property
    def manifest(self):
        return self._manifest
    
    def add(self, *item_consts):
        self._manifest.extend(item_consts)
        #print(f'Manifest{self._shop.memo} extending to {item_consts} {len(self._manifest)}')

    def matches_category(self, category):
        return getattr(self._shop, category)

    def is_empty(self):
        return len(self._manifest) == 0

    def is_full(self):
        return len(self._manifest) >= 8


def apply(env):
    shops_dbview = databases.get_shops_dbview()

    items_dbview = databases.get_items_dbview()
    item_categories = {it.const : it.category for it in items_dbview}
    items_dbview.refine(lambda it: it.tier)
    
    banned_items = []
    if env.options.flags.has('shops_no_apples'):
        banned_items.append('#item.AgApple')
        banned_items.append('#item.AuApple')
        banned_items.append('#item.SomaDrop')
    if env.options.flags.has('shops_no_damage_items'):
        banned_items.append('#item.Bomb')
        banned_items.append('#item.BigBomb')
        banned_items.append('#item.Notus')
        banned_items.append('#item.Boreas')
        banned_items.append('#item.ThorRage')
        banned_items.append('#item.ZeusRage')
        banned_items.append('#item.FireBomb')
        banned_items.append('#item.Blizzard')
        banned_items.append('#item.LitBolt')
        banned_items.append('#item.Grimoire')
        banned_items.append('#item.Kamikaze')
        banned_items.append('#item.Stardust')
        banned_items.append('#item.GaiaDrum')
        banned_items.append('#item.Vampire')
    if env.options.flags.has('shops_no_sirens'):
        banned_items.append('#item.Siren')
    if env.options.flags.has('shops_no_vampires'):
        banned_items.append('#item.Vampire')
    if env.options.flags.has('shops_no_bacchus'):
        banned_items.append('#item.Bacchus')
    if env.options.flags.has('shops_no_starveil'):
        banned_items.append('#item.StarVeil')
    if env.options.flags.has('shops_no_cure3'):
        banned_items.append('#item.Cure3')
    if env.options.flags.has('shops_no_hourglass'):
        banned_items.append('#item.HrGlass2')
    if env.options.flags.has('shops_no_illusion'):
        banned_items.append('#item.Illusion')
    if env.options.flags.has('shops_no_coffin'):
        banned_items.append('#item.Coffin')
    if env.options.flags.has('shops_no_life'):
        banned_items.append('#item.Life')        
    if env.options.flags.has('no_adamants'):
        banned_items.append('#item.AdamantArmor')
    if env.options.flags.has('no_cursed_rings'):
        banned_items.append('#item.Cursed')
    if banned_items:
        items_dbview.refine(lambda it: it.const not in banned_items)

    if env.options.flags.has('shops_no_j_items'):
        items_dbview.refine(lambda it: not it.j)

    wacky = env.meta.get('wacky_challenge', [])
    if 'kleptomania' in wacky:
        items_dbview.refine(lambda it: (it.category not in ['weapon', 'armor']) or (it.tier == 1))
    if 'friendlyfire' in wacky:
        items_dbview.refine(lambda it: (it.const not in ['#item.Cure3', '#item.Elixir']))
    if 'afflicted' in wacky:
        items_dbview.refine(lambda it: it.const != '#item.Heal')
    if '3point' in wacky:
        items_dbview.refine(lambda it: it.const != '#item.SomaDrop')

    shop_assignments = [ShopAssignment(sh) for sh in shops_dbview.find_all()]

    def place_item(item_const, candidate_shop_assignments):
        # fill an empty shop whenever possible
        empty_shop_assignments = list(filter(lambda sa: sa.is_empty(), candidate_shop_assignments))
        if empty_shop_assignments:
            #print('Empty Shop assignment')
            candidate_shop_assignments = empty_shop_assignments
        elif env.options.flags.has('shops_singles'):
            candidate_shop_assignments = None
        
        if not env.options.flags.has('shops_singles'):
            candidate_shop_assignments = list(filter(lambda sa: not sa.is_full(), candidate_shop_assignments))

        if candidate_shop_assignments:
            # weight the distribution to favor less full shops
            dist = util.Distribution({sa : 12 - len(sa.manifest) for sa in candidate_shop_assignments})
            shop_assignment = dist.choose(env.rnd)
            if item_const not in shop_assignment.manifest:
                #print(f' Adding {item_const} to shop {shop_assignment.shop.memo}')
                shop_assignment.add(item_const)

    if env.options.flags.has('shops_vanilla'):
        # copy base manifests
        for shop_assignment in shop_assignments:
            shop = shop_assignment.shop
            manifest = (shop.jmanifest if (shop.jmanifest and not env.options.flags.has('shops_no_j_items')) else shop.manifest)
            shop_assignment.add(*[i for i in manifest if i.strip()])

            if '#item.Pass' in shop_assignment.manifest and not env.options.flags.has('pass_in_shop'):
                shop_assignment.manifest.remove('#item.Pass')
    elif env.options.flags.has('shops_empty'):
        # literally do nothing
        pass
    elif env.options.flags.has('shops_same'):
        if 'saveusbigchocobo' in env.meta.get('wacky_challenge',[]):
            items_dbview.refine(lambda it: it.const == '#item.Carrot')
        all_candidates = items_dbview.find_all()
        env.rnd.shuffle(all_candidates)
        for shop_assignment in shop_assignments:
            shop_assignment.add(all_candidates[0].const)
    elif env.options.flags.has('shops_cabins'):
        for shop_assignment in shop_assignments:
            shop_assignment.add('#item.Cabin')
    elif env.options.flags.has('shops_vanillaish'):
        weapons_by_tier = { 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}
        armor_by_tier = { 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}
        items_by_tier = { 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}

        for shop_assignment in shop_assignments:
            shop = shop_assignment.shop
            manifest = (shop.jmanifest if (shop.jmanifest and not env.options.flags.has('shops_no_j_items')) else shop.manifest)
            for item_const in manifest:
                item = items_dbview.find_one(lambda it: it.const == item_const) 
                if item:
                    candidate = None
                    if item.category == 'weapon':
                        if not weapons_by_tier[item.tier]:
                            weapons_by_tier[item.tier] = items_dbview.find_all(lambda it: it.category == 'weapon' and it.tier == item.tier) 
                        candidate = env.rnd.choice(weapons_by_tier[item.tier])
                        weapons_by_tier[item.tier].remove(candidate)
                    if item.category == 'armor':
                        if not armor_by_tier[item.tier]:
                            armor_by_tier[item.tier] = items_dbview.find_all(lambda it: it.category == 'armor' and it.tier == item.tier) 
                        candidate = env.rnd.choice(armor_by_tier[item.tier])
                        armor_by_tier[item.tier].remove(candidate)
                    if item.category == 'item':
                        if not items_by_tier[item.tier]:
                            items_by_tier[item.tier] = items_dbview.find_all(lambda it: it.category == 'item' and it.tier == item.tier and not (it.shopoverride == 'wild')) 
                        candidate = env.rnd.choice(items_by_tier[item.tier])
                        items_by_tier[item.tier].remove(candidate)
                    if candidate:
                        shop_assignment.add(candidate.const)
                
    elif env.options.flags.has('shops_shuffle'):
        shop_tiers = [
            list(filter(lambda sa: sa.shop.level == 'free', shop_assignments)),
            list(filter(lambda sa: sa.shop.level != 'free', shop_assignments))
            ]

        pools = []
        for shop_tier in shop_tiers:
            pool = {'weapon':[], 'armor':[], 'item':[]}
            pools.append(pool)

            for shop_assignment in shop_tier:
                for item_const in shop_assignment.shop.manifest:
                    if item_const != '#item.Pass':
                        pool[item_categories[item_const]].append(item_const)

        if len(pools) > 1:
            for category in pools[0]:
                mixed_pools = crosspolinate(pools[0][category], pools[1][category], 0.5, 0.4, env.rnd)
                pools[0][category] = mixed_pools[0]
                pools[1][category] = mixed_pools[1]

        for pool,shop_tier in zip(pools,shop_tiers):            
            for category in pool:
                eligible_shop_assignments = list(filter(lambda sa: sa.matches_category(category), shop_tier))
                remaining_items = list(pool[category])
                env.rnd.shuffle(remaining_items)
                for item_const in remaining_items:
                    place_item(item_const, eligible_shop_assignments)
    else:
        # revised Rivers rando
        def can_be_in_shop(item, shop):            
            shop_level = (shop if type(shop) is str else shop.level)

            if env.options.flags.has('shops_wild'):
                return True
            elif item.shopoverride == 'wild':
                return False
            elif env.options.flags.has('shops_standard'):
                if item.tier == 6:
                    return (shop_level == 'kokkol')
                elif item.tier == 5:                    
                    return (shop_level == 'gated')
                elif item.tier < 5:
                    return (shop_level in ['free', 'gated'])
                else:
                    return False
            elif env.options.flags.has('shops_wildish'):
                if item.tier == 7:
                    return (shop_level in ['kokkol'])
                elif item.tier == 6:
                    return (shop_level in ['gated', 'kokkol'])
                elif item.tier == 5:
                    if (item.category in ['weapon', 'armor']):
                        return (shop_level in ['free', 'gated']) 
                    else:
                        return shop_level == 'gated' 
                elif item.tier < 5:
                    return (shop_level in ['free', 'gated']) 
                else:
                    return False
            elif env.options.flags.has('shops_pro'):
                if item.tier == 5 or item.tier == 6:
                    return (shop_level == 'kokkol')
                elif item.tier == 4:
                    return (shop_level == 'gated')
                elif item.tier < 4:
                    return (shop_level in ['free', 'gated'])
                else:
                    return False
            else:
                return False

        # Kokkol shop
        max_kokkol_items = 4
        if env.options.flags.has('shops_singles'):
            max_kokkol_items = 1

        kokkol_shop_assignment = next(filter(lambda sa: sa.shop.level == 'kokkol', shop_assignments))
        kokkol_candidates = items_dbview.find_all(lambda it: can_be_in_shop(it, 'kokkol'))
        kokkol_shop_assignment.add(*[it.const for it in env.rnd.sample(kokkol_candidates, min(len(kokkol_candidates), max_kokkol_items))])

        # guaranteed items
        guaranteed_free_items = []
        guaranteed_gated_items = []

        desired_guaranteed_items = []
        if env.options.flags.has('shops_always_damage_items'):
            desired_guaranteed_items.append('#item.Bomb')
            desired_guaranteed_items.append('#item.BigBomb')
            desired_guaranteed_items.append('#item.Notus')
            desired_guaranteed_items.append('#item.Boreas')
            desired_guaranteed_items.append('#item.ThorRage')
            desired_guaranteed_items.append('#item.ZeusRage')
            desired_guaranteed_items.append('#item.FireBomb')
            desired_guaranteed_items.append('#item.Blizzard')
            desired_guaranteed_items.append('#item.LitBolt')
            desired_guaranteed_items.append('#item.Grimoire')
            desired_guaranteed_items.append('#item.Kamikaze')
        if env.options.flags.has('shops_always_apples'):
            desired_guaranteed_items.append('#item.AgApple')
            desired_guaranteed_items.append('#item.AuApple')
            desired_guaranteed_items.append('#item.SomaDrop')
        if env.options.flags.has('shops_always_vampires'):
            desired_guaranteed_items.append('#item.Vampire')
        if env.options.flags.has('shops_always_hourglass'):
            desired_guaranteed_items.append('#item.HrGlass2')
        if env.options.flags.has('shops_always_cure3'):
            desired_guaranteed_items.append('#item.Cure3')
        if env.options.flags.has('shops_always_illusion'):
            desired_guaranteed_items.append('#item.Illusion')
        if env.options.flags.has('shops_always_sirens'):
            desired_guaranteed_items.append('#item.Siren')
        if env.options.flags.has('shops_always_bacchus'):
            desired_guaranteed_items.append('#item.Bacchus')
        if env.options.flags.has('shops_always_starveil'):
            desired_guaranteed_items.append('#item.StarVeil')
        if env.options.flags.has('shops_always_coffin'):
            desired_guaranteed_items.append('#item.Coffin')

        free_items_view = {}
        gated_items_view = {}
        for item_const in desired_guaranteed_items:
            raw_items_dbview = databases.get_items_dbview()
            raw_items_dbview.refine(lambda it: it.tier)
            free_items_view = raw_items_dbview.find_all(lambda it: item_const == it.const and can_be_in_shop(it, 'free'))
            gated_items_view = raw_items_dbview.find_all(lambda it: item_const == it.const and can_be_in_shop(it, 'gated'))
            for item in free_items_view:
                guaranteed_free_items.append(item.const)
            for item in gated_items_view:
                if item in free_items_view:
                    continue
                guaranteed_gated_items.append(item.const)

        if not env.options.flags.has('shops_unsafe'):
            # Begin guaranteed 'safe' items
            if 'friendlyfire' not in env.meta.get('wacky_challenge',[]):
                guaranteed_free_items.append('#item.Cure2')

            if not env.options.flags.has('shops_no_life'):
                guaranteed_free_items.append('#item.Life')

            if not env.options.flags.has('shops_no_j_items') and not env.options.flags.has('shops_no_starveil') and not env.options.flags.has('shops_no_damage_items'):
                guaranteed_free_items.append('#item.StarVeil')
                if not env.options.flags.has('bosses_unsafe'):
                    guaranteed_free_items.append('#item.ThorRage')

            if 'saveusbigchocobo' in env.meta.get('wacky_challenge',[]):
                guaranteed_free_items.append('#item.Carrot')

            white_mage_not_guaranteed = env.meta['available_characters'].isdisjoint(WHITE_MAGES)
            if white_mage_not_guaranteed:
                guaranteed_gated_items.append('#item.Cure3')

            if 'saveusbigchocobo' in env.meta.get('wacky_challenge',[]):
                guaranteed_gated_items.append('#item.Whistle')
            # End guaranteed 'safe' items

        free_shop_assignments = list(filter(lambda sa: sa.matches_category('item') and sa.shop.level == 'free', shop_assignments))
        # don't add guaranteed items if they are already in a free shop
        for shop_assignment in free_shop_assignments:
            for item_const in list(guaranteed_free_items):
                if item_const in shop_assignment.manifest:
                    guaranteed_free_items.remove(item_const)

        for item_const in guaranteed_free_items:
            place_item(item_const, free_shop_assignments)

        gated_shop_assignments = list(filter(lambda sa: sa.matches_category('item') and sa.shop.level == 'gated', shop_assignments))
        for shop_assignment in gated_shop_assignments:
            for item_const in list(guaranteed_gated_items):
                if item_const in shop_assignment.manifest:
                    guaranteed_gated_items.remove(item_const)

        for item_const in guaranteed_gated_items:
            place_item(item_const, gated_shop_assignments)

        for category in CATEGORY_QTYS:
            candidates = items_dbview.find_all(lambda it: it.category == category and (can_be_in_shop(it, 'free') or can_be_in_shop(it, 'gated')) )
            category_qty = CATEGORY_QTYS[category]
            # number of 'item' items is dependent on S tier            
            if category == 'item':
                if env.options.flags.has('shops_standard'):
                    category_qty = max(category_qty, int(len(candidates) * 0.9))
                elif env.options.flags.has('shops_wild') or env.options.flags.has('shops_wildish'):
                    category_qty = len(candidates)

            if len(candidates) > category_qty:
                candidates = env.rnd.sample(candidates, category_qty)
            elif len(candidates) > 0:
                add_pool = list(candidates)
                while len(candidates) < category_qty:
                    if len(add_pool) + len(candidates) > category_qty:
                        add_pool = env.rnd.sample(add_pool, category_qty - len(candidates))
                    candidates.extend(add_pool)

            env.rnd.shuffle(candidates)
            candidates.sort(key = lambda it: it.tier, reverse=True)

            if category == 'item' and env.options.flags.has('shops_standard') and not env.options.flags.has('shops_singles'):
                # special behavior: guarantee two tier-5 items in Cave Eblan item shop
                for sa in shop_assignments:
                    if sa.shop.id == 0x18:
                        break

                seed_items = list(filter(lambda it: it.tier == 5, candidates))[:2]
                for item in seed_items:
                    if sa.is_full():
                        break
                    candidates.remove(item)
                    sa.add(item.const)

            if category == 'item' and env.options.flags.has('shops_wildish'):
                # Pick two of: Siren, Coffin, HrGlass2, Bacchus, Elixir, Levia
                # and 1-2 of the damage "wild" items and distribute them
                # to free shops.
                first_pool = ['#item.Siren', '#item.Coffin', '#item.HrGlass2', '#item.Bacchus', '#item.Elixir', '#item.Levia']
                first_pool = list(filter(lambda i: i not in banned_items, first_pool))
                env.rnd.shuffle(first_pool)
                picks = first_pool[slice(2)]
                second_pool = ['#item.Grimoire', '#item.GaiaDrum', '#item.LitBolt', '#item.Blizzard', '#item.FireBomb', '#item.Stardust', '#item.ZeusRage', '#item.Boreas', '#item.BigBomb']
                second_pool = list(filter(lambda i: i not in banned_items, second_pool))
                env.rnd.shuffle(second_pool)
                picks = picks + second_pool[slice(env.rnd.randint(1, 2))]

                free_shops = []

                for sa in shop_assignments:
                    if sa.shop.level == 'free' and sa.matches_category('item') and (not sa.is_full()):
                        free_shops = free_shops + [sa]

                env.rnd.shuffle(free_shops)

                assigned_picks = []
                for pick in picks:
                    sa = free_shops.pop()
                    sa.add(pick)
                    assigned_picks = assigned_picks + [pick]
                    if (not free_shops):
                        break

                candidates = filter(lambda it: it.const not in assigned_picks, candidates)

            category_shop_assignments = list(filter(lambda sa: sa.matches_category(category) and sa.shop.level in ['free', 'gated'], shop_assignments))
            for item in candidates:
                eligible_shop_assignments = list(filter(lambda sa: can_be_in_shop(item, sa.shop), category_shop_assignments))
                place_item(item.const, eligible_shop_assignments)

        # guaranteed items
        if not env.options.flags.has('shops_unsafe'):
            guaranteed_free_items = []
            if 'friendlyfire' in wacky:
                pass
            else:
                guaranteed_free_items.append('#item.Cure2')

            if not env.options.flags.has('shops_no_life'):
                guaranteed_free_items.append('#item.Life')

            if not env.options.flags.has('shops_no_j_items'):
                if not env.options.flags.has('shops_no_starveil'):
                    guaranteed_free_items.append('#item.StarVeil')
                if not env.options.flags.has('bosses_unsafe'):
                    guaranteed_free_items.append('#item.ThorRage')

            if 'saveusbigchocobo' in wacky:
                guaranteed_free_items.append('#item.Carrot')

            free_shop_assignments = list(filter(lambda sa: sa.matches_category('item') and sa.shop.level == 'free', shop_assignments))

            # don't add guaranteed items if they are already in a free shop
            for shop_assignment in free_shop_assignments:
                for item_const in list(guaranteed_free_items):
                    if item_const in shop_assignment.manifest:
                        guaranteed_free_items.remove(item_const)

            for item_const in guaranteed_free_items:
                place_item(item_const, free_shop_assignments)


            gated_shop_assignments = list(filter(lambda sa: sa.matches_category('item') and sa.shop.level == 'gated', shop_assignments))
            guaranteed_gated_items = []

            white_mage_not_guaranteed = env.meta['available_characters'].isdisjoint(WHITE_MAGES)
            if white_mage_not_guaranteed:
                guaranteed_gated_items.append('#item.Cure3')

            if 'saveusbigchocobo' in wacky:
                guaranteed_gated_items.append('#item.Whistle')

            for shop_assignment in gated_shop_assignments:
                for item_const in list(guaranteed_gated_items):
                    if item_const in shop_assignment.manifest:
                        guaranteed_gated_items.remove(item_const)

            for item_const in guaranteed_gated_items:
                place_item(item_const, gated_shop_assignments)

    if env.options.flags.has('pass_in_shop') and not env.options.flags.has('shops_vanilla'):
        # (vanilla case is handled earlier)
        eligible_shop_assignments = list(filter(lambda sa: sa.matches_category('item') and sa.shop.level in ['free', 'gated'], shop_assignments))
        place_item('#item.Pass', eligible_shop_assignments)

    # generate scripts
    shop_assignments = {sa.shop.id : sa for sa in shop_assignments}
    shop_manifest_lines = []
    shop_type_bytes = []

    for shop_id in range(max(shop_assignments) + 1):
        if shop_id in shop_assignments:
            shop_assignment = shop_assignments[shop_id]

            shop_manifest_lines.append(f"// {shop_assignment.shop.memo} (0x{shop_id:02X})")
            for item_const in shop_assignment.manifest:
                shop_manifest_lines.append(item_const)
            if len(shop_assignment.manifest) < 8:
                shop_manifest_lines.append('FF ' * (8 - len(shop_assignment.manifest)))
            shop_manifest_lines.append("")

            if shop_assignment.shop.weapon:
                shop_type_bytes.append(0x00)
            elif shop_assignment.shop.armor:
                shop_type_bytes.append(0x01)
            else:
                shop_type_bytes.append(0x02)
        else:
            shop_manifest_lines.append(f"// Unused shop ({shop_id:02X})")
            shop_manifest_lines.append("FF FF FF FF FF FF FF FF")
            shop_manifest_lines.append("")
            shop_type_bytes.append(0x00)

    env.add_substitution('compiled_shops', '\n'.join(shop_manifest_lines))
    env.add_substitution('shop_types', ' '.join([f"{b:02X}" for b in shop_type_bytes]))

    env.add_file('scripts/extra_shop_manifests.f4c')

    if env.options.flags.has('shops_sell_quarter'):
        env.add_file('scripts/sell_quarter.f4c')
    elif env.options.flags.has('shops_sell_zero'):
        env.add_file('scripts/sell_zero.f4c')

    # generate spoilers
    def spoiler_sort_key(sa):
        key = [-1]
        for i,town_name in enumerate(SHOP_SPOILER_ORDER):
            if town_name in sa.shop.memo:
                key[0] = i
                break
        key.append(not sa.shop.weapon)
        key.append(not sa.shop.armor)
        key.append(not sa.shop.item)
        key.append(len(sa.shop.memo))
        return key

    shop_spoilers = []
    sorted_shop_assignments = sorted([shop_assignments[sid] for sid in shop_assignments], key=spoiler_sort_key)
    for sa in sorted_shop_assignments:
        if sa.manifest:
            for item in sa.manifest:
                shop_spoilers.append( SpoilerRow(sa.shop.memo, databases.get_item_spoiler_name(item), obscurable=True) )
        else:
            shop_spoilers.append( SpoilerRow(sa.shop.memo, "(nothing)", obscurable=True) )

        shop_spoilers.append( tuple() )
    env.spoilers.add_table("SHOPS", shop_spoilers, public=env.options.flags.has_any('-spoil:all', '-spoil:shops'), ditto_depth=1)


if __name__ == '__main__':
    import random
    import argparse
    import FreeEnt

    parser = argparse.ArgumentParser();
    parser.add_argument('flags', nargs='?')
    parser.add_argument('--highlight', nargs='+')
    parser.add_argument('--iterations', type=int, default=1)
    args = parser.parse_args();

    options = FreeEnt.FreeEntOptions()
    options.flags.load(args.flags if args.flags else 'Spro')

    highlight_count = 0
    for iteration_id in range(args.iterations):
        options.seed = ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(10)])
        env = FreeEnt.Environment(options)
        env.meta['available_characters'] = set(['cecil'])#set('cecil kain rydia tellah edward rosa yang palom porom cid edge fusoya'.split())
        apply(env)

        output = env.substitutions['compiled_shops']
        if args.highlight:
            for highlight in args.highlight:
                if not highlight.startswith('#item.'):
                    highlight = '#item.' + highlight
                if highlight in output:
                    highlight_count += 1
                    output += output.replace(highlight, highlight + '                   <<<<<<<<<<<<<<<<<<')

        print(output)

    if args.highlight:
        print(f"Highlight count: {highlight_count}")
