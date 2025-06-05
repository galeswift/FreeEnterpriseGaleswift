from . import databases
from .address import *

def apply(env):
    spells_dbview = databases.get_spells_dbview()
    update_spells_dbview = databases.get_update_spells_dbview()

    for update in update_spells_dbview:
        matching_spell = spells_dbview.find_one(lambda sp: sp.code == update.code)
        # update casting time/targeting data
        env.add_binary(
            BusAddress(0xF97A0 + (0x06 * matching_spell.code)),
            [(update.data[0])],
            as_script=True
        )
