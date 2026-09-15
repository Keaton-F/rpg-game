import random

from src.inventory import Inventory


class Character:
    def __init__(
        self,
        name,
        unit_class,
        health,
        strength,
        intelligence,
        armor,
        resistance,
        speed,
        skill,
        luck,
        constitution,
        growth_rates,
        sex="male",
    ):
        self.name = name
        self.unit_class = unit_class
        self.sex = sex

        self.lvl = 1
        self.exp = 0

        self.health = health
        self.max_health = health
        self.strength = strength
        self.intelligence = intelligence
        self.armor = armor
        self.resistance = resistance
        self.speed = speed
        self.skill = skill
        self.luck = luck
        self.constitution = constitution

        self.growth_rates = growth_rates

        self.hands = None
        self.inventory = Inventory()

    def level_up(self):
        """
        Повышает уровень персонажа и случайно увеличивает его характеристики
        согласно шансам роста, указанным в growth_rates.

        Для каждой характеристики выполняется отдельная проверка:
        если случайное число от 1 до 100 не превышает установленный шанс,
        характеристика увеличивается на 1.

        При успешном росте здоровья увеличиваются одновременно health
        и max_health.

        Возвращает:
            None: изменяет состояние текущего персонажа напрямую.
        """
        print("Уровень повышен!")
        self.lvl += 1

        for stat, chance in self.growth_rates.items():
            if random.randint(1, 100) <= chance:
                print(f"Число оказалось меньше, чем {chance}")
                print(f"По этой причине хар-ка {stat} улучшается на 1.")

                if stat == "health":
                    self.max_health += 1
                    self.health += 1
                else:
                    setattr(self, stat, getattr(self, stat) + 1)
            else:
                print(f"Число оказалось больше, чем {chance}")
                print(f"По этой причине хар-ка {stat} не меняется.")

    def gain_exp(self, amount):
        """
        Начисляет персонажу указанное количество опыта.

        Если после начисления опыта персонаж достигает 100 очков,
        его уровень повышается, а оставшийся опыт переносится
        на следующий уровень.

        Аргументы:
            amount (int): количество получаемого опыта.

        Возвращает:
            None: изменяет опыт и уровень персонажа напрямую.
        """
        self.exp += amount

        while self.exp >= 100:
            self.exp -= 100
            self.level_up()

    @classmethod
    def from_dict(cls, data):
        character = cls.__new__(cls)

        character.name = data["name"]
        character.unit_class = data["unit_class"]
        character.sex = data["sex"]

        character.lvl = data["lvl"]
        character.exp = data["exp"]

        character.health = data["health"]
        character.max_health = data["max_health"]
        character.strength = data["strength"]
        character.intelligence = data["intelligence"]
        character.armor = data["armor"]
        character.resistance = data["resistance"]
        character.speed = data["speed"]
        character.skill = data["skill"]
        character.luck = data["luck"]
        character.constitution = data["constitution"]

        character.growth_rates = data["growth_rates"]

        character.hands = data["hands"]

        inventory_data = data["inventory"]

        character.inventory = Inventory()
        character.inventory.slots = inventory_data["slots"]
        character.inventory.currency = inventory_data["currency"]

        return character


class Spy(Character):
    def __init__(self, name, sex="male"):
        super().__init__(
            name,
            "Шпион",
            16,
            4,
            3,
            1,
            1,
            10,
            8,
            3,
            5,
            {
                "health": 30,
                "strength": 30,
                "intelligence": 10,
                "armor": 10,
                "resistance": 10,
                "speed": 80,
                "skill": 70,
                "luck": 25,
            },
            sex,
        )


class Knight(Character):
    def __init__(self, name, sex="male"):
        super().__init__(
            name,
            "Рыцарь",
            23,
            6,
            1,
            6,
            2,
            4,
            5,
            1,
            8,
            {
                "health": 60,
                "strength": 40,
                "intelligence": 5,
                "armor": 65,
                "resistance": 40,
                "speed": 15,
                "skill": 25,
                "luck": 15,
            },
            sex,
        )


