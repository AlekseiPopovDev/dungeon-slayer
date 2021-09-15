import random
from . import battle_logic
from . import characters

class Exploration():
    def __init__(self, player) -> None:
        self.player = player

    def explore(self):
        random_encounter = random.randint(0,1)
        if random_encounter:
            enemy = self.full_random_enemy()
            print(f"!!! Random Encounter: {enemy.name} (HP:{enemy.hp} DMG:{enemy.damage}) !!!\n")
            self.battle_initialization(enemy)
            self.player.exp += 1
            self.loot(1)
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
        generated_enemy = characters.Enemy.make_enemy(random_name, random_hp, 0, random_damage)
        return generated_enemy

    def loot(self, after_battle):
        if not after_battle:
            dice = random.randint(1,100)
            if dice <= 70:
                self.get_item()
            else:
                print("... Found literally nothing ...\n")
        else:
            dice = random.randint(1,10)
            if dice == 1:
                print("... No loot found ...\n")
            else:
                self.get_item()

    def get_item(self):
        dice = random.randint(1, 100)
        if dice <= 10:
            print("+++ Found new weapon! +10DMG +++")
            self.player.damage += 10
        elif dice <= 30 and dice > 10:
            print("+++ Found health crystal! Maximum HP increased! +++")
            self.player.maxhp += 15
        elif dice <= 45 and dice > 30:
            print("+++ Found mana crystal! Maximum MP increased! +++")
            self.player.maxmp += 15
        elif dice <= 70 and dice > 45:
            print("+++ Found health potion! 50HP restored! +++")
            self.player.heal(50)
        else:
            print("+++ Found mana potion! 50MP restored! +++")
            self.player.restore_mana(50)
        print()

    def battle_initialization(self, enemy):
        fight = battle_logic.Battle(self.player, enemy)
        while True:
            if not self.player.is_alive:
                self.game_over()
            fight.player_phase()
            if not enemy.is_alive:
                self.enemy_down()
                return True
            fight.enemy_phase()

    def enemy_down(self):
        print("~~~YOU HUNTED~~~\n")
        self.player.defense_buff = 0
        self.player.damage_buff = 0

    def game_over(self):
        print(f"~~~YOU DIED~~~\nSlained {self.player.exp} monsters")
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
                print("This magic cannot be casted now. You can only heal now.\n")
                return 0
            mana_check = self.player.cast_spell(spell_to_cast)
            if not mana_check:
                print("Not enough mana!")
                return 0
            self.player.heal(spell_to_cast.damage)
            print(f'{self.player.name} casts {spell_to_cast.name} and heals {spell_to_cast.damage} HP!\n')

