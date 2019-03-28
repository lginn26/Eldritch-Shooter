# Imports
import pygame
import random
import math
from eldritch_fleets import fleets

# Initialize game engine
pygame.init()


# Window
WIDTH = 1870
HEIGHT = 1000 
SIZE = (WIDTH, HEIGHT)
TITLE = "Eldritch Shooter"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60
display_clock = 0 

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)


# Fonts
FONT_SM = pygame.font.Font("assets/fonts/Singo.ttf", 24)
FONT_MD = pygame.font.Font("assets/fonts/Singo.ttf", 32)
FONT_LG = pygame.font.Font("assets/fonts/Singo.ttf", 64)
FONT_XL = pygame.font.Font("assets/fonts/Singo.ttf", 96)

WEAPON_TXT = pygame.font.Font("assets/fonts/Bigspace.ttf", 96)
FLEET_TXT = pygame.font.Font("assets/fonts/Bigspace.ttf", 32)
# Images
ship_img = pygame.image.load('assets/images/player.png').convert_alpha()
ship_img2 = pygame.image.load('assets/images/player_damaged.png').convert_alpha()
ship_img3 = pygame.image.load('assets/images/player_death_door.png').convert_alpha() 
ship_img4 = pygame.image.load('assets/images/player_destroyed.png').convert_alpha()

bullet_img = pygame.image.load('assets/images/bullet_img.png').convert_alpha()
bounce_bullet_img = pygame.image.load('assets/images/bouncing_bullet_img.png').convert_alpha()
shield_img = pygame.image.load('assets/images/shield.png').convert_alpha()
bomb_img = pygame.image.load('assets/images/enemy_proj.png').convert_alpha()
bomb_s_img = pygame.image.load('assets/images/sniper_proj.png').convert_alpha()
bomb_cb_img = pygame.image.load('assets/images/chaos_proj.png').convert_alpha()

enemy_img = pygame.image.load('assets/images/eldritch_basic.png').convert_alpha()

enemy_ts_img = pygame.image.load('assets/images/eldritch_triplespitter.png').convert_alpha()
enemy_ts_d_img = pygame.image.load('assets/images/eldritch_triplespitter_d.png').convert_alpha()
enemy_ts_dd_img = pygame.image.load('assets/images/eldritch_triplespitter_dd.png').convert_alpha()

enemy_s_img = pygame.image.load('assets/images/eldritch_sniper.png').convert_alpha()
enemy_s_d_img = pygame.image.load('assets/images/eldritch_sniper_d.png').convert_alpha()
enemy_s_dd_img = pygame.image.load('assets/images/eldritch_sniper_dd.png').convert_alpha()

enemy_cb_img = pygame.image.load('assets/images/chaos_breaker.png').convert_alpha()
enemy_cb_d_img = pygame.image.load('assets/images/chaos_breaker_d.png').convert_alpha()
enemy_cb_dd_img = pygame.image.load('assets/images/chaos_breaker_dd.png').convert_alpha()

background_img = pygame.image.load('assets/images/background/background.png').convert()

powerup_sg_img = pygame.image.load('assets/images/shotgun_powerup.png').convert_alpha()
powerup_pu_img = pygame.image.load('assets/images/puncher_powerup.png').convert_alpha()
powerup_hx_img = pygame.image.load('assets/images/helix_powerup.png').convert_alpha()
powerup_bn_img = pygame.image.load('assets/images/bouncer_powerup.png').convert_alpha()
powerup_b_img = pygame.image.load('assets/images/powerup.png').convert_alpha()
shield_up_img = pygame.image.load('assets/images/shield_up.png').convert_alpha()
                                   
# Sounds
EXPLOSION = pygame.mixer.Sound('assets/sounds/explosion.ogg')
shoot = pygame.mixer.Sound('assets/sounds/player_shoot.ogg')
b_shoot = pygame.mixer.Sound('assets/sounds/basic_fire.ogg')
ts_shoot = pygame.mixer.Sound('assets/sounds/triple_fire.ogg')
cb_shoot = pygame.mixer.Sound('assets/sounds/chaos_fire.ogg')
s_shoot = pygame.mixer.Sound('assets/sounds/sniper_fire.ogg')
powerup_sound = pygame.mixer.Sound('assets/sounds/powerup.ogg')
shieldup_sound = pygame.mixer.Sound('assets/sounds/shieldup.ogg')

