from src.characters import CHARACTER_CLASSES
from src.items import Weapon


def create_player_from_input():
    """
    Запрашивает у пользователя данные нового персонажа
    и возвращает выбранный класс, имя и пол персонажа.
    """
    print("""
На данный момент, это игровое пространство будет напоминать всего-лишь
дуэль в абстрактной и абсолютно ровной местности.
Вам предстоит создать своего персонажа.
""")

    user_input = input("Выбери пол персонажа (м/ж): ").lower()

    while user_input != "м" and user_input != "ж":
        print(
            'Любой вариант, кроме "М" и "Ж" не может быть установлен, '
            "это необходимо для корректного отображения текста "
            "в диалоговых окнах."
        )
        user_input = input("Выбери пол персонажа (м/ж) ещё раз: ").lower()

    if user_input == "м":
        sex = "male"
    else:
        sex = "female"

    print("Как (его/её) зовут?")
    unit_name = input("Введи имя персонажа: ").capitalize()

    for number, character_class in enumerate(
        CHARACTER_CLASSES,
        start=1,
    ):
        print(f"{number}. {character_class}")

    while True:
        try:
            user_input = int(input("\nВведи номер класса, для выбора: "))
        except ValueError:
            print("Ошибка ввода: необходимо ввести целое число.")
            continue

        if 1 <= user_input <= len(CHARACTER_CLASSES):
            selected_class = list(CHARACTER_CLASSES.values())[user_input - 1]
            class_name = list(CHARACTER_CLASSES.keys())[user_input - 1]

            print(f"Выбран класс {class_name}.")
            break

        print("Ошибка ввода: такого класса нет.")

    return selected_class, unit_name, sex


def show_statistics(player):
    """
    Выводит полную статистику персонажа.

    Отображает основные данные персонажа, его характеристики,
    текущее оружие и количество денег.
    """
    hands = player.hands.name if player.hands else "Пусто"

    print(f"""
========================================
              СТАТИСТИКА
========================================
{"Имя:":<17}{player.name}
{"Класс:":<17}{player.unit_class}
{"Уровень:":<17}{player.lvl}
{"Опыт:":<17}{player.exp}/100
{"Здоровье:":<17}{player.health}/{player.max_health}
{"Сила:":<17}{player.strength}
{"Интеллект:":<17}{player.intelligence}
{"Броня:":<17}{player.armor}
{"Сопротивление:":<17}{player.resistance}
{"Скорость:":<17}{player.speed}
{"Навык:":<17}{player.skill}
{"Удача:":<17}{player.luck}
{"Конституция:":<17}{player.constitution}
{"Сейчас в руках:":<17}{hands}
{"Деньги:":<17}{player.inventory.currency}
========================================
""")

    input("Нажми Enter, чтобы вернуться в меню.")


def show_battle_analysis(player, enemy):
    """
    Выводит сравнительную информацию о персонаже игрока и противнике.

    Отображает имена, классы, уровни, опыт, здоровье, все характеристики,
    оружие в руках, его текущую и максимальную прочность и количество
    денег обоих персонажей.

    Функция используется непосредственно во время сражения
    и не изменяет состояние персонажей.
    """
    player_weapon = player.hands.name if player.hands else "Пусто"
    enemy_weapon = enemy.hands.name if enemy.hands else "Пусто"

    player_durability = f"{player.hands.durability}/{player.hands.max_durability}" if player.hands else "-"
    enemy_durability = f"{enemy.hands.durability}/{enemy.hands.max_durability}" if enemy.hands else "-"

    print(f"""
========================================
          АНАЛИЗ ПРОТИВНИКА
========================================
{"":<16}{"ИГРОК":<10}{"|":^4}{"ПРОТИВНИК":<10}
{"Имя:":<16}{player.name:<10}{"|":^4}{enemy.name:<10}
{"Класс:":<16}{player.unit_class:<10}{"|":^4}{enemy.unit_class:<10}
{"Уровень:":<16}{player.lvl:<10}{"|":^4}{enemy.lvl:<10}
{"Опыт:":<16}{player.exp:<10}{"|":^4}{enemy.exp:<10}
{"ОЗ:":<16}{f"{player.health}/{player.max_health}":<10}{"|":^4}{f"{enemy.health}/{enemy.max_health}":<10}
----------------------------------------
{"Сила:":<16}{player.strength:<10}{"|":^4}{enemy.strength:<10}
{"Интеллект:":<16}{player.intelligence:<10}{"|":^4}{enemy.intelligence:<10}
{"Броня:":<16}{player.armor:<10}{"|":^4}{enemy.armor:<10}
{"Сопротивление:":<16}{player.resistance:<10}{"|":^4}{enemy.resistance:<10}
{"Скорость:":<16}{player.speed:<10}{"|":^4}{enemy.speed:<10}
{"Навык:":<16}{player.skill:<10}{"|":^4}{enemy.skill:<10}
{"Удача:":<16}{player.luck:<10}{"|":^4}{enemy.luck:<10}
{"Конституция:":<16}{player.constitution:<10}{"|":^4}{enemy.constitution:<10}
----------------------------------------
{"Оружие:":<16}{player_weapon:<10}{"|":^4}{enemy_weapon:<10}
{"Прочность:":<16}{player_durability:<10}{"|":^4}{enemy_durability:<10}
{"Деньги:":<16}{player.inventory.currency:<10}{"|":^4}{enemy.inventory.currency:<10}
========================================
""")

    input("Нажми Enter, чтобы вернуться к бою.")


