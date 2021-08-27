"""
Dungeon Slayer
Simple Dungeon Crawling game written in Python.
github.com/rin39
"""
import random


def main():
    player = user_character_creation()
    dungeon = Exploration(player)
    # Don't like this menu system, should redo later
    actions = {
        'e': dungeon,
        'l': player,
        'm': player,
        'q': dungeon,
        's': player,
        'c': dungeon
    }
    while True:
        action = input("(e)xplore, (l)ist magic, (m)anage magic, (c)ast spell, (s)status, (q)uit dungeon: ")
        if action in actions:
            if action == 'e':
                actions[action].explore()
            elif action == 'l':
                actions[action].list_magic()
            elif action == 'm':
                actions[action].manage_magic()
            elif action == 'q':
                actions[action].leave_dungeon()
            elif action == 's':
                actions[action].get_player_status()
            elif action == 'c':
                actions[action].exploration_cast_spell()
        else:
            continue

def user_character_creation():
    while True:
        name = input("Enter character name: ")
        if name != '':
            break
    while True:
        user_class = input("Choose your class/difficulty: Normal:[(w)arrior (m)age] Hard:(r)ouge Harder:(d)eprived: ")
        if user_class == 'w':
            player = Player.warrior(name)
        elif user_class == 'm':
            player = Player.mage(name)
        elif user_class == 'r':
            player = Player.rouge(name)
        elif user_class == 'd':
            player = Player.deprived(name)
        else:
            continue
        return player

class Exploration():
    def __init__(self, player) -> None:
        self.player = player

    def explore(self):
        random_encounter = random.randint(0,1)
        if random_encounter:
            enemy = Exploration.full_random_enemy(self)
            print(f"!!! Random Encounter: {enemy.name} (HP:{enemy.hp} DMG:{enemy.damage}) !!!")
            Exploration.battle_initialization(self, enemy)
            self.player.exp += 1
            Exploration.loot(self, 1)
            self.player.new_magic()
        else:
            Exploration.loot(self, 0)

    def full_random_enemy(self):
        enemy_names = (
            'Troll', 'Goblin', 'Fairy', 'Wolf', 'Fox'
        )
        if self.player.exp <= 10:
            random_hp_min = 20
            random_hp_cap = 50
            random_dmg_min = 10
            random_dmg_cap = 30
        elif self.player.exp <= 20 and self.player.exp > 10:
            random_hp_min = 40
            random_hp_cap = 60
            random_dmg_min = 20
            random_dmg_cap = 40
        else:
            random_hp_min = 60
            random_hp_cap = 120
            random_dmg_min = 30
            random_dmg_cap = 50
        random_hp = random.randrange(random_hp_min, random_hp_cap, 5)
        random_damage = random.randrange(random_dmg_min, random_dmg_cap, 5)
        random_name = random.choice(enemy_names)
        generated_enemy = Enemy.make_enemy(random_name, random_hp, 0, random_damage)
        return generated_enemy

    def loot(self, after_battle):
        if not after_battle:
            dice = random.randint(1,100)
            if dice <= 70:
                Exploration.get_item(self)
            else:
                print("Found literally nothing.")
        else:
            dice = random.randint(1,10)
            if dice == 1:
                print("No loot found.")
            else:
                Exploration.get_item(self)

    def get_item(self):
        dice = random.randint(1, 100)
        if dice <= 10:
            print("Found new weapon! +10DMG")
            self.player.damage += 10
        elif dice <= 30 and dice > 10:
            print("Found health crystal! Maximum HP increased!")
            self.player.maxhp += 15
        elif dice <= 45 and dice > 30:
            print("Found mana crystal! Maximum MP increased!")
            self.player.maxmp += 15
        elif dice <= 70 and dice > 45:
            print("Found health potion! 50HP restored!")
            self.player.heal(50)
        else:
            print("Found mana potion! 50MP restored!")
            self.player.restore_mana(50)

    def battle_initialization(self, enemy):
        fight = Battle(self.player, enemy)
        while True:
            if not self.player.is_alive:
                Exploration.game_over(self)
            fight.player_phase()
            if not enemy.is_alive:
                Exploration.enemy_down(self)
                return True
            fight.enemy_phase()

    def enemy_down(self):
        print("YOU HUNTED")
        self.player.defense_buff = 0
        self.player.damage_buff = 0

    def game_over(self):
        print(f"YOU DIED\nSlained {self.player.exp} monsters")
        exit()

    def leave_dungeon(self):
        print(f"{self.player.name} left the dungeon and has slained {self.player.exp} monster(s)!")
        exit()

    def exploration_cast_spell(self):
        spell_to_choose = {
                        'h': self.player.magic[0],
                        'j': self.player.magic[1],
                        'k': self.player.magic[2],
                        'l': self.player.magic[3]
                    }
        self.player.list_magic()
        spell_to_cast = input("Enter spell to cast (hjkl) or any other key to get back: ")
        try:
            spell_to_cast = spell_to_choose[spell_to_cast]
        except KeyError:
            return 0
        else:
            if spell_to_cast.magic_type != 'healing':
                print("This magic cannot be casted now, you can only heal now!")
                return 0
            mana_check = self.player.cast_spell(spell_to_cast)
            if not mana_check:
                print("Not enough mana!")
                return 0
            self.player.heal(spell_to_cast.damage)
            print(f'{self.player.name} casts {spell_to_cast.name} and heals {spell_to_cast.damage} HP!')


