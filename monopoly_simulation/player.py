

class PlayerActionsHandler:
    def jail_card_handler(self):
        return True

class Player(PlayerActionsHandler):
    id = 0
    properties_owned = []
    money = 0
    in_jail = False
    rounds_in_jail = 0
    mortgages = []
    location = ""
    jail_card = False

    def use_jail_card(self):
        if self.jail_card:
            return self.jail_card_handler()
            # prompt user response to use or not
        else:
            return False

