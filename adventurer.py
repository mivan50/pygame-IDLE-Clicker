class Adventurer:
    def __init__(self, name, buy_cost, upgrade_scale, damage, damage_scale, image_path):
        self.name = name
        self.buy_cost = buy_cost
        self.level = 0
        self.unlocked = False
        self.upgrade_scale = upgrade_scale
        self.upgrade_cost = int(buy_cost + buy_cost/4)
        self.damage = damage
        self.damage_scale = damage_scale
        self.image_path = image_path

    def unlock(self, curr_gold):
        if not self.unlocked and curr_gold >= self.buy_cost:
            self.unlocked = True
            curr_gold -= self.buy_cost
            self.level = 1
        return curr_gold

    def upgrade(self, curr_gold):
        if self.unlocked and curr_gold >= self.upgrade_cost:
            self.level += 1
            self.damage *= self.damage_scale
            curr_gold -= self.upgrade_cost
            self.upgrade_cost = int(self.buy_cost * self.upgrade_scale * self.level)
        return curr_gold
