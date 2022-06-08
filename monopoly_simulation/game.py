import json
import random
from . import tile,player
from . import utility as util


def game(**kwargs):

    # initialize game and players
    gs = GameState()

    # determine player order

    in_game = True
    turn_id = 0

    # while game
    while(in_game):
        for p in gs.players:
            p.player_action()
        # play turn
        turn(player.Player(), state=gs, repeat_round=0)
        # switch player
        turn_id = turn_id + 1 % len(gs.players)



def turn(player, state, repeat_round):
    if repeat_round > 2:
        # move to jail
        return

    # handle jail
    if player.rounds_in_jail>0:
        # check if eligible to get out
        player.jail_round()
        player.rounds_in_jail -= 1

    if player in state.eliminated_players:
        return


    # handle housing

    # roll dice
    rolls = [dice_roll(),dice_roll()]
    moves = rolls[0] + rolls[1]

    # move
    player.location = player.location+moves
    if player.location > 39: # passed Go
        player.money += 200
        player.location = player.location%40

    state.tiles[player.location].round_action(game_state=state)

    if rolls[0] == rolls[1]:
        turn(player, state, repeat_round=repeat_round+1)




def dice_roll():
    return random.randint(1,6)



def buy_houses(participating_players):
    for player in participating_players:
        pass # prompt if buying houses





class GameState:
    players = []
    tiles = []
    eliminated_players = []
    houses_remaining = 32
    hotels_remaining = 12
    round = 0

    def __init__(self, players):
        self.players = players
        map_data = {}
        with open("setting/maps.json", "r") as map_file:
            map_data = json.load(map_file)
            with open("setting/tilesinfo.json", "r") as tilesinfo:
                tiles_database = json.load(tilesinfo)
                for i in range(0,40):
                    tile = tiles_database[map_data[str(i)]]
                    # switch on type


