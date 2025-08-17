import json

from FreeEnt.sprite_rando import NON_PLAYER_SPRITES

try:
    from . import databases
except ImportError:
    import databases

from .rewards import RewardSlot

towns = {"#Overworld": ['#BaronTown', '#Mist', '#Kaipo', '#Mysidia', '#Silvera', '#ToroiaTown', '#Agart'],
         "#Underworld": ['#Tomra', '#Feymarch1F', "#Feymarch2F", "#CaveOfSummons1F", "#SylvanCave1F"], "#Moon": []}
towns_flat = ['#BaronTown', '#Mist', '#Kaipo', '#Mysidia', '#Silvera', '#ToroiaTown', '#Agart', '#Tomra',
              '#Feymarch1F', "#Feymarch2F", "#CaveOfSummons1F", "#SylvanCave1F"]
omnicraft_locked_locations = ["#CaveEblanEntrance", "#AdamantGrotto"]

entrances_locked = {"#RoomToSewer": "*[#item.Baron]", "#Moon": "*[#item.DarkCrystal]",
                    "#BaronEquipment": "*[#item.Baron]",
                    "#Underworld": "UNDERWORLD", "#CaveEblanEntrance": "*[#item.fe_Hook]",
                    "#AdamantGrotto": "*[#item.fe_Hook]"}

slots_locked = {
    RewardSlot.baron_castle_item : "*[#item.Baron]", 
    RewardSlot.baron_throne_item : "*[#item.Baron]",
    RewardSlot.giant_chest : "*[#item.DarkCrystal]", 
    RewardSlot.zot_item : "*[#item.EarthCrystal]",
    RewardSlot.pink_trade_item : "*[#item.Pink]", 
    RewardSlot.sealed_cave_item : "*[#item.Luca]",
    RewardSlot.pan_trade_item : "*[#item.Pan]", 
    RewardSlot.sylph_item : "*[#item.Pan]",
    RewardSlot.rat_trade_item : "*[#item.Rat]", 
    RewardSlot.cannon_item : "*[#item.Tower]",
    RewardSlot.magnes_item : "*[#item.TwinHarp]"
}

