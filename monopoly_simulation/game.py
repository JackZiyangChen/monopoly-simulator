import json
import random
import os
from pathlib import Path
from . import utility as util
from .player import Player
from .utility import Trade
from .tile import *





class GameState:
    players = []
    tiles = []
    eliminated_players = []
    houses_remaining = 32
    hotels_remaining = 12
    round = 0

    CHANCES_DICT = {}
    COMMUNITY_CHEST_DICT = {}

    chances_queue = []
    chances_queue_top = 0
    community_chest_queue = []
    community_chest_queue_top = 0

    in_game = True



    def __init__(self, players):
        self.players = players

        self.tiles = []
        self.eliminated_players = []
        self.houses_remaining = 32
        self.hotels_remaining = 12
        self.round = 0

        self.CHANCES_DICT = {}
        self.COMMUNITY_CHEST_DICT = {}

        self.chances_queue = []
        self.chances_queue_top = 0
        self.community_chest_queue = []
        self.community_chest_queue_top = 0

        self.initialize_tiles()
        self.initialize_drawables()


    def __dict__(self):
        out = {'in_game': self.in_game, 'round': self.round, 'houses_remaining': self.houses_remaining,
               'hotels_remaining': self.hotels_remaining}

        tiles_dict = {}
        for t in self.tiles:
            tile = {}
            tile['name'] = t.name
            tile['type'] = t.__class__.__name__
            tiles_dict[str(t.position)] = tile
        out['tiles'] = tiles_dict


        properties_dict = {}
        for property in self.tiles:
            if isinstance(property,Property):
                if property.set not in properties_dict.keys():
                    properties_dict[property.set] = {}
                properties_dict[property.set][property.name] = property.property_info(game_state=self)
        out['properties'] = properties_dict


        players_dict = {'active_players':{},'eliminated_players':{}}
        for p in self.players:
            players_dict['active_players'].update({f'{str(p.id)}': p.player_info()})
        for p in self.eliminated_players:
            players_dict['eliminated_players'].update({f'{str(p.id)}': p.player_info()})
        out['players'] = players_dict


        drawable_dict = {}
        chances_dict = {}
        community_chests_dict = {}

        chances_queue = [self.chances_queue[(i+self.chances_queue_top)%len(self.chances_queue)]
                         for i in range(len(self.chances_queue))]

        for i in range(len(chances_queue)):
            chances_dict[str(i)] = chances_queue[i]
        drawable_dict['chances'] = chances_dict

        community_chests_queue = [self.community_chest_queue[(i + self.community_chest_queue_top) % len(self.community_chest_queue)]
                         for i in range(len(self.community_chest_queue))]

        for i in range(len(community_chests_queue)):
            community_chests_dict[str(i)] = community_chests_queue[i]
        drawable_dict['community_chests'] = community_chests_dict

        out['drawable'] = drawable_dict

        return out


    def from_json_file(self, file_name):
        curr_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
        with open(os.path.join(curr_dir, file_name), "r") as source_file:
            src_dict = json.load(source_file)

        self.from_json(src_dict)

    def from_json(self, src_dict):

        self.in_game = src_dict['in_game']
        self.round = src_dict['round']
        self.houses_remaining = src_dict['houses_remaining']
        self.hotels_remaining = src_dict['hotels_remaining']

        local_active_players = {}
        for p in self.players:
            local_active_players[str(p.id)] = p

        active_players = src_dict['players']['active_players']
        for k,v in active_players.items():
            local_active_players[k].from_json(v, self.tiles)

        local_eliminated_players = {}
        for p in self.players:
            local_eliminated_players[str(p.id)] = p

        eliminated_players = src_dict['players']['eliminated_players']
        for k, v in eliminated_players.items():
            local_eliminated_players[int(k)].from_json(v, self.tiles)


        local_tiles_info = {}
        for t in self.tiles:
            local_tiles_info[t.name] = t

        properties = src_dict['properties']
        for s in properties.values():
            for k,v in s.items():
                local_tiles_info[k].from_json(v,self.players)

        

        drawable = src_dict['drawable']
        self.chances_queue_top = self.chances_queue.index(
            drawable['chances'][min(drawable['chances'].keys())])
        self.community_chest_queue_top = self.community_chest_queue.index(
            drawable['community_chests'][min(drawable['community_chests'].keys())])






        



    def initialize_tiles(self):
        map_data = {}
        tile_to_add = Tile()
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(curr_dir, "setting/map.json"), "r") as map_file:
            map_data = json.load(map_file)
            with open(os.path.join(curr_dir, "setting/tilesinfo.json"), "r") as tilesinfo:
                tiles_database = json.load(tilesinfo)
                for i in range(0, 40):
                    if map_data[str(i)] not in tiles_database.keys():
                        tile_to_add = Tile()
                        tile_to_add.name = map_data[str(i)]
                        tile_to_add.position = i
                        self.tiles.append(tile_to_add)
                        continue
                    tile_info = tiles_database[map_data[str(i)]]
                    type = tile_info['type']
                    # switch on type
                    if type == 'jail':
                        tile_to_add = Jail()
                    elif type == 'street':
                        tile_to_add = Street()

                        tile_to_add.set = tile_info['set']
                        tile_to_add.price = tile_info['price']
                        tile_to_add.base_rent = tile_info['base_rent']
                        tile_to_add.premium_rents = tile_info['premium_rent']
                        tile_to_add.housing_cost = tile_info['housing_cost']
                        tile_to_add.mortgage = tile_info['mortgage']

                    elif type == 'railroad' or type == 'utility':
                        tile_to_add = PublicProperty()

                        tile_to_add.set = tile_info['set']
                        tile_to_add.price = tile_info['price']
                        tile_to_add.mortgage = tile_info['mortgage']
                    elif type == 'chance' or type == 'community chest':
                        tile_to_add = Drawable()

                        tile_to_add.drawable_type = type
                    elif type == 'tax':
                        tile_to_add = Tax()

                        tile_to_add.tax = tile_info['tax']
                    else:
                        tile_to_add = Tile()

                    tile_to_add.name = map_data[str(i)]
                    tile_to_add.position = i

                    self.tiles.append(tile_to_add)

        # sort through tiles list
        self.tiles.sort(key=lambda tile: tile.position)
        prop_id_counter  = 0
        for prop in self.tiles:
            if isinstance(prop, Property):
                prop.id = prop_id_counter
                prop_id_counter += 1

    def initialize_drawables(self):
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(curr_dir, "setting/drawables.json"), "r") as source_file:
            src_dict = json.load(source_file)

        for k,v in src_dict.items():
            if v['type'] == 'community chest':
                self.COMMUNITY_CHEST_DICT[k] = v
                self.community_chest_queue.append(k)
            elif v['type'] == 'chance':
                self.CHANCES_DICT[k] = v
                self.chances_queue.append(k)

        random.shuffle(self.chances_queue)
        random.shuffle(self.community_chest_queue)






