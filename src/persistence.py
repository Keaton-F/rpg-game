import json

from src.characters import CHARACTER_CLASSES
from src.factories import create_item_from_data


def load_character():
    """
    Загружает персонажа из файла сохранения.

    Читает данные из data/save.json, определяет сохранённый тип персонажа,
    находит соответствующий класс в CHARACTER_CLASSES и восстанавливает
    персонажа с помощью метода from_dict().

    Возвращает:
        Character | None: восстановленного персонажа или None,
        если файл отсутствует, содержит некорректный JSON, имеет
        неподходящий формат данных или содержит неизвестный тип персонажа.
    """
    try:
        with open("data/save.json", "r", encoding="utf-8") as file:
            character_data = json.load(file)

        if not isinstance(character_data, dict):
            return None

        character_type = character_data["type"]
        character_class = CHARACTER_CLASSES[character_type]

        character = character_class.from_dict(character_data)

        character.hands = create_item_from_data(character_data["hands"])

        inventory_data = character_data["inventory"]

        character.inventory.slots = [create_item_from_data(item_data) for item_data in inventory_data["slots"]]

        return character

    except (
        FileNotFoundError,
        json.JSONDecodeError,
        TypeError,
        UnicodeDecodeError,
        KeyError,
    ):
        return None


def save_character(character):
    """
    Сохраняет состояние персонажа в файл data/save.json.

    Преобразует атрибуты персонажа в словарь, добавляет информацию
    о его классе и записывает полученные данные в формате JSON.

    Аргументы:
        character (Character): персонаж, состояние которого необходимо сохранить.
    """
    character_data = character.__dict__.copy()

    if character.hands is None:
        character_data["hands"] = None
    else:
        character_data["hands"] = {
            "id": character.hands.item_id,
            "durability": character.hands.durability,
        }

    character_data["inventory"] = {
        "slots": [
            (
                None
                if item is None
                else {
                    "id": item.item_id,
                    "durability": item.durability,
                }
            )
            for item in character.inventory.slots
        ],
        "currency": character.inventory.currency,
    }

    character_data["type"] = character.__class__.__name__

    with open("data/save.json", "w", encoding="utf-8") as file:
        json.dump(character_data, file, ensure_ascii=False, indent=4)