REWARDS_LOCATIONS = {"-doorsrando": {
                            RewardSlot.antlion_item: "#AntlionCave1F", 
                            RewardSlot.babil_boss_item: "#Babil1F",
                            RewardSlot.bahamut_item : "#Bahamut1F",
                            RewardSlot.baron_castle_character : "#RoomToSewer",
                            RewardSlot.baron_castle_item : "#RoomToSewer",
                            RewardSlot.baron_inn_character : "#BaronInn",
                            RewardSlot.baron_inn_item : "#BaronInn", 
                            RewardSlot.baron_throne_item : "#RoomToSewer",
                            RewardSlot.cannon_item : "#Babil1F",
                            RewardSlot.cave_eblan_character : "#CaveEblanEntrance",
                            RewardSlot.cave_eblan_chest : "#CaveEblanEntrance",
                            RewardSlot.cave_of_summons_chest : "#CaveOfSummons1F",
                            RewardSlot.damcyan_character : "#Damcyan",
                            RewardSlot.dwarf_castle_character : "#DwarfCastle|#DwarfCastleBasement",
                            RewardSlot.dwarf_hospital_item : "#DwarfCastle",
                            RewardSlot.eblan_chest_1 : "#Eblan", 
                            RewardSlot.eblan_chest_2 : "#Eblan",
                            RewardSlot.eblan_chest_3 : "#Eblan", 
                            RewardSlot.fabul_item : "#Fabul",
                            RewardSlot.feymarch_item : "#Feymarch1F",
                            RewardSlot.feymarch_king_item : "#FeymarchLibrary1F",
                            RewardSlot.feymarch_queen_item : "#FeymarchLibrary1F",
                            RewardSlot.forge_item : "#SmithyHouse",
                            RewardSlot.found_yang_item : "#SylvanCaveYangRoom&#FabulWestTower1F",
                            RewardSlot.giant_character : "#Mysidia",
                            RewardSlot.giant_chest : "#Mysidia", 
                            RewardSlot.hobs_character : "#MountHobsEast",
                            RewardSlot.kaipo_character : "#KaipoHospital",
                            RewardSlot.lower_babil_chest_1 : "#Babil1F",
                            RewardSlot.lower_babil_chest_2 : "#Babil1F",
                            RewardSlot.lower_babil_chest_3 : "#Babil1F",
                            RewardSlot.lower_babil_chest_4 : "#Babil1F",
                            RewardSlot.luca_item : "#DwarfCastle|#DwarfCastleBasement",
                            RewardSlot.lunar_boss_1_item : "#LunarPalaceLobby",
                            RewardSlot.lunar_boss_2_item : "#LunarPalaceLobby",
                            RewardSlot.lunar_boss_3_item : "#LunarPalaceLobby",
                            RewardSlot.lunar_boss_4_item_1 : "#LunarPalaceLobby",
                            RewardSlot.lunar_boss_4_item_2 : "#LunarPalaceLobby",
                            RewardSlot.lunar_boss_5_item : "#LunarPalaceLobby",
                            RewardSlot.lunar_core_chest_1 : "#LunarPalaceLobby",
                            RewardSlot.lunar_core_chest_2 : "#LunarPalaceLobby",
                            RewardSlot.lunar_core_chest_3 : "#LunarPalaceLobby",
                            RewardSlot.lunar_core_chest_4 : "#LunarPalaceLobby",
                            RewardSlot.lunar_core_chest_5 : "#LunarPalaceLobby",
                            RewardSlot.lunar_core_chest_6 : "#LunarPalaceLobby",
                            RewardSlot.lunar_core_chest_7 : "#LunarPalaceLobby",
                            RewardSlot.lunar_core_chest_8 : "#LunarPalaceLobby",
                            RewardSlot.lunar_core_chest_9 : "#LunarPalaceLobby",
                            RewardSlot.lunar_palace_character : "#LunarPalaceLobby",
                            RewardSlot.lunar_path_chest : "#LunarPassage1",
                            RewardSlot.magnes_item : "#CaveMagnes1F",
                            RewardSlot.mist_character : "#Mist&#KaipoInn",
                            RewardSlot.mysidia_character_1 : "#HouseOfWishes",
                            RewardSlot.mysidia_character_2 : "#HouseOfWishes",
                            RewardSlot.ordeals_character : "#MountOrdeals1F",
                            RewardSlot.ordeals_item : "#MountOrdeals1F",
                            RewardSlot.pan_trade_item : "#SylvanCaveYangRoom&#FabulWestTower1F",
                            RewardSlot.pink_trade_item : "#AdamantGrotto",
                            RewardSlot.rat_trade_item : "#AdamantGrotto",
                            RewardSlot.rydias_mom_item : "#Mist",
                            RewardSlot.sealed_cave_item : "#SealedCaveEntrance",
                            RewardSlot.starting_character : "None", 
                            RewardSlot.starting_item : "starting",
                            RewardSlot.starting_partner_character : "None",
                            RewardSlot.sylph_cave_chest_1 : "#SylvanCave1F",
                            RewardSlot.sylph_cave_chest_2 : "#SylvanCave1F",
                            RewardSlot.sylph_cave_chest_3 : "#SylvanCave1F",
                            RewardSlot.sylph_cave_chest_4 : "#SylvanCave1F",
                            RewardSlot.sylph_cave_chest_5 : "#SylvanCave1F",
                            RewardSlot.sylph_cave_chest_6 : "#SylvanCave1F",
                            RewardSlot.sylph_cave_chest_7 : "#SylvanCave1F",
                            RewardSlot.sylph_item : "#SylvanCaveYangRoom",
                            RewardSlot.upper_babil_chest : "#BabilB1",
                            RewardSlot.watery_pass_character : "#WateryPass1F|#WateryPass5F",
                            RewardSlot.zot_character_1 : "#ToroiaCastle",
                            RewardSlot.zot_character_2 : "#ToroiaCastle",
                            RewardSlot.zot_chest : "#ToroiaCastle", 
                            RewardSlot.zot_item : "#ToroiaCastle",
                            RewardSlot.fixed_crystal : "#LunarPalaceLobby",
                            RewardSlot.toroia_hospital_item : "#ToroiaCastleHospital"},
               "-entrancesrando": {
                                RewardSlot.antlion_item : "#AntlionCave1F",
                                RewardSlot.babil_boss_item : "#Babil1F",
                                RewardSlot.bahamut_item : "#Bahamut1F",
                                RewardSlot.baron_castle_character : "#BaronTown",
                                RewardSlot.baron_castle_item : "#BaronTown",
                                RewardSlot.baron_inn_character : "#BaronTown",
                                RewardSlot.baron_inn_item : "#BaronTown",
                                RewardSlot.baron_throne_item : "#BaronTown",
                                RewardSlot.cannon_item : "#Babil1F",
                                RewardSlot.cave_eblan_character : "#CaveEblanEntrance",
                                RewardSlot.cave_eblan_chest : "#CaveEblanEntrance",
                                RewardSlot.cave_of_summons_chest : "#CaveOfSummons1F",
                                RewardSlot.damcyan_character : "#Damcyan",
                                RewardSlot.dwarf_castle_character : "#DwarfCastle|#DwarfCastleBasement",
                                RewardSlot.dwarf_hospital_item : "#DwarfCastle",
                                RewardSlot.eblan_chest_1 : "#Eblan", 
                                RewardSlot.eblan_chest_2 : "#Eblan",
                                RewardSlot.eblan_chest_3 : "#Eblan", 
                                RewardSlot.fabul_item : "#Fabul",
                                RewardSlot.feymarch_item : "#CaveOfSummons1F",
                                RewardSlot.feymarch_king_item : "#CaveOfSummons1F",
                                RewardSlot.feymarch_queen_item : "#CaveOfSummons1F",
                                RewardSlot.forge_item : "#SmithyHouse",
                                RewardSlot.found_yang_item : "#SylvanCave1F&#Fabul",
                                RewardSlot.giant_character : "#Mysidia",
                                RewardSlot.giant_chest : "#Mysidia", 
                                RewardSlot.hobs_character : "#MountHobsEast",
                                RewardSlot.kaipo_character : "#Kaipo", 
                                RewardSlot.lower_babil_chest_1 : "#Babil1F",
                                RewardSlot.lower_babil_chest_2 : "#Babil1F",
                                RewardSlot.lower_babil_chest_3 : "#Babil1F",
                                RewardSlot.lower_babil_chest_4 : "#Babil1F",
                                RewardSlot.luca_item : "#DwarfCastle|#DwarfCastleBasement",
                                RewardSlot.lunar_boss_1_item : "#LunarPalaceLobby",
                                RewardSlot.lunar_boss_2_item : "#LunarPalaceLobby",
                                RewardSlot.lunar_boss_3_item : "#LunarPalaceLobby",
                                RewardSlot.lunar_boss_4_item_1 : "#LunarPalaceLobby",
                                RewardSlot.lunar_boss_4_item_2 : "#LunarPalaceLobby",
                                RewardSlot.lunar_boss_5_item : "#LunarPalaceLobby",
                                RewardSlot.lunar_core_chest_1 : "#LunarPalaceLobby",
                                RewardSlot.lunar_core_chest_2 : "#LunarPalaceLobby",
                                RewardSlot.lunar_core_chest_3 : "#LunarPalaceLobby",
                                RewardSlot.lunar_core_chest_4 : "#LunarPalaceLobby",
                                RewardSlot.lunar_core_chest_5 : "#LunarPalaceLobby",
                                RewardSlot.lunar_core_chest_6 : "#LunarPalaceLobby",
                                RewardSlot.lunar_core_chest_7 : "#LunarPalaceLobby",
                                RewardSlot.lunar_core_chest_8 : "#LunarPalaceLobby",
                                RewardSlot.lunar_core_chest_9 : "#LunarPalaceLobby",
                                RewardSlot.lunar_palace_character : "#LunarPalaceLobby",
                                RewardSlot.lunar_path_chest : "#LunarPassage1",
                                RewardSlot.magnes_item : "#CaveMagnes1F",
                                RewardSlot.mist_character : "#Mist&#Kaipo",
                                RewardSlot.mysidia_character_1 : "#HouseOfWishes",
                                RewardSlot.mysidia_character_2 : "#HouseOfWishes",
                                RewardSlot.ordeals_character : "#MountOrdeals1F",
                                RewardSlot.ordeals_item : "#MountOrdeals1F",
                                RewardSlot.pan_trade_item : "#SylvanCave1F&#Fabul",
                                RewardSlot.pink_trade_item : "#AdamantGrotto",
                                RewardSlot.rat_trade_item : "#AdamantGrotto",
                                RewardSlot.rydias_mom_item : "#Mist",
                                RewardSlot.sealed_cave_item : "#SealedCaveEntrance",
                                RewardSlot.starting_character : "None", 
                                RewardSlot.starting_item : "starting",
                                RewardSlot.starting_partner_character : "None",
                                RewardSlot.sylph_cave_chest_1 : "#SylvanCave1F",
                                RewardSlot.sylph_cave_chest_2 : "#SylvanCave1F",
                                RewardSlot.sylph_cave_chest_3 : "#SylvanCave1F",
                                RewardSlot.sylph_cave_chest_4 : "#SylvanCave1F",
                                RewardSlot.sylph_cave_chest_5 : "#SylvanCave1F",
                                RewardSlot.sylph_cave_chest_6 : "#SylvanCave1F",
                                RewardSlot.sylph_cave_chest_7 : "#SylvanCave1F",
                                RewardSlot.sylph_item : "#SylvanCave1F",
                                RewardSlot.upper_babil_chest : "#CaveEblanEntrance",
                                RewardSlot.watery_pass_character : "#WateryPass1F|#WateryPass5F",
                                RewardSlot.zot_character_1 : "#ToroiaCastle",
                                RewardSlot.zot_character_2 : "#ToroiaCastle",
                                RewardSlot.zot_chest : "#ToroiaCastle", 
                                RewardSlot.zot_item : "#ToroiaCastle",
                                RewardSlot.fixed_crystal : "#LunarPalaceLobby",
                                RewardSlot.toroia_hospital_item : "#ToroiaCastle"}}
