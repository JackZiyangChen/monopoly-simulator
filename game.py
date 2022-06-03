import random


def game():

    # initialize game and players

    # while game
        # play turn
        # switch player

    pass


def turn(player):
    # handle jail

    # handle housing

    # roll dice
    moves = dice_roll()
    # move
    player.location = (player.location+moves)%40

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
    return random.randint(2,12)