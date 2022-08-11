import monopoly_simulation
from players.ai_player import AIPlayer
from monopoly_simulation.game import game
import os
import neat


def run_ai_games(config):
    pop = neat.Population(config)

    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.Checkpointer(1))

    pop.run(eval_genomes, config)


def eval_genomes(genomes, config):
    pass


def run_simulation(config):

    players = []
    for i in range(4):
        player = AIPlayer()
        player.initialize_brain(config)
        players.append(player)

    game(4, players=players)