class Magic:
    MAGIC_TYPES = ('attack', 'dmg_buff', 'healing', 'none', 'def_buff')
    def __init__(self, name, damage, cost, magic_type):
        self.name = name
        self.damage = damage
        self.cost = cost
        self.magic_type = magic_type

    def __repr__(self) -> str:
        return f'{self.name}:{self.cost}MP;{self.damage}DMG'

    def __str__(self) -> str:
        if self.magic_type == 'attack':
            return f'<{self.name} {self.cost}MP:{self.damage}DMG>'
        elif self.magic_type == 'dmg_buff':
            return f'<{self.name} {self.cost}MP+{self.damage}DMG>'
        elif self.magic_type == 'def_buff':
            return f'<{self.name} {self.cost}MP-{self.damage}DMG>'
        elif self.magic_type == 'healing':
            return f'<{self.name} {self.cost}MP+{self.damage}HP>'
        else:
            return f'<{self.name}>'

    @classmethod
    def attack_type(cls, name, damage, cost):
        return cls(name, damage, cost, cls.MAGIC_TYPES[0])

    @classmethod
    def dmg_buff_type(cls, name, damage, cost):
        return cls(name, damage, cost, cls.MAGIC_TYPES[1])

    @classmethod
    def healing_type(cls, name, damage, cost):
        return cls(name, damage, cost, cls.MAGIC_TYPES[2])

    @classmethod
    def no_type(cls, name, damage, cost):
        return cls(name, damage, cost, cls.MAGIC_TYPES[3])

    @classmethod
    def def_type(cls, name, damage, cost):
        return cls(name, damage, cost, cls.MAGIC_TYPES[4])


# Title, DMG, MP
fireball = Magic.attack_type('Fireball', 15, 15)
firestorm = Magic.attack_type('Firestorm', 25, 25)
firearrow = Magic.attack_type('Firearrow', 20, 20)
firespear = Magic.attack_type('Firespear', 30, 25)
fireorb = Magic.attack_type('Fireorb', 40, 45)
blessing = Magic.dmg_buff_type('Blessing', 10, 50)
greatblessing = Magic.dmg_buff_type('Great Blessing', 15, 60)
berserk = Magic.dmg_buff_type('Berserk', 20, 80)
heal = Magic.healing_type('Healing', 50, 35)
regeneration = Magic.healing_type('Regeneration', 100, 60)
barrier = Magic.def_type('Barrier', 5, 30)
magicshield = Magic.def_type('Magic Shield', 10, 50)
empty_magic = Magic.no_type('Empty', 0, 0)

all_magic_list = [
    fireball, firestorm, firearrow, firespear, fireorb, blessing, greatblessing, berserk, heal, regeneration, barrier, magicshield
]


