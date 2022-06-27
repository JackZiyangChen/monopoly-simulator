import builtins

from .player import Player


def auction(participants, minimum_bid, **kwargs):
    if len(participants) == 1:
        return participants[0]
    max_bid = minimum_bid
    bid_list = []
    for i in range(len(participants)):
        bid = participants[i].place_bid(max_bid=max_bid)
        if bid <= max_bid or bid > participants[i].money:
            if 'max_bidder' in kwargs.keys() and participants[i] != kwargs['max_bidder']:
                participants.remove(participants[i])
        else:
            bid_list[i] = bid
    max_bid = max(bid)
    max_bidder = participants[bid_list.index(max_bid)]
    return auction(participants=participants, minimum_bid=max_bid, max_bidder=max_bidder)


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


def payment(provider, receiver, game_state, amount):
    provider.money -= amount

    if provider.money < 0:
        debt = abs(provider.money)
        money_available = 0

        eligible_tiles = provider.get_all_eligible_housing_tiles()
        sets = []
        for tile in eligible_tiles:
            if any(tile in s for s in sets):
                continue
            sets.append(tile.get_others_in_set(game_master=game_state).append(tile))

        sorted(sets,key=lambda item:item[0].position)

        # sell houses
        for set_of_properties in sets:
            total_houses = 0
            sorted(set_of_properties, key=sort_by_housing)

            for property in set_of_properties:
                total_houses += property.houses

            houses_to_sell = provider.sell_houses_handler(max_houses=total_houses,
                                                              state=game_state) # sell houses
            for i in range(houses_to_sell):
                p = set_of_properties[i%len(set_of_properties)]
                if p.hotel > 0:
                    if game_state.houses_remaining < 4:
                        for prop in set_of_properties:
                            prop.hotel -= 1
                            prop.houses = 0
                            game_state.hotels_remaining += 1
                            money_available += p.housing_cost/2*5
                        continue
                    else:
                        p.hotel -= 1
                        p.houses += 4
                        game_state.hotels_remaining += 1
                        game_state.houses_remaining -= 4
                else:
                    p.houses -= 1
                    game_state.houses_remaining += 1
                    money_available += p.housing_cost/2

            if money_available >= debt:
                provider.money += money_available
                receiver.money += amount
                return True

        # mortgage
        player_properties = provider.properties_owned
        sorted(player_properties,key=lambda item:item.position)
        for prop in player_properties:
            if provider.mortgage_handler(property_to_mortgage=prop,state=game_state):
                prop.is_mortgaged = True
                money_available += prop.mortgage
            if money_available >= debt:
                provider.money += money_available
                receiver.money += amount
                return True

        for i in range(provider.num_jail_card):
            provider.num_jail_card -= 1
            money_available += 50

        if money_available < debt:
            receiver.money += amount - debt
            return False # player is declare bankruptcy and is dead

    else:
        if isinstance(receiver,Player): receiver.money += amount
        return True


def sort_by_housing(street):
    return 5 if street.hotel > 0 else street.houses


