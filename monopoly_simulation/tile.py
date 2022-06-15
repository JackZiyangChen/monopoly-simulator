import abc
import math

from . import utility
from . import game
from . import player
from .player import Player


class Tile:

    name = ""


    def round_action(self, player, **kwarg):
        pass



class Property(Tile):
    owner: Player = player.Player()
    is_owned = False
    price = 0
    base_rent = 0
    premium_rents = [] # 0 being set owned, 5 being hotel, rest being their respective number of houses
    set = ""
    is_mortgaged = False
    # note: railroads/utility work differently

    def calculate_rent(self, game_master, **kwargs):
        pass

    def round_action(self, player, **kwarg):
        if self.is_owned and not self.is_mortgaged:
            rent = self.calculate_rent(game_master=kwarg.get('game_state'), dice_roll=kwarg.get('moves')) # calculate rents
            # apply rent to player
            self.owner.money += rent
        else:
            if player.buy_property_handler():
                # buy prpoerty
                player.money -= self.price
                self.owner = player
                player.properties_owned.append(self)
            else:
                auction_players = []
                for p in kwarg.get('game_state').players:
                    if not player.__eq__(p):
                        auction_players.append(p)
                auction_winner= utility.auction(participants=auction_players,minimum_bid=self.price)
                self.owner = kwarg.get('game_state').players[auction_winner]
                self.owner.properties_owned.append(self)



    def get_others_in_set(self, game_master):
        out = []
        for tile in game_master.tiles:
            if isinstance(tile, Property):
                if tile.set == self.set and (not tile.name == self.name):
                    out.append(tile)

        return out





class Jail(Tile):
    def round_action(self, player, **kwarg):
        player.rounds_in_jail = 3
        player.location = 10




class Street(Property):
    houses = 0
    housing_cost = 0
    hotel_cost = 0
    hotel = 0

    def calculate_rent(self, game_master, **kwargs):
        # check if set is owned
        set_owned = True
        other_properties = self.get_others_in_set(game_master=game_master)
        for p in other_properties:
            if p not in self.owner.properties_owned:
                set_owned = False

        if set_owned:
            if self.hotel>0:
                return self.premium_rents[5]
            else:
                return self.premium_rents[0]




class PublicProperty(Property):
    def calculate_rent(self, game_master, **kwargs):
        set_owned = True
        other_properties = self.get_others_in_set(game_master=game_master)
        for p in other_properties:
            if p not in self.owner.properties_owned:
                set_owned = False

        if self.set == 'railroad':
            return (int)(25*math.pow(2,len(other_properties)))
        elif self.set == 'utility':
            multiplier = 10 if set_owned else 4
            dice_roll = kwargs.get('dice_roll')
            return dice_roll * multiplier



class Drawable(Tile):
    pass


class tax(Tile):
    tax = 0

    def round_action(self, player, **kwarg):
        player.money -= self.tax