def initialize_game(players_list):
    # initialize game and players

    # determine player order
    for p in players_list:
        p.init_roll = dice_roll() + dice_roll()
        p.money = 1500

    players_list.sort(key=lambda player: player.init_roll, reverse=True)

    gs = GameState(players=players_list)

    gs.players = players_list
    i = 0
    for player in gs.players:
        player.id = i
        i += 1

    return gs



def game(number_of_players,**kwargs):


    players_list = kwargs.get('players') if 'players' in kwargs.keys() else []
    for i in range(abs(number_of_players - len(players_list))):
        players_list.append(Player())


    gs=initialize_game(players_list) # initialize game state

    turn_player = 0

    # while game
    while gs.in_game and gs.round < 500:

        housing_round(random.shuffle(gs.players.copy),game_state=gs)
        # trade(state=gs) # handle trade
        # TODO: handle mortgage and un-mortgage (latter is very important)

        # play turn
        turn(gs.players[turn_player], state=gs, repeat_round=0)


        # switch player
        turn_player = (turn_player + 1) % len(gs.players)
        if turn_player == 0: gs.round += 1



def turn(player, state, repeat_round):
    if repeat_round > 2:
        # move to jail
        player.location = 10
        player.rounds_in_jail = 3
        return

    # handle jail
    if player.rounds_in_jail>0:
        # check if eligible to get out
        player.jail_round()
        player.rounds_in_jail -= 1

    if player in state.eliminated_players:
        return

    # roll dice
    rolls = [dice_roll(),dice_roll()]
    moves = rolls[0] + rolls[1]

    # move
    player.location = player.location+moves
    if player.location > 39: # passed Go
        player.money += 200
        player.location = player.location%40

    state.tiles[player.location].round_action(game_state=state, moves=moves)

    if player.money<0:
        player.on_debt(amount=0-player.money) # TODO: replace with tested payment method


    if rolls[0] == rolls[1]:
        turn(player, state, repeat_round=repeat_round+1)