slot_locations = {
    "-doorsrando": {"dmist_slot": "#MistCave", "officer_slot": "#Mist&#Kaipo", "octomamm_slot": "#Waterfall2F",
                    "antlion_slot": "#AntlionCave1F", "mombomb_slot": "#MountHobsEast", "fabulgauntlet_slot": "#Fabul",
                    "milon_slot": "#MountOrdeals1F", "milonz_slot": "#MountOrdeals1F",
                    "mirrorcecil_slot": "#MountOrdeals1F", "karate_slot": "#BaronInn", "guard_slot": "#BaronInn",
                    "baigan_slot": "#RoomToSewer", "kainazzo_slot": "#RoomToSewer", "darkelf_slot": "#CaveMagnes1F",
                    "magus_slot": "#ToroiaCastle", "valvalis_slot": "#ToroiaCastle",
                    "calbrena_slot": "#DwarfCastle|#DwarfCastleBasement",
                    "golbez_slot": "#DwarfCastle|#DwarfCastleBasement", "lugae_slot": "#Babil1F",
                    "darkimp_slot": "#Babil1F", "kingqueen_slot": "#BabilB1",
                    "rubicant_slot": "#BabilB1", "evilwall_slot": "#SealedCaveEntrance",
                    "asura_slot": "#FeymarchLibrary1F", "leviatan_slot": "#FeymarchLibrary1F",
                    "odin_slot": "#RoomToSewer", "bahamut_slot": "#Bahamut1F", "elements_slot": "None",
                    "cpu_slot": "None", "paledim_slot": "#LunarPalaceLobby", "wyvern_slot": "#LunarPalaceLobby",
                    "plague_slot": "#LunarPalaceLobby", "dlunar_slot": "#LunarPalaceLobby",
                    "ogopogo_slot": "#LunarPalaceLobby"},
    "-entrancesrando": {"dmist_slot": "#MistCave", "officer_slot": "#Mist&#Kaipo", "octomamm_slot": "#Waterfall2F",
                        "antlion_slot": "#AntlionCave1F", "mombomb_slot": "#MountHobsEast",
                        "fabulgauntlet_slot": "#Fabul",
                        "milon_slot": "#MountOrdeals1F", "milonz_slot": "#MountOrdeals1F",
                        "mirrorcecil_slot": "#MountOrdeals1F", "karate_slot": "#BaronTown", "guard_slot": "#BaronTown",
                        "baigan_slot": "#BaronTown", "kainazzo_slot": "#BaronTown", "darkelf_slot": "#CaveMagnes1F",
                        "magus_slot": "#ToroiaCastle", "valvalis_slot": "#ToroiaCastle",
                        "calbrena_slot": "#DwarfCastle|#DwarfCastleBasement",
                        "golbez_slot": "#DwarfCastle|#DwarfCastleBasement", "lugae_slot": "#Babil1F",
                        "darkimp_slot": "#Babil1F", "kingqueen_slot": "#CaveEblanEntrance",
                        "rubicant_slot": "#CaveEblanEntrance", "evilwall_slot": "#SealedCaveEntrance",
                        "asura_slot": "#CaveOfSummons1F", "leviatan_slot": "#CaveOfSummons1F",
                        "odin_slot": "#BaronTown", "bahamut_slot": "#Bahamut1F", "elements_slot": "None",
                        "cpu_slot": "None", "paledim_slot": "#LunarPalaceLobby", "wyvern_slot": "#LunarPalaceLobby",
                        "plague_slot": "#LunarPalaceLobby", "dlunar_slot": "#LunarPalaceLobby",
                        "ogopogo_slot": "#LunarPalaceLobby"}}
DIRECTION_MAP = {
    'up': 0,
    'right': 1,
    'down': 2,
    'left': 3,
}


def map_exit_to_entrance(remapped_entrances, exit, scope ):

    if scope == "-entrancesrando":
        if "SylvanCaveYangRoom" in exit[0]:
            exit = ["#SylvanCave1F", "", "", "", "#Underworld"]
        elif "#FeymarchTreasury" in exit[0]:
            exit = ["#CaveOfSummons1F", "", "", "", "#Underworld"]
    if "SylvanCaveTreasury" in exit[0] or "#SylvanCave3F" in exit[0]:
        exit = ["#SylvanCave1F", "", "", "", "#Underworld"]
    elif "CaveOfSummons3F" in exit[0]:
        exit = ["#CaveOfSummons1F", "", "", "", "#Underworld"]
    elif exit[0] == "#EblanBasement":
        exit = ["#Eblan", "", "", "", "#Overworld"]

    try:
        entrance_key = f"{exit[4]}_{exit[0]}_{exit[7]}"
    except IndexError:
        entrance_key = f"{exit[4]}_{exit[0]}_"
    for i in remapped_entrances:
        if i[10] == entrance_key:
            return [i[0]] + i[2:4] + [i[12]]
    entrance_key_up = f"{exit[4]}_{exit[0]}_up"
    for i in remapped_entrances:
        if i[10] == entrance_key_up:
            return [i[0]] + i[2:4] + [i[12]]
    entrance_key_down = f"{exit[4]}_{exit[0]}_down"
    for i in remapped_entrances:
        if i[10] == entrance_key_down:
            return [i[0]] + i[2:4] + [i[12]]

    # print(exit)
    return ""


def shuffle_locations(rnd, entrances, exits, scope):
    towns_ = towns_flat
    entrance_destinations = [entrance[4:] for entrance in entrances]
    exit_dict = {}
    for dest in entrance_destinations:
        exit_tup = (dest[0], dest[3])
        if exit_tup not in exit_dict:
            exit_dict[exit_tup] = dest[1:]

    exit__ = [[list(i)[0]] + exit_dict[i] + [list(i)[1]] for i in exit_dict]
    rnd.shuffle((exit__))
    shuffled_exits = list(exit__)
    exit_dict = {}
    rnd.shuffle(shuffled_exits)
    overworld_entrances = 0
    # print("max_towns", world, max_towns_in_overworld)
    tries = 0
    while exit__:
        if tries > 20:
            return False
        exit___ = exit__.pop(0)
        shuffled_exit = shuffled_exits.pop(0)
        if shuffled_exit[0] in towns_ and shuffled_exit[4] == 'entrance' and exit___[4] == "entrance":
            overworld_entrances += 1

        if (shuffled_exit[0] in towns_ and shuffled_exit[4] == 'entrance' and exit___[5].split("_")[0] ==
            shuffled_exit[0]) or (
                shuffled_exit[0] == "#Feymarch2F" and shuffled_exit[4] == 'town_building' and exit___[5].split("_")[1]
                in ["#FeymarchTreasury", "#FeymarchSaveRoom", "#FeymarchLibrary1F", "#FeymarchWeapon", "#FeymarchArmor",
                    "#FeymarchInn"]) or (
                shuffled_exit[0] == "#SylvanCave1F" and exit___[5].split("_")[1] == "#SylvanCaveYangRoom") or (
                shuffled_exit[0] == "#CaveOfSummons1F" and exit___[5].split("_")[1] == "#Feymarch1F") or (
                shuffled_exit[0] == "#Feymarch1F" and exit___[5].split("_")[1] in ["#FeymarchTreasury",
                                                                                   "Feymarch2F"]):
            exit__ = [exit___] + exit__
            rnd.shuffle(exit__)
            shuffled_exits.append(shuffled_exit)
            rnd.shuffle(shuffled_exits)
            tries += 1
            continue
        exit_dict[tuple([exit___[0], exit___[3]])] = shuffled_exit
    remapped_entrances = []
    for entrance in entrances:
        exit_key = tuple([entrance[4], entrance[7]])
        remapped_exit = exit_dict[exit_key]
        remapped_entrances.append(entrance[0:4] + [entrance[-2]] + remapped_exit)

    remapped_exits = []
    for i in exits:
        entrance = map_exit_to_entrance(remapped_entrances, i, scope)
        if entrance:
            remapped_exits.append(i[0:4] + [i[-2]] + entrance)
        else:
            if i[0] in ['#FeymarchTreasury', '#SylvanCaveYangRoom']:
                pass # doors rando, not entrances rando
            else:
                print("not found")
                print(i)
    return [remapped_entrances, remapped_exits]


