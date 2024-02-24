import math
import pygame
import sys

backgrounds = {
    'level_1': pygame.image.load('Picture/level1_map.jpg'),
    'level_2': pygame.image.load('Picture/level2_map.jpg'),
    #    'level_3' : pygame.image.load('Picture/level3_map.jpg'),
    #    'level_4' : pygame.image.load('Picture/level4_map.jpg'),
    #    'level_5' : pygame.image.load('Picture/level5_map.jpg')
}
paths_top = {
    'level_1': [(1250, 0), (800, 350), (10, 300)],
    #    'level_2': [(1250, 0), (800, 350), (10, 300)],
    #    'level_3': [(1250, 0), (800, 350), (10, 300)],
    #    'level_4': [(1250, 0), (800, 350), (10, 300)],
    #    'level_5': [(1250, 0), (800, 350), (10, 300)],
}
paths_low = {
    'level_1': [(1250, 650), (800, 350), (10, 400)],
    #    'level_2': [(1250, 650), (800, 350), (10, 400)],
    #    'level_3': [(1250, 650), (800, 350), (10, 400)],
    #    'level_4': [(1250, 650), (800, 350), (10, 400)],
    #    'level_5': [(1250, 650), (800, 350), (10, 400)],
}
Special_location_Tower = {
    'level_1': [(150, 170, 60), (345, 170, 60), (515, 170, 60), (670, 170, 60), (1075, 355, 60),
                (515, 545, 60),(150, 545, 60), (345, 545, 60), (670, 545, 60)],
    'level_2': [(275, 111, 60), (565, 111, 60), (855, 111, 60), (1145, 111, 60),
                (275, 630, 60), (565, 630, 60), (855, 630, 60), (1145, 630, 60)],
    #    'level_3': [(150, 170, 60), (345, 170, 60), (540, 170, 60), (735, 170, 60), (1075, 355, 60), (540, 545, 60),(150, 545, 60), (345, 545, 60), (735, 170, 60)],
    #    'level_4': [(150, 170, 60), (345, 170, 60), (540, 170, 60), (735, 170, 60), (1075, 355, 60), (540, 545, 60),(150, 545, 60), (345, 545, 60), (735, 170, 60)],
    #    'level_5': [(150, 170, 60), (345, 170, 60), (540, 170, 60), (735, 170, 60), (1075, 355, 60), (540, 545, 60),(150, 545, 60), (345, 545, 60), (735, 170, 60)]
}
Special_location_Obstacle = {
#    'level_2': [(150, 170, 60), (345, 170, 60), (540, 170, 60), ]
    #    'level_3': [(150, 170, 60), (345, 170, 60), (540, 170, 60), (735, 170, 60), (1075, 355, 60), (540, 545, 60),(150, 545, 60), (345, 545, 60), (735, 170, 60)],
    #    'level_4': [(150, 170, 60), (345, 170, 60), (540, 170, 60), (735, 170, 60), (1075, 355, 60), (540, 545, 60),(150, 545, 60), (345, 545, 60), (735, 170, 60)],
    #    'level_5': [(150, 170, 60), (345, 170, 60), (540, 170, 60), (735, 170, 60), (1075, 355, 60), (540, 545, 60),(150, 545, 60), (345, 545, 60), (735, 170, 60)]
}


