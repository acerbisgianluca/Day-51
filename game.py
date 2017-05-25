import pygame
import random
import sys

#screen dimension
WIDTH = 800
HEIGHT = 600
SCREED_D = (WIDTH, HEIGHT)
FPS = 60

#colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)

#time between each shoot
DELTASHOOT = 100

pygame.init()

#music
pygame.mixer.init()
bg_music = pygame.mixer.music.load('music/background.mp3')
bg_music = pygame.mixer.music.play(-1)
bg_music = pygame.mixer.music.set_volume(100)

shoot_music = pygame.mixer.Sound('music/shoot.ogg')
shoot_music.set_volume(100)

#screen
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Day 51")

#clock
clock = pygame.time.Clock()

#font and print
font1 = pygame.font.Font('font/font.ttf', 40)
font2 = pygame.font.Font('font/font.ttf', 20)
def print_text(msg, pos, _font, color = (0,0,0), bgcolor = (255,255,255)):
        text = _font.render(msg, True, color, bgcolor)
        screen.blit(text, pos)

#icon
icon = pygame.image.load('icon.png')
icon = pygame.transform.scale(icon, (32,32))
pygame.display.set_icon(icon)

#sprites image
background = pygame.image.load('background/darkPurple.png').convert()
background = pygame.transform.scale(background, SCREED_D)
background_rect = background.get_rect()

player_img = pygame.image.load('sprites/player.png').convert()
player_img = pygame.transform.scale(player_img, (50,40))
player_img.set_colorkey(BLACK)

mob_img = pygame.image.load('sprites/mob.png').convert()
mob_img.set_colorkey(BLACK)
mob_img1 = pygame.image.load('sprites/mob1.png').convert()
mob_img1.set_colorkey(BLACK)
mob_list = [mob_img, mob_img1]

bullet_img = pygame.image.load('sprites/bullet.png').convert()
bullet_img = pygame.transform.scale(bullet_img, (10,30))
bullet_img.set_colorkey(BLACK)

#save record
def saveRecord():
	file = open('record/save.txt', 'w')
	file.write(str(record))
	file.close()

#load record
def loadRecord():
	file = open('record/save.txt', 'r')
	data = file.read()
	file.close()
	return data

#score & bonus
score = 0
record = int(loadRecord())
newRecord = False
bonus = 1

def bgGen():
	screen.fill(BLACK)
	screen.blit(background, background_rect)

def showIntro():
	print_text("WELCOME TO DAY 51!", (150, 100), font1, WHITE, BLACK)
	print_text("PRESS SPACE TO START!", (250, 300), font2, YELLOW, BLACK)

def showSummary():
	print_text("SUMMARY", (250, 100), font1, WHITE, BLACK)
	print_text("SCORE = {0}".format(score), (250, 250), font1, YELLOW, BLACK)
	if newRecord:
		print_text("NEW RECORD = {0}".format(record), (175, 350), font1, RED, BLACK)
	else:
		print_text("RECORD = {0}".format(record), (200, 350), font1, RED, BLACK)
	print_text("PRESS ESC TO QUIT!", (250, 500), font2, YELLOW, BLACK)

def quit():
	pygame.quit()
	sys.exit()

#class 
class Player(pygame.sprite.Sprite):
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = player_img
                self.rect = self.image.get_rect()
                self.rect.centerx = WIDTH / 2
                self.rect.bottom = HEIGHT - 10
                self.speedx = 0

        def shoot(self):
        	bullet = Bullet(self.rect.centerx, self.rect.top)
	        shoot_music.play()
	        all_sprites.add(bullet)
	        bullets.add(bullet)

        def update(self):
                self.speedx = 0
                keystate = pygame.key.get_pressed()
                if keystate[pygame.K_LEFT]:
                        self.speedx = -8
                if keystate[pygame.K_RIGHT]:
                        self.speedx = 8
                self.rect.x += self.speedx

                if self.rect.right > WIDTH:
                        self.rect.right = WIDTH
                if self.rect.left < 0:
                        self.rect.left = 0

class Mob(pygame.sprite.Sprite):
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.original_image = mob_list[random.randrange(0,2)]
                self.original_image = pygame.transform.scale(self.original_image, (random.randrange(30,60),random.randrange(30,60)))
                self.image = self.original_image.copy()
                self.rect = self.image.get_rect()
                self.rect.x = random.randrange(0, WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedx = random.randrange(-3,3)
                self.speedy = bonus + random.randrange(1,5)
                self.rot = 0
                self.rotspeed = random.randrange(-8,8)
                self.last_update = pygame.time.get_ticks()

        def rotate(self):
                now = pygame.time.get_ticks()
                if now - self.last_update > 50:
                        self.last_update = now
                        self.rot = (self.rot + self.rotspeed) % 360
                        old_center = self.rect.center
                        self.image = pygame.transform.rotate(self.original_image, self.rot)
                        self.rect = self.image.get_rect()
                        self.rect.center = old_center


        def update(self):
                self.rect.x += self.speedx
                self.rect.y += self.speedy
                self.rotate()

                if self.rect.top > HEIGHT+10 or self.rect.left < -25 or self.rect.right > WIDTH+20:
                        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
                        self.rect.y = random.randrange(-100, -40)
                        self.speedy = random.randrange(1,8)

class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                self.image = bullet_img
                self.rect = self.image.get_rect()
                self.rect.bottom = y
                self.rect.centerx = x
                self.speedy = -10
                previous = pygame.time.get_ticks()

        def update(self):
                self.rect.y += self.speedy

                if self.rect.bottom < 0:
                        self.kill()
intro = True
while intro:
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				intro = False
			if event.key == pygame.K_ESCAPE:
				quit()
		elif event.type == pygame.QUIT:
			quit()
	bgGen()
	showIntro()
	pygame.display.flip()

all_sprites = pygame.sprite.Group() #contiene tutti gli sprite e viene aggiornata per la grafica
mobs = pygame.sprite.Group() #contiene solo i mob
bullets = pygame.sprite.Group() #contiene tutti i proiettili
player=Player()

all_sprites.add(player)

for i in range(8):
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

previous = 0
running = True
while running:
        #run at right speed
        clock.tick(FPS)

        #Process events
        for event in pygame.event.get():

                #check window closing
                if event.type == pygame.QUIT:
                        running = False
                #shoot
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                        		now = pygame.time.get_ticks()
                        		print str(now) + "-" + str(previous) 
                        		if now - previous > DELTASHOOT:
                        				previous = pygame.time.get_ticks()
                                			player.shoot()

        #update
        all_sprites.update()

        hits = pygame.sprite.spritecollide(player, mobs, False)
        if hits:
                running = False

        bullet_hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        #ricreo i mob che sono stati distrutti
        for h in bullet_hits:
                m = Mob()
                all_sprites.add(m)
                mobs.add(m)
                score += 10
                if(score % 500 == 0):
                	bonus += 1

        #draw
        bgGen()
        all_sprites.draw(screen) #disegna tutti gli sprite
        if record < score:
        	record = score
        	newRecord = True
        print_text("SCORE = {0}".format(score), (575,10), font2, RED, BLACK)
        print_text("RECORD = {0}".format(record), (575,30), font2, YELLOW, BLACK)
        pygame.display.flip()

#save record
if newRecord:
	saveRecord()

while True:
	for event in pygame.event.get():
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_ESCAPE:
				quit()
		elif event.type == pygame.QUIT:
			quit()
	bgGen()
	showSummary()
	pygame.display.flip()
