from monopoly_simulation.player import *


class TestingPlayer(Player):
    '''
    This player will take inputs from command prompt and make decision based on human input
    '''

    # TODO: implement human input

    def jail_card_handler(self, **kwargs):
        return super().jail_card_handler(**kwargs)

    def jail_actions_handler(self, **kwargs):
        return super().jail_actions_handler(**kwargs)

    def buy_property_handler(self, **kwargs):
        return super().buy_property_handler(**kwargs)

    def debt_handler(self, properties, **kwargs):
        return super().debt_handler(properties, **kwargs)

    def place_bid(self, **kwargs):
        return super().place_bid(**kwargs)

    def trade_handler(self, state, **kwargs):
        return super().trade_handler(state, **kwargs)

    def accept_trade(self, trade, **kwargs):
        return super().accept_trade(trade, **kwargs)