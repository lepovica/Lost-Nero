import player
import creep
import pygame


def start_battle(attacker, target, time_passed):
    attacker.Attack(target, time_passed)
    target.Attack(attacker, time_passed)
