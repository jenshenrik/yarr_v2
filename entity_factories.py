from components.ai import HostileEnemy
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item

import copy

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=30),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
    strength=12
)

goblin = Actor(
    char="g",
    color=(63, 127, 63),
    name="Goblin",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=7),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=50),
    strength=8,
    dexterity=14
)

orc = Actor(
    char="O",
    color=(0, 127, 0),
    name="Orc",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=15),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
    strength=16,
    dexterity=12
)

troll = Actor(
    char="T",
    color=(0, 127, 0),
    name="Troll",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
    strength=15
)

health_potion = Item(
    char="!",
    color=(127, 0, 255),
    name="Potion of Healing",
    consumable=consumable.HealingConsumable(die=4, number_of_dice=2, bonus=2),
)
confusion_scroll = Item(
    char="~",
    color=(207, 63, 255),
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)
fireball_scroll = Item(
    char="~",
    color=(255, 0, 0),
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)
lightning_scroll = Item(
    char="~",
    color=(255, 255, 0),
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)

dagger = Item(
    char="/", color=(0, 191, 255), name="Dagger", equippable=equippable.Dagger()
)
sword = Item(char="/", color=(0, 191, 255), name="Sword", equippable=equippable.Shortsword())
scimitar = Item(char="/", color=(0, 191, 255), name="Scimitar", equippable=equippable.Scimitar())
greataxe= Item(char="P", color=(0, 191, 255), name="Greataxe", equippable=equippable.Greataxe())

leather_armor = Item(
    char="[",
    color=(139, 69, 19),
    name="Leather Armor",
    equippable=equippable.LeatherArmor(),
)

hide_armor = Item(
    char="[",
    color=(139, 69, 19),
    name="Hide Armor",
    equippable=equippable.HideArmor(),
)

chain_mail = Item(
    char="[", color=(139, 69, 19), name="Chain Mail", equippable=equippable.ChainMail()
)

def spawn_orc() -> Actor:
    o = copy.deepcopy(orc)
    armor = copy.deepcopy(hide_armor)
    weapon = copy.deepcopy(greataxe)
    give_and_equip_item(o, armor)
    give_and_equip_item(o, weapon)
    return o

def spawn_goblin() -> Actor:
    g = copy.deepcopy(goblin)
    armor = copy.deepcopy(leather_armor)
    weapon = copy.deepcopy(scimitar)
    give_and_equip_item(g, armor)
    give_and_equip_item(g, weapon)
    return g

def give_and_equip_item(actor: Actor, item: Item):
    actor.inventory.items.append(item)
    item.parent = actor.inventory
    actor.equipment.toggle_equip(item, add_message=False)
