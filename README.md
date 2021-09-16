## Character Creation

1. Enter name
2. Choose class

| Class | Difficulty | HP | MP | DMG | Spells |
| --- | --- | --- | --- | --- | --- |
| Warrior | Normal | 120 | 80 | 15 | Blessing<br> |
| Mage | Normal | 90 | 100 | 10 | Fireball<br>Blessing<br>Barrier<br>Heal |
| Rouge | Hard| 80 | 75 | 10 | Barrier |
| Deprived | Harder| 75 | 50 | 10 |  |

### Exploration

| Key | Description | Action |
| --- | --- | --- |
| `e` | explore | Explore dungeon. Possible to find items or encounter monsters |
| `l` | list magic | Display currently equipped magic |
| `m` | manage magic | Learn new spells (if any new obtained) |
| `c` | cast spell | Cast some spell (only healing magic can be cased out of battle) |
| `s` | get status | Show player's status |
| `q` | quit dungeon | Quit game |

#### Random Encounters

Chance of random encounter: 50%

| Slained Monsters | Monster HP | Monster DMG |
| --- | --- | --- |
| 0-10 | 20-50 | 10-30|
| 10-20 | 40-60 | 20-40 |
| 20+ | 60-120 | 30-50 |

#### Loot Chance

Chances to find any item:

* Not after battle: 70%
* After battle: 90%

Chances to find particular item:

| Item | Description | Chance |
| --- | --- | --- |
| New weapon | +10 DMG | 10% |
| Mana crystal | +15 MAX MP | 15% |
| Health crystal | +15 MAX HP | 20% |
| Health potion | +50 HP | 25% |
| Mana potion | +50 MP | 30% |

#### New Spells

Player gets new spell every 5 slained monsters.

#### Battle

| Key | Description | Action |
| --- | --- | --- |
| `a` | attack | Perform attack. |
| `m` | magic list | Display currently equipped magic. |
| `h, j, k, l` | Cast spell | Quick cast spell.|

#### Hit Chance

| Type | Chance |
| --- | --- |
| Player damage spell cast| 80% |
| Player attack | 70% |
| Monster attack| 60% |

#### Spells

* Damage: deals damage to monster
* Heal: heals player
* Buff (defense): reduces damage dealt to player
* Buff (damage): increases damage dealt by player

| Name | Effect | MP |
| --- | --- | --- |
| Fireball | 15 DMG | 15 |
| Firestorm | 25 DMG | 25 |
| Firearrow | 20 DMG | 20 |
| Firespear | 30 DMG | 25 |
| Fireorb | 40 DMG | 45  |
| Blessing | +10 DMG | 50 |
| Great Blessing | +15 DMG | 60 |
| Berserk | +20 DMG | 80 |
| Heal | +50 HP| 35 |
| Regeneration | +100 HP | 60 |
| Barrier | +5 DEF | 30 |
| Magic Shield | +10 DEF | 50 |
