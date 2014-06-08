import player
import creep
import pygame

class Battle():
    _battle_time = 0

    @classmethod
    def creep_start_battle(cls, attacker, target, time_passed):
        cls._battle_time = 0
        cls.do_battle(attacker, target, time_passed)

    @classmethod
    def player_start_battle(cls, attacker, target, time_passed):
        if 50 ** 2 <= (attacker.pos.x - target.pos.x) ** 2 + (attacker.pos.y - target.pos.y) ** 2 <= 250 ** 2:
            attacker.chasing(target)
        elif (attacker.pos.x - target.pos.x) ** 2 + (attacker.pos.y - target.pos.y) ** 2 < 50 ** 2:
            cls._battle_time = 0
            cls.do_battle(attacker, target, time_passed)
        else:
            pass

    @classmethod
    def do_battle(cls, attacker, target, time_passed):
        if cls._battle_time == 0:
            attacker.attack(target, time_passed)
            target.attack(attacker, time_passed)
        cls._battle_time += time_passed
        if cls._battle_time >= 500:
            cls._battle_time = 0