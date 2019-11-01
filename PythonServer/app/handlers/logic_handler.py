# -*- coding: utf-8 -*-

# python imports
from copy import deepcopy

# project imports
from ..ks.models import World


class LogicHandler:

    def __init__ (self, world, sides):
        self._sides = sides
        self.world = world


    def initialize(self):
        self.clear_commands()


    def store_command(self, side_name, command):
        self._last_cycle_commands[side_name][command.agent_type] = command


    def clear_commands(self):
        self._last_cycle_commands = {side: {} for side in self._sides}


    def process(self, current_cycle):
        gui_events = []
        gui_events.extend(self.world.apply_commands(self._last_cycle_commands))
        gui_events.extend(self.world.tick())
        return gui_events


    def get_client_world(self, side_name):
        enemy_side = [s for s in self._sides if s != side_name][0]
        world = deepcopy(self.world)
        world.bases[enemy_side] = None
        return self.world


    def check_end_game(self, current_cycle):
        end_game = self.world.check_end_game(current_cycle)

        if end_game:
            winner = self.world.get_winner()
            details = {
                'Remaining Healths': {
                    side: str(health) for side, health in self.world.total_healths.items()
                }
            }
            return end_game, winner, details

        return end_game, None, None
