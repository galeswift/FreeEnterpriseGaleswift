from . import databases
from .address import *
import random

def apply(env):
    prices = []
    megaprices = {}

    items_dbview = databases.get_items_dbview()
    altered_item_prices = env.meta.get('altered_item_prices', {})
    randomized_item_codes = list(range(0x100))
    env.rnd.shuffle(randomized_item_codes)
    for item_code in range(0x100):
        if env.options.flags.has('shops_free'):
            price = 0
        elif env.options.flags.has('shops_mixed'):
            item = items_dbview.find_one(lambda it: it.code == item_code)
            random_item = items_dbview.find_one(lambda it: it.code == randomized_item_codes[item_code])
            price = (random_item.price if random_item else 0)
            #print(f'Price {price} {item.const}')
        elif item_code in altered_item_prices:
            price = altered_item_prices[item_code]
        else:
            item = items_dbview.find_one(lambda it: it.code == item_code)
            price = (item.price if item else 0)

        price_adjustment = env.options.flags.get_suffix('Sprice:')        
        has_any_adjustment_filters = env.options.flags.get_suffix('Spricey:')
        can_adjust_price = not has_any_adjustment_filters or ((env.options.flags.has('Spricey:items') and item.category == 'item' ) or (env.options.flags.has('Spricey:weapons') and item.category == 'weapon' ) or (env.options.flags.has('Spricey:armor') and item.category == 'armor' ))
        if price_adjustment and can_adjust_price: 
            prevPrice = price;
            price = price * float(price_adjustment)//100.0
            price = int(price)
            if (price > 0 and price < 10):
                price = 10
            #print(f"{item.const} adjust pricing from "+price_adjustment+" from "+str(prevPrice)+" to "+str(price))

        if price > 126000:
            prices.append(0xFF)
            megaprices[item_code] = price
        elif price > 1270:
            if price % 1000:
                new_price = 1000 * (price // 1000)
                print(f"WARNING: {item.const} has non-representable cost {price}; rounding to {new_price}")
                price = new_price
            prices.append(0x80 | (price // 1000))
        else:
            if price % 10:
                new_price = 10 * (price // 10)
                print(f"WARNING: {item.const} has non-representable cost {price}; rounding to {new_price}")
                price = new_price
            prices.append(price // 10)

    env.add_binary(UnheaderedAddress(0x7A450), prices, as_script=True)
    
    megaprice_bytes = []
    for item_code in megaprices:
        price = megaprices[item_code]
        megaprice_bytes.append(item_code)
        megaprice_bytes.extend([((price >> (i * 8)) & 0xFF) for i in range(3)])
    megaprice_bytes.append(0x00)

    env.add_binary(BusAddress(0x218080), megaprice_bytes, as_script=True)
