from src.battle import battle_loop
from src.factories import create_enemy, create_player, create_item
from src.persistence import load_character, save_character
from src.ui import create_player_from_input, show_inventory, show_main_menu, show_statistics

player = load_character()
player.inventory.slots[1] = create_item("healing_potion")

print("""
Добро пожаловать в виртуальный мир, дорогой искатель приключений!
""")

while player is None:
    selected_class, unit_name, sex = create_player_from_input()

    player = create_player(
        selected_class,
        unit_name,
        sex,
    )

    save_character(player)

    print(f"""
Персонаж {player.name} успешно создан!

Данные персонажа сохранены.
Теперь начинается настоящее приключение.
""")


while True:
    user_input = show_main_menu()

    if user_input == "1":
        enemy = create_enemy(player)
        battle_loop(player, enemy)

        input("\nНажми Enter, чтобы вернуться в меню.")

    elif user_input == "2":
        show_statistics(player)

    elif user_input == "3":
        show_inventory(player)

    elif user_input == "4":
        save_character(player)

        print("""
До новых встреч, путешественник!

Данные персонажа сохранены.
""")
        break

    else:
        print("""
Ошибка ввода: необходимо выбрать один из
доступных пунктов меню.
""")
