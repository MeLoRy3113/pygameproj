import pygame
import os
import sys
import random
import sqlite3
import csv



con = sqlite3.connect('userdatabase.db')
cur = con.cursor()

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global killed
        self.image = pygame.transform.scale(load_image("frontafk.png"), (23 * 2, 41 * 2))
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        self.counter = 0
        killed = 0
        self.images_for_right_walk = ["rightmove1.png", "rightmove2.png"]
        self.images_for_left_walk = ["leftmove1.png", "leftmove2.png"]
        self.images_for_back_walk = ["backmove1.png", "backmove2.png"]
        self.images_for_front_walk = ["frontmove1.png", "frontmove2.png"]        
    
    def give_coords(self):
        return self.rect.x, self.rect.y
    
    def amount(self):
        global killed
        killed += 1
    
    def destroy(player):
        player.kill()
    
    def update(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and can_move:
            self.rect.x -= v
            self.rect.x = self.rect.x % 800
            self.image = pygame.transform.scale(load_image(self.images_for_left_walk[self.counter]), (23 * 2, 41 * 2))
            self.counter = (self.counter + 1) % len(self.images_for_left_walk)
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and can_move:
            self.rect.x += v
            self.rect.x = self.rect.x % 800
            self.image = pygame.transform.scale(load_image(self.images_for_right_walk[self.counter]), (23 * 2, 41 * 2))
            self.counter = (self.counter + 1) % len(self.images_for_right_walk)            
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and can_move:
            self.rect.y -= v
            self.rect.y = self.rect.y % 600
            self.image = pygame.transform.scale(load_image(self.images_for_back_walk[self.counter]), (23 * 2, 41 * 2))
            self.counter = (self.counter + 1) % len(self.images_for_back_walk)            
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and can_move:
            self.rect.y += v
            self.rect.y = self.rect.y % 600
            self.image = pygame.transform.scale(load_image(self.images_for_front_walk[self.counter]), (23 * 2, 41 * 2))
            self.counter = (self.counter + 1) % len(self.images_for_front_walk)            
            

class Box(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("box.png"), (45, 45))
    def __init__(self):
        super().__init__()
        self.image = Box.image
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, 800), random.randint(0, 600))
    
    def destroy(box):
        box.kill()
    
    def is_used(box):
        global dmg, total_hp, maxhp, x
        gived_hp = 0
        if player_x - 50 < box.rect.x < player_x + 50 and player_y - 50 < box.rect.y < player_y + 50 and can_move:
            box_sound.play()
            gambling = random.randint(1, 3)
            if gambling == 1:
                gived_hp = random.randint(2, bonus_hp_create)
                if gived_hp + total_hp >= maxhp:
                    maxhp += gived_hp + total_hp - maxhp   
                total_hp += gived_hp
            if gambling == 2:
                give_dmg = random.randint(1, bonus_dmg_create)
                if dmg + give_dmg < 99:
                    dmg += give_dmg
                else:
                    dmg = 99
            if gambling == 3:
                give_dmg = random.randint(1, bonus_dmg_create)
                if dmg + give_dmg < 99:
                    dmg += give_dmg
                else:
                    dmg = 99
                gived_hp = random.randint(2, bonus_hp_create)
                if gived_hp + total_hp >= maxhp:
                    maxhp += gived_hp + total_hp - maxhp     
                total_hp += gived_hp
            if total_hp >= (maxhp * 7) // 8:
                x = 7
            if (maxhp * 6) // 8 <= total_hp < (maxhp * 7) // 8:
                x = 6
            if (maxhp * 5) // 8 <= total_hp < (maxhp * 6) // 8:
                x = 5
            if (maxhp * 4) // 8 <= total_hp < (maxhp * 5) // 8:
                x = 4
            if (maxhp * 3) // 8 <= total_hp < (maxhp * 4) // 8:
                x = 3
            if (maxhp * 2) // 8 <= total_hp < (maxhp * 3) // 8: 
                x = 2
            if (maxhp * 1) // 8 <= total_hp < (maxhp * 2) // 8:
                x = 1
            if total_hp < (maxhp * 1) // 8:
                x = 0        
            box.kill()
            


