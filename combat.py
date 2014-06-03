import player
import creep
import pygame


def creep_start_battle(attacker, target, time_passed):
    attacker.attack(target, time_passed)
    target.attack(attacker, time_passed)


def player_start_battle(attacker, target, time_passed):
    if 50 ** 2 <= (attacker.pos.x - target.pos.x) ** 2 + (attacker.pos.y - target.pos.y) ** 2 <= 250 ** 2:
        attacker.chasing(target, time_passed)
    elif (attacker.pos.x - target.pos.x) ** 2 + (attacker.pos.y - target.pos.y) ** 2 < 50 ** 2:
        while target.life > 0 and attacker.life > 0:
            attacker.attack(target, time_passed)
    else:
    	pass
