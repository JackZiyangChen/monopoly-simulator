from .player import Player


def auction(participants, minimum_bid):
    max = minimum_bid
    bid_list = []
    for i in range(len(participants)):
        bid = participants[i].place_bid()
        if bid <= max:
            participants.remove(i)
        else:
            bid_list[i] = bid

    if len(participants) == 1:
        return participants[0]
    else:
        return auction(participants=participants, minimum_bid=max)


class Trade:
    money_placed = 0
    properties_placed = []

    properties_wants = []
    money_wants = 0

    proposing_player = Player()
    target_player = Player()

    def execute(self, game_state):
        buy_id = self.target_player.id
        sell_id = self.proposing_player.id
        from_player = game_state.players[sell_id]
        to_player = game_state.players[buy_id]

        from_player.money -= self.money_placed + self.money_wants
        to_player.money += self.money_placed - self.money_wants

        to_player.properties_owned.extend(self.properties_placed)
        for prop in self.properties_placed:
            from_player.properties_owned.remove(prop)

        from_player.properties_owned.extend(self.properties_wants)
        for prop in self.properties_wants:
            to_player.properties_owned.remove(prop)



