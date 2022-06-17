import abc
import math

from . import utility
from . import game
from . import player
from .player import Player
from game import dice_roll


class Tile:

    name = ""
    position = -1


    def round_action(self, player, game_state, **kwarg):
        pass


    def __str__(self):
        return f'({self.position}:{self.name})'



class Property(Tile):
    owner: Player = player.Player()
    is_owned = False
    price = 0
    base_rent = 0
    premium_rents = [] # 0 being set owned, 5 being hotel, rest being their respective number of houses
    set = ""
    is_mortgaged = False
    mortgage = 0
    # note: railroads/utility work differently

    def calculate_rent(self, game_master, **kwargs):
        pass

    def round_action(self, player, game_state, **kwarg):
        if self.is_owned and not self.is_mortgaged:
            rent = self.calculate_rent(game_master=game_state,
                                       dice_roll=kwarg.get('moves'),
                                       from_chances=kwarg.get('from_chances',False)) # calculate rents
            # apply rent to player
            player.money -= rent
            self.owner.money += rent
        else:
            if player.buy_property_handler():
                # buy prpoerty
                player.money -= self.price
                self.owner = player
                player.properties_owned.append(self)
            else:
                auction_players = []
                for p in game_state.players:
                    if not player.__eq__(p):
                        auction_players.append(p)
                auction_winner= utility.auction(participants=auction_players,minimum_bid=self.price)
                self.owner = game_state.players[auction_winner]
                self.owner.properties_owned.append(self)



    def get_others_in_set(self, game_master):
        out = []
        for tile in game_master.tiles:
            if isinstance(tile, Property):
                if tile.set == self.set and tile.name != self.name:
                    out.append(tile)

        return out





class Jail(Tile):
    def round_action(self, player, game_state, **kwarg):
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
        else:
            return self.base_rent




class PublicProperty(Property):
    def calculate_rent(self, game_master, **kwargs):
        set_owned = True
        other_properties = self.get_others_in_set(game_master=game_master)
        for p in other_properties:
            if p not in self.owner.properties_owned:
                set_owned = False

        if self.set == 'railroad':
            return (int)(25*math.pow(2,len(other_properties))) if not kwargs.get('from_chances') \
                else (int)(25*math.pow(2,len(other_properties))) * 2
        elif self.set == 'utility':
            multiplier = 10 if set_owned or kwargs.get('from_chances') else 4
            dice_roll = kwargs.get('dice_roll')
            return dice_roll * multiplier



class Drawable(Tile):
    drawable_type = ''


    def round_action(self, player, game_state, **kwarg):
        card_info = {}
        queue = []
        top_index=0
        drawable_data = {}

        if self.drawable_type == 'community chest':
            drawable_data = game_state.COMMUNITY_CHEST_DICT
            queue = game_state.chances_queue
            top_index = game_state.community_chest_queue_top
            game_state.community_chest_queue_top = (top_index+1) % len(queue)

        elif self.drawable_type == 'chance':
            drawable_data = game_state.CHANCES_DICT
            queue = game_state.community_chest_queue
            top_index = game_state.chances_queue_top
            game_state.chances_queue_top = (top_index + 1) % len(queue)

        card_info = drawable_data[queue[top_index]]
        action = card_info['action']
        if action == 'move':
            if card_info.get('jail',False) or str(card_info.get('location')) == 'jail':
                game_state.tiles[30].round_action(player=player,game_state=game_state) # jail index at 30
            else:
                prev_location = player.location
                new_location = card_info.get('location')
                if str(new_location) == 'railroad':
                    railroad_positions = []
                    for t in game_state.tiles:
                        if 'Railroad' not in t.name:
                            railroad_positions.append(t.position)
                    new_location = min([abs(i-prev_location) for i in railroad_positions])
                    from_chances = True
                else:
                    player.money += 200 if new_location < prev_location else 0
                    from_chances = False

                player.location = new_location
                game_state.tiles[player.location].round_action(player=player,
                                                               game_state=game_state,
                                                               from_chances=from_chances,
                                                               dice_roll=dice_roll())
        elif action == 'step':
            player.location += card_info["steps"]
            game_state.tiles[player.location].round_action(player=player, game_state=game_state)
        elif action == 'money':
            player.money += card_info["amount"]
        elif action == 'money_from_players':
            total = 0
            for p in game_state.players:
                p.money -= card_info["due_per_player"]
                total += card_info["due_per_player"]
            player.money += total
        elif action == 'jail_card':
            player.num_jail_card += 1
            queue.pop(top_index)
            if self.drawable_type == 'chance':
                game_state.chances_queue = queue
            else:
                game_state.community_chest_queue = queue
        elif action == 'housing':
            house_cost = card_info['house_cost']
            hotel_cost = card_info['hotel_cost']
            num_hotel = 0
            num_houses = 0
            for p in player.properties_owned:
                if isinstance(p,Street):
                    num_houses += p.houses
                    num_hotel += p.hotel
            player.money -= house_cost * num_houses + hotel_cost * num_hotel












class Tax(Tile):
    tax = 0

    def round_action(self, player, game_state, **kwarg):
        player.money -= self.tax