class Enemy(pygame.sprite.Sprite):
    image = load_image("Enemy.png")
    image = pygame.transform.scale(image, (23 * 2, 41 * 2))
    def __init__(self):
        super().__init__()
        self.counter = 0
        self.image = Enemy.image
        self.rect = self.image.get_rect()
        pos = random.randint(1, 4)
        self.enemy_hp = enemy_hp
        self.anim_counter = 0
        if pos == 1:
            self.rect.center = (-5, random.randint(0, 600))
        elif pos == 2:
            self.rect.center = (805, random.randint(0, 600))
        elif pos == 3:
            self.rect.center = (random.randint(0, 800), -5)
        elif pos == 3:
            self.rect.center = (random.randint(0, 800), 605)
        self.images_for_right_walk = ["enemyright1.png", "enemyright2.png"]
        self.images_for_left_walk = ["enemyleft1.png", "enemyleft2.png"]
        self.images_for_back_walk = ["enemyback1.png", "enemyback2.png"]
        self.images_for_front_walk = ["enemyfront1.png", "enemyfront2.png"]        
        
    def give_coords(self):
        return self.rect.x, self.rect.y

    def update(self):
        player_coords_x, player_coords_y = player_x, player_y
        if player_coords_x < self.rect.x and can_move:
            self.rect.x -= v2
            self.image = pygame.transform.scale(load_image(self.images_for_left_walk[self.anim_counter]), (23 * 2, 41 * 2))
            self.anim_counter = (self.anim_counter + 1) % len(self.images_for_left_walk)
        if player_coords_x > self.rect.x and can_move:
            self.rect.x += v2
            self.image = pygame.transform.scale(load_image(self.images_for_right_walk[self.anim_counter]), (23 * 2, 41 * 2))
            self.anim_counter = (self.anim_counter + 1) % len(self.images_for_right_walk)            
        if player_coords_y < self.rect.y and can_move:
            self.rect.y -= v2
            self.image = pygame.transform.scale(load_image(self.images_for_back_walk[self.anim_counter]), (23 * 2, 41 * 2))
            self.anim_counter = (self.anim_counter + 1) % len(self.images_for_back_walk)            
        if player_coords_y >= self.rect.y and can_move:
            self.rect.y += v2
            self.image = pygame.transform.scale(load_image(self.images_for_front_walk[self.anim_counter]), (23 * 2, 41 * 2))
            self.anim_counter = (self.anim_counter + 1) % len(self.images_for_front_walk)            
    
    def is_damage(enemy):
        global total_hp, dmg, x, maxhp
        if player_x - 20 < enemy.rect.x < player_x + 20 and player_y - 20 < enemy.rect.y < player_y + 20 and can_move:
            if enemy.counter % 15 == 0:
                punch_sound.play()
                enemy.enemy_hp -= dmg
                
                if enemy.enemy_hp <= 0:
                    enemy.kill()
                    if total_hp + bonus_hp > maxhp:
                        maxhp += bonus_hp + total_hp - maxhp
                    total_hp += bonus_hp
                    maxhp += bonus_hp
                    if dmg + bonus_dmg < 99:
                        dmg += bonus_dmg
                    else:
                        dmg = 99
                    if total_hp >= (maxhp * 7) // 8:
                        x = 7
                    if (maxhp * 6) // 8 <= total_hp < (maxhp * 7) // 8:
                        x = 6
                    if (maxhp * 5) // 8 <= total_hp < (maxhp * 6) // 8:
                        x = 5
                    if (maxhp * 4) // 8 <= total_hp < (maxhp * 5) // 8:
                        x = 4
                    if (maxhp * 3) // 8 <= total_hp < (maxhp * 4) // 8:
                        x = 3
                    if (maxhp * 2) // 8 <= total_hp < (maxhp * 3) // 8: 
                        x = 2
                    if (maxhp * 1) // 8 <= total_hp < (maxhp * 2) // 8:
                        x = 1
                    if total_hp < (maxhp * 1) // 8:
                        x = 0                    
                    return 'killed'
                total_hp -= enemy_dmg
                if total_hp <= 0:
                    return False
                if total_hp >= (maxhp * 7) // 8:
                    x = 7
                if (maxhp * 6) // 8 <= total_hp < (maxhp * 7) // 8:
                    x = 6
                if (maxhp * 5) // 8 <= total_hp < (maxhp * 6) // 8:
                    x = 5
                if (maxhp * 4) // 8 <= total_hp < (maxhp * 5) // 8:
                    x = 4
                if (maxhp * 3) // 8 <= total_hp < (maxhp * 4) // 8:
                    x = 3
                if (maxhp * 2) // 8 <= total_hp < (maxhp * 3) // 8: 
                    x = 2
                if (maxhp * 1) // 8 <= total_hp < (maxhp * 2) // 8:
                    x = 1
                if total_hp < (maxhp * 1) // 8:
                    x = 0
            enemy.counter += 1
        return True
        
    def destroy(enemy):
        enemy.kill()


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.can_write = True
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and self.can_write:
                self.active = not self.active
            elif self.can_write:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN and self.can_write:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.can_write = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)    
    
    def get_name(self):
        return self.text
    
    def next(self):
        self.can_write = True
        

def switch_screen(screens):
    screen.blit(screens, (0, 0))
    pygame.display.flip()
            
