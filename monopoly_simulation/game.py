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


    def __init__(self, players):
        self.players = players
        self.initialize_tiles()
        self.initialize_drawables()


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

    def initialize_drawables(self):
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(curr_dir, "setting/drawables.json"), "r") as source_file:
            src_dict = json.load(source_file)

        for k,v in src_dict.items():
            if v['type'] == 'community_chest':
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


    players_list = kwargs.get('../players') if 'players' in kwargs.keys() else []
    for i in range(abs(number_of_players - len(players_list))):
        players_list.append(Player())


    gs=initialize_game(players_list) # initialize game state

    in_game = True
    turn_player = 0

    # while game
    while(in_game):
        for p in gs.players:
            p.player_action() # TODO: use specific functions for specific player action (e.g. trading)
        # play turn
        turn(gs[turn_player], state=gs, repeat_round=0)

        # trade
        trade(state=gs)

        # switch player
        turn_player = (turn_player + 1) % len(gs.players)
        gs.round += 1



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
        player.on_debt(amount=0-player.money)


    if rolls[0] == rolls[1]:
        turn(player, state, repeat_round=repeat_round+1)




def dice_roll():
    return random.randint(1,6)



def buy_houses(participating_players):
    # TODO: implement buy houses
    for player in participating_players:
        pass # prompt if buying houses


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









