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


# Spell Name, DMG, MP

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

# Probably there is a better way to do it.

all_magic_list = [
    fireball, firestorm, firearrow, firespear, fireorb, blessing, greatblessing, berserk, heal, regeneration, barrier, magicshield
]

