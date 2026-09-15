from src.characters import CHARACTER_CLASSES
from src.items import Weapon


def create_player_from_input():
    """
    Запрашивает у пользователя данные нового персонажа
    и создаёт его через переданный класс.
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
    Выводит статистику персонажа.
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

Сейчас в руках: {hands}
========================================
""")

    input("Нажми Enter, чтобы вернуться в меню.")


def show_inventory(player):
    """
    Открывает меню инвентаря персонажа.

    Позволяет просматривать содержимое инвентаря, деньги,
    экипированное оружие, снимать оружие с рук и экипировать
    оружие из выбранной ячейки.
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
            if item is None:
                item_name = "Пусто"
            else:
                item_name = item.name

            print(f"{number}. {item_name}")

        print(f"""
----------------------------------------
Деньги: {player.inventory.currency}
В руках: {player.hands.name if player.hands else "Пусто"}
----------------------------------------

6. Снять оружие с рук
7. Экипировать оружие
8. Выйти
========================================
""")

        choice = input("Выбери действие: ")

        if choice == "6":
            unequip_weapon(player)

        elif choice == "7":
            equip_weapon(player)

        elif choice == "8":
            return

        else:
            print("Ошибка ввода: такого действия нет.")


def unequip_weapon(player):
    """
    Снимает оружие с рук и помещает его в первую свободную
    ячейку инвентаря.
    """
    if player.hands is None:
        print("\nВ руках ничего нет.")
        return

    empty_slot = None

    for number, item in enumerate(player.inventory.slots):
        if item is None:
            empty_slot = number
            break

    if empty_slot is None:
        print("\nНет свободного места в инвентаре.")
        return

    player.inventory.slots[empty_slot] = player.hands
    player.hands = None

    print(f"\nОружие убрано в ячейку " f"{empty_slot + 1}.")


def equip_weapon(player):
    """
    Позволяет выбрать оружие из инвентаря и экипировать его.

    Если в руках уже есть оружие, оно меняется местами
    с выбранным предметом в инвентаре.
    """
    try:
        slot_number = int(input("\nВведи номер ячейки оружия: "))
    except ValueError:
        print("Ошибка ввода: необходимо ввести целое число.")
        return

    if not 1 <= slot_number <= len(player.inventory.slots):
        print("Ошибка ввода: такой ячейки нет.")
        return

    slot_index = slot_number - 1
    item = player.inventory.slots[slot_index]

    if item is None:
        print("Эта ячейка пуста.")
        return

    if not isinstance(item, Weapon):
        print("Этот предмет нельзя экипировать как оружие.")
        return

    player.inventory.slots[slot_index] = player.hands
    player.hands = item

    print(f"\nОружие «{player.hands.name}» экипировано.")


def show_main_menu():
    """
    Выводит главное меню игры.
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
