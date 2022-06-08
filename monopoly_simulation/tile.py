import abc
from . import utility
from . import game


class Tile:
    owner = ""
    is_owned = False


    def round_action(self, player, **kwarg):
        pass



class Property(Tile):

    price = 0
    base_rent = 0
    premium_rents = [] # 0 being set owned, 5 being hotel, rest being their respective number of houses
    set = ""
    # note: railroads/utility work differently

    def calculate_rent(self):
        pass

    def round_action(self, player, **kwarg):
        if self.is_owned:
            rent = self.calculate_rent() # calculate rents
            # apply rent to player
        else:
            if player.buy_property_handler():
                # buy prpoerty
                player.money -= self.price
                self.owner = player
            else:
                auction_players = []
                for p in kwarg.get('game_state').players:
                    if not player.__eq__(p):
                        auction_players.append(p)
                self.owner = utility.auction(participants=auction_players,minimum_bid=self.price)




class Jail(Tile):
    def round_action(self, player, **kwarg):
        player.rounds_in_jail = 3
        player.position = 10




class Street(Property):
    houses = 0
    housing_cost = 0
    hotel_cost = 0
    hotel = 0

    def calculate_rent(self):
        # check if set is owned
        set_owned = False

        if set_owned:
            if self.hotel>0: return self.premium_rents[5]
            else: return self.premium_rents[0]




class Public_property(Property):
    pass


class Drawable(Tile):
    pass
