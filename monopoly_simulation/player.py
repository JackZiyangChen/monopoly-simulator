

class PlayerConcept:
    id = 0
    properties_owned = []
    money = 0
    rounds_in_jail = 0
    mortgages = []
    location = 0
    num_jail_card = 0
    jail_card = num_jail_card > 0

class PlayerActionsHandler():
    def jail_card_handler(self):
        return True

    def jail_actions_handler(self):
        return True

    def buy_property_handler(self):
        return True

    def debt_handler(self,properties):
        return True

    def place_bid(self):
        return 0


class Player(PlayerActionsHandler,PlayerConcept):
    init_roll = 0
    def jail_round(self):
        if self.jail_card_handler():
            self.jail_card = False
            return True
        else:
            if self.jail_actions_handler():
                self.money -= 50
                return True


    def on_debt(self, amount):
        pass