def sync_entrances_exits(graph):
    new_graph = graph.copy()
    for location in graph:
        entrances = graph[location]["entrances"]
        exits = graph[location]["exits"]

        for entrance in entrances:
            if entrance not in new_graph:
                new_graph[entrance] = {"entrances": [], "exits": []}
            if location not in new_graph[entrance]["exits"]:
                new_graph[entrance]["exits"].append(location)
        for exit_ in exits:
            if exit_ not in new_graph:
                new_graph[exit_] = {"entrances": [], "exits": []}
            if location not in new_graph[exit_]["entrances"]:
                new_graph[exit_]["entrances"].append(location)

    return new_graph


def find_all_paths(graph, start, end, type, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph:
        return []
    paths = []
    for node in graph[start][type]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, type, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths


def map_path_to_entrance_names(path, remapped_map):
    new_path = []
    for location in path:
        if location in ["#Overworld", "#Underworld", "#Moon"]:
            new_path.append(location)
        else:
            try:
                new_path.append([remapped_map[location], location])
            except KeyError:
                new_path.append([location, location])
    return new_path


def randomize_doors(env, entrances, exits, scope):
    is_loop = False
    loop_count = 0
    tries = 1
    paths_to_world = {}
    world_paths = {"#Overworld": [], "#Underworld": [], "#Moon": []}

    graph = {}
    remapped_map = {}
    shuffled_entrances = {}
    shuffled_exits = {}
    spoil_entrances = []
    spoil_entrances_for_spoiler = []
    while not is_loop:
        graph = {}
        remapped_map = {}
        paths_to_world = {}
        world_paths = {"#Overworld": [], "#Underworld": [], "#Moon": []}
        spoil_entrances = []
        spoil_entrances_for_spoiler = []
        if loop_count > 200:
            return False
        loop_count += 1
        max_tries = 1000
        try:
            remapped_entrances, remapped_exits = shuffle_locations(env.rnd, entrances, exits, scope)
        except TypeError:
            tries += 1
            if tries < max_tries:
                continue
            else:
                return False
        #print("max locations took tries: ", tries)
        shuffled_entrances = remapped_entrances
        shuffled_exits = remapped_exits

        for j in remapped_entrances + remapped_exits:
            location = j[0]
            destination = j[5]
            if len(j) == 13:
                type = "entrances"
                entrance_location=j[4].split('_')[1]
                message = f"{destination} is in the {entrance_location} location"
                if message not in spoil_entrances:
                    if destination == "#Mist":
                        if "#Mist" not in remapped_map:
                            remapped_map[destination] = []
                        remapped_map[destination].append(entrance_location)

                    else:
                        remapped_map[destination] = entrance_location
                    spoil_entrances.append(message)
                    if ("Mist" in entrance_location and not ("MistCave" in entrance_location
                                        or "MistInn" in entrance_location or "MistWeapon" in entrance_location or "MistArmor" in entrance_location)):
                        if j[2]==96:
                            entrance_location = "#Mist West"
                        else:
                            entrance_location = "#Mist East"

                    elif "MistCave" in entrance_location:
                        if j[2]==76:
                            entrance_location = "#MistCave South"
                        else:
                            entrance_location = "#MistCave North"
                    elif "LunarPassage1" in entrance_location:
                        if j[3]==20:
                            entrance_location = "#LunarPassage1 South"
                        else:
                            entrance_location = "#LunarPassage1 North"
                    elif "LunarPassage2" in entrance_location:
                        if j[2]==40:
                            entrance_location = "#LunarPassage2 South"
                        else:
                            entrance_location = "#LunarPassage2 North"



                    if "#Mist" == destination:
                        if j[6]==3:
                            destination = "#Mist West"
                        else:
                            destination = "#Mist East"

                    elif "#MistCave" == destination:
                        if j[6]==2:
                            destination = "#MistCave South"
                        else:
                            destination = "#MistCave North"
                    elif "#LunarPassage1" == destination:
                        if j[6]==12:
                            destination = "#LunarPassage1 South"
                        else:
                            destination = "#LunarPassage1 North"
                    elif "#LunarPassage2" == destination:
                        if j[6]==9:
                            destination = "#LunarPassage2 South"
                        else:
                            destination = "#LunarPassage2 North"
                    spoil_entrances_for_spoiler.append((destination, entrance_location))
            else:
                type = "exits"
            if location not in graph:
                graph[location] = {"entrances": [], "exits": []}
            if destination not in graph[location][type]:
                graph[location][type].append(destination)

        paths_to_world = {}
        is_loop = False

        try:
            graph["#Fabul"]["entrances"].append("#FabulLobby")
            graph["#FabulLobby"]["exits"].append("#Fabul")
            graph["#CaveEblanExit"]["exits"].append("#CaveEblanSettlement")
            graph["#CaveEblanEntrance"]["entrances"].append("#CaveEblanSettlement")
            graph["#CaveEblanSettlement"]["entrances"].append("#CaveEblanExit")
            graph["#CaveEblanSettlement"]["exits"].append("#CaveEblanEntrance")

        except:
            pass  # Not overworld
        try:
            graph["#SylvanCave1F"]["entrances"].append("#SylvanCave3F")
            graph["#CaveOfSummons1F"]["entrances"].append("#CaveOfSummons3F")
            graph["#SylvanCave3F"]["exits"].append("#SylvanCave1F")
            graph["#CaveOfSummons3F"]["exits"].append("#CaveOfSummons1F")
        except:
            pass  # Not underworld
        graph = sync_entrances_exits(graph)

        locations_to_ignore = ["#SylvanCaveTreasury", "#EblanBasement", "#CaveOfSummons3F", "#SylvanCave3F"]
        for location in graph:
            if location in locations_to_ignore:
                continue
            paths_to_world[location] = []
            for world in ["#Overworld", "#Underworld", "#Moon"]:
                findallpaths = find_all_paths(graph, world, location, "entrances", [])
                paths_to_world[location] += findallpaths
                if findallpaths:
                    world_paths[world].append(location)
            if paths_to_world[location]:

                location_doors = []
                for path in paths_to_world[location]:
                    location_doors.append(map_path_to_entrance_names(path, remapped_map))
                paths_to_world[location] = location_doors
                if location == "#Damcyan":
                    is_Damcyan_accessible = []
                    for damcyan_path in paths_to_world[location]:
                        if damcyan_path[1][0] in ["#AdamantGrotto", "#CaveEblanEntrance"]:
                            is_Damcyan_accessible.append(False)
                        else:
                            is_Damcyan_accessible.append(True)
                    if True not in is_Damcyan_accessible:
                        print("Damcyan is hovercraft locked")
                        is_loop = False
                        break
                if location == "#BlackChocoboForest":
                    is_magnes = []
                    is_overworld = False
                    for bcf_path in paths_to_world[location]:
                        if "#Overworld" in bcf_path:
                            is_overworld = True
                        if bcf_path[1][0] == '#CaveMagnes1F':
                            is_magnes.append(True)
                        else:
                            is_magnes.append(False)

                    if (not is_overworld) or (False not in is_magnes):
                        #print("Black Chocobo Forest is not accessible... retrying")
                        is_loop = False
                        break

                is_loop = True
                continue
            else:
                #print("not able find overworld to exit for:", location, "due to loop... retrying")
                is_loop = False
                break
        if is_loop:
            break
        print("not able to validate exits, retrying")
    print("needed loops: ", loop_count, "to validate exits for ")
    return shuffled_entrances, shuffled_exits, spoil_entrances, spoil_entrances_for_spoiler, graph, paths_to_world, world_paths


def get_entrances_exits(world_object, scope, doors_view):
    entrances = []
    exits = []

    if scope == "-doorsrando":
        if isinstance(world_object, list):
            for world in world_object:
                entrances += [list(i) for i in doors_view.find_all(
                    lambda sp: (sp.type == "entrance" or sp.type == "town_building") and sp.world == world)]
                exits += [list(i) for i in
                          doors_view.find_all(
                              lambda sp: (sp.type == "exit" or sp.type == "return") and sp.world == world)]
        else:
            entrances += [list(i) for i in doors_view.find_all(
                lambda sp: (sp.type == "entrance" or sp.type == "town_building") and sp.world == world_object)]
            exits += [list(i) for i in
                      doors_view.find_all(
                          lambda sp: (sp.type == "exit" or sp.type == "return") and sp.world == world_object)]

    else:
        if isinstance(world_object, list):
            for world in world_object:
                entrances += [list(i) for i in doors_view.find_all(
                    lambda sp: (sp.type == "entrance" and sp.map == world) and sp.world == world)]
                exits += [list(i) for i in
                          doors_view.find_all(
                              lambda sp: (sp.type == "exit" and sp.dest == world) and sp.world == world)]
        else:
            entrances += [list(i) for i in doors_view.find_all(
                lambda sp: (sp.type == "entrance" and sp.map == world_object) and sp.world == world_object)]
            exits += [list(i) for i in
                      doors_view.find_all(
                          lambda sp: (sp.type == "exit" and sp.dest == world_object) and sp.world == world_object)]

    return entrances, exits


def return_gated_paths(paths_to_world):
    gated_paths = {}
    for path in paths_to_world:
        gated_by = []
        for entrance in paths_to_world[path]:
            if isinstance(entrance, str):
                entrance_name = entrance

            else:
                entrance_name = entrance[0]
            if not isinstance(entrance_name, str):
                entrance_name_1, entrance_name_2 = entrance_name
                locked_1 = ""
                locked_2 = ""
                try:
                    locked_1 = entrances_locked[entrance_name_1]
                except KeyError:
                    pass  # not gated
                try:
                    locked_2 = entrances_locked[entrance_name_2]
                except KeyError:
                    pass  # not gated

                if locked_1 and locked_2:
                    gated_by.append(locked_1 + "|" + locked_2)

            else:
                try:

                    gated_by.append(entrances_locked[entrance_name])
                except KeyError:
                    pass  # not gated
        gated_paths[path] = gated_by
    return gated_paths


def return_gated_kis(key_items, gated_paths):
    gated_ki = {}
    for i in key_items:
        gated_ki[i] = {}
        gated_ki[i]["and"] = []
        gated_ki[i]["or"] = []
        ki_required_location = ""
        try:
            ki_required_location = key_items[i]["and_location"]
        except:
            pass
        if ki_required_location:
            if ki_required_location:
                for location in ki_required_location:
                    if location != "starting" and location != "None":
                        gated_ki[i]["and"] += gated_paths[location]
                if len(gated_ki[i]["and"]) == 2 and gated_ki[i]["and"][0] == gated_ki[i]["and"][1]:
                    gated_ki[i]["and"] = gated_ki[i]["and"][0]
                if len(gated_ki[i]["and"]) == 1 and gated_ki[i]["and"][0] == "*[#item.Magma]|*[#item.fe_Hook]":
                    gated_ki[i]["and"] = []
                    gated_ki[i]["or"] = [["*[#item.Magma]"], ["*[#item.fe_Hook]"]]
                elif len(gated_ki[i]["and"]) == 2:

                    if gated_ki[i]["and"][0] == "*[#item.Magma]|*[#item.fe_Hook]":
                        gated_ki[i]["or"] += ["*[#item.Magma]", "*[#item.fe_Hook]"]
                        gated_ki[i]["and"] = gated_ki[i]["and"][1]
                    elif gated_ki[i]["and"][1] == "*[#item.Magma]|*[#item.fe_Hook]":
                        gated_ki[i]["or"] += [["*[#item.Magma]"], ["*[#item.fe_Hook]"]]
                        gated_ki[i]["and"] = gated_ki[i]["and"][0]

        else:
            try:
                ki_required_location = key_items[i]["or_location"]
            except:
                continue
            if ki_required_location:
                for location in ki_required_location:
                    gated_ki[i]["or"] += gated_paths[location]
                if len(gated_ki[i]["or"]) < 2:
                    gated_ki[i]["or"] = []

                elif gated_ki[i]["or"][0] == gated_ki[i]["or"][1]:
                    if gated_ki[i]["or"][0] == "*[#item.Magma]|*[#item.fe_Hook]":
                        gated_ki[i]["or"] = [["*[#item.Magma]"], ["*[#item.fe_Hook]"]]
                    else:
                        gated_ki[i]["and"] = [gated_ki[i]["or"][0]]
                    gated_ki[i]["or"] = []

    return gated_ki


def return_gated_slots(key_items, gated_ki):
    gated_slots = {}
    for i in key_items:
        gated_slots[i] = {}

        slot_location = key_items[i]["slot"]
        try:
            ki_required_for_slot = slots_locked[slot_location]
            gated_slots[i]["and"] = [ki_required_for_slot]
            try:
                gated_slots[i]["and"] += gated_ki[ki_required_for_slot]["and"]
            except KeyError:
                pass
        except:
            pass
        if not gated_slots[i]:
            del gated_slots[i]
    return gated_slots


def recursive_spheres(available_ki, locked_stack, ki_full_locked, spheres, current_sphere):
    locked_temp = []
    available_temp = []
    spheres[current_sphere] = []
    temp_array = []
    for i in locked_stack:
        if isinstance(i, list):
            i = i[0]
        temp_array.append(i)

    locked_stack = list(temp_array)
    for i in locked_stack:

        if isinstance(i, list):
            i = i[0]
        ands = ki_full_locked[i]["and"]
        ors = ki_full_locked[i]["or"]
        is_available = True
        if ands:
            temp_array = []
            for j in ands:
                if j and isinstance(j, list):
                    j = j[0]
                temp_array.append(j)

            ands = list(temp_array)

            for ki in ands:
                if ki not in available_ki:
                    is_available = False
                    break

        if ors:
            temp_array = []
            for j in ors:
                if isinstance(j, list) and len(j) == 1:
                    j = j[0]
                temp_array.append(j)
            ors = list(temp_array)
            all_available_parent = []
            for or_path in ors:
                if isinstance(or_path, list):
                    all_available_sub = []
                    for ki in or_path:
                        if isinstance(ki, list) and len(ki) == 1:
                            ki = ki[0]

                        if ki not in available_ki:
                            all_available_sub.append(False)
                    if False in all_available_sub:
                        all_available_parent.append(False)
                    else:
                        all_available_parent.append(True)


                else:
                    if or_path not in available_ki:
                        all_available_parent.append(False)
                    else:
                        all_available_parent.append(True)

            if True not in all_available_parent:
                is_available = False
            else:
                is_available = True
        if is_available:
            spheres[current_sphere].append(i)
            available_temp.append(i)
        else:
            if i not in locked_temp:
                locked_temp.append(i)
    if sorted(locked_temp) == sorted(locked_stack):
        return False
    elif locked_temp:
        current_sphere += 1
        available_ki += available_temp
        return recursive_spheres(available_ki, locked_temp, ki_full_locked, spheres, current_sphere)
    elif not locked_temp:
        return spheres


def calculate_spheres(ki_full_locked):
    spheres = {}
    current_sphere = 0
    spheres[current_sphere] = []
    available_ki = []
    locked_stack = []
    for i in ki_full_locked:
        if not ki_full_locked[i]["and"] and not ki_full_locked[i]["or"]:
            spheres[current_sphere].append(i)
        else:
            locked_stack.append(i)
    available_ki += spheres[current_sphere]
    current_sphere += 1
    is_valid = recursive_spheres(available_ki, locked_stack, ki_full_locked, spheres, current_sphere)
    return is_valid


def normalize_ands_ors(ki_full_locked):
    for i in ki_full_locked:
        ands = ki_full_locked[i]["and"]
        ors = ki_full_locked[i]["or"]
        if ands and ors:
            new_ors = []
            for or_ki in ors:
                new_ors.append(ands + [or_ki])
            ki_full_locked[i]["and"] = []
            ki_full_locked[i]["or"] = new_ors

    return ki_full_locked


def is_omnicraft_blocked(location, paths_to_world):
    if location == "starting":
        return False
    if location == '#DwarfCastle|#DwarfCastleBasement':
        dc = is_omnicraft_blocked("#DwarfCastle", paths_to_world)
        dcb = is_omnicraft_blocked("#DwarfCastleBasement", paths_to_world)
        if dc and dcb:
            return True
        else:
            return False
    if location == '#SylvanCaveYangRoom&#FabulWestTower1F':
        sc = is_omnicraft_blocked("#SylvanCaveYangRoom", paths_to_world)
        fwt = is_omnicraft_blocked("#FabulWestTower1F", paths_to_world)
        if sc and fwt:
            return True
        else:
            return False
    if location == '#SylvanCave1F&#Fabul':
        sc = is_omnicraft_blocked("#SylvanCave1F", paths_to_world)
        fwt = is_omnicraft_blocked("#Fabul", paths_to_world)
        if sc and fwt:
            return True
        else:
            return False
    else:
        world_entrance = paths_to_world[location][0][1][0]
        if isinstance(world_entrance, list):
            blocked_array = []
            for entrance in world_entrance:
                if entrance in omnicraft_locked_locations:
                    blocked_array.append(True)
                else:
                    blocked_array.append(False)
            if False in blocked_array:
                return False
        else:
            if world_entrance not in omnicraft_locked_locations:
                return False

    return True

def return_all_required_ki(key_item,key_items,slots_locked):
    ki_locking=[]

    while True:
        ki_slot = key_items[key_item]["slot"]

        if ki_slot in slots_locked:
            key_item = slots_locked[ki_slot]
            ki_locking.append(key_item)
        else:
            break

    return ki_locking

def check_underworld(key_items, paths_to_world, gated_paths, world_paths, scope):
    magma = True
    tower = True
    hook = True

    magma_location = key_items['*[#item.Magma]']["location"]
    tower_key_location = key_items['*[#item.Tower]']["location"]
    darkness_location = key_items['*[#item.DarkCrystal]']["location"]

    magma_slot = key_items['*[#item.Magma]']["slot"]
    tower_key_slot = key_items['*[#item.Tower]']["slot"]

    magma_slot_locked_ki = return_all_required_ki('*[#item.Magma]',key_items,slots_locked)
    magma_slot_locked_locations = []
    for ki in magma_slot_locked_ki:
        magma_slot_locked_locations.append(key_items[ki]["location"])

    tower_key_slot_locked_ki = return_all_required_ki('*[#item.Tower]',key_items,slots_locked)
    tower_key_slot_locked_locations = []
    for ki in tower_key_slot_locked_ki:
        tower_key_slot_locked_locations.append(key_items[ki]["location"])

    darkness_underground = True if darkness_location not in world_paths["#Overworld"] \
                                   and darkness_location not in world_paths["#Moon"] else False
    tower_key_underground = True if tower_key_location not in world_paths["#Overworld"] \
                                    and tower_key_location not in world_paths["#Moon"] else False
    magma_underground = True if magma_location not in world_paths["#Overworld"] \
                                and magma_location not in world_paths["#Moon"] else False

    tower_key_locked_underground = False
    for ki_location in tower_key_slot_locked_locations:
        if ki_location not in world_paths["#Overworld"] and ki_location not in world_paths["#Moon"]:
            tower_key_locked_underground=True
            break

    magma_locked_underground = False
    for ki_location in magma_slot_locked_locations:
        if ki_location not in world_paths["#Overworld"] and ki_location not in world_paths["#Moon"]:
            magma_locked_underground = True
            break

    damcyan_underground = True if "UNDERWORLD" in gated_paths['#Damcyan'] else False

    magma_moon = True if magma_location not in world_paths["#Overworld"] \
                         and magma_location not in world_paths["#Underworld"] else False
    tower_key_moon = True if tower_key_location not in world_paths["#Overworld"] \
                             and tower_key_location not in world_paths["#Underworld"] else False


    tower_key_locked_moon = False
    for ki_location in tower_key_slot_locked_locations:
        if ki_location not in world_paths["#Overworld"] and ki_location not in world_paths["#Underworld"]:
            tower_key_locked_moon=True
            break

    magma_locked_moon  = False
    for ki_location in magma_slot_locked_locations:
        if ki_location not in world_paths["#Overworld"] and ki_location not in world_paths["#Underworld"]:
            magma_locked_moon = True
            break


    damcyan_moon = True if '*[#item.DarkCrystal]' in gated_paths['#Damcyan'] else False
    mysidia_moon = True if '*[#item.DarkCrystal]' in gated_paths['#Mysidia'] else False
    mysidia_underground = True if 'UNDERWORLD' in gated_paths['#Mysidia'] else False

    well_entrance = '#AgartWell' if scope == "-doorsrando" else "#Agart"
    hook_route_entrance = '#BabilB1' if scope == "-doorsrando" else "#CaveEblanEntrance"

    if is_omnicraft_blocked(darkness_location, paths_to_world) and damcyan_moon:
        print("Damcyan is on the moon and Darkness is omnicraft locked")
        return False

    if mysidia_moon:
        print("Mysidia is on the moon, so locking itself")
        return False

    while magma:
        if (well_entrance in world_paths['#Underworld'] or magma_underground or magma_locked_underground) \
                or ((well_entrance in world_paths['#Moon'] or magma_moon or magma_locked_moon) and (
                darkness_underground or mysidia_underground)):
            magma = False
            break
        if (is_omnicraft_blocked(well_entrance, paths_to_world)
            or is_omnicraft_blocked(magma_location, paths_to_world)) and \
                (damcyan_underground or (damcyan_moon and darkness_underground)):
            magma = False
            break
        magma = True
        break

    while tower:
        if ("#Babil1F" in world_paths['#Underworld'] or tower_key_underground or tower_key_locked_underground) \
                or (("#Babil1F" in world_paths['#Moon'] or tower_key_moon or tower_key_locked_moon) and (
                darkness_underground or mysidia_underground)):
            tower = False
            break
        if (is_omnicraft_blocked('#Babil1F', paths_to_world)
            or is_omnicraft_blocked(tower_key_location, paths_to_world)) and \
                (damcyan_underground or (damcyan_moon and (darkness_underground or mysidia_underground))):
            tower = False
            break
        tower = True
        break
    while hook:
        if (hook_route_entrance in world_paths['#Underworld']) \
                or (hook_route_entrance in world_paths['#Moon'] and (darkness_underground or mysidia_underground)):
            hook = False
            break

        if is_omnicraft_blocked(hook_route_entrance, paths_to_world) and \
                (damcyan_underground or (damcyan_moon and (darkness_underground or mysidia_underground))):
            hook = False
            break
        hook = True
        break

    if not magma and not tower and not hook:
        return False

    if hook:
        return []
    gated = []
    if magma:
        gated_magma = []
        gated_magma += gated_paths[magma_location]
        gated_magma += gated_paths[well_entrance]
        if not gated_magma:
            return []
        else:
            gated.append("&".join(gated_magma))
    if tower:
        gated_tower = []
        gated_tower += gated_paths[tower_key_location]
        gated_tower += gated_paths["#Babil1F"]
        if not gated_tower:
            return []
        else:
            gated.append("&".join(gated_tower))

    return "|".join(gated)


def check_logic(key_items, paths_to_world, world_paths, scope):
    gated_paths = return_gated_paths(paths_to_world)
    underworld_required_ki = check_underworld(key_items, paths_to_world, gated_paths, world_paths, scope)
    if underworld_required_ki is False:
        return False
    elif underworld_required_ki:
        if underworld_required_ki == ['UNDERWORLD']:
            return False

        print("Underground is actually locked by something", underworld_required_ki)
    for i in gated_paths:
        if len(gated_paths[i]) > 1:
            for num, path in enumerate(gated_paths[i]):
                if path == 'UNDERWORLD':
                    gated_paths[i][num] = underworld_required_ki
            if gated_paths[i] == [[], []]:
                gated_paths[i] = []
        elif gated_paths[i] == ['UNDERWORLD']:
            gated_paths[i] = underworld_required_ki
    entrances_locked["#Underworld"] = underworld_required_ki
    gated_ki = return_gated_kis(key_items, gated_paths)
    gated_slots = return_gated_slots(key_items, gated_ki)

    ki_full_locked = {}
    for i in key_items:
        ki_full_locked[i] = {"and": [], "or": []}
        if i in gated_ki:
            try:
                ki_full_locked[i]["and"] += gated_ki[i]["and"]
            except:
                pass
            try:
                ki_full_locked[i]["or"] += gated_ki[i]["or"]
            except:
                pass

        if i in gated_slots:
            ki_full_locked[i]["and"] += gated_slots[i]["and"]

    ki_full_locked = normalize_ands_ors(ki_full_locked)
    # for i in ki_full_locked:
    #     print(i,ki_full_locked[i])
    return calculate_spheres(ki_full_locked)


def add_doors_paths_entrancerando(paths_to_world):
    paths_to_world['#RoomToSewer'] = paths_to_world['#BaronTown']
    paths_to_world['#SylvanCaveYangRoom'] = paths_to_world['#SylvanCave1F']
    return paths_to_world


def apply(env, randomize_scope, randomize_type, testing=False):
    doors_view = databases.get_doors_dbview()
    non_random_locations=[]
    if randomize_scope == "-doorsrando":
        non_random_locations = [list(i) for i in doors_view.find_all(lambda sp: (sp.type == "non_randomized"))]

        non_random_normalized_location = []
        for i in non_random_locations:
            non_random_normalized_location.append([i[0], i[1], i[2], i[3], i[8], i[4], i[5], i[6], i[7]])

        non_random_locations = list(non_random_normalized_location)
    print(f"Rando type is {randomize_type}")
    # randomize_type = "gated"
    if randomize_type == "normal":
        worlds = ["#Overworld", "#Underworld", "#Moon"]
    elif randomize_type == "blue_planet":
        worlds = [["#Overworld", "#Underworld"], "#Moon"]
    elif randomize_type == "gated":
        worlds = ["#Overworld", ["#Underworld", "#Moon"]]
    elif randomize_type == "why":
        worlds = [["#Overworld", "#Moon"], "#Underworld"]
    elif randomize_type == "all":
        worlds = [["#Overworld", "#Underworld", "#Moon"]]
    else:
        worlds = ["#Overworld", "#Underworld", "#Moon"]
    attempts = 0
    while True:
        if attempts >= 200:
            return False
        shuffled_entrances = []
        shuffled_exits = []
        spoil_entrances = []
        spoil_entrances_for_spoiler = []
        graph = {}
        paths_to_world = {}
        world_paths = {}
        for i in worlds:
            entrances, exits = get_entrances_exits(i, randomize_scope, doors_view)
            shuffled_entrances_temp, shuffled_exits_temp, spoil_entrances_temp, spoil_entrances_for_spoiler_temp, graph_temp, paths_to_world_temp, world_paths_temp = randomize_doors(
                env, entrances, exits,randomize_scope)
            shuffled_entrances += shuffled_entrances_temp
            shuffled_exits += shuffled_exits_temp
            spoil_entrances += spoil_entrances_temp
            spoil_entrances_for_spoiler += spoil_entrances_for_spoiler_temp
            graph.update(graph_temp)
            paths_to_world.update(paths_to_world_temp)
            world_paths.update(world_paths_temp)

        # if randomize_scope == "-entrancesrando":
        #     for i in
        #     door_to_entrance =
        #     paths_to_world = add_doors_paths_entrancerando(paths_to_world)

        # print([(i, str(env.assignments[i])) for i in env.assignments])
        key_items = {}
        for x in env.assignments:
            # to update if/when gated objectives can be handled logically 
            # flagsetcore.py should be updated to allow this combo
            if x == RewardSlot.gated_objective:
                continue
            if "*" in str(env.assignments[x]) and "[#item.Crystal]" not in str(env.assignments[x]):
                key_items[str(env.assignments[x])] = {"location": REWARDS_LOCATIONS[randomize_scope][x], "slot": x}

        miab_locations_sylph = [i for i in env.meta["miab_locations"] if
                                env.meta["miab_locations"][i][0] == "#SylvanCaveYangRoom"]
        for i in key_items:
            if key_items[i]["slot"] in miab_locations_sylph and randomize_scope == "-doorsrando":
                key_items[i]["location"] = "#SylvanCaveYangRoom"
        no_free_flags = [str(x) for x in env.options.flags._flags if "Knofree" in x]
        for item in key_items:
            ki_required_room = key_items[item]["location"]
            ki_slot = key_items[item]["slot"]
            if ki_slot == RewardSlot.rydias_mom_item:
                if no_free_flags[0] == "Knofree":
                    dmist_slot = [str(x) for x in env.assignments if str(env.assignments[x]) == "dmist"][0]
                    ki_required_room += f"&{slot_locations[randomize_scope][dmist_slot]}"
                if no_free_flags[0] == 'Knofree:package':
                    ki_required_room += f"&{key_items['*[#item.Package]']['location']}"
            if ki_required_room == "starting":
                key_items[item]["and"] = None
                key_items[item]["and_location"] = None
                continue
            if ki_required_room == "#Mist&#DwarfCastle|#DwarfCastleBasement":
                key_items[item]["or"] = ['#DwarfCastle', '#DwarfCastleBasement']
                key_items[item]["and"] = ['#Mist']
            elif '|' in ki_required_room:
                key_items[item]["or"] = []

                ki_required_room = ki_required_room.split("|")
                key_items[item]["or_location"] = ki_required_room
                for room in ki_required_room:
                    key_items[item]["or"] += paths_to_world[room]

            elif '&' in ki_required_room:
                key_items[item]["and"] = []

                ki_required_room = ki_required_room.split("&")
                key_items[item]["and_location"] = ki_required_room
                for room in ki_required_room:
                    if room != "None" and room != "starting":
                        key_items[item]["and"] += (paths_to_world[room])

            else:
                key_items[item]["and"] = paths_to_world[ki_required_room]
                key_items[item]["and_location"] = [ki_required_room]
        is_valid = check_logic(key_items, paths_to_world, world_paths, randomize_scope)
        if not is_valid:
            attempts += 1
        else:
            #print(f"Needed {attempts + 1} attempts for KI to be available")
            #print(is_valid)
            break
    #
    # for i in key_items:
    #     print(i, key_items[i])
    # for path in paths_to_world:
    #     print(path,paths_to_world[path])
    remapped_ = []
    remapped_spoiled = []
    special_triggers = []
    remapped_ += shuffled_entrances + shuffled_exits + non_random_locations
    remapped_spoiled += spoil_entrances
    script = ""

    for index, i in enumerate(remapped_):
        # Ok, so this is a big ugly hack to stick a lookup index into the trigger data
        # without breaking the compilation process.
        # We use a special map id to indicate that the trigger should be overridden.
        # (we TRIED using the apparently unused "#CurrentMap" ($FE), but it turns out $FE
        #  has a special meaning for the compiler, indicating a treasure trigger)
        # Because we're relying on the compiler, we only get 6 bits for the target's X
        # coord, so we put the high byte in there and the low byte in the target's Y coord.
        # In the long run, we'd probably want to manually override the trigger data,
        # rather than hacking around the f4c compiler.
        script += (
            f'trigger({i[0]} {i[1]}) {{\n'
            f'position {i[2]} {i[3]}\n'
            f'teleport #EndingFabulThroneRoom at {index >> 8} {index & 0xFF}'
        )

        x_coord = i[6]
        if i[5] not in ["#Overworld", "#Underworld", "#Moon"]:
            x_coord |= (DIRECTION_MAP[i[8]] << 6)
        script += f'  // [${index:04X}] {i[5]} at {i[6]} {i[7]}\n'
        script += f'facing up'
        script += '}\n\n'
        special_triggers.append(f"##map.{i[5][1:]} {x_coord:X} {i[7]:X}")
        # print(script)

    bytes_used = len(special_triggers) * 4

    # for item in key_items:
    #     print(item, key_items[item])

    return2teleport = ["mapgrid ($04 17 31) { 7C }",  # Silvera return tile to trigger tile
                       "mapgrid ($05 16 29) { 7C }",  # Tororia return tile to trigger tile
                       "mapgrid ($06 15 31) { 7C }",  # Agart return tile to trigger tile
                       "mapgrid ($06 16 31) { 7C }",  # Agart return tile to trigger tile
                       "mapgrid ($06 17 31) { 7C }",  # Agart return tile to trigger tile
                       "mapgrid ($136 17 9) { 72 }",  # CaveOfSummons1F return tile to trigger tile
                       "mapgrid ($145 16 1) { 72 }",  # Sylph Cave return tile to trigger tile
                       "mapgrid ($160 16 29) { 6E }",  # Lunar Palace Lobby return tile to trigger tile
                       ]
    return2teleport_doorsonly = ["mapgrid ($137 4 18) { 72 }",  # CaveOfSummons2F return tile to trigger tile
                                 "mapgrid ($138 11 1) { 72 }",  # CaveOfSummons3F return tile to trigger tile
                                 "mapgrid ($13A 12 14) { 25 }",  # Feymarch 1F return tile to trigger tile
                                 "mapgrid ($13B 16 21) { 25 }",  # Feymarch treasury return tile to trigger tile
                                 "mapgrid ($13B 16 24) { 51 }",  # Feymarch treasury removing exit tile
                                 "mapgrid ($13C 28 11) { 25 }",  # Feymarch 2F return tile to trigger tile
                                 "mapgrid ($145 16 27) { 72 }",  # Sylph Cave 1F return tile to trigger tile
                                 "mapgrid ($146 6 26) { 72 }",  # Sylph Cave 2F return tile to trigger tile
                                 "mapgrid ($146 17 17) { 72 }",  # Sylph Cave 2F return tile to trigger tile
                                 "mapgrid ($147 5 6) { 72 }",  # Sylph Cave 3F return tile to trigger tile
                                 "mapgrid ($149 11 10) { 70 }",  # Sylph Yang Room removing exit tile
                                 "mapgrid ($149 9 4) { 23 }",  # Sylph Yang room return tile to trigger tile
                                 ]

    for i in return2teleport:
        env.add_script(i)
    if randomize_scope == "-doorsrando":
        for i in return2teleport_doorsonly:
            env.add_script(i)

    env.add_script(script)
    special_triggers_script = '\n'.join(special_triggers)
    env.add_script(f'patch($21e000 bus) {{\n{special_triggers_script}\n}}')

    if randomize_scope == "-doorsrando":
        randomized_sprite='''npc(#LockedDoorWaterway)
        {
            // %weird_sprite waterway_door%
            // %end%
        
            eventcall {
                $1F   //Unlock the Waterway door
            }
        }
        '''
        env.add_script(randomized_sprite)
        name = "waterway_door"
        sprite = env.rnd.choice(NON_PLAYER_SPRITES)
        env.add_substitution(f'weird_sprite {name}', 'sprite ${:02X}'.format(sprite['npc_sprite']))
    # print(script)

    towns_map = []
    other_entrances = []
    for i in sorted(remapped_spoiled):
        istown = ""
        for j in towns_flat:
            if i.startswith(j + " is in"):
                istown = True
                break
        if istown:
            towns_map.append(i)
        else:
            other_entrances.append(i)

    # print("\n".join(["", "", "", ] + towns_map + ["", "", "", ] + other_entrances))
    env.spoilers.add_table("Entrance Randomization\nLocation X is in Entrance Y", sorted(spoil_entrances_for_spoiler),
                           public=env.options.flags.has_any('-spoil:all', '-spoil:misc'), ditto_depth=1)

    return bytes_used


if __name__ == '__main__':
    import random


    class Environment:
        def __init__(self):
            self.rnd = random.Random()


    apply(Environment(), None, True)
