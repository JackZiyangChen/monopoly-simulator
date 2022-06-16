from monopoly_simulation import game,player,tile,utility
import json


def properties_load_test(game_state):
    gs = game_state
    tile_list = gs.tiles
    output = open('sample_tiles_output.json','w')
    for t in tile_list:
        json.dump(t.__dict__, output,indent=6)
    output.close()


if __name__ == '__main__':
    players_list = [player.Player() for i in range(4)]


    gs = game.initialize_game(players_list)

    properties_load_test(game_state=gs)

