import pygame
import random
import os

# 遊戲設定
# 畫面更新率
FPS = 60
clock = pygame.time.Clock()

# 顏色
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

# 長寬
WIDTH = 1000
HEIGHT = 800

# 遊戲初始化 
pygame.init()
pygame.mixer.init()
# 建立遊戲視窗並設定畫面大小
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Smol Ame game(made by konayuki)")

# 載入圖片(必須先讓遊戲初始化)
background_img = pygame.image.load(os.path.join("img", "space.png")).convert()
player_img = pygame.image.load(os.path.join("img", "ame.png")).convert()
bubba_img = pygame.image.load(os.path.join("img", "bubba.png")).convert()
player_mini_img = pygame.transform.scale(bubba_img, (60, 45))
player_mini_img.set_colorkey(BLACK)
ame_game_img = pygame.image.load(os.path.join("img", "ame_game.png")).convert()
ame_game_img.set_colorkey(BLACK)
ame_drive_img = pygame.image.load(os.path.join("img", "ame_drive.gif")).convert()
weapon_img = pygame.image.load(os.path.join("img", "machine-gun.png")).convert()
bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert()
# 石頭圖片集
rock_imgs = []
for i in range(8):
    rock_imgs.append(pygame.image.load(os.path.join("img", f"rock{i}.png")).convert())

# 道具圖片集
power_imgs = {}
power_imgs['medkit'] = (pygame.image.load(os.path.join("img", "medkit.png")).convert())
power_imgs['gunup'] = (pygame.image.load(os.path.join("img", "ammo.png")).convert())

# 水果圖片集
fruit_imgs = {}
fruit_imgs['apple'] = (pygame.image.load(os.path.join("fruit_img", "apple.png")).convert())
fruit_imgs['banana'] = (pygame.image.load(os.path.join("fruit_img", "banana.png")).convert())
fruit_imgs['blueberry'] = (pygame.image.load(os.path.join("fruit_img", "blueberry.png")).convert())
fruit_imgs['grapes'] = (pygame.image.load(os.path.join("fruit_img", "grapes.png")).convert())
fruit_imgs['kiwi'] = (pygame.image.load(os.path.join("fruit_img", "kiwi.png")).convert())
fruit_imgs['orange'] = (pygame.image.load(os.path.join("fruit_img", "orange.png")).convert())
fruit_imgs['passion-fruit'] = (pygame.image.load(os.path.join("fruit_img", "passion-fruit.png")).convert())
fruit_imgs['star-fruit'] = (pygame.image.load(os.path.join("fruit_img", "star-fruit.png")).convert())

# 設定遊戲右上角icon
pygame.display.set_icon(player_mini_img)

# 載入爆炸動畫
expls_anime = {}
expls_anime['large'] = []
expls_anime['small'] = []
expls_anime['player'] = []
for i in range(9):
    expls_imgs = (pygame.image.load(os.path.join("img", f"expl{i}.png")).convert())
    expls_imgs.set_colorkey(BLACK)
    expls_anime['large'].append(pygame.transform.scale(expls_imgs,(70, 70)))
    expls_anime['small'].append(pygame.transform.scale(expls_imgs,(30, 30)))
    player_expls_imgs = (pygame.image.load(os.path.join("img", f"player_expl{i}.png")).convert())
    player_expls_imgs.set_colorkey(BLACK)
    expls_anime['player'].append(pygame.transform.scale(player_expls_imgs,(70, 70)))


# 載入音樂(必須先讓遊戲初始化)
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.mp3"))
getitem_sound = pygame.mixer.Sound(os.path.join("sound", "item.mp3"))
eatfruit_sound = pygame.mixer.Sound(os.path.join("sound", "eatfruit.mp3"))
die_sound = pygame.mixer.Sound(os.path.join("sound", "rumble.mp3"))
expls_sound = [
    pygame.mixer.Sound(os.path.join("sound", "expl0.mp3")),
    pygame.mixer.Sound(os.path.join("sound", "expl1.mp3"))
]
pygame.mixer.music.load(os.path.join("sound", "ame_bgm.mp3"))

# 控制音量大小
pygame.mixer.music.set_volume(0.4)

# 播放背景音樂(-1代表循環播放)
pygame.mixer.music.play(-1)

# 設定文字字型
''' font_name_arial = pygame.font.match_font("arial") '''
font_name = os.path.join("font.ttf")

# 顯示文字
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.bottom = y
    surf.blit(text_surface, text_rect)

# 顯示玩家血量
def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 200
    BAR_HEIGHT = 20
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 4)

# 顯示玩家生命數
def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x - 65 * i
        img_rect.y = y
        surf.blit(img, img_rect)

