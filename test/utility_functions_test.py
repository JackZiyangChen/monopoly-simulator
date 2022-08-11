from monopoly_simulation import game, player, tile, utility

'''
    methods to test:
        game.py:
        player.py: get_all_eligible_housing_tile()
        tile.py: get_others_in_set()
        utility.py: payment(), auction() Trade
'''


def get_in_set_test(game_state):
    prop_set = game_state.tiles[5].get_others_in_set(game_master=game_state) # SUCCESS
    prop_set.append(game_state.tiles[5])
    print([str(p) for p in prop_set])


def payment_test(game_state):
    p1 = game_state.players[0]
    p2 = game_state.players[1]
    p1.money = 500
    p2.money = 700

    # case 1
    utility.payment(provider=p2, receiver=p1,game_state=game_state,amount=200) # SUCCESS
    print(f'player 1 money: {p1.money}\nplayer 2 money: {p2.money}')

    # case 2
    if not utility.payment(provider=p1, receiver=p2,game_state=game_state,amount=800): # SUCCESS
        print("bankruptcy triggered")
        game.on_player_bankruptcy(p1,p2,game_state) # SUCCESS
    print(f'player 1 money: {p1.money}\nplayer 2 money: {p2.money}')
    print(f'eliminated players:{[p.id for p in game_state.eliminated_players]}')

    # case 3: payment can be paid using mortgage


def auction_test(game_state):
    participants = [game_state.players[i] for i in range(len(game_state.players))]
    winner = utility.auction(participants, 10)
    winner.money += 20


if __name__ == '__main__':
    game_state = game.GameState([player.Player() for i in range(4)])

    payment_test(game_state)
    get_in_set_test(game_state)
    # auction_test(game_state)
    print('done')
    