class Enemy:
    def __init__(self, name, hp, mp, damage):
        self.name = name
        self.maxhp = hp
        self.maxmp = mp
        self.hp = hp
        self.mp = mp
        self.damage = damage
        self.is_alive = True
        self.damage_buff = 0
        self.defense_buff = 0

    def __repr__(self) -> str:
        return f'Enemy: {self.name} hp={self.hp} mp={self.mp} damage={self.damage}'

    def __str__(self) -> str:
        return f'{self.name}: HP:{self.hp} DMG:{self.damage}'

    def get_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.is_alive = False
            self.hp = 0

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def restore_mana(self, amount):
        self.mp += amount
        if self.mp > self.maxmp:
            self.mp = self.maxmp

    def recieve_damage_buff(self, buff_amount):
        self.damage_buff += buff_amount

    def recieve_defense_buff(self, buff_amount):
        self.defense_buff += buff_amount

    @classmethod
    def make_enemy(cls, name, hp, mp, damage):
        return cls(name, hp, mp, damage)


class Player(Enemy):
    def __init__(self, name, hp, mp, damage):
        super().__init__(name, hp, mp, damage)
        self.magic = []
        self.not_learnt_magic = []
        self.exp = 0

    def __repr__(self) -> str:
        return f'Player: {self.name} hp={self.hp} mp={self.mp} damage={self.damage} magic={self.magic}'
    def __str__(self) -> str:
        return f'{self.name}: HP:{self.hp}/{self.maxhp} MP:{self.mp}/{self.maxmp} DMG:{self.damage}+{self.damage_buff} +DEF:{self.defense_buff}'

    def add_magic(self, name):
        self.magic.append(name)
        if len(self.magic) > 4:
            self.magic.remove(empty_magic)

    def remove_magic(self, name):
        self.magic.remove(name)
        self.magic.append(empty_magic)

    def cast_spell(self, magic_object):
        if self.mp >= magic_object.cost:
            self.mp -= magic_object.cost
            return True
        else:
            return False

    @staticmethod
    def character_generation(name, hp, mp, damage, magic1=empty_magic, magic2=empty_magic, magic3=empty_magic, magic4=empty_magic):
        generated_player = Player.make_player(name, hp, mp, damage)
        generated_player.add_magic(magic1)
        generated_player.add_magic(magic2)
        generated_player.add_magic(magic3)
        generated_player.add_magic(magic4)
        return generated_player

    @staticmethod
    def warrior(name):
        hp = 120
        mp = 80
        damage = 15
        magic1 = blessing
        character = Player.character_generation(name, hp, mp, damage, magic1)
        return character

    @staticmethod
    def mage(name):
        hp = 90
        mp = 100
        damage = 10
        magic1 = fireball
        magic2 = blessing
        magic3 = barrier
        magic4 = heal
        character = Player.character_generation(name, hp, mp, damage, magic1, magic2, magic3, magic4)
        return character

    @staticmethod
    def rouge(name):
        hp = 80
        mp = 75
        damage = 10
        magic1 = barrier
        character = Player.character_generation(name, hp, mp, damage, magic1)
        return character

    @staticmethod
    def deprived(name):
        hp = 75
        mp = 50
        damage = 10
        character = Player.character_generation(name, hp, mp, damage)
        return character

    @classmethod
    def make_player(cls, name, hp, mp, damage):
        return cls(name, hp, mp, damage)

    def list_magic(self):
        for magic in self.magic:
            print(f'{magic}', end=' ')
        print()

    def list_not_learnt_magic(self):
        for magic in self.not_learnt_magic:
            print(f'{magic}', end=' ')
        print()

    def get_player_status(self):
        print(f'{self}\nSlained {self.exp} monsters')

    def manage_magic(self):
        if len(self.not_learnt_magic) == 0:
            print("No new magic to manage. Slain more monsters, get new spells and come back!")
            return 0
        else:
            spell_to_choose = {
                            'h': self.magic[0],
                            'j': self.magic[1],
                            'k': self.magic[2],
                            'l': self.magic[3]
                        }
            print("Your magic:")
            self.list_magic()
            print("Not yet learnt:")
            self.list_not_learnt_magic()
            learn = input("Learn new magic (y/n)?")
            if learn != 'y':
                return 0
            else:
                spell = input("Choose spell to REMOVE from your KNOWN magic (hjkl) or type any other key to get back: ")
                try:
                    spell_to_remove = spell_to_choose[spell]
                except KeyError:
                    return 0
                else:
                    spell = input("Choose spell to LEARN (number i.e. 1, 2...) or type any other key to get back: ")
                    spell = int(spell) - 1
                    try:
                        spell_to_add = self.not_learnt_magic[spell]
                    except KeyError:
                        return 0
                    else:
                        self.remove_magic(spell_to_remove)
                        self.add_magic(spell_to_add)
                        self.not_learnt_magic.remove(spell_to_add)

    def new_magic(self):
        player_magic = set(self.magic)
        all_magic = set(all_magic_list)
        unknown_magic = all_magic.difference(player_magic)
        new_magic = random.choice(list(unknown_magic))
        if self.exp % 5 == 0:
            print(f'==={self.name} has obtained a new magic: {new_magic.name}! Enter Magic Managment to check it!===')
            self.not_learnt_magic.append(new_magic)


