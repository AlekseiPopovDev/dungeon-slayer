import random
from . import magic

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
            self.magic.remove(magic.empty_magic)

    def remove_magic(self, name):
        self.magic.remove(name)
        self.magic.append(magic.empty_magic)

    def cast_spell(self, magic_object):
        if self.mp >= magic_object.cost:
            self.mp -= magic_object.cost
            return True
        else:
            return False

    @staticmethod
    def character_generation(name, hp, mp, damage, magic1=magic.empty_magic, magic2=magic.empty_magic, magic3=magic.empty_magic, magic4=magic.empty_magic):
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
        magic1 = magic.blessing
        character = Player.character_generation(name, hp, mp, damage, magic1)
        return character

    @staticmethod
    def mage(name):
        hp = 90
        mp = 100
        damage = 10
        magic1 = magic.fireball
        magic2 = magic.blessing
        magic3 = magic.barrier
        magic4 = magic.heal
        character = Player.character_generation(name, hp, mp, damage, magic1, magic2, magic3, magic4)
        return character

    @staticmethod
    def rouge(name):
        hp = 80
        mp = 75
        damage = 10
        magic1 = magic.barrier
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
        print('\n')

    def list_not_learnt_magic(self):
        for magic in self.not_learnt_magic:
            print(f'{magic}', end=' ')
        print('\n')

    def get_player_status(self):
        print(f'{self}\nSlained {self.exp} monsters\n')

    def manage_magic(self):
        if len(self.not_learnt_magic) == 0:
            print("No new magic to manage. Slain more monsters, get new spells and come back!\n")
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
            learn = input("Learn new magic (y/n)? ")
            if learn != 'y':
                return 0
            else:
                spell = input("Choose spell to REMOVE from your KNOWN magic (or an empty slot) (hjkl) or type any other key to get back: ")
                try:
                    spell_to_remove = spell_to_choose[spell]
                except KeyError:
                    return 0
                else:
                    spell = input("Choose spell to LEARN (number e.g. 1, 2...) or type any other key to get back: ")
                    spell = int(spell) - 1
                    try:
                        spell_to_add = self.not_learnt_magic[spell]
                    except KeyError:
                        return 0
                    except IndexError:
                        return 0
                    else:
                        self.remove_magic(spell_to_remove)
                        self.add_magic(spell_to_add)
                        self.not_learnt_magic.remove(spell_to_add)
                        print()

    def new_magic(self):
        player_magic = set(self.magic)
        all_magic = set(magic.all_magic_list)
        unknown_magic = all_magic.difference(player_magic)
        new_magic = random.choice(list(unknown_magic))
        if self.exp % 5 == 0:
            print(f'+++ {self.name} has obtained a new magic: {new_magic.name}! Enter Magic Managment to check it! +++\n')
            self.not_learnt_magic.append(new_magic)


def user_character_creation():
    while True:
        name = input("Enter character name: ")
        if name != '':
            break
    while True:
        user_class = input("Choose your class/difficulty: Normal:[(w)arrior (m)age] Hard:(r)ouge Harder:(d)eprived: ")
        print()
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