# 顯示初始畫面
def draw_init():
    screen.blit(background_img, (0, 0))
    screen.blit(ame_drive_img, (30, 100))
    screen.blit(ame_game_img, (800, 100))
    draw_text(screen, 'Smol Ame Game', 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, '上下左右鍵控制Ame移動 躲避隕石並吃下水果可以獲得分數 !', 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, '獲得武器道具後按下空白鍵可以讓Ame發射子彈破壞隕石 並持續10秒', 19, WIDTH/2, HEIGHT/1.85)
    draw_text(screen, '醫療包可以回復20點血量   彈藥包可以強化子彈威力 並持續4秒', 19, WIDTH/2, HEIGHT/1.75)
    draw_text(screen, '~ press any key to start game ~', 40, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    waitting = True
    while waitting:
        # 設定畫面更新率
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            # 關閉視窗
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            # 按下任意鍵開始遊戲
            elif event.type == pygame.KEYUP:
                waitting = False
                return False


# 讓碰撞後消失的石頭新增回來，以保持相同的石頭數量
def new_rock():
    rock = Rock()
    all_sprites.add(rock)
    rocks.add(rock)

# 讓碰撞後消失的水果新增回來，以保持相同的水果數量
def new_fruit():
    fruit = Fruit()
    all_sprites.add(fruit)
    fruits.add(fruit)

# 設定物件精靈
# 設定玩家
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # 設定物件大小顏色(可用圖片取代)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        '''
        self.image = pygame.Surface((50,40))
        self.image.fill(GREEN)
        '''
        # rect定位這張圖片
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8
        # 設定玩家血量
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.weapon_switch = False
        self.weapon_time = 0
        self.gun_level = 1
        self.gun_leveltime = 0

    def update(self):
        # 判斷武器持續時間(10秒)
        now = pygame.time.get_ticks()
        if now - self.weapon_time > 10000:
            self.weapon_switch = False
            self.weapon_time = now
    
        # 判斷射擊強化時間(4秒)
        now = pygame.time.get_ticks()
        if (self.gun_level > 1) and (now - self.gun_leveltime > 4000):
            self.gun_level -= 1
            self.gun_leveltime = now

        # 判斷飛船是否隱藏，如果是的話讓飛船出現
        if self.hidden and pygame.time.get_ticks() - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT - 10

        # 判斷鍵盤上是否有按鍵被按，回傳其布林值
        key_pressed = pygame.key.get_pressed()

        # 鍵盤操縱物件上下左右移動
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speedx
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speedx
        
        
        # 讓玩家不要超出視窗範圍
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        # 判斷物件超過畫面後從另一邊出現(以下註解不會用到)
        ''' 
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.right = 500 
        '''
    # 射擊函式
    def shoot(self):
        if not(self.hidden):
            if self.weapon_switch:
                if self.gun_level == 1:
                    bullet = Bullet(self.rect.centerx, self.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    shoot_sound.play()
                elif self.gun_level >= 2:
                    bullet1 = Bullet(self.rect.left + 20, self.rect.centery)
                    bullet2 = Bullet(self.rect.right - 20, self.rect.centery)
                    all_sprites.add(bullet1)
                    all_sprites.add(bullet2)
                    bullets.add(bullet1)
                    bullets.add(bullet2)
                    shoot_sound.play()

    # 飛船隱藏函式 
    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+500)

    # 獲得武器函式
    def weapon(self):
        self.weapon_switch = True
        self.weapon_time = pygame.time.get_ticks()

    # 射擊強化函式
    def gunup(self):
        self.gun_level += 1
        self.gun_leveltime = pygame.time.get_ticks()

# 設定石頭
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs)
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        # 隨機生成位置
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        # 掉落速度隨機
        self.speedx = random.randrange(-4, 4)
        self.speedy = random.randrange(3, 10)
        # 石頭隨機選轉
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)

    # 讓圖片旋轉
    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        # 讓旋轉的圖片重新定位
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # 假如石頭超出左右視窗和下面的範圍就重新生成石頭
        if (self.rect.top > HEIGHT) or (self.rect.left > WIDTH) or (self.rect.right < 0):
            # 隨機生成位置
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            # 掉落速度隨機
            self.speedx = random.randrange(-4, 4)
            self.speedy = random.randrange(3, 10)

# 設定子彈
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img 
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # 子彈生成在飛船(玩家)位置
        self.rect.centerx = x
        self.rect.bottom = y
        # 子彈速度
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill() # sprite內建函數 可以刪除物件

# 設定水果
class Fruit(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['apple', 'banana', 'blueberry', 'grapes', 'kiwi', 'orange', 'passion-fruit', 'star-fruit'])
        self.image = fruit_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # 隨機生成位置
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        # 水果掉落速度
        self.speedy = random.randrange(3, 6)

    def update(self):
        self.rect.y += self.speedy
        # 假如水果超出左右視窗和下面的範圍就重新生成水果
        if (self.rect.top > HEIGHT) or (self.rect.left > WIDTH) or (self.rect.right < 0):
            # 隨機生成位置
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            # 掉落速度隨機
            self.speedy = random.randrange(3, 6)

# 設定武器
class Weapon(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        '''
        self.type = random.choice(['apple', 'banana', 'blueberry', 'grapes', 'kiwi'])
        self.image = fruit_imgs[self.type]
        '''
        self.image = weapon_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # 隨機生成位置
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        # 武器掉落速度
        self.speedy = random.randrange(3, 6)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill() # sprite內建函數 可以刪除物件

# 設定道具
class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['medkit', 'gunup'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        # 道具掉落速度
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill() # sprite內建函數 可以刪除物件

# 設定爆炸
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expls_anime[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expls_anime[self.size]):
                self.kill()
            else:
                self.image = expls_anime[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center



# 遊戲迴圈
show_init = True
running = True
while running:
    # 顯示初始畫面
    if show_init:
        # close來接收初始畫面的回傳值
        close  = draw_init()
        # 當初始畫面選擇直接關閉時，避免程式出錯，直接跳出迴圈不執行以下程式
        if close:
            break
        show_init = False
        # 物件群組
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        fruits = pygame.sprite.Group()
        weapons = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        # 創建物件精靈
        player = Player()
        # 將創建的物件精靈加到all_sprites這個群組裡
        all_sprites.add(player)

        # 創建9顆石頭
        for i in range(9):
            new_rock()

        # 創建8個水果
        for i in range(8):
            new_fruit()

        # 設定分數
        score = 0
    
    # 設定畫面更新率
    clock.tick(FPS)
    # 取得輸入
    for event in pygame.event.get():
        # 關閉視窗
        if event.type == pygame.QUIT:
            running = False
        # 按下空白鍵就觸發射擊(按下空白鍵的方式也可以用上面的方法寫)
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()



    # 更新遊戲
    all_sprites.update()
    # 判斷2個群組的物件(子彈和石頭)是否有碰撞(True代表刪除，前後分別代表不同物件)
    hits = pygame.sprite.groupcollide(rocks, bullets , True , True)
    for i in hits:
        random.choice(expls_sound).play()
        score += i.radius
        expl = Explosion(i.rect.center, 'large')
        all_sprites.add(expl)
        # 破壞石頭後機率性生成道具
        if random.random() > 0.9:
            pow = Power(i.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        new_rock()

    # 判斷飛船(玩家)是否被石頭撞到
    player_hits = pygame.sprite.spritecollide(player, rocks , True , pygame.sprite.collide_circle)
    for i in player_hits:
        expls_sound[1].play()
        new_rock()
        player.health -= i.radius
        expl = Explosion(i.rect.center, 'small')
        all_sprites.add(expl)
        # 玩家死亡
        if player.health <= 0:
            death_expl = Explosion(player.rect.center, 'player')
            all_sprites.add(death_expl)
            die_sound.play()
            player.lives -= 1
            player.health = 100
            player.hide()

    # 判斷飛船(玩家)是否吃到水果
    fruit_hits = pygame.sprite.spritecollide(player, fruits , True, pygame.sprite.collide_circle)
    for i in fruit_hits:
        eatfruit_sound.play()
        if i.type == 'apple':
            score += 10
        if i.type == 'banana':
            score += 30
        if i.type == 'blueberry':
            score += 50
        if i.type == 'grapes':
            score += 70
        if i.type == 'orange':
            score += 20
        if i.type == 'passion-fruit':
            score += 100 
        if i.type == 'star-fruit':
            score += 250
        new_fruit()
        # 吃到水果有低機率生成武器
        if random.random() > 0.9:
            weapon = Weapon()
            all_sprites.add(weapon)
            weapons.add(weapon)
        

    # 判斷飛船(玩家)是否獲得道具
    power_hits = pygame.sprite.spritecollide(player, powers , True, pygame.sprite.collide_circle)
    for i in power_hits:
        if i.type == 'medkit':
            player.health += 20
            if player.health > 100:
                player.health = 100
            getitem_sound.play()
        if i.type == 'gunup':
            player.gunup()
            getitem_sound.play()

    # 判斷飛船(玩家)是否獲得武器
    weapon_hits = pygame.sprite.spritecollide(player, weapons , True, pygame.sprite.collide_circle)
    for i in weapon_hits:
        getitem_sound.play()
        player.weapon()

    # 判斷玩家是否生命歸0(完全死亡)
    if player.lives == 0 and not(death_expl.alive()):
        # 直接關閉遊戲
        '''
        running = False 
        '''
        # 遊戲結束後回到初始畫面
        show_init = True


    # 畫面顯示
    screen.fill(BLACK)
    screen.blit(background_img, (0, 0))
    # 將物件畫在螢幕上
    all_sprites.draw(screen)
    # 將文字顯示在螢幕上
    draw_text(screen, str(score), 25, WIDTH/2, 50)
    # 將血量條和生命值顯示在螢幕上
    draw_health(screen, player.health, 20, 20)
    draw_lives(screen, player.lives, player_mini_img, WIDTH - 80, 15)
    pygame.display.update()

pygame.quit()