class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def get_status(self):
        print(self.player)
        print(self.enemy)

    def player_phase(self):
        spell_to_choose = {
                        'h': self.player.magic[0],
                        'j': self.player.magic[1],
                        'k': self.player.magic[2],
                        'l': self.player.magic[3]
                    }
        print("===Player Phase===")
        while True:
            action = input("(a)ttack, (m)agic list; hjkl - magic: ")
            if action == "a":
                Battle.attack(self)
                break
            elif action == "m":
                Player.list_magic(self.player)
            elif action in spell_to_choose:
                spell_to_cast = spell_to_choose[action]
                if spell_to_cast.name == "Empty":
                    continue
                mana_check = self.player.cast_spell(spell_to_cast)
                if not mana_check:
                    print("Not enough mana!")
                    continue
                Battle.cast_spell(self, spell_to_cast)
                break
            else:
                continue
        Battle.get_status(self)

    def attack(self):
        attack_success = Battle.attack_check('player_attack')
        if not attack_success:
            print(f'{self.player.name} attack misses!')
        else:
            self.enemy.get_damage(self.player.damage + self.player.damage_buff)
            print(f'{self.player.name} attacks and deals {self.player.damage + self.player.damage_buff} damage!')

    def enemy_phase(self):
        print("===Enemy Phase===")
        enemy_dealt_damage = self.enemy.damage - self.player.defense_buff
        if enemy_dealt_damage < 1:
            enemy_dealt_damage = 1
        attack_success = Battle.attack_check('enemy_attack')
        if not attack_success:
            print(f"{self.enemy.name} attack misses!")
        else:
            self.player.get_damage(enemy_dealt_damage)
            print(f"{self.enemy.name} attacks and deals {enemy_dealt_damage} damage!")
        Battle.get_status(self)


    def cast_spell(self, spell_to_cast):
        if spell_to_cast.magic_type == 'attack':
            cast_success = Battle.attack_check('player_magic_attack')
            if not cast_success:
                print(f'{self.player.name} casts {spell_to_cast.name} and misses!')
            else:
                self.enemy.get_damage(spell_to_cast.damage)
                print(f'{self.player.name} casts {spell_to_cast.name} and deals {spell_to_cast.damage} damage!')
        elif spell_to_cast.magic_type == 'dmg_buff':
            self.player.recieve_damage_buff(spell_to_cast.damage)
            print(f'{self.player.name} casts {spell_to_cast.name} and recieves {spell_to_cast.damage} attack bonus!')
        elif spell_to_cast.magic_type == 'healing':
            self.player.heal(spell_to_cast.damage)
            print(f'{self.player.name} casts {spell_to_cast.name} and heals {spell_to_cast.damage} HP!')
        elif spell_to_cast.magic_type == 'def_buff':
            self.player.recieve_defense_buff(spell_to_cast.damage)
            print(f'{self.player.name} casts {spell_to_cast.name} and recieves {spell_to_cast.damage} defense bonus!')
        else:
            raise NotImplementedError

    @staticmethod
    def attack_check(type):
        if type == 'player_attack':
            check = 3
        elif type == 'enemy_attack':
            check = 4
        elif type == 'player_magic_attack':
            check = 2
        else:
            check = 10
        dice = random.randint(1,10)
        if dice <= check:
            return False
        else:
            return True


main()

