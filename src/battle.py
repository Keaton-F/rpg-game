import random

from src.ui import show_battle_analysis, show_inventory


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

    При успешной атаке оружие теряет единицу прочности. Если его
    прочность достигает нуля, оружие уничтожается и убирается
    из рук атакующего.

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

    accuracy = int(60 + (attacker.skill - defender.speed) * 5 + attacker.luck - weapon_weight + 0.5)

    convert = 0

    if accuracy > 100:
        convert = (accuracy - 100) / 10
        accuracy = 100

    critical_chance = int((attacker.skill / defender.skill) * 3 + convert + attacker.luck + 0.5)

    dice = random.randint(1, 100)

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


def try_counterattack(attacker, defender):
    """
    Проверяет возможность контратаки защищающегося персонажа.

    Базовый шанс контратаки зависит от разницы скорости между
    защищающимся и атакующим персонажами. Чем выше скорость
    защищающегося относительно атакующего, тем выше его шанс.

    После этого шанс дополнительно уменьшается пропорционально
    текущему здоровью защищающегося персонажа. Поэтому раненый
    персонаж значительно реже способен выполнить контратаку.

    При успешной проверке защищающийся атакует первоначального
    атакующего.

    Аргументы:
        attacker (Character): персонаж, который совершил атаку.
        defender (Character): персонаж, который получил атаку
            и может выполнить контратаку.

    Возвращает:
        None: функция только выполняет контратаку при успешной проверке.
    """
    chance = 20 + (defender.speed - attacker.speed) * 5
    chance = max(0, min(chance, 100))

    health_percent = int(defender.health / (defender.max_health / 100) + 0.5)

    chance = int(chance / 100 * health_percent + 0.5)

    if random.randint(1, 100) <= chance:
        print(f"{defender.name} контратакует!")
        attack(defender, attacker)


def battle_loop(player, enemy):
    """
    Запускает цикл сражения между игроком и противником.

    В каждом ходу игрок может атаковать противника, открыть инвентарь,
    посмотреть информацию о нём или сбежать.

    После атаки игрока живой противник получает возможность
    выполнить контратаку.

    Затем живой противник атакует игрока. После этой атаки
    игрок также получает возможность выполнить контратаку.

    Анализ противника не расходует ход и после просмотра
    возвращает игрока к выбору действия.

    Просмотр инвентаря также не расходует ход, если игрок
    не совершил действие с предметом.

    Опыт за действия в бою сначала накапливается отдельно,
    а затем начисляется игроку при завершении сражения.

    При победе игрок получает весь накопленный боевой опыт.
    При побеге накопленный опыт уменьшается вдвое.
    При поражении накопленный опыт не начисляется.

    После завершения боя здоровье игрока полностью восстанавливается.

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
{player.name} ({player.unit_class})    VS
{enemy.name} ({enemy.unit_class})
========================================
""")

    while player.health > 0 and enemy.health > 0:
        print(f"""
----------------------------------------
{player.name}{" ОЗ:":<8}{player.health}/{player.max_health}
----------------------------------------
{enemy.name}{" ОЗ:":<8}{enemy.health}/{enemy.max_health}
----------------------------------------
1. Удар
2. Инвентарь
3. Анализ противника
4. Побег
""")

        user_input = input("Выбери действие: ")

        if user_input == "1":
            attack(player, enemy)

            if enemy.health > 0:
                try_counterattack(player, enemy)

            battle_exp += 10

            if enemy.health <= 0:
                print(f"""
{enemy.name} повержен!
{player.name} одержал победу!
""")

                player.gain_exp(battle_exp)

                print(f"Получено опыта: {battle_exp}")
                break

            input("\nНажми Enter, чтобы продолжить.")

            attack(enemy, player)

            if player.health > 0:
                try_counterattack(enemy, player)

            battle_exp += 2

            if player.health <= 0:
                print(f"""
{player.name} теряет сознание...
Поражение.
""")
                break

            input("\nНажми Enter, чтобы продолжить.")

        elif user_input == "2":
            turn_spent = show_inventory(player, in_battle=True)

            if not turn_spent:
                continue

            input("\nНажми Enter, чтобы продолжить.")

            attack(enemy, player)

            if player.health > 0:
                try_counterattack(enemy, player)

            battle_exp += 2

            if player.health <= 0:
                print(f"""
{player.name} теряет сознание...
Поражение.
""")
                break

            input("\nНажми Enter, чтобы продолжить.")

        elif user_input == "3":
            show_battle_analysis(player, enemy)

        elif user_input == "4":
            battle_exp = int(battle_exp / 2 + 0.5)
            player.gain_exp(battle_exp)

            print(f"""
{player.name} покидает сражение.
Бой завершён.
Получено опыта: {battle_exp} exp.
""")
            break

        else:
            print("Ошибка ввода: необходимо выбрать 1, 2, 3 или 4.")

    player.health = player.max_health
    print("Здоровье восстановлено.")
