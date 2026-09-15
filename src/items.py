class Item:
    def __init__(self, name, durability):
        self.name = name
        self.durability = durability

    def use(self):
        self.durability = max(self.durability - 1, 0)

        if self.durability == 0:
            print(f"{self.name} был уничтожен")
            return True

        return False


class Weapon(Item):
    def __init__(
        self,
        item_id,
        name,
        durability,
        damage,
        weight,
        damage_type,
        can_melee,
        can_ranged,
    ):
        super().__init__(name, durability)

        self.item_id = item_id
        self.damage = damage
        self.weight = weight
        self.damage_type = damage_type
        self.can_melee = can_melee
        self.can_ranged = can_ranged
