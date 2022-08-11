import math

from .tile import Property, Street


class PlayerConcept:
    id = 0
    properties_owned = []
    money = 0
    rounds_in_jail = 0
    location = 0
    num_jail_card = 0
    jail_card = num_jail_card > 0

    def player_info(self):
        out = {}
        out['id']  = self.id
        out['location'] = self.location
        out['money'] = self.money
        out['is_in_jail'] = self.rounds_in_jail > 0
        out['round_in_jail'] = self.rounds_in_jail

        assets = {} # jail card, money, sets, properties, mortgage
        assets['jail_cards'] = self.jail_card
        assets['money'] = self.money
        assets['properties'] = {}
        assets['mortgage'] = {}
        assets['sets'] = []
        for prop in self.properties_owned:
            assets['mortgage' if prop.is_mortgaged else 'properties'].update({f'{str(prop.id)}': prop.name})
            if prop.set not in assets['sets'] and all([p in self.properties_owned for p in prop.get_others_in_set()]):
                assets['sets'].append(prop.set)

        out.update({'assets': assets})
        return out

    def from_json(self,src, tiles):
        self.id = src['id']
        self.location = src['location']
        self.is_in_jail = src['is_in_jail']
        self.rounds_in_jail = src['round_in_jail']

        self.money = src['money']
        self.jail_card = src['assets']['jail_cards']
        self.properties_owned = [tiles[p['position']] for p in src['assets']['properties']]
        self.properties_owned.extend([tiles[p['position']] for p in src['assets']['mortgage']])
    

class PlayerActionsHandler():
    def jail_card_handler(self, **kwargs):
        return True

    def jail_actions_handler(self, **kwargs):
        return True

    def buy_property_handler(self, **kwargs):
        return True

    def debt_handler(self,properties, **kwargs):
        return True

    def place_bid(self, **kwargs):
        return 0

    def trade_handler(self, state, **kwargs):
        return []

    def accept_trade(self, trade, **kwargs):
        return False

    def build_houses_handler(self, max_houses, state):
        return math.floor(0.5*max_houses)

    def sell_houses_handler(self, max_houses, state):
        return math.floor(0.5*max_houses)

    def mortgage_handler(self, property_to_mortgage, state):
        return False

    def unmortgage_handler(self, property_to_unmortgage, state):
        return False



class Player(PlayerActionsHandler,PlayerConcept):
    init_roll = 0

    # TODO: implement a system to copy from game state, so decision can be made

    # TODO: revisit jail system
    def jail_round(self):
        if self.jail_card_handler():
            self.jail_card = False
            return True
        else:
            if self.jail_actions_handler():
                self.money -= 50
                return True

    def get_all_eligible_housing_tiles(self, game_state):
        out = []
        for p in self.properties_owned:
            if isinstance(p,Street):
                others = p.get_others_in_set(game_master=game_state)
                is_eligible = True
                for p_other in others:
                    if p_other.is_mortgaged or p_other not in self.properties_owned:
                        is_eligible = False
                        break
                if is_eligible:
                    out.append(p)
        return out







    def on_debt(self, amount):
        pass
