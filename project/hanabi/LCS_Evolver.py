from typing import List
import os
import time
from threading import Thread, Semaphore

from LCS_Rules import LCSRules, RuleSet
from LCS_Actor import LCSActor
import server
from LCS_Rules import RuleSet
from player_LCS import LCSPlayer
import LCS_Sensor as sens


class Evolver:

    def __init__(self, lcs_rules_list: List[RuleSet]):
        self.LCS_rules_list = lcs_rules_list

    def evolve(self, activations, fitness):
        # Activations arriva dal metodo EndGameData
        # sto metodo mi ritorna altri ruleSet
        pass


def get_fitness(rule_list: List[LCSRules]):
    pass


if __name__ == '__main__':
    for i in range(10):
        n_players = 2
        print("MATCH ", i)
        sem = Semaphore(0)
        server = Thread(target=server.start_server, args=[sem])
        server.start()
        sem.acquire()
        sensor_list = sens.package_sensors(n_players)
        rule = [LCSRules(sensor_list=sensor_list,
                         action_length=LCSActor.get_action_length(),
                         rule=RuleSet.empty_rules(0, action_length=LCSActor.get_action_length()))
                for _ in range(n)]
        players = [LCSPlayer(name='LCS1', rules=rule[0]), LCSPlayer(name='LCS2', rules=rule[1])]
        threads = [Thread(target=player.start) for player in players]
        [t.start() for t in threads]
        [t.join() for t in threads]
        server.join()
        if not os.path.exists('./logs'):
            os.mkdir('./logs')
        os.rename('./game.log', f'./logs/{time.strftime("%y%m%d%H%M%S")}.log')
