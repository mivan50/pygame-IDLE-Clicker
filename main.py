import pygame
import sys
import random
from monster import Monster
from adventurer import Adventurer
from healthbar import HealthBar

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Click Conquest')
programIcon = pygame.image.load('images/adv4.png')
pygame.display.set_icon(programIcon)

background = pygame.image.load('images/background.png')
setting = pygame.image.load('images/forrest.png').convert()
font = pygame.font.Font(None, 36)
gold_font = pygame.font.Font(None, 72)
back_button_rect = pygame.Rect(650, 50, 110, 50)
back_button_text = font.render("Go Back", True, (255, 255, 255))
button_rect2 = pygame.Rect(285, 50, 350, 50)

gold = 0
currLevel = 1
monsterNum = 1
clickDamage = 1
DPS = 0
upgrade_cost = 15
running = True
elapsed_time = 0
monster = Monster(currLevel)


settings = ['images/forrest.png', 'images/desert.png', 'images/cave.png', 'images/ice.png', 'images/fire.png',
            'images/win.png']

boss1 = Monster(level=10, is_boss=True, boss_image='images/boss1.png')
boss2 = Monster(level=20, is_boss=True, boss_image='images/boss2.png')
boss3 = Monster(level=30, is_boss=True, boss_image='images/boss3.png')
boss4 = Monster(level=40, is_boss=True, boss_image='images/boss4.png')
boss5 = Monster(level=50, is_boss=True, boss_image='images/boss5.png')

bosses = [boss1, boss2, boss3, boss4, boss5]

adventurer1_image = pygame.image.load('images/adv1.png').convert_alpha()
adventurer2_image = pygame.image.load('images/adv2.png').convert_alpha()
adventurer3_image = pygame.image.load('images/adv3.png').convert_alpha()
adventurer4_image = pygame.image.load('images/adv4.png').convert_alpha()
adventurer5_image = pygame.image.load('images/adv5.png').convert_alpha()

adventurer1 = Adventurer("Brawler", 50, 1.7, 10, 1.75, adventurer1_image)
adventurer2 = Adventurer("Ninja", 200, 2, 70, 1.75, adventurer2_image)
adventurer3 = Adventurer("Wizard", 1000, 1.4, 300, 2.2, adventurer3_image)
adventurer4 = Adventurer("Knight", 2000, 1.0, 750, 2.5, adventurer4_image)
adventurer5 = Adventurer("Samurai", 5000, 1.0, 2000, 2.7, adventurer5_image)

adventurers = [adventurer1, adventurer2, adventurer3, adventurer4, adventurer5]

button_height = 75
button_width = 225
button_spacing = 20

adventurer_buttons = []

for i, adventurer in enumerate(adventurers):
    button_rect = pygame.Rect(10, i * (button_height + button_spacing) + 10, button_width, button_height)
    adventurer_buttons.append(button_rect)


def get_setting_image(level):
    setting_index = (level - 1) // 10
    return pygame.image.load(settings[setting_index]).convert()


def get_dps():
    damage = 0
    for adv in adventurers:
        if adv.unlocked:
            damage += adv.damage
    return damage


def run_boss_fight(boss, screen2):
    boss_timer = 30
    start_time2 = pygame.time.get_ticks()
    while boss_timer > 0 and boss.health >= 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos2 = pygame.mouse.get_pos()
                pos_in_mask2 = pos2[0] - boss.rect.x, pos2[1] - boss.rect.y
                if boss.rect.collidepoint(*pos2) and boss.mask.get_at(pos_in_mask2):
                    boss.health -= clickDamage
                if back_button_rect.collidepoint(pos2):
                    boss.health = boss.max_health
                    return False

        boss_health_bar = HealthBar(375, 175, 300, 40, boss.health, boss.max_health)
        screen2.blit(boss.image, boss.rect)
        boss_health_bar.draw(screen2)

        pygame.draw.rect(screen2, (0, 0, 0), (375, 130, 300, 40))

        if pygame.time.get_ticks() - start_time2 >= 1000:
            boss.health -= DPS
            start_time2 = pygame.time.get_ticks()
            boss_timer -= 1

        timer_text = font.render(f"Boss Timer: {int(boss_timer)} seconds", True, (255, 255, 255))
        screen2.blit(timer_text, (385, 140))

        pygame.display.update()
        pygame.time.Clock().tick(60)

    if boss.health <= 0:
        return True
    else:
        boss.health = boss.max_health
        return False


