"""
Dungeon Slayer
Simple Dungeon Crawling game written in Python.
github.com/rin39
"""

from game.exploration_logic import Exploration
from game.characters import user_character_creation


def main():
    player = user_character_creation()
    dungeon = Exploration(player)
    while True:
        action = input("(e)xplore, (l)ist magic, (m)anage magic, (c)ast spell, (s)status, (q)uit dungeon: ")
        print()
        if action == 'e':
            dungeon.explore()
        elif action == 'l':
            player.list_magic()
        elif action == 'm':
            player.manage_magic()
        elif action == 'q':
            dungeon.leave_dungeon()
        elif action == 's':
            player.get_player_status()
        elif action == 'c':
            dungeon.exploration_cast_spell()
        else:
            continue


main()