class Mercenary(Character):
    def __init__(self, name, sex="male"):
        super().__init__(
            name,
            "Наёмник",
            21,
            5,
            1,
            3,
            0,
            6,
            6,
            1,
            7,
            {
                "health": 65,
                "strength": 45,
                "intelligence": 5,
                "armor": 30,
                "resistance": 10,
                "speed": 45,
                "skill": 35,
                "luck": 15,
            },
            sex,
        )


class Mage(Character):
    def __init__(self, name, sex="male"):
        super().__init__(
            name,
            "Маг",
            15,
            2,
            6,
            0,
            5,
            6,
            6,
            0,
            5,
            {
                "health": 45,
                "strength": 15,
                "intelligence": 70,
                "resistance": 60,
                "speed": 35,
                "skill": 45,
                "luck": 15,
            },
            sex,
        )


class Shaman(Character):
    def __init__(self, name, sex="male"):
        super().__init__(
            name,
            "Шаман",
            18,
            3,
            8,
            0,
            6,
            3,
            4,
            2,
            6,
            {
                "health": 55,
                "strength": 20,
                "intelligence": 85,
                "resistance": 70,
                "speed": 10,
                "skill": 20,
                "luck": 10,
            },
            sex,
        )


class Monk(Character):
    def __init__(self, name, sex="male"):
        super().__init__(
            name,
            "Монах",
            13,
            2,
            5,
            0,
            7,
            5,
            7,
            3,
            4,
            {
                "health": 35,
                "strength": 15,
                "intelligence": 50,
                "resistance": 75,
                "speed": 30,
                "skill": 60,
                "luck": 20,
            },
            sex,
        )


class Swordsman(Character):
    def __init__(self, name, sex="male"):
        super().__init__(
            name,
            "Мечник",
            17,
            6,
            2,
            1,
            1,
            9,
            9,
            2,
            5,
            {
                "health": 45,
                "strength": 55,
                "intelligence": 5,
                "armor": 20,
                "resistance": 10,
                "speed": 75,
                "skill": 75,
                "luck": 15,
            },
            sex,
        )


class Bandit(Character):
    def __init__(self, name, sex="male"):
        super().__init__(
            name,
            "Разбойник",
            20,
            7,
            1,
            1,
            0,
            5,
            4,
            2,
            7,
            {
                "health": 60,
                "strength": 65,
                "intelligence": 5,
                "armor": 15,
                "resistance": 5,
                "speed": 30,
                "skill": 30,
                "luck": 20,
            },
            sex,
        )


class Soldier(Character):
    def __init__(self, name, sex="male"):
        super().__init__(
            name,
            "Солдат",
            26,
            5,
            2,
            3,
            1,
            5,
            6,
            1,
            7,
            {
                "health": 75,
                "strength": 40,
                "intelligence": 5,
                "armor": 35,
                "resistance": 10,
                "speed": 30,
                "skill": 45,
                "luck": 10,
            },
            sex,
        )


class Archer(Character):
    def __init__(self, name, sex="male"):
        super().__init__(
            name,
            "Лучник",
            17,
            4,
            3,
            1,
            1,
            7,
            9,
            3,
            5,
            {
                "health": 45,
                "strength": 30,
                "intelligence": 10,
                "armor": 15,
                "resistance": 10,
                "speed": 55,
                "skill": 85,
                "luck": 20,
            },
            sex,
        )


CHARACTER_CLASSES = {
    "Spy": Spy,
    "Knight": Knight,
    "Mercenary": Mercenary,
    "Mage": Mage,
    "Shaman": Shaman,
    "Monk": Monk,
    "Swordsman": Swordsman,
    "Bandit": Bandit,
    "Soldier": Soldier,
    "Archer": Archer,
}

STARTING_WEAPONS = {
    "Knight": "spear",
    "Archer": "bow",
    "Mage": "fire_tome",
    "Shaman": "dark_tome",
    "Bandit": "axe",
    "Swordsman": "sword",
    "Soldier": "spear",
    "Spy": "sword",
    "Mercenary": "axe",
    "Monk": "light_tome",
}
