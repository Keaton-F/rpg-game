import random


def attack(attacker, defender):
    """
    Выполняет атаку одного персонажа на другого.

    Тип атаки и используемые характеристики определяются оружием
    в руках атакующего. Без оружия персонаж выполняет физическую атаку.

    Физическая атака использует силу атакующего и броню противника.
    Магическая атака использует интеллект атакующего и сопротивление
    противника.

    Вес оружия уменьшает меткость атаки, а урон оружия добавляется
    к урону атакующего.

    Аргументы:
        attacker (Character): персонаж, который атакует.
        defender (Character): персонаж, который получает удар.

    Возвращает:
        int: количество нанесённого урона.
    """
    weapon_weight = 0
    weapon_damage = 0
    attack_power = attacker.strength
    defense = defender.armor

    if attacker.hands is not None:
        weapon_weight = attacker.hands.weight
        weapon_damage = attacker.hands.damage

        if attacker.hands.damage_type == "magical":
            attack_power = attacker.intelligence
            defense = defender.resistance

    accuracy = int(
        60 + (attacker.skill - defender.speed) * 5 + attacker.luck - weapon_weight + 0.5
    )

    convert = 0

    if accuracy > 100:
        convert = (accuracy - 100) / 10
        accuracy = 100

    critical_chance = int(
        (attacker.skill / defender.skill) * 3 + convert + attacker.luck + 0.5
    )

    dice = random.randint(1, 100)
    # Бросок на успешную атаку.

    print(f"""
{attacker.name} атакует!

{"Меткость атакующего:":<25}{accuracy}%
{"Шанс крит. попадания:":<25}{critical_chance}%
{"Урон атакующего:":<25}{attack_power + weapon_damage}
{"Защита противника:":<25}{defense}

ОЗ {defender.name}: {defender.health}/{defender.max_health}
""")

    if dice <= accuracy:
        critical_dice = random.randint(1, 100)
        # Бросок на критический урон.

        if critical_dice <= critical_chance:
            print(f"{attacker.name} в ярости! Сокрушительная атака!")
            attack_power *= 2
        else:
            print("Успешная атака!")

        damage = max(
            attack_power + weapon_damage - defense,
            0,
        )

        defender.health -= damage

        if attacker.hands is not None:
            destroyed = attacker.hands.use()

            if destroyed:
                attacker.hands = None

        print(f"""
Нанесено урона: {damage}
ОЗ {defender.name}: {max(defender.health, 0)}/{defender.max_health}
""")
    else:
        damage = 0

        print(f"""
Промах!

{defender.name} увернулся от атаки, не получив никаких повреждений.
ОЗ {defender.name}: {defender.health}/{defender.max_health}
""")

    return damage


def battle_loop(player, enemy):
    """
    Запускает цикл сражения между игроком и противником.

    Игрок может атаковать противника или гарантированно сбежать.
    После успешной атаки игрока противник, если остался жив,
    всегда атакует в ответ.

    Опыт за бой сначала накапливается отдельно,
    а после завершения боя начисляется персонажу.

    Аргументы:
        player (Character): персонаж игрока.
        enemy (Character): противник.

    Возвращает:
        None: завершает бой после победы, поражения или побега.
    """
    battle_exp = 0

    print(f"""
========================================
              НАЧАЛО БОЯ
========================================
{player.name} ({player.unit_class})
    VS
{enemy.name} ({enemy.unit_class})
========================================
""")

    while player.health > 0 and enemy.health > 0:
        print(f"""
----------------------------------------
{player.name}
{"ОЗ:":<8}{player.health}/{player.max_health}
----------------------------------------
{enemy.name}
{"ОЗ:":<8}{enemy.health}/{enemy.max_health}
----------------------------------------

1. Удар
2. Побег
""")

        user_input = input("Выбери действие: ")

        if user_input == "1":
            attack(player, enemy)
            battle_exp += 10

            if enemy.health <= 0:
                print(f"""
{enemy.name} повержен!
{player.name} одержал победу!
""")

                player.gain_exp(battle_exp)

                print(f"""
Получено опыта: {battle_exp}
""")
                break

            input("\nНажми Enter, чтобы продолжить.")

            attack(enemy, player)
            battle_exp += 2

            if player.health <= 0:
                print(f"""
{player.name} теряет сознание...
Поражение.
""")
                break

            input("\nНажми Enter, чтобы продолжить.")

        elif user_input == "2":
            battle_exp = int(battle_exp / 2 + 0.5)
            player.gain_exp(battle_exp)

            print(f"""
{player.name} покидает сражение.
Бой завершён.

Получено опыта: {battle_exp} exp.
""")
            break

        else:
            print("""
Ошибка ввода: необходимо выбрать 1 или 2.
""")

    player.health = player.max_health
    print("Здоровье восстановлено.")