curr_time = pygame.time.get_ticks()
start_time = pygame.time.get_ticks()
while currLevel <= 50 and running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            pos = pygame.mouse.get_pos()
            pos_in_mask = pos[0] - monster.rect.x, pos[1] - monster.rect.y
            if monster.rect.collidepoint(*pos) and monster.mask.get_at(pos_in_mask):
                monster.health -= clickDamage

            if button_rect2.collidepoint(pos) and gold >= upgrade_cost:
                gold -= upgrade_cost
                clickDamage *= 2
                upgrade_cost *= 2

            if back_button_rect.collidepoint(pos):
                if currLevel > 1:
                    currLevel -= 1
                    monsterNum = 0

            for i, button_rect in enumerate(adventurer_buttons):
                if button_rect.collidepoint(pos):
                    adventurer = adventurers[i]
                    if not adventurer.unlocked:
                        gold = adventurer.unlock(gold)
                    else:
                        gold = adventurer.upgrade(gold)
                    DPS = get_dps()

    if currLevel % 10 == 0:
        if run_boss_fight(bosses[currLevel // 10 - 1], screen):
            gold += currLevel*30
            currLevel += 1
            setting = get_setting_image(currLevel)
        else:
            currLevel -= 1

    if monster.health <= 0:
        monster = Monster(currLevel)
        monsterNum += 1
        gold += random.randint(currLevel, currLevel * 2) * (currLevel // 15 + 1)
        if monsterNum >= 10:
            currLevel += 1
            monsterNum = 0

    gold_text = gold_font.render(str(gold), True, (255, 255, 255))
    level_text = font.render("Level: {}".format(currLevel), True, (255, 255, 255))
    monster_text_line1 = font.render("Monsters:", True, (255, 255, 255))
    monster_text_line2 = font.render("{}/10".format(monsterNum), True, (255, 255, 255))

    health = HealthBar(375, 175, 300, 40, monster.health, monster.max_health)

    setting_rect = setting.get_rect(bottomright=(800, 600))

    screen.blit(background, (0, 0))
    screen.blit(setting, setting_rect)
    screen.blit(gold_text, (125, 500))

    pygame.draw.rect(screen, (0, 128, 255), button_rect2)
    button_text = font.render(f"Upgrade Click Damage: {upgrade_cost}", True, (255, 255, 255))
    screen.blit(button_text, (300, 60))

    pygame.draw.rect(screen, (255, 0, 0), back_button_rect)
    screen.blit(back_button_text, (655, 60))

    for i, button_rect in enumerate(adventurer_buttons):
        adventurer = adventurers[i]
        if not adventurer.unlocked:
            button_text = font.render(f"Buy: {adventurer.buy_cost}", True, (255, 255, 255))
            if gold >= adventurer.buy_cost:
                pygame.draw.rect(screen, (0, 128, 0), button_rect)
            else:
                pygame.draw.rect(screen, (128, 0, 0), button_rect)
        else:
            button_text = font.render(f"Upgrade: {adventurer.upgrade_cost}", True, (255, 255, 255))
            if gold >= adventurer.upgrade_cost:
                pygame.draw.rect(screen, (0, 128, 0), button_rect)
            else:
                pygame.draw.rect(screen, (128, 0, 0), button_rect)
            green_box_rect = pygame.Rect(button_rect.x + button_width - 50, button_rect.y, 50, button_height)
            pygame.draw.rect(screen, (0, 128, 0), green_box_rect)

        adventurer_image_rect = adventurer.image_path.get_rect()
        adventurer_image_rect.topright = (button_rect.x + button_width, button_rect.y)
        screen.blit(adventurer.image_path, adventurer_image_rect)
        screen.blit(button_text, (button_rect.x + 10, button_rect.y + 25))

    if currLevel % 10 != 0:
        screen.blit(monster.image, monster.rect)
        health.draw(screen)
        screen.blit(level_text, (265, 160))
        screen.blit(monster_text_line1, (680, 160))
        screen.blit(monster_text_line2, (720, 190))

    if pygame.time.get_ticks() - curr_time >= 10:
        monster.health -= DPS/75
        curr_time = pygame.time.get_ticks()

    pygame.display.update()
    pygame.time.Clock().tick(60)

final_time = pygame.time.get_ticks() - start_time
while running and currLevel > 50:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    win_image = pygame.image.load('images/win.png').convert()
    screen.blit(win_image, (0, 0))

    minutes = int(final_time / 1000 // 60)
    seconds = int(final_time / 1000 % 60)

    font = pygame.font.Font(None, 70)
    time_text = font.render(f"Final Time: {minutes:02d}:{seconds:02d}", True, (255, 255, 255))
    screen.blit(time_text, (200, 400))

    pygame.display.update()

pygame.quit()
sys.exit()