def show_inventory(player, in_battle=False):
    """
    Открывает универсальное меню инвентаря персонажа.

    Позволяет просматривать содержимое слотов, открывать информацию
    о предметах, экипировать оружие и перемещать предмет из рук
    в выбранный пустой слот.

    Возвращает:
        bool: True, если в бою было совершено действие,
        расходующее ход. Иначе False.
    """
    while True:
        print("""
========================================
              ИНВЕНТАРЬ
========================================
""")

        for number, item in enumerate(
            player.inventory.slots,
            start=1,
        ):
            item_name = item.name if item else "Пусто"
            print(f"{number}. {item_name}")

        print(f"""
----------------------------------------
Деньги: {player.inventory.currency}
В руках: {player.hands.name if player.hands else "Пусто"}
----------------------------------------
6. Выйти
========================================
""")

        choice = input("Выбери ячейку: ")

        if choice == "6":
            return False

        try:
            slot_number = int(choice)
        except ValueError:
            print("Ошибка ввода: необходимо ввести номер ячейки.")
            continue

        if not 1 <= slot_number <= len(player.inventory.slots):
            print("Ошибка ввода: такой ячейки нет.")
            continue

        slot_index = slot_number - 1
        item = player.inventory.slots[slot_index]

        if item is None:
            turn_spent = handle_empty_slot(player, slot_index)
        else:
            turn_spent = show_item_details(player, slot_index)

        if in_battle and turn_spent:
            return True


def show_item_details(player, slot_index):
    """
    Показывает характеристики предмета и доступные действия.
    Возвращает:
        bool: True, если было совершено действие, расходующее ход.
        Иначе False.
    """
    item = player.inventory.slots[slot_index]

    print(f"""========================================
             ИНФОРМАЦИЯ
========================================
{"ID:":<20}{item.item_id}
{"Название:":<20}{item.name}
{"Прочность:":<20}{item.durability}/{item.max_durability}
""")

    if isinstance(item, Weapon):
        print(f"""
{"Урон:":<20}{item.damage}
{"Вес:":<20}{item.weight}
{"Тип урона:":<20}{item.damage_type}
{"Ближний бой:":<20}{"Да" if item.can_melee else "Нет"}
{"Дальний бой:":<20}{"Да" if item.can_ranged else "Нет"}
""")

    action = "Экипировать" if isinstance(item, Weapon) else "Использовать"

    print(f"""
Описание:
{item.description}

1. {action}
2. Назад
========================================
""")

    choice = input("Выбери действие: ")

    if choice == "1":
        if isinstance(item, Weapon):
            equip_item(player, slot_index)
            return True

        return use_item(player, slot_index)

    if choice != "2":
        print("Ошибка ввода: необходимо выбрать 1 или 2.")

    return False


def use_item(player, slot_index):
    """Использует обычный предмет из выбранного слота."""

    item = player.inventory.slots[slot_index]

    if item.heal is not None:
        if player.health >= player.max_health:
            print("\nЗдоровье уже полностью восстановлено.")
            return False

        old_health = player.health
        player.health = min(
            player.health + item.heal,
            player.max_health,
        )
        restored = player.health - old_health

        item.use()

        print(
            f"\n{item.name} использовано."
            f"\nВосстановлено здоровья: {restored}"
            f"\nОЗ: {player.health}/{player.max_health}"
        )

        if item.durability == 0:
            player.inventory.slots[slot_index] = None

        return True

    print("Для этого предмета пока нет доступного действия.")
    return False


def equip_item(player, slot_index):
    """
    Меняет выбранный предмет в инвентаре с предметом в руках.
    """
    item = player.inventory.slots[slot_index]

    player.inventory.slots[slot_index] = player.hands
    player.hands = item

    print(f"\nПредмет «{player.hands.name}» экипирован.")


def handle_empty_slot(player, slot_index):
    """
    Обрабатывает выбор пустого слота инвентаря.

    Возвращает:
        bool: True, если предмет был помещён в слот.
        Иначе False.
    """
    if player.hands is None:
        print("\nЭта ячейка пуста, и в руках ничего нет.")
        input("Нажми Enter, чтобы продолжить.")
        return False

    print(f"""
Ячейка пуста.
В руках: {player.hands.name}

1. Положить предмет сюда
2. Назад
""")

    choice = input("Выбери действие: ")

    if choice == "1":
        player.inventory.slots[slot_index] = player.hands
        player.hands = None

        print(f"\nПредмет «{player.inventory.slots[slot_index].name}» " f"помещён в ячейку {slot_index + 1}.")
        return True

    if choice != "2":
        print("Ошибка ввода: необходимо выбрать 1 или 2.")

    return False


def show_main_menu():
    """
    Выводит главное меню игры и возвращает выбранное действие.
    """
    print("""
========================================
                 МЕНЮ
========================================
1. Сражаться
2. Статистика
3. Инвентарь
4. Выход
========================================
""")

    return input("Выбери действие: ")
