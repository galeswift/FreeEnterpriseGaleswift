from . import databases

# automatically generate tvanillaish_j.csvdb and tvanillaish.csvdb

# load the treasure csvdb, then for each area, 
# inspect all non-excluded items and ID their tiers (separated by MIAB/non-MIAB
# if necessary), then create the distribution row
# use curves.csvdb for the wikiname

curves = databases.get_curves_dbview()
treasure = databases.get_treasure_dbview()
items = databases.get_items_dbview()

vanillaish_weights = {}
vanillaish_j_weights = {}

vanilla_items = {}
vanilla_j_items = {}

GP_CHEST_TIERS = [1000, 4000, 15000, 30000, 50000, 70000, 90000, 500000]

for t_row in treasure:
    if t_row.exclude:
        continue

    if t_row.fight:
        weights = vanillaish_weights.setdefault('MIAB_'+t_row.area, {})
        area_items = vanilla_items.setdefault('MIAB_'+t_row.area, {})
        j_weights = vanillaish_j_weights.setdefault('MIAB_'+t_row.area, {})
        area_j_items = vanilla_j_items.setdefault('MIAB_'+t_row.area, {})
    else:
        weights = vanillaish_weights.setdefault(t_row.area, {})
        area_items = vanilla_items.setdefault(t_row.area, {})
        j_weights = vanillaish_j_weights.setdefault(t_row.area, {})
        area_j_items = vanilla_j_items.setdefault(t_row.area, {})

    t_item = items.find_one(lambda it: it.const == t_row.contents)
    if not t_item:
        # this is a GP chest; read the GP value and assign it a tier based on value
        val = int(t_row.contents[:-len(" gp")])
        for gp in GP_CHEST_TIERS:
            if val <= gp:
                tier = GP_CHEST_TIERS.index(gp) + 1
                break
    else:
        tier = t_item.tier

    if t_row.jcontents:
        t_j_item = items.find_one(lambda it: it.const == t_row.jcontents)
        if not t_j_item:
            # this is a GP chest; read the GP value and assign it a tier based on value
            val = int(t_row.jcontents[:-len(" gp")])
            for gp in GP_CHEST_TIERS:
                if val <= gp:
                    j_tier = GP_CHEST_TIERS.index(gp) + 1
                    break
        else:
            # note that the only tier 99 items are HrGlass1/3, which are J items 
            # (call them tier 5 for this purpose)
            j_tier = (t_j_item.tier if t_j_item.tier != 99 else 5)
    else:
        t_j_item = t_item
        j_tier = tier

    weights.setdefault(tier, 0)
    weights[tier] += 1
    j_weights.setdefault(j_tier, 0)
    j_weights[j_tier] += 1

    area_items.setdefault(tier, [])
    area_items[tier].append(t_row.contents)
    area_j_items.setdefault(j_tier, [])
    area_j_items[j_tier].append((t_row.jcontents if t_row.jcontents else t_row.contents))

# uncomment to output a full comparison of US/J treasure layouts by tier, to validate the weights
# with open('us_vs_j_items.txt', 'w') as outfile:
#     for area in vanilla_items:
#         outfile.write(area + " - US:\n")
#         for tier in range(1,9):
#             if tier in vanilla_items[area]:
#                 outfile.write('  ' + f'{tier}: ' + ', '.join(vanilla_items[area][tier]) + '\n')
#         outfile.write('\n')

#         outfile.write(area + " - J:\n")
#         for tier in range(1,9):
#             if tier in vanilla_j_items[area]:
#                 outfile.write('  ' + f'{tier}: ' + ', '.join(vanilla_j_items[area][tier]) + '\n')
#         outfile.write('\n')

with open('FreeEnt\\assets\\db\\tvanillaish.csvdb', 'w') as outfile:
    outfile.write('area,wikiindex,wikiname,tier1,tier2,tier3,tier4,tier5,tier6,tier7,tier8\n')
    for tres_area in curves:
        if 'Quest' in tres_area.area:
            # use Tpro weights for quests
            row_list = ([tres_area.area, f'{tres_area.wikiindex}', tres_area.wikiname]
                        + [str(getattr(tres_area,f'tier{i}')) for i in range(1,9)])
        else:
            row_list = [tres_area.area, f'{tres_area.wikiindex}', tres_area.wikiname]
            for i in range(1,9):
                if i not in vanillaish_weights[tres_area.area].keys():
                    row_list.append('0')
                else:
                    row_list.append(f'{vanillaish_weights[tres_area.area][i]}')
        outfile.write(','.join(row_list) + '\n')

with open('FreeEnt\\assets\\db\\tvanillaish_j.csvdb', 'w') as outfile:
    outfile.write('area,wikiindex,wikiname,tier1,tier2,tier3,tier4,tier5,tier6,tier7,tier8\n')
    for tres_area in curves:
        if 'Quest' in tres_area.area:
            # use Tpro weights for quests
            row_list = ([tres_area.area, f'{tres_area.wikiindex}', tres_area.wikiname]
                        + [str(getattr(tres_area,f'tier{i}')) for i in range(1,9)])
        else:
            row_list = [tres_area.area, f'{tres_area.wikiindex}', tres_area.wikiname]
            for i in range(1,9):
                if i not in vanillaish_j_weights[tres_area.area].keys():
                    row_list.append('0')
                else:
                    row_list.append(f'{vanillaish_j_weights[tres_area.area][i]}')
        outfile.write(','.join(row_list) + '\n')