if __name__ == '__main__':
    pygame.init()
    my_font = pygame.font.SysFont('Sixtyfour', 50)
    my_font_2 = pygame.font.SysFont('Sixtyfour', 40)
    my_font_3 = pygame.font.SysFont('Sixtyfour', 50)
    my_font_4 = pygame.font.SysFont('Sixtyfour', 80)
    lst = []
    COLOR_INACTIVE = pygame.Color('lightskyblue3')
    COLOR_ACTIVE = pygame.Color('dodgerblue2')
    FONT = pygame.font.Font(None, 50)
    bg_img = pygame.transform.scale(load_image("bg1.png"), (800, 600))
    pause = pygame.transform.scale(load_image("pause.png"), (800, 600))
    lose = pygame.transform.scale(load_image("lose.png"), (800, 600))
    win = pygame.transform.scale(load_image("win.png"), (800, 600))
    bg_start = pygame.transform.scale(load_image("bg2.png"), (800, 600))
    fps = 30
    # chisla
    img_0 = pygame.transform.scale(load_image("0.png"), (15, 15))
    img_1 = pygame.transform.scale(load_image("1.png"), (15, 15))
    img_2 = pygame.transform.scale(load_image("2.png"), (15, 15))
    img_3 = pygame.transform.scale(load_image("3.png"), (15, 15))
    img_4 = pygame.transform.scale(load_image("4.png"), (15, 15))
    img_5 = pygame.transform.scale(load_image("5.png"), (15, 15))
    img_6 = pygame.transform.scale(load_image("6.png"), (15, 15))
    img_7 = pygame.transform.scale(load_image("7.png"), (15, 15))
    img_8 = pygame.transform.scale(load_image("8.png"), (15, 15))
    img_9 = pygame.transform.scale(load_image("9.png"), (15, 15))
    dmg_img = pygame.transform.scale(load_image("dmg.png"), (30, 30))
    numbers = [img_0, img_1, img_2, img_3, img_4, img_5, img_6, img_7, img_8, img_9]
    one_im = pygame.transform.scale(load_image("1of8_hp.png"), (75, 7))
    two_im = pygame.transform.scale(load_image("1of4_hp.png"), (75, 7))
    three_im = pygame.transform.scale(load_image("3of8_hp.png"), (75, 7))
    four_im = pygame.transform.scale(load_image("half_hp.png"), (75, 7))
    five_im = pygame.transform.scale(load_image("5of8_hp.png"), (75, 7))
    six_im = pygame.transform.scale(load_image("3of4_hp.png"), (75, 7))
    seven_im = pygame.transform.scale(load_image("7of8_hp.png"), (75, 7))
    full_im = pygame.transform.scale(load_image("full_hp.png"), (75, 7))
    hp_cur = [one_im, two_im, three_im, four_im, five_im, six_im, seven_im, full_im]
    pygame.display.set_caption('Проектная игра')
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    running = True
    v = 5
    v2 = 0
    dmg = 0
    menu_screen = pygame.Surface(size)
    levels_screen = pygame.Surface(size)
    level_screen = pygame.Surface(size)
    record_screen = pygame.Surface(size)
    pause_screen = pygame.Surface(size)
    lose_screen = pygame.Surface(size)
    win_screen = pygame.Surface(size)
    shop_screen = pygame.Surface(size)
    shop_screen.blit(bg_start, (0, 0))
    lose_screen.blit(lose, (0, 0))
    win_screen.blit(win, (0, 0))
    pause_screen.blit(pause, (0, 0))
    level_screen.blit(bg_img, (0, 0))
    menu_screen.blit(bg_start, (0, 0))
    levels_screen.blit(bg_start, (0, 0))
    record_screen.blit(bg_start, (0, 0))
    current_screen = menu_screen
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)    
    enemy_sprites = pygame.sprite.Group()
    box_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    can_move = False
    recorded_now = False
    levels_screen_now = False
    menu_now = False
    end_game = False
    paused = False
    started_endless = 0
    not_endless = True
    start_button = pygame.draw.rect(menu_screen, (225, 194, 246), (250, 80, 300, 75))
    record_button = pygame.draw.rect(menu_screen, (225, 194, 246), (250, 185, 300, 75))
    shop_button = pygame.draw.rect(menu_screen, (225, 194, 246), (250, 290, 300, 75))
    record_button_quit = pygame.draw.rect(record_screen, (225, 194, 246), (40, 30, 150, 50))
    quit_button = pygame.draw.rect(menu_screen,(225, 194, 246), (250, 395, 300, 75))
    first_button = pygame.draw.rect(levels_screen,(225, 194, 246), (250, 160, 300, 75))
    second_button = pygame.draw.rect(levels_screen,(225, 194, 246), (250, 280, 300, 75))
    endless_button = pygame.draw.rect(levels_screen,(225, 194, 246), (250, 400, 300, 75))
    continue_button = pygame.draw.rect(pause_screen,(82, 82, 82), (130, 450, 160, 45))
    title_button = pygame.draw.rect(pause_screen,(82, 82, 82), (320, 450, 160, 45))
    exit_button = pygame.draw.rect(pause_screen,(82, 82, 82), (510, 450, 160, 45))
    retry_lose_button = pygame.draw.rect(lose_screen,(82, 82, 82), (85, 380, 200, 50))
    title_lose_button = pygame.draw.rect(lose_screen,(82, 82, 82), (85, 455, 200, 50))
    next_win_button = pygame.draw.rect(win_screen,(82, 82, 82), (70, 390, 200, 50))
    title_win_button = pygame.draw.rect(win_screen,(82, 82, 82), (70, 455, 200, 50))
    levels_back_button = pygame.draw.rect(levels_screen,(225, 194, 246), (40, 30, 150, 50))
    shop_back_button = pygame.draw.rect(shop_screen, (225, 194, 246), (40, 30, 150, 50))
    record_list = pygame.draw.rect(record_screen, (225, 194, 246), (215, 45, 200, 525))
    shop_list = pygame.draw.rect(shop_screen, (225, 194, 246), (50, 100, 700, 450))
    shop_buy_sec = pygame.draw.rect(shop_screen, (225, 94, 229), (130, 440, 190, 50))
    shop_buy_thr = pygame.draw.rect(shop_screen, (225, 94, 229), (470, 440, 190, 50))
    start_menu_sound = pygame.mixer.Sound("data/Retro Blop 07.wav")
    start_menu_sound.set_volume(1)
    easy_sound = pygame.mixer.Sound("data/easy.wav")
    easy_sound.set_volume(1)    
    normal_sound = pygame.mixer.Sound("data/normal.wav")
    normal_sound.set_volume(1)
    endless_sound = pygame.mixer.Sound("data/endless.wav")
    endless_sound.set_volume(1)    
    punch_sound = pygame.mixer.Sound("data/punch.wav")
    punch_sound.set_volume(0.5)
    pause_sound = pygame.mixer.Sound("data/pause.wav")
    pause_sound.set_volume(0.5)
    unpause_sound = pygame.mixer.Sound("data/unpause.wav")
    unpause_sound.set_volume(0.5)    
    lose_sound = pygame.mixer.Sound("data/lose.wav")
    lose_sound.set_volume(0.5)     
    win_sound = pygame.mixer.Sound("data/win.wav")
    win_sound.set_volume(0.5)
    no_purchase = pygame.mixer.Sound("data/no_purchase.wav")
    no_purchase.set_volume(0.5) 
    box_sound = pygame.mixer.Sound("data/box.wav")
    box_sound.set_volume(0.5)     
    pygame.mixer.music.load("data/menu_music.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    level = 0
    spawnrate = 1
    timer = 0
    f = 2
    x = 7
    killed = 0
    amount_enemy = 1
    perem = True
    createrate = 20
    input_box1 = InputBox(450, 200, 140, 50)
    input_boxes = [input_box1]    
    lst = []
    if cur.execute("select id from record").fetchall():
        no_users = False
    else:    
        no_users = True
    fir_bought = True
    sec_bought = cur.execute("select sec_open from openedbg").fetchall()[0][0]
    thr_bought = cur.execute("select thr_open from openedbg").fetchall()[0][0]
    fir_equiped = cur.execute("select fir_used from openedbg").fetchall()[0][0]
    sec_equiped = cur.execute("select sec_used from openedbg").fetchall()[0][0]
    thr_equiped = cur.execute("select thr_used from openedbg").fetchall()[0][0]
    if sec_equiped:
        bg_start = pygame.transform.scale(load_image("bg4.png"), (800, 600))
        sec_equiped = True
        fir_equiped = False
        thr_equiped = False
        shop_screen.blit(bg_start, (0, 0))
        menu_screen.blit(bg_start, (0, 0))
        record_screen.blit(bg_start, (0, 0))
        levels_screen.blit(bg_start, (0, 0))
    if thr_equiped:
        bg_start = pygame.transform.scale(load_image("bg3.jpg"), (800, 600))
        thr_equiped = True
        fir_equiped = False
        sec_equiped = False
        shop_screen.blit(bg_start, (0, 0))
        menu_screen.blit(bg_start, (0, 0))
        record_screen.blit(bg_start, (0, 0))
        levels_screen.blit(bg_start, (0, 0))
    if fir_equiped:
        sec_equiped = False
        fir_equiped = True
        thr_equiped = False
        bg_start = pygame.transform.scale(load_image("bg2.png"), (800, 600))
        shop_screen.blit(bg_start, (0, 0))
        menu_screen.blit(bg_start, (0, 0))
        record_screen.blit(bg_start, (0, 0))
        levels_screen.blit(bg_start, (0, 0))        
    
    
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_button.collidepoint(event.pos) and menu_now:
                        start_menu_sound.play()
                        current_screen = levels_screen
                        menu_now = False
                    if record_button.collidepoint(event.pos) and menu_now:
                        start_menu_sound.play()
                        current_screen = record_screen
                        menu_now = False
                    if record_button_quit.collidepoint(event.pos) and recorded_now:
                        start_menu_sound.play()
                        current_screen = menu_screen
                        recorded_now = False
                        
                    if quit_button.collidepoint(event.pos) and menu_now:
                        running = False
                    if first_button.collidepoint(event.pos) and levels_screen_now:
                        easy_sound.play()
                        pygame.mixer.music.load("data/battle.ogg")
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)
                        current_screen = level_screen
                        levels_screen_now = False
                        level = 1
                        dmg = 10
                        v = 7
                        spawnrate = 200
                        v2 = 2
                        enemy_dmg = 2
                        total_hp = 20
                        enemy_hp = 60
                        maxhp = 20
                        bonus_hp = 7
                        bonus_dmg = 2
                        amount_enemy = 5
                        createrate = 120
                        bonus_hp_create = 10
                        bonus_dmg_create = 4
                    if second_button.collidepoint(event.pos) and levels_screen_now:
                        normal_sound.play()
                        pygame.mixer.music.load("data/battle.ogg")
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)                        
                        current_screen = level_screen
                        levels_screen_now = False
                        level = 2
                        dmg = 10
                        v = 7
                        spawnrate = 190
                        v2 = 4
                        enemy_dmg = 3
                        total_hp = 20
                        enemy_hp = 70
                        maxhp = 20
                        bonus_hp = 5
                        bonus_dmg = 1
                        amount_enemy = 15
                        createrate = 150
                        bonus_hp_create = 8
                        bonus_dmg_create = 3
                    if endless_button.collidepoint(event.pos) and levels_screen_now:
                        endless_sound.play()
                        pygame.mixer.music.load("data/battle.ogg")
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)                        
                        started_endless = 1
                        current_screen = level_screen
                        levels_screen_now = False
                        level = 3
                        dmg = 7
                        v = 7
                        spawnrate = 200
                        v2 = 6
                        enemy_dmg = 3
                        total_hp = 17
                        enemy_hp = 70
                        maxhp = 15
                        bonus_hp = 5
                        bonus_dmg = 1
                        amount_enemy = 15
                        createrate = 150
                        bonus_hp_create = 8
                        bonus_dmg_create = 3
                        not_endless = False
                    if paused and continue_button.collidepoint(event.pos):
                        pygame.mixer.music.unpause()   
                        unpause_sound.play()
                        current_screen = level_screen
                        can_move = True
                        paused = False
                    if paused and title_button.collidepoint(event.pos):
                        pygame.mixer.music.load("data/menu_music.wav")
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)                                                
                        current_screen = menu_screen
                        menu_now = True
                        paused = False
                        for i in enemy_sprites:
                            i.destroy()
                        for i in box_sprites:
                            i.destroy()
                        player.destroy()
                        player = Player()
                        all_sprites.add(player) 
                        not_endless = True
                    if paused and exit_button.collidepoint(event.pos):
                        running = False
                    if current_screen == lose_screen and title_lose_button.collidepoint(event.pos):
                        lose_sound.stop()
                        pygame.mixer.music.load("data/menu_music.wav")
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)                        
                        current_screen = menu_screen
                        end_game = False
                        menu_now = True
                        if not not_endless:
                            shop_screen.blit(bg_start, (0, 0))
                            shop_list = pygame.draw.rect(shop_screen, (225, 194, 246), (50, 100, 700, 450))
                            shop_buy_sec = pygame.draw.rect(shop_screen, (225, 94, 229), (130, 440, 190, 50))
                            shop_buy_thr = pygame.draw.rect(shop_screen, (225, 94, 229), (470, 440, 190, 50))  
                            shop_back_button = pygame.draw.rect(shop_screen, (225, 194, 246), (40, 30, 150, 50))                            
                            if no_users:
                                cur.execute('''INSERT INTO record(name, score, itog) VALUES(?, ?, ?)''', (input_box1.get_name(), killed, 0 + killed))
                                no_users = False
                            else:    
                                cur.execute('''INSERT INTO record(name, score, itog) VALUES(?, ?, ?)''', (input_box1.get_name(), killed, int(cur.execute("select itog from record order by id desc limit 1").fetchall()[0][0]) + killed))
                            con.commit()                              
                        for i in enemy_sprites:
                            i.destroy()
                        for i in box_sprites:
                            i.destroy()
                        player.destroy()
                        player = Player()
                        all_sprites.add(player)
                        if level == 3:
                            not_endless = True
                        x = 7 
                        level_screen.blit(hp_cur[x], (player_x - 13, player_y - 30))
                        input_box1.next()
                        
                    if current_screen == lose_screen and retry_lose_button.collidepoint(event.pos):
                        lose_sound.stop()
                        pygame.mixer.music.load("data/battle.ogg")
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)
                        current_screen = level_screen
                        end_game = False
                        can_move = True
                        if not not_endless:
                            shop_screen.blit(bg_start, (0, 0))
                            shop_list = pygame.draw.rect(shop_screen, (225, 194, 246), (50, 100, 700, 450))
                            shop_buy_sec = pygame.draw.rect(shop_screen, (225, 94, 229), (130, 440, 190, 50))
                            shop_buy_thr = pygame.draw.rect(shop_screen, (225, 94, 229), (470, 440, 190, 50))  
                            shop_back_button = pygame.draw.rect(shop_screen, (225, 194, 246), (40, 30, 150, 50))                            
                            if no_users:
                                cur.execute('''INSERT INTO record(name, score, itog) VALUES(?, ?, ?)''', (input_box1.get_name(), killed, 0 + killed))
                                no_users = False
                            else:    
                                cur.execute('''INSERT INTO record(name, score, itog) VALUES(?, ?, ?)''', (input_box1.get_name(), killed, int(cur.execute("select itog from record order by id desc limit 1").fetchall()[0][0]) + killed))
                            con.commit()    
                            
                            no_users = False
                        for i in enemy_sprites:
                            i.destroy()
                        for i in box_sprites:
                            i.destroy()
                        player.destroy()
                        player = Player()
                        all_sprites.add(player)
                        x = 7
                        if not_endless:
                            total_hp = 20
                            maxhp = 20
                            dmg = 10
                            killed = 0
                        else:
                            total_hp = 15
                            maxhp = 15
                            dmg = 7
                            killed = 0
                        input_box1.next()
                        
                        level_screen.blit(hp_cur[x], (player_x - 13, player_y - 30))
                    if current_screen == win_screen and title_win_button.collidepoint(event.pos):
                        pygame.mixer.music.load("data/menu_music.wav")
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)                        
                        current_screen = menu_screen
                        end_game = False
                        menu_now = True
                        for i in enemy_sprites:
                            i.destroy()
                        for i in box_sprites:
                            i.destroy()
                        player.destroy()
                        player = Player()
                        all_sprites.add(player)
                        x = 7                     
                        level_screen.blit(hp_cur[x], (player_x - 13, player_y - 30))
                    if current_screen == win_screen and next_win_button.collidepoint(event.pos):
                        pygame.mixer.music.load("data/battle.ogg")
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)                        
                        current_screen = level_screen
                        end_game = False
                        can_move = True
                        for i in enemy_sprites:
                            i.destroy()
                        for i in box_sprites:
                            i.destroy()
                        player.destroy()
                        player = Player()
                        all_sprites.add(player)
                        x = 7
                        killed = 0
                        if level == 1:
                            level = 2
                            total_hp = 20
                            maxhp = 20
                            dmg = 10                            
                            enemy_hp == 70
                            bonus_hp = 5
                            bonus_dmg = 1   
                            spawnrate = 190
                            amount_enemy = 15    
                            createrate = 150
                            bonus_hp_create = 8
                            bonus_dmg_create = 3                            
                            v2 = 5
                        elif level == 2:
                            level = 3
                            dmg = 7
                            v = 10
                            spawnrate = 200
                            v2 = 7
                            enemy_dmg = 3
                            total_hp = 15
                            enemy_hp = 70
                            maxhp = 15
                            bonus_hp = 5
                            bonus_dmg = 1
                            amount_enemy = 15
                            createrate = 150
                            bonus_hp_create = 8
                            bonus_dmg_create = 3
                            not_endless = False                            
                        level_screen.blit(hp_cur[x], (player_x - 13, player_y - 30))
                    if levels_screen_now and levels_back_button.collidepoint(event.pos):
                        start_menu_sound.play()
                        current_screen = menu_screen
                        levels_screen_now = False
                    if shop_button.collidepoint(event.pos) and menu_now:
                        start_menu_sound.play()
                        current_screen = shop_screen
                        menu_now = False
                    if shop_back_button.collidepoint(event.pos) and current_screen == shop_screen:
                        start_menu_sound.play()
                        current_screen = menu_screen
                        menu_now = True
                    if shop_buy_sec.collidepoint(event.pos) and current_screen == shop_screen:
                        if not no_users:
                            if not sec_bought and cur.execute("select itog from record order by id desc limit 1").fetchall()[0][0] > 50:
                                sec_bought = True
                                cur.execute('''UPDATE record SET itog = ? where id = ?''', (cur.execute("select itog from record order by id desc limit 1").fetchall()[0][0] - 50, 
                                                                                            cur.execute("select id from record order by id desc limit 1").fetchall()[0][0]))
                                cur.execute('''UPDATE openedbg SET sec_open = 1''')
                                con.commit()
                                shop_screen.blit(bg_start, (0, 0))
                                shop_list = pygame.draw.rect(shop_screen, (225, 194, 246), (50, 100, 700, 450))
                                shop_buy_sec = pygame.draw.rect(shop_screen, (225, 94, 229), (130, 440, 190, 50))
                                shop_buy_thr = pygame.draw.rect(shop_screen, (225, 94, 229), (470, 440, 190, 50))  
                                shop_back_button = pygame.draw.rect(shop_screen, (225, 194, 246), (40, 30, 150, 50))
                            elif sec_bought and not sec_equiped:
                                cur.execute('''UPDATE openedbg SET sec_used = 1''')
                                cur.execute('''UPDATE openedbg SET fir_used = 0''')
                                cur.execute('''UPDATE openedbg SET thr_used = 0''')
                                con.commit()
                                bg_start = pygame.transform.scale(load_image("bg4.png"), (800, 600))
                                sec_equiped = True
                                fir_equiped = False
                                thr_equiped = False
                                shop_screen.blit(bg_start, (0, 0))
                                menu_screen.blit(bg_start, (0, 0))
                                record_screen.blit(bg_start, (0, 0))
                                levels_screen.blit(bg_start, (0, 0))
                            elif sec_bought and sec_equiped:
                                cur.execute('''UPDATE openedbg SET sec_used = 0''')
                                cur.execute('''UPDATE openedbg SET fir_used = 1''')
                                cur.execute('''UPDATE openedbg SET thr_used = 0''')   
                                con.commit()
                                sec_equiped = False
                                fir_equiped = True
                                thr_equiped = False
                                bg_start = pygame.transform.scale(load_image("bg2.png"), (800, 600))
                                shop_screen.blit(bg_start, (0, 0))
                                menu_screen.blit(bg_start, (0, 0))
                                record_screen.blit(bg_start, (0, 0))
                                levels_screen.blit(bg_start, (0, 0))
                            else:
                                no_purchase.play()
                    if shop_buy_thr.collidepoint(event.pos) and current_screen == shop_screen:
                        if not no_users:
                            if not thr_bought and cur.execute("select itog from record order by id desc limit 1").fetchall()[0][0] > 50:
                                cur.execute('''UPDATE openedbg SET thr_open = 1''')
                                thr_bought = True
                            
                                cur.execute('''UPDATE record SET itog = ? where id = ?''', (cur.execute("select itog from record order by id desc limit 1").fetchall()[0][0] - 50, 
                                                                                        cur.execute("select id from record order by id desc limit 1").fetchall()[0][0]))
                                con.commit()
                                shop_screen.blit(bg_start, (0, 0))
                                shop_list = pygame.draw.rect(shop_screen, (225, 194, 246), (50, 100, 700, 450))
                                shop_buy_sec = pygame.draw.rect(shop_screen, (225, 94, 229), (130, 440, 190, 50))
                                shop_buy_thr = pygame.draw.rect(shop_screen, (225, 94, 229), (470, 440, 190, 50))  
                                shop_back_button = pygame.draw.rect(shop_screen, (225, 194, 246), (40, 30, 150, 50))
                            elif thr_bought and not thr_equiped:
                                cur.execute('''UPDATE openedbg SET sec_used = 0''')
                                cur.execute('''UPDATE openedbg SET fir_used = 0''')
                                cur.execute('''UPDATE openedbg SET thr_used = 1''')
                                con.commit()
                                bg_start = pygame.transform.scale(load_image("bg3.jpg"), (800, 600))
                                thr_equiped = True
                                fir_equiped = False
                                sec_equiped = False
                                shop_screen.blit(bg_start, (0, 0))
                                menu_screen.blit(bg_start, (0, 0))
                                record_screen.blit(bg_start, (0, 0))
                                levels_screen.blit(bg_start, (0, 0))
                            elif thr_bought and thr_equiped:
                                thr_equiped = False
                                fir_equiped = True
                                sec_equiped = False
                                cur.execute('''UPDATE openedbg SET sec_used = 0''')
                                cur.execute('''UPDATE openedbg SET fir_used = 1''')
                                cur.execute('''UPDATE openedbg SET thr_used = 0''') 
                                con.commit()
                                bg_start = pygame.transform.scale(load_image("bg2.png"), (800, 600))
                                shop_screen.blit(bg_start, (0, 0))
                                menu_screen.blit(bg_start, (0, 0))
                                record_screen.blit(bg_start, (0, 0))
                                levels_screen.blit(bg_start, (0, 0))
                            else:
                                no_purchase.play()
            if keys[pygame.K_ESCAPE] and can_move and current_screen == level_screen and f > 5:
                pygame.mixer.music.pause()
                pause_sound.play()
                current_screen = pause_screen
                can_move = False
                paused = True
                f = 1
            if current_screen == pause_screen and f > 5 and keys[pygame.K_ESCAPE]:
                pygame.mixer.music.unpause()
                unpause_sound.play()
                can_move = True
                paused = False
                current_screen = level_screen
                f = 1
            for box in input_boxes:
                box.handle_event(event)
            f += 1
        
            start_button = pygame.draw.rect(menu_screen, (225, 194, 246), (250, 80, 300, 75))
            record_button = pygame.draw.rect(menu_screen, (225, 194, 246), (250, 185, 300, 75))
            shop_button = pygame.draw.rect(menu_screen, (225, 194, 246), (250, 290, 300, 75))
            record_button_quit = pygame.draw.rect(record_screen, (225, 194, 246), (40, 30, 150, 50))
            quit_button = pygame.draw.rect(menu_screen,(225, 194, 246), (250, 395, 300, 75))
            first_button = pygame.draw.rect(levels_screen,(225, 194, 246), (250, 160, 300, 75))
            second_button = pygame.draw.rect(levels_screen,(225, 194, 246), (250, 280, 300, 75))
            endless_button = pygame.draw.rect(levels_screen,(225, 194, 246), (250, 400, 300, 75))
            continue_button = pygame.draw.rect(pause_screen,(82, 82, 82), (130, 450, 160, 45))
            title_button = pygame.draw.rect(pause_screen,(82, 82, 82), (320, 450, 160, 45))
            exit_button = pygame.draw.rect(pause_screen,(82, 82, 82), (510, 450, 160, 45))
            retry_lose_button = pygame.draw.rect(lose_screen,(82, 82, 82), (85, 380, 200, 50))
            title_lose_button = pygame.draw.rect(lose_screen,(82, 82, 82), (85, 455, 200, 50))
            next_win_button = pygame.draw.rect(win_screen,(82, 82, 82), (70, 390, 200, 50))
            title_win_button = pygame.draw.rect(win_screen,(82, 82, 82), (70, 455, 200, 50))
            levels_back_button = pygame.draw.rect(levels_screen,(225, 194, 246), (40, 30, 150, 50))
            shop_back_button = pygame.draw.rect(shop_screen, (225, 194, 246), (40, 30, 150, 50))
            record_list = pygame.draw.rect(record_screen, (225, 194, 246), (215, 45, 200, 525))
            shop_list = pygame.draw.rect(shop_screen, (225, 194, 246), (50, 100, 700, 450))
            shop_buy_sec = pygame.draw.rect(shop_screen, (225, 94, 229), (130, 440, 190, 50))
            shop_buy_thr = pygame.draw.rect(shop_screen, (225, 94, 229), (470, 440, 190, 50))        
        if not not_endless:
            if started_endless % 580 == 0:
                enemy_hp += 5
                enemy_dmg += 1
            started_endless += 1
        if timer % spawnrate == 0 and can_move:
            enemy = Enemy()
            enemy_sprites.add(enemy)    
        if timer % createrate == 0 and can_move:
            box = Box()
            box_sprites.add(box)
        timer += 1
        if current_screen == menu_screen:
            menu_now = True
        elif current_screen == levels_screen:
            levels_screen_now = True
        elif current_screen == record_screen:
            recorded_now = True
        elif current_screen == level_screen:
            can_move = True
        text_surface = my_font.render('Start Game', False, (0, 0, 0))
        text_surface_shop = my_font.render('Shop', False, (0, 0, 0))
        text_surface_trend = my_font.render('Record Board', False, (0, 0, 0))
        text_surface_quit = my_font.render('Quit Game', False, (0, 0, 0))
        text_surface_record_quit = my_font.render('Back', False, (0, 0, 0))
        text_surface_levels_quit = my_font.render('Back', False, (0, 0, 0))
        text_surface_first = my_font.render('Easy', False, (0, 0, 0))
        text_surface_second = my_font.render('Normal', False, (0, 0, 0))
        text_surface_third = my_font.render('ENDLESS MODE', False, (0, 0, 0))
        text_surface_pause = my_font.render('PAUSE', False, (255, 0, 0))
        text_surface_continue = my_font_2.render('Continue', False, (223, 119, 0))
        text_surface_title = my_font_2.render('To Title', False, (0, 204, 0))
        curcat = cur.execute("SELECT score, name FROM record").fetchall()
        record_list = pygame.draw.rect(record_screen, (225, 194, 246), (215, 45, 370, 525))
        for i in range(len(curcat)):
            lst.append([str(curcat[i][0]), str(curcat[i][1])])
        lst = sorted(curcat, reverse = True)[:10]
        for b in range(len(lst)):
            record_screen.blit(my_font_2.render(str(b + 1) + '   ' + str(lst[b][1]) + ' - ' + str(lst[b][0]), False, (0, 0, 0)) , (240, 70 + 50 * b))
        text_surface_record_list_1 = my_font_2.render('1. ', False, (0, 0, 0))
        text_surface_record_list_2 = my_font_2.render('2. ', False, (0, 0, 0))
        text_surface_record_list_3 = my_font_2.render('3. ', False, (0, 0, 0))
        text_surface_record_list_4 = my_font_2.render('4. ', False, (0, 0, 0))
        text_surface_record_list_5 = my_font_2.render('5. ', False, (0, 0, 0))
        text_surface_record_list_6 = my_font_2.render('6. ', False, (0, 0, 0))
        text_surface_record_list_7 = my_font_2.render('7. ', False, (0, 0, 0))
        text_surface_record_list_8 = my_font_2.render('8. ', False, (0, 0, 0))
        text_surface_record_list_9 = my_font_2.render('9. ', False, (0, 0, 0))
        text_surface_record_list_10 = my_font_2.render('10. ', False, (0, 0, 0))
        if no_users:
            text_surface_balance = my_font.render('Bank: ' + '0', False, (0, 0, 0))
        else:
            if not sec_equiped:
                text_surface_balance = my_font.render('Bank: ' + str(cur.execute("select itog from record order by id desc limit 1").fetchall()[0][0]), False, (0, 0, 0))
            else:
                text_surface_balance = my_font.render('Bank: ' + str(cur.execute("select itog from record order by id desc limit 1").fetchall()[0][0]), False, (255, 255, 255))
        text_surface_exit = my_font_2.render('Exit', False, (0, 128, 255))
        text_surface_lose = my_font_4.render('You Lose', False, (255, 0, 0))
        text_surface_win_text = my_font_4.render('You Win', False, (0, 0, 255))
        text_surface_lose_retry = my_font_3.render('Retry Game', False, (0, 0, 0))
        text_surface_win_next = my_font_3.render('Next Level', False, (0, 0, 0))
        text_surface_win_title = my_font_3.render('To Title', False, (0, 0, 0))
        text_surface_lose_title = my_font_3.render('To Title', False, (0, 0, 0))
        text_surface_lose1 = my_font_4.render('Game Over', False, (255, 0, 0))
        text_surface_lose_name = my_font_3.render('Name Yourself:', False, (0, 0, 255))
        text_surface_amount = my_font_3.render("", False, (0, 128, 255))
        if not_endless:
            text_surface_amount = my_font_3.render(str(killed) + '/' + str(amount_enemy), False, (0, 128, 255))
        menu_screen.blit(text_surface, (302,98))
        record_screen.blit(text_surface_record_list_1, (240,70))
        record_screen.blit(text_surface_record_list_2, (240,120))
        record_screen.blit(text_surface_record_list_3, (240,170))
        record_screen.blit(text_surface_record_list_4, (240,220))
        record_screen.blit(text_surface_record_list_5, (240,270))
        record_screen.blit(text_surface_record_list_6, (240,320))
        record_screen.blit(text_surface_record_list_7, (240,370))
        record_screen.blit(text_surface_record_list_8, (240,420))
        record_screen.blit(text_surface_record_list_9, (240,470))
        record_screen.blit(text_surface_record_list_10, (240,520))
        menu_screen.blit(text_surface_shop, (350, 310))
        shop_screen.blit(text_surface_record_quit, (71, 37))
        shop_screen.blit(text_surface_balance, (550, 20))
        lose_screen.blit(text_surface_lose_retry, (85, 390))
        win_screen.blit(text_surface_win_next, (85, 400))
        win_screen.blit(text_surface_win_title, (105, 465))
        lose_screen.blit(text_surface_lose_title, (120, 465))
        lose_screen.blit(text_surface_lose, (65, 80))
        win_screen.blit(text_surface_win_text, (65, 80))
        lose_screen.blit(text_surface_lose1, (30, 180))
        pause_screen.blit(text_surface_pause, (350,150))
        level_screen.blit(text_surface_amount, (100, 100))
        pause_screen.blit(text_surface_continue, (147, 460))
        pause_screen.blit(text_surface_title, (346, 460))
        pause_screen.blit(text_surface_exit, (560, 460))
        menu_screen.blit(text_surface_trend, (283,204))
        menu_screen.blit(text_surface_quit, (312,416))
        levels_screen.blit(text_surface_first, (350,180))
        levels_screen.blit(text_surface_levels_quit, (71, 37))
        levels_screen.blit(text_surface_second, (335,300))
        levels_screen.blit(text_surface_third, (264,420))
        record_screen.blit(text_surface_record_quit, (71, 37))
        text_surface_shop1 = my_font_2.render('Menu Background 1', False, (0, 0, 0))
        text_surface_shop_price = my_font_2.render('50', False, (0, 0, 0))
        text_surface_shop2 = my_font_2.render('Menu Background 2', False, (0, 0, 0))
        if sec_bought and not sec_equiped:
            text_surface_shop3 = my_font_2.render('   Equip', False, (0, 0, 0))
        elif sec_bought and sec_equiped:
            text_surface_shop3 = my_font_2.render('Unequip', False, (0, 0, 0))
        else:
            text_surface_shop3 = my_font_2.render('Purchase', False, (0, 0, 0))
        if thr_bought and not thr_equiped:
            text_surface_shop4 = my_font_2.render('   Equip', False, (0, 0, 0))
        elif thr_bought and thr_equiped:
            text_surface_shop4 = my_font_2.render('Unequip', False, (0, 0, 0))
        else:
            text_surface_shop4 = my_font_2.render('Purchase', False, (0, 0, 0))
        
        shop_screen.blit(text_surface_shop3, (160, 450))
        shop_screen.blit(text_surface_shop4, (500, 450))
        shop_screen.blit(text_surface_shop1, (93, 365))
        shop_screen.blit(text_surface_shop_price, (200, 400))
        shop_screen.blit(text_surface_shop_price, (550, 400))
        shop_screen.blit(text_surface_shop2, (445, 365))
        image_shop1 = pygame.transform.scale(load_image("bg4.png"), (300, 225))
        shop_screen.blit(image_shop1, (75, 130))
        image_shop2 = pygame.transform.scale(load_image("bg3.jpg"), (300, 225))
        shop_screen.blit(image_shop2, (425, 130))        
        if not not_endless:
            lose_screen.blit(text_surface_lose_name, (422, 160))
        if end_game:
            pygame.mixer.music.stop()
            lose_sound.play(-1)
            can_move = False
            current_screen = lose_screen
            
        if killed == amount_enemy and not_endless:
            pygame.mixer.music.stop()
            win_sound.play()
            can_move = False
            current_screen = win_screen
            killed = 0
        for boxs in input_boxes:
            boxs.update()
        
        player_x, player_y = player.give_coords()
        for i in enemy_sprites:
            perem = i.is_damage()
            if perem == False:
                end_game = True
            if perem == 'killed':
                killed += 1
        for i in box_sprites:
            i.is_used()        
        if dmg // 10 > 0:
            level_screen.blit(numbers[dmg // 10], (player_x + 62, player_y - 35))
        level_screen.blit(numbers[dmg % 10], (player_x + 75, player_y - 35))
        level_screen.blit(hp_cur[x], (player_x - 13, player_y - 30))
        level_screen.blit(dmg_img, (player_x + 90, player_y - 47))
        switch_screen(current_screen)
        all_sprites.update()
        enemy_sprites.update()
        
        level_screen.blit(bg_img, (0, 0))
        lose_screen.blit(lose, (0, 0))
        for boxs in input_boxes:
            if not not_endless:
                boxs.draw(lose_screen)
        retry_lose_button = pygame.draw.rect(lose_screen,(82, 82, 82), (85, 380, 200, 50))
        title_lose_button = pygame.draw.rect(lose_screen,(82, 82, 82), (85, 455, 200, 50))
        all_sprites.draw(level_screen)
        enemy_sprites.draw(level_screen)
        box_sprites.draw(level_screen)
        pygame.display.flip()
        clock.tick(fps)
    query = "SELECT name, score FROM record"
    cur.execute(query)
    data = cur.fetchall()
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([i[0] for i in cur.description])
        writer.writerows(data)  
    pygame.quit()

    