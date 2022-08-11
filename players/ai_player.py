from monopoly_simulation.player import *
import neat


class AIPlayer(Player):
    '''
    AI player powered by NEAT neural network
    '''
    brain = neat.nn.FeedForwardNetwork()
    def initialize_brain(self, genome, config):
        self.brain = neat.nn.FeedForwardNetwork.create(genome, config)
        self.genome = genome

    def activate_brain_from_game_state(self):
        out = self.brain.activate()

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