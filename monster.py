import pygame
import random


class Monster:
    Monsters_Images = {
        1: ['images/jelly.png', 'images/goblin.png', 'images/bee.png', 'images/flower.png',
            'images/sheep.png', 'images/beaver.png', 'images/tree.png'],
        2: ['images/2cactus.png', 'images/2snake.png', 'images/2scorpion.png', 'images/3skeleton.png',
            'images/2beetle.png'],
        3: ['images/3bat.png', 'images/3round1.png', 'images/3round2.png', 'images/3skeleton.png',
            'images/jelly.png', 'images/2scorpion.png'],
        4: ['images/4bergmite.png', 'images/4eskimo.png', 'images/jellyBlue.png',
            'images/4penguin.png', 'images/4snowman.png'],
        5: ['images/5coal.png', 'images/5fire.png', 'images/jellyRed.png', 'images/5knight.png', 'images/5brawler.png']
    }

    def __init__(self, level, is_boss=False, boss_image=None):
        self.level = level
        if is_boss:
            self.image = pygame.image.load(boss_image).convert_alpha()
        else:
            self.image = pygame.image.load(random.choice(self.get_image_set())).convert_alpha()
        self.rect = self.image.get_rect(bottomright=(800, 600))
        self.mask = pygame.mask.from_surface(self.image)
        self.max_health = 10 + (level * level * level)//4 if not is_boss else self.get_boss_health()
        self.health = self.max_health

    def is_boss(self):
        return self.is_boss

    def get_image_set(self):
        monster_set = self.level // 10 + 1
        return Monster.Monsters_Images[monster_set]

    def get_boss_health(self):
        boss_healths = [6000, 50000, 150000, 300000, 650000]
        return boss_healths[self.level // 10 - 1]
