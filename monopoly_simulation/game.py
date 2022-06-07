import json
import random
from . import tile,player
from . import utility as util


def game(**kwargs):

    # initialize game and players
    gs = GameState()

    # while game
    # play turn
    turn(player.Player(), gs)
    # switch player



def turn(player, state):
    # handle jail
    if player.in_jail:
        # check if eligible to get out
        player.rounds_in_jail -= 1


    # handle housing

    # roll dice
    rolls = [dice_roll(),dice_roll()]
    moves = rolls[0] + rolls[1]

    # move
    player.location = (player.location+moves)%40

    state.tiles[player.location].round_action(game_state=state)




    # action
        # if housing
            # check if bought: what are the rents
            # else ask if want to buy
        # if special card:
            # railroad
            # utility
        # if land in jail
        # if


    pass


def dice_roll():
    return random.randint(1,6)


def buy_houses(participating_players):
    for player in participating_players:
        pass # prompt if buying houses





class GameState:
    players = []
    tiles = []
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