def dice_roll():
    return random.randint(1,6)



def housing_round(participating_players, game_state):
    for player in participating_players:
        eligible_tiles = player.get_all_eligible_housing_tiles()
        sets = []
        if len(eligible_tiles) == 0:
            continue

        for tile in eligible_tiles:
            if any([tile in s for s in sets]):
                continue
            sets.append(tile.get_others_in_set(game_master=game_state).append(tile))

        for street_set in sets:
            total_possible = len(street_set) * 5
            curr_houses = 0
            for p in street_set:
                curr_houses += p.houses
            max_to_build = total_possible - curr_houses
            max_can_afford = player.money // street_set[0].housing_cost
            num_houses_to_build = player.build_houses_handler(max_houses=min(max_to_build,max_can_afford),
                                                              state=game_state)

            if num_houses_to_build > game_state.houses_remaining:
                num_houses_to_build = game_state.houses_remaining - 1
                house_bidders = []
                for potential_bidder in participating_players:
                    if potential_bidder.build_houses_handler(max_houses=2,state=game_state):
                        house_bidders.append(potential_bidder)
                winner = utility.auction(participants=house_bidders,minimum_bid=10)
                # TODO: question: what to do with where to build?

            total_cost = 0
            street_set.sort(key=lambda prop_in_set:prop_in_set.houses)
            for i in range(num_houses_to_build):
                street_set[i%len(street_set)].houses += 1
                game_state.houses_remaining -= 1
                if street_set[i%len(street_set)].houses > 4 and game_state.hotels_remaining>0:
                    street_set[i%len(street_set)].hotel += 1
                    street_set[i % len(street_set)].houses = 0
                    game_state.houses_remaining += 4
                    game_state.hotels_remaining -= 1
                total_cost += street_set[i%len(street_set)].housing_cost

            if not utility.payment(player, 'bank',game_state,total_cost):
                on_player_bankruptcy(player=player, game_state=game_state, debt_holder='bank')



def trade(state):
    MAX_TRADE_ATTEMPTS_PER_ROUND = 7
    for player in state.players:
        i=0
        trade_attempt = player.trade_handler(state=state)
        while i<MAX_TRADE_ATTEMPTS_PER_ROUND and len(trade_attempt)>0:
            if trade_attempt.target_player.accpet_trade(trade_attempt):
                trade_attempt.execute(game_state=state)
            trade_attempt = player.trade_handler(state=state)
            i+=1



def on_player_bankruptcy(player,debt_holder,game_state):

    if isinstance(debt_holder,Player):
        for prop in player.properties_owned:
            prop.owner = debt_holder
            debt_holder.properties_owned.append(prop)
            if prop.is_mortgaged:
                debt_holder.unmortgage_handler(property_to_unmortgage=prop, state=game_state)
            while prop.houses > 0:
                prop.houses -= 1
                game_state.houses_remaining += 1
            while prop.hotel > 0:
                prop.hotel -= 1
                game_state.hotels_remaining += 1

    else:
        remainder_players = []
        for pl in game_state.players:
            if pl.id != player.id: remainder_players.append(pl)
        for p in player.properties_owned:
            p.is_mortgaged = False
            p.is_owned = False
            p.owner = None
            utility.auction(participants=remainder_players,minimum_bid=p.price)

    game_state.eliminated_players.append(player)
    game_state.players.remove(player)
    if len(game_state.players) == 0: # game ends
        game_state.in_game = False








