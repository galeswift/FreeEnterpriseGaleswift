from . import databases
from .address import *

def apply(env):
    prices = []
    megaprices = {}

    items_dbview = databases.get_items_dbview()
    altered_item_prices = env.meta.get('altered_item_prices', {})

    randomized_item_codes = list(range(0x100))
    env.rnd.shuffle(randomized_item_codes)
    if not env.options.flags.has('sellsmith'):
        normal_items_dbview = items_dbview.get_refined_view(lambda it: not (it.flag == 'D') and not (it.flag == 'K' and it.code not in [0x3E, 0xEC]))
    else:
        normal_items_dbview = items_dbview.get_refined_view(lambda it: it.code == 0x46 or (not (it.flag == 'D') and not (it.flag == 'K' and it.code not in [0x3E, 0xEC])))
    randomized_normal_item_codes = [it.code for it in normal_items_dbview]
    env.rnd.shuffle(randomized_normal_item_codes)
    # since randomized_normal_item_codes isn't length 0x100, insert the excluded items in their normal spots
    for item_code in range(0x100):
        if item_code not in randomized_normal_item_codes:
            randomized_normal_item_codes.insert(item_code,item_code)

    for item_code in range(0x100):
        if env.options.flags.has('shops_free'):
            price = 0
        elif env.options.flags.has_any('shops_mixed_all','shops_mixed_exclude'):
            item = items_dbview.find_one(lambda it: it.code == item_code)
            if env.options.flags.has('shops_mixed_all'):
                random_item = items_dbview.find_one(lambda it: it.code == randomized_item_codes[item_code])
            else: 
                random_item = normal_items_dbview.find_one(lambda it: it.code == randomized_normal_item_codes[item_code])
            # assert that the S flag happens *after* changed item prices e.g. via the Mystery Juice wacky,
            # so shuffle altered item prices into the pool
            price = altered_item_prices.get(randomized_item_codes[item_code],(random_item.price if random_item else 0))
            #print(f'Price {price} {item.code}')
        elif item_code in altered_item_prices:
            item = items_dbview.find_one(lambda it: it.code == item_code)
            price = altered_item_prices[item_code]
        else:
            item = items_dbview.find_one(lambda it: it.code == item_code)
            price = (item.price if item else 0)

        price_adjustment = env.options.flags.get_suffix('Sprice:')        
        has_any_adjustment_filters = env.options.flags.get_suffix('Spricey:')
        can_adjust_price = not has_any_adjustment_filters or ((env.options.flags.has('Spricey:items') and item.category == 'item' ) or (env.options.flags.has('Spricey:weapons') and item.category == 'weapon' ) or (env.options.flags.has('Spricey:armor') and item.category == 'armor' ))
        if env.options.flags.has('sellsmith') and item_code == 0x46 and env.options.flags.has('Spricey:weapons'):
            can_adjust_price = True
        if price_adjustment and can_adjust_price: 
            #prevPrice = price
            price = price * float(price_adjustment)//100.0
            price = int(price)
            if (price > 0 and price < 10):
                price = 10
            #print(f"{item.const} adjust pricing by "+price_adjustment+" percent from "+str(prevPrice)+" to "+str(price))

        if price > 126000:
            prices.append(0xFF)
            megaprices[item_code] = price
        elif price > 1270:
            if price % 1000:
                new_price = 1000 * (price // 1000)
                # print(f"WARNING: {item.const} has non-representable cost {price}; rounding to {new_price}")
                price = new_price
            prices.append(0x80 | (price // 1000))
        else:
            if price % 10:
                new_price = 10 * (price // 10)
                # print(f"WARNING: {item.const} has non-representable cost {price}; rounding to {new_price}")
                price = new_price
            prices.append(price // 10)

    env.add_binary(UnheaderedAddress(0x7A450), prices, as_script=True)
    
    megaprice_bytes = []
    for item_code in megaprices:
        if item_code == 0x00:
            continue
        price = megaprices[item_code]
        megaprice_bytes.append(item_code)
        megaprice_bytes.extend([((price >> (i * 8)) & 0xFF) for i in range(3)])
    megaprice_bytes.append(0x00)

    env.add_binary(BusAddress(0x21D300), megaprice_bytes, as_script=True)