class Subwindow:
    def __init__(self, x, y, width, height, color, content):
        self.surface = pygame.Surface((width, height))
        self.rect = self.surface.get_rect(topleft=(x, y))
        self.color = color
        self.content = content

    def draw(self, surface):
        pygame.draw.rect(self.surface, self.color, self.surface.get_rect())
        font = pygame.font.Font(None, 36)
        text = font.render(' '.join(self.content), True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
        self.surface.blit(text, text_rect)
        surface.blit(self.surface, self.rect)
        self.rect.topleft = (self.rect.x,self.rect.y)


Score_Subwindow = Subwindow(0, 50, 125, 50, (30, 100, 50), 'score')
Player_health_Subwindow = Subwindow(0, 0, 350, 50, (30, 100, 50), 'your gate health')
Fail_Subwindow = Subwindow(350, 250, 550, 200, (155, 10, 60), 'your village has been destroy')
Fail_re_start_Subwindow = Subwindow(350, 450, 550, 50, (155, 110, 60), 'did you want fight again ? ')
Level_win_Subwindow = Subwindow(300, 250, 675, 200, (130, 200, 150), 'your village-defend was successful !')
Ready_to_next_level_Subwindow = Subwindow(300, 250, 625, 200, (130, 200, 150), 'are you ready for NEXT LEVEL ?')
Go_to_next_level = Subwindow(300, 450, 625, 75, (180, 200, 150), 'yes,IM READY')
Return_pervious_level = Subwindow(300, 525, 625, 75, (230, 200, 150), 'not yet,letme return back')


class Dialog_box:
    def __init__(self, x, y):
        self.radius = 30
        self.surface = pygame.Surface((60, 120))
        self.square_surface = pygame.Surface((520, 75))
        self.rect = self.surface.get_rect(center=(x, y))
        self.color = (0, 200, 200)
        self.yes_rect = pygame.Rect(x,y -30,60,30)
        self.no_rect = pygame.Rect(x,y +30,60, 30)

    def reminder(self, surface):
        pygame.draw.rect(self.square_surface, self.color, (0, 0, 520, 75))
        font = pygame.font.Font(None, 27)
        text = font.render("          you will spend 100 score to buliding a new Tower", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.square_surface.get_width() // 2, self.square_surface.get_height() // 2))
        self.square_surface.blit(text, text_rect)
        surface.blit(self.square_surface, self.rect)

    def yes(self, surface):
        pygame.draw.circle(self.surface, (self.color), (self.radius, self.radius), self.radius)
        font = pygame.font.Font(None, 36)
        text = font.render("yes", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.surface.get_width() // 2, self.surface.get_height() // 2 - 30))
        self.surface.blit(text, text_rect)
        surface.blit(self.surface, self.rect)

    def no(self, surface):
        pygame.draw.circle(self.surface, (self.color), (self.radius, self.radius +60), self.radius)
        font = pygame.font.Font(None, 36)
        text = font.render("no", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.surface.get_width() // 2, self.surface.get_height() // 2 + 30))
        self.surface.blit(text, text_rect)
        surface.blit(self.surface, self.rect)


class Tower:
    def __init__(self, x, y, radius, content, attack_damage, attack_interval, attack_range, color, attack_range_color,
                 bullet_color, bullet_size):
        self.surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        self.attack_range_surface = pygame.Surface((attack_range * 2, attack_range * 2), pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=(x, y))
        self.color = color
        self.content = content
        self.radius = radius

        self.attack_damage = attack_damage
        self.attack_range = attack_range
        self.attack_range_color = attack_range_color

        self.bullet_color = bullet_color
        self.bullet_size = bullet_size

        self.last_attack_time = pygame.time.get_ticks()
        self.attack_cooldown = attack_interval * 1000

    def draw(self, surface):
        pygame.draw.circle(surface,
                           (self.attack_range_color[0], self.attack_range_color[1], self.attack_range_color[2]),
                           (self.rect.centerx, self.rect.centery), self.attack_range, 3)
        pygame.draw.circle(self.surface, self.color,
                           (self.radius, self.radius), self.radius)
        font = pygame.font.Font(None, 36)
        text = font.render(self.content, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.surface.get_width() // 2, self.surface.get_height() // 2))
        self.surface.blit(text, text_rect)
        surface.blit(self.surface, self.rect)

    def attack(self, enemy):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time > self.attack_cooldown:
            self.last_attack_time = current_time
            return Bullet(self.rect.centerx, self.rect.centery, enemy,
                          15, self.attack_damage, self.bullet_color, self.bullet_size)
        else:
            return None

    def detect_enemy(self, enemy):
        dx = self.rect.centerx - enemy.rect.centerx
        dy = self.rect.centery - enemy.rect.centery
        distance = math.sqrt(dx * dx + dy * dy)
        return distance <= self.attack_range


Bow_Tower = Tower(107500, 35000, 50, 'BOW',
                  120, 0, 220, (255, 0, 120),
                  (135, 200, 250), (255, 0, 0), 10)


class Bullet:
    def __init__(self, x, y, target, speed, damage, color, size):
        self.x = x
        self.y = y
        self.target = target
        self.speed = speed
        self.damage = damage
        self.color = color
        self.size = size

    def move(self):
        dx = self.target.rect.centerx - self.x
        dy = self.target.rect.centery - self.y
        distance = math.sqrt(dx * dx + dy * dy)
        if distance == 0:
            return
        dx /= distance
        dy /= distance
        dx *= self.speed
        dy *= self.speed
        self.x += dx
        self.y += dy

    def hit_target(self):
        dx = self.target.rect.centerx - self.x
        dy = self.target.rect.centery - self.y
        distance = math.sqrt(dx * dx + dy * dy)
        return distance <= self.target.radius

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)


class Enemy:
    def __init__(self, x, y, radius, color, health, speed, content, score, path):
        self.surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=(x, y))
        self.color = color
        self.content = content
        self.radius = radius

        self.health = health
        self.speed = speed
        self.score = score
        self.path = []
        self.path_index = 0
        self.position = (0, 0)

    def set_path(self, path):
        self.path = path
        self.path_index = 0
        self.position = self.path[self.path_index]

    def move(self):
        if self.path_index >= len(self.path):
            return
        target_x, target_y = self.path[self.path_index]
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < self.speed:
            self.path_index += 1
        else:
            dx /= distance
            dy /= distance
            self.rect.centerx += dx * self.speed
            self.rect.centery += dy * self.speed

    def take_damage(self, damage):
        self.health -= damage

    def draw(self, surface):
        pygame.draw.circle(self.surface, self.color, (self.radius, self.radius), self.radius)
        font = pygame.font.Font(None, 36)
        text = font.render(self.content, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.surface.get_width() // 2, self.surface.get_height() // 2))
        self.surface.blit(text, text_rect)
        surface.blit(self.surface, self.rect)

pygame.init()
clock = pygame.time.Clock()

current_screen = 'level_1'

background = backgrounds[current_screen]
background_size = background.get_rect().size
window = pygame.display.set_mode(background_size)
pygame.display.set_caption('tower defense game')

def Initialize():
    global towers, bullets, bullets_to_remove, enemies, create_top_enemy_time, \
        create_low_enemy_time, enemies_to_remove, current_create_time, last_create_time, \
        score, player_health

    towers = []
    towers.append(Bow_Tower)

    bullets = []
    bullets_to_remove = []

    enemies = []
    create_top_enemy_time = 0
    create_low_enemy_time = 0
    enemies_to_remove = []

    current_create_time = 0
    last_create_time = 0

    score = 100
    player_health = 3

running = True
paused = False
dialog_box = None
need_initialize = True
while running:
    if need_initialize:
        Initialize()
        need_initialize = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                paused = not paused

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if dialog_box is not None and event.button == 1:
                if dialog_box.yes_rect.collidepoint(mouse_x, mouse_y) and score >= 100:
                    new_Tower = Tower(dialog_box.rect.centerx, dialog_box.rect.centery, 50, 'BOW', 20, 0.45, 250,
                                      (255, 0, 120), (135, 200, 250), (255, 0, 0), 10)
                    towers.append(new_Tower)
                    score -= 100
                    dialog_box = None
                elif dialog_box.no_rect is not None and dialog_box.no_rect.collidepoint(mouse_x, mouse_y) or not dialog_box.yes_rect.collidepoint(mouse_x, mouse_y):
                    dialog_box = None
            elif current_screen in Special_location_Tower:
                for location in Special_location_Tower[current_screen]:
                    x, y, r = location
                    distance = ((mouse_x - x) ** 2 + (mouse_y - y) ** 2) ** 0.5
                    if distance <= r:
                        dialog_box = Dialog_box(x, y)

    if not paused:
        if current_screen == 'level_1':
            if need_initialize:
                Initialize()
                need_initialize = False
            window.blit(background, (0, 0))

            if dialog_box is not None:
                dialog_box.reminder(window)
                dialog_box.yes(window)
                dialog_box.no(window)

            Score_Subwindow.draw(window)
            Score_Subwindow.content = ('score:', str(score))
            Player_health_Subwindow.draw(window)
            Player_health_Subwindow.content = ('your vallage gate health:', str(player_health))

            current_create_time = pygame.time.get_ticks()
            if create_top_enemy_time < 3 and create_low_enemy_time < 3 and current_create_time - last_create_time >= 1000:
                last_create_time = current_create_time
                new_top_small_Enemy = Enemy(1250, 0, 20, (0, 111, 161), 40, 6, 'new_small_enemy', 50, paths_top)
                new_low_small_Enemy = Enemy(1250, 650, 20, (50, 111, 161), 40, 6, 'new_small_enemy', 50, paths_low)
                new_top_small_Enemy.set_path(paths_top[current_screen])
                new_low_small_Enemy.set_path(paths_low[current_screen])
                enemies.append(new_top_small_Enemy)
                enemies.append(new_low_small_Enemy)
                create_top_enemy_time += 1
                create_low_enemy_time += 1

            for tower in towers:
                tower.draw(window)
                for enemy in enemies:
                    if tower.detect_enemy(enemy):
                        bullet = tower.attack(enemy)
                        if bullet is not None:
                            bullets.append(bullet)

            for bullet in bullets:
                bullet.move()
                bullet.draw(window)
                if bullet.hit_target():
                    bullet.target.take_damage(bullet.damage)
                    if bullet.target.health <= 0:
                        enemies_to_remove.append(bullet.target)
                        continue
                    if bullet not in bullets_to_remove:
                        bullets_to_remove.append(bullet)
            for bullet in bullets_to_remove:
                if bullet in bullets:
                    bullets.remove(bullet)

            for enemy in enemies:
                if enemy.health < 0:
                    enemies_to_remove.append(enemy)
                else:
                    enemy.move()
                    enemy.draw(window)
                    enemy.content = str(enemy.health)
            for enemy in enemies_to_remove:
                if enemy in enemies:
                    enemies.remove(enemy)
                    score += enemy.score
                    for bullet in bullets:
                        if bullet.target == enemy:
                            bullets_to_remove.append(bullet)
            for bullet in bullets_to_remove:
                if bullet in bullets:
                    bullets.remove(bullet)

            for enemy in enemies:
                if enemy.rect.x <= 10:
                    player_health -= 1
                    enemies_to_remove.append(enemy)
            for enemy in enemies_to_remove:
                if enemy in enemies:
                    enemies.remove(enemy)

            if player_health <= 0:
                Fail_Subwindow.draw(window)
                Fail_re_start_Subwindow.draw(window)
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if Fail_re_start_Subwindow.rect.collidepoint(mouse_x,mouse_y) and event.button == 1:
                            need_initialize = True

            if enemies == [] and create_low_enemy_time == 3 and player_health > 0:
                Level_win_Subwindow.draw(window)
                if 'last_completion_time' not in locals():
                    last_completion_time = pygame.time.get_ticks()
                current_completion_time = pygame.time.get_ticks()
                if current_completion_time - last_completion_time >= 5000:
                    current_screen = 'halftime'

        elif current_screen == 'halftime':
            if need_initialize:
                Initialize()
                need_initialize = False
            window.fill((0, 0, 0))
            Score_Subwindow.draw(window)
            Ready_to_next_level_Subwindow.draw(window)
            Go_to_next_level.draw(window)
            Return_pervious_level.draw(window)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if Go_to_next_level.rect.collidepoint(mouse_x,mouse_y) and event.button == 1:
                        current_screen = 'level_2'
                        need_initialize = True
                    elif Return_pervious_level.rect.collidepoint(mouse_x,mouse_y) and event.button == 1 :
                        current_screen = 'level_1'
                        need_initialize = True

        elif current_screen == 'level_2':
            if need_initialize:
                Initialize()
                need_initialize = False
            background = backgrounds[current_screen]
            window.blit(background,(0,0))

            if dialog_box is not None:
                dialog_box.reminder(window)
                dialog_box.yes(window)
                dialog_box.no(window)

            for tower in towers:
                tower.draw(window)


            Score_Subwindow.draw(window)
            Score_Subwindow.content = ('score:', str(score))
            Player_health_Subwindow.draw(window)
            Player_health_Subwindow.content = ('your vallage gate health:', str(player_health))


    clock.tick(30)
    pygame.display.flip()
pygame.quit()
sys.exit()
