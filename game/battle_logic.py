import random

class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def get_status(self):
        print(self.player)
        print(self.enemy)
        print()

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
                self.attack()
                break
            elif action == "m":
                self.player.list_magic()
            elif action in spell_to_choose:
                spell_to_cast = spell_to_choose[action]
                if spell_to_cast.name == "Empty":
                    continue
                mana_check = self.player.cast_spell(spell_to_cast)
                if not mana_check:
                    print("Not enough mana!")
                    continue
                self.cast_spell(spell_to_cast)
                break
            else:
                continue
        self.get_status()

    def attack(self):
        attack_success = self.attack_check('player_attack')
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
        attack_success = self.attack_check('enemy_attack')
        if not attack_success:
            print(f"{self.enemy.name} attack misses!")
        else:
            self.player.get_damage(enemy_dealt_damage)
            print(f"{self.enemy.name} attacks and deals {enemy_dealt_damage} damage!")
        self.get_status()

    def cast_spell(self, spell_to_cast):
        if spell_to_cast.magic_type == 'attack':
            cast_success = self.attack_check('player_magic_attack')
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