# Music
track1 = pygame.mixer.music.load('assets/sounds/music_track1.ogg')

# Stages
START = 0
PLAYING = 1
DEAD = 3
END = 2

fleet_no = 1 
# Power Ups
class Shield_Up(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1

    def apply(self):
        ship.shield += 1
        shieldup_sound.play()

    def update(self):
        self.rect.y += self.speed
        self.speed += .02
        
        if self.rect.y > HEIGHT:
            self.kill()

class Power_Up(pygame.sprite.Sprite):
    def __init__(self, x, y, buff, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1

        self.buff = buff

    def apply(self):
        global display_clock
        ship.weapon = self.buff
        display_clock += 100
        powerup_sound.play()

    def update(self):
        self.rect.y += self.speed
        self.speed += .02
        
        if self.rect.y > HEIGHT:
            self.kill()
        

# Bullet Types

class Bounce_bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx, speed, move_left, move_up, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.speedx = speedx

        self.move_left = move_left
        self.move_up = move_up 
        
        self.bounces = 4

    def update(self):

        if self.move_left:
            self.rect.x -= self.speedx
        else:
            self.rect.x += self.speedx

        if self.move_up:
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

        if self.rect.right >= WIDTH and self.bounces >= 0:
            self.move_left = True
            self.bounces -= 1
        elif self.rect.left <= 0 and self.bounces >= 0:
            self.move_left = False
            self.bounces -= 1
            
        if self.rect.bottom <= 0 and self.bounces >= 0:
            self.move_up = False
            self.bounces -= 1
        elif self.rect.top >= HEIGHT and self.bounces >= 0:
            self.move_up = True
            self.bounces -= 1

        if self.bounces <= 0:
            self.kill() 
        

class Helix_bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        self.direction = direction

    def update(self):
        self.rect.y -= self.speed
        if self.direction == 1:
            self.rect.x = 50 * math.sin((self.rect.y - 3)/40) + (self.rect.x)
        else:
            self.rect.x = -50 * math.sin((self.rect.y - 3)/40) + (self.rect.x)
        
        if self.rect.y < -50:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, speedx, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.speedx = speedx

    def update(self):
        self.rect.y -= self.speed
        self.rect.x += self.speedx
        
        self.speed += .5

        if self.rect.y < -50:
            self.kill()

# Bomb Types

class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx, speedy, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speedx
        self.side_speed = speedy

    def update(self):
        self.rect.y += self.speed
        self.rect.x += self.side_speed
        
        if self.rect.y > HEIGHT:
            self.kill()

# Mob Types

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def drop_bomb(self):
        b_shoot.play()
        bomb = Bomb(self.rect.x, self.rect.y, 5, 0, bomb_img)
        
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)
        

    def update(self):
        hit_list = pygame.sprite.spritecollide(self, bullets, True, pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            self.kill()

class Mob_Triple_Shot(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 3

    def drop_bomb(self):
        ts_shoot.play()

        bomb_list = [Bomb(self.rect.x, self.rect.y, 5, 0, bomb_img),
                     Bomb(self.rect.x, self.rect.y, 5, -5, bomb_img),
                     Bomb(self.rect.x, self.rect.y, 5, 5, bomb_img)]

        for b in bomb_list:
            b.rect.centerx = self.rect.centerx
            b.rect.centery = self.rect.bottom
            bombs.add(b)
            

    def update(self):
        hit_list = pygame.sprite.spritecollide(self, bullets, True, pygame.sprite.collide_mask)

        if self.health == 2:
            self.image = enemy_ts_d_img
        elif self.health == 1:
            self.image = enemy_ts_dd_img

        if len(hit_list) > 0:
            self.health -= 1

        if self.health <= 0:
            self.kill()

class Mob_Sniper(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 3

    def drop_bomb(self):
        s_shoot.play()

        x_velocity = (ship.rect.x - self.rect.x) // 100
        y_velocity = (ship.rect.y - self.rect.y) // 100

        print(str(x_velocity) + " " + str(y_velocity))
        
        bomb = Bomb(self.rect.x, self.rect.y, y_velocity, x_velocity, bomb_s_img)
        
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)
        

    def update(self):
        hit_list = pygame.sprite.spritecollide(self, bullets, True, pygame.sprite.collide_mask)

        if self.health == 2:
            self.image = enemy_s_d_img
        elif self.health == 1:
            self.image = enemy_s_dd_img

        if len(hit_list) > 0:
            self.health -= 1

        if self.health <= 0:
            self.kill()


class Mob_Chaos_Breaker(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 5

    def drop_bomb(self):
        cb_shoot.play()
        for b in range(4):
            bombs.add(Bomb(self.rect.x, self.rect.y, random.randint(5,10), random.randint(-5,5), bomb_cb_img))
            

    def update(self):
        hit_list = pygame.sprite.spritecollide(self, bullets, True, pygame.sprite.collide_mask)

        if self.health <= 1:
            self.image = enemy_cb_dd_img
        elif self.health <= 3:
            self.image = enemy_cb_d_img

        if len(hit_list) > 0:
            self.health -= 1

        if self.health <= 0:
            self.kill()


# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.rect.x = x
        self.rect.y = y
        self.shield = 3
        
        self.speed = 5
        self.bullet_limit = 1

        self.weapon = "b"
        
    def move_left(self):
        self.rect.x -= self.speed
    
    def move_right(self):
        self.rect.x += self.speed

    def move_up(self):
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed

    def procces_powerups(self):
        hit_list = pygame.sprite.spritecollide(self, powerups, True, pygame.sprite.collide_mask)
        for hit in hit_list:
            hit.apply()
        
        
    def shoot(self):
        if len(bullets) < self.bullet_limit:
            shoot.play()
            if self.weapon == "b":
                bullet = Bullet(self.rect.x, self.rect.y, 1, 0, bullet_img)
                
                bullet.rect.centerx = self.rect.centerx
                bullet.rect.centery = self.rect.top
                bullets.add(bullet)
            elif self.weapon == "sg":
                for _ in range(4):
                    bullet = Bullet(self.rect.x, self.rect.y, random.randint(-5, 5), random.randint(-5, 5), bullet_img)

                    bullet.rect.centerx = self.rect.centerx
                    bullet.rect.centery = self.rect.top
                    bullets.add(bullet)
            elif self.weapon == "pu":
                bullet1 = Bullet(self.rect.x+15, self.rect.y, 1, 0, bullet_img)
                bullet2 = Bullet(self.rect.x+5, self.rect.y+10, 1, 0, bullet_img)
                bullet3 = Bullet(self.rect.x+35, self.rect.y+10, 1, 0, bullet_img)

                bulletlist = [bullet1, bullet2, bullet3]
                for b in bulletlist:
                    bullets.add(b)
            elif self.weapon == "h":
                bullet = Helix_bullet(self.rect.x, self.rect.y, 1, bullet_img)
                bullet2 = Helix_bullet(self.rect.x, self.rect.y, 0, bullet_img)

                bullet.rect.centerx = self.rect.centerx
                bullet.rect.centery = self.rect.top

                bullet2.rect.centerx = self.rect.centerx
                bullet2.rect.centery = self.rect.top
                
                bullets.add(bullet, bullet2)
            elif self.weapon == "bo":
                for b in [[10, 10, True, True], [10, 10, False, True], [3, 10, True, True], [3, 10, False, True], [0, 10, False, True]]:
                    bullet = Bounce_bullet(self.rect.x, self.rect.y, b[0], b[1], b[2], b[3], bounce_bullet_img)
                    bullet.rect.centerx = self.rect.centerx
                    bullet.rect.centery = self.rect.top
                    bullets.add(bullet)

                    
                

    def update(self):
        # Keep ship within bounds
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
        elif self.rect.y < HEIGHT-200:
            self.rect.y = HEIGHT-200
        elif self.rect.y > HEIGHT-75:
            self.rect.y = HEIGHT-75

        # Detect hits and subtract shield
        hit_list = pygame.sprite.spritecollide(self, bombs, True, pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            self.shield -= 1

        if self.shield >= 3:
            self.image = ship_img
        elif self.shield == 2:
            self.image = ship_img2
        elif self.shield == 1:
            self.image = ship_img3
        else:
            self.image = ship_img4

        if self.shield <= 0:
            stage = DEAD
            self.image = ship_img4

class Fleet():
    def __init__(self, mobs):
        self.mobs = mobs
        self.speed = 5
        self.moving_right = True
        self.drop_speed = 10
        self.bomb_rate = 60

    def move(self):
        hits_edge = False
        
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed

                if m.rect.x >= WIDTH-175:
                    hits_edge = True

            else:
                m.rect.x -= self.speed

                if m.rect.left <= 100:
                    hits_edge = True

        if hits_edge:
            self.reverse()
            self.move_down()

    def reverse(self):
        self.moving_right = not self.moving_right

    def move_down(self):
        for m in mobs:
            m.rect.y += self.drop_speed

    def choose_bomber(self):
        rand = random.randrange(self.bomb_rate)
        mob_list = mobs.sprites()

        if len(mob_list) > 0 and rand == 0:
            bomber = random.choice(mob_list)
            bomber.drop_bomb()
            
    def update(self):
        self.move()
        self.choose_bomber()

        for mob in self.mobs:
            if mob.rect.bottom > HEIGHT-195:
                ship.shield = 0
                

    def __len__(self):
        return len(mobs)
    
# Game helper functions

def draw_grid(scale, color, width=SIZE[0], height=SIZE[1]):
    '''
    Draws a grid that can overlay your picture.
    This should make it easier to figure out coordinates
    when drawing pictures.
    '''
    for x in range(0, width, scale):
        pygame.draw.line(screen, color, [x, 0], [x, height], 1)
    for y in range(0, height, scale):
        pygame.draw.line(screen, color, [0, y], [width, y], 1)

def prep_fleet(prefleet, mobs):
    for mob in prefleet:
        if mob[0] == "b":
            mobs.add(Mob(mob[1], mob[2], enemy_img))
        elif mob[0] == "ts":
            mobs.add(Mob_Triple_Shot(mob[1], mob[2], enemy_ts_img))
        elif mob[0] == "s":
            mobs.add(Mob_Sniper(mob[1], mob[2], enemy_s_img))
        elif mob[0] == "cb":
            mobs.add(Mob_Chaos_Breaker(mob[1], mob[2], enemy_cb_img))
        
        

def spawn_powerup():
    chance = random.randint(1, 1000)
    if chance == 500:
        powerup_choice = random.choice([["b", powerup_b_img], ["sg", powerup_sg_img], ["pu", powerup_pu_img],
                                        ["h", powerup_hx_img], ["bo", powerup_bn_img], ["shield", shield_up_img]])
                                       
        if powerup_choice[0] == "shield":
            powerup = Shield_Up(random.randint(0, WIDTH), 0, powerup_choice[1])
        else:
            powerup = Power_Up(random.randint(0, WIDTH), 0, powerup_choice[0], powerup_choice[1])
            

        powerups.add(powerup)

def show_sheild_bar(shield):
    for s, loc in zip(range(shield), [0, 100, 200, 300, 400, 500]):
        screen.blit(shield_img, [loc, 0])

def draw_background():
    screen.blit(background_img, [0, 0])

def show_weapon_txt(weapon):
    if weapon == "b":
        text = WEAPON_TXT.render("!9mm Cannon!", 1, RED)
    elif weapon == "sg":
        text = WEAPON_TXT.render("!Shotgun!", 1, RED)
    elif weapon == "pu":
        text = WEAPON_TXT.render("!Puncher!", 1, RED)
    elif weapon == "h":
        text = WEAPON_TXT.render("!Helix Cannon!", 1, RED)
    elif weapon == "bo":
        text = WEAPON_TXT.render("!Rubber Gun!", 1, RED)

    w = text.get_width()

    screen.blit(text, [(SIZE[0]/2 - w/2), 400])

def display_fleet_no(fleet_no):
    fleet_txt = FLEET_TXT.render("Level: " + str(fleet_no), 1, RED)
    w = fleet_txt.get_width()

    screen.blit(fleet_txt, [WIDTH - w-150, 20])
    
def show_title_screen():
    title_text = FONT_XL.render("!Eldritch Shooter!", 1, RED)
    w = title_text.get_width()

    lower_text = FONT_LG.render("!Press SPACE to start!", 1, RED)
    w2 = lower_text.get_width()

    screen.blit(title_text, [(SIZE[0]/2 - w/2), 400])
    screen.blit(lower_text, [(SIZE[0]/2 - w2/2), 490])

def show_end_screen():
    ending_text = FONT_XL.render("!Nightmares Eradicated!", 1, RED)
    lower_text = FONT_LG.render("!Press R to restart!", 1, RED)

    w = ending_text.get_width()
    w2 = lower_text.get_width()
    
    screen.blit(ending_text, [(SIZE[0]/2 - w/2), 400])
    screen.blit(lower_text, [(SIZE[0]/2 - w2/2), 490])

def show_dead_screen():
    ending_text = FONT_XL.render("!You have Perished!", 1, RED)
    lower_text = FONT_LG.render("!Press R to restart!", 1, RED)

    w = ending_text.get_width()
    w2 = lower_text.get_width()
    
    screen.blit(ending_text, [(SIZE[0]/2 - w/2), 400])
    screen.blit(lower_text, [(SIZE[0]/2 - w2/2), 490])

def draw_mov_limit():
    pygame.draw.line(screen, RED, [65 ,HEIGHT-205], [WIDTH-65, HEIGHT-205], 5)

    
def setup():
    global stage, done, player, ship, bullets, mobs, fleet, bombs, powerups
    global fleet_no
    ''' Begin at First Level '''
    fleet_no = 1
    ''' Make game objects '''
    ship = Ship(935, 900, ship_img)

    ''' Make sprite groups '''
    player = pygame.sprite.GroupSingle()
    player.add(ship)
       
    bullets = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    mobs = pygame.sprite.Group()
    prep_fleet(fleets[fleet_no-1], mobs)

    fleet = Fleet(mobs)
    
    ''' set stage '''
    stage = START
    done = False
    
# Game loop
setup()
pygame.mixer.music.play(10)
while not done:
    # Input handling (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    ship.shoot()
            elif stage == END or stage == DEAD:  
                if event.key == pygame.K_r:
                    setup()
                    pygame.mixer.music.rewind()

    
    # Game logic (Check for collisions, update points, etc.)
    
    pressed = pygame.key.get_pressed()

    # Detect Game End
    
    if fleet_no == len(fleets):
        stage = END
        
    # Player Movment
    
    if stage == PLAYING:
        
        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()
           
        if pressed[pygame.K_UP]:
            ship.move_up() 
        elif pressed[pygame.K_DOWN]:
            ship.move_down()
            
    # Core Game Functions
    
        if stage == PLAYING and ship.shield > 0:
            ship.update()
            bullets.update()
            bombs.update()
            fleet.update()
            mobs.update()
            spawn_powerup()
            powerups.update()
            ship.procces_powerups()
            
            if ship.shield <= 0:
                stage = DEAD
                
    # fleet handling
    if len(fleet) <= 0 and fleet_no < len(fleets)+1:
        fleet_no += 1
        prep_fleet(fleets[fleet_no-1], mobs)
        
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    draw_background()
    
    #screen.fill(BLACK)
    #draw_grid(50, WHITE)
    #draw_grid(200, GREEN)
    
    bullets.draw(screen)
    player.draw(screen)
    mobs.draw(screen)
    bombs.draw(screen)
    powerups.draw(screen)
    show_sheild_bar(ship.shield)
    display_fleet_no(fleet_no)
    draw_mov_limit()

    if display_clock > 0:
        show_weapon_txt(ship.weapon)
        display_clock -= 1
    
    if stage == START:
        show_title_screen()
    if stage == END:
        show_end_screen()
    if stage == DEAD:
        show_dead_screen()
        
        

        
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
