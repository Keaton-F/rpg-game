import random

from src.characters import CHARACTER_CLASSES, STARTING_WEAPONS
from src.item_data import ITEM_DATA
from src.items import Item, Weapon
from src.progression import set_level


def create_item(item_id):
    """
    Создаёт экземпляр предмета по его идентификатору.

    Аргументы:
        item_id (str): идентификатор предмета из ITEM_DATA.

    Возвращает:
        Item: новый экземпляр предмета.
    """
    item_data = ITEM_DATA[item_id].copy()
    item_type = item_data.pop("type")

    if item_type == "weapon":
        return Weapon(
            item_id=item_id,
            **item_data,
        )

    if item_type == "item":
        return Item(
            item_id=item_id,
            **item_data,
        )

    raise ValueError(f"Неизвестный тип предмета: {item_type}")


def create_item_from_data(item_data):
    """
    Создаёт предмет из сохранённых данных.
    """
    if item_data is None:
        return None

    item_id = item_data["id"]
    item = create_item(item_id)
    item.durability = item_data["durability"]

    return item


def create_player(character_class, name, sex="male", level=1):
    """
    Создаёт персонажа игрока указанного класса, имени и пола.

    Персонаж сначала создаётся на первом уровне, после чего
    получает стартовое оружие и последовательно повышает уровень.

    Аргументы:
        character_class (type[Character]): класс создаваемого персонажа.
        name (str): имя персонажа.
        sex (str): пол персонажа. По умолчанию "male".
        level (int): целевой уровень персонажа. По умолчанию 1.

    Возвращает:
        Character: созданного персонажа игрока.
    """
    created_player = character_class(name, sex)

    weapon_id = STARTING_WEAPONS[character_class.__name__]
    created_player.hands = create_item(weapon_id)

    set_level(created_player, level)

    return created_player


def create_enemy(player):
    """
    Создаёт случайного противника для дуэли с игроком.

    Случайным образом выбирает класс противника из доступных классов
    и устанавливает ему уровень в диапазоне ±2 от уровня игрока.

    Аргументы:
        player (Character): игрок, относительно уровня которого
            подбирается уровень противника.

    Возвращает:
        Character: созданного и прокачанного противника.
    """
    enemy_class = random.choice(list(CHARACTER_CLASSES.values()))
    created_enemy = enemy_class("Враг")

    weapon_id = STARTING_WEAPONS[enemy_class.__name__]
    created_enemy.hands = create_item(weapon_id)

    enemy_level = random.randint(player.lvl - 2, player.lvl + 2)

    if enemy_level < 1:
        enemy_level = 1

    set_level(created_enemy, enemy_level)

    return created_enemy
