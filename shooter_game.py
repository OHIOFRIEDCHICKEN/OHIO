from pygame import *
from random import randint
missed = 0
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()



class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_UP] and self.rect.y > self.speed:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN] and self.rect.y:
            self.rect.y += self.speed
        if keys_pressed[K_LEFT] and self.rect.x > self.speed:
             self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 700 - self.speed:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx,self.rect.top,15, 20, - 20)
        bullets.add(bullet)

class Enemy (GameSprite):
    def update(self):
        self.rect.y += self.speed
        global missed
        if self.rect.y > 500:
           missed += 1
           self.rect.y = 0
           self.rect.x = randint(80, 400)
font.init()
font2 = font.SysFont("Calibri", 30)
hero = Player('rocket.png', 5, 500 -80, 50, 70, 10)
window = display.set_mode((700, 500))
display.set_caption("Shooter game")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
monster = sprite.Group()
bullets = sprite.Group()
for i in range(4):
    ufo = Enemy('ufo.png', randint(80,400), -40, 80, 50, randint(1,2))
    monster.add(ufo)

#parameters of the image sprite

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

kick = mixer.Sound('fire.ogg')
kick.play()

#game loop
run = True
finish = False
clock = time.Clock()
FPS = 80

score = 0

health = 3
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e. key == K_SPACE:
                hero.fire()
    if finish != True:
        window.blit(background,(0, 0))
        text_missed = font2.render("Missed:" +str(missed),1, (0, 0, 255 ))
        window.blit(text_missed, (10, 50))
        text_Score = font2.render("Score:" +str(score),1, (0, 0, 255 ))
        window.blit(text_Score, (575, 50))
        hero.reset()
        hero.update()
        monster.update()
        monster.draw(window)
        bullets.update()
        bullets.draw(window)
        
        text_missed = font2.render("health:" +str(health),1, (0, 0, 255 ))
        window.blit(text_missed, (250, 50))

        sprites_list = sprite.spritecollide(hero, monster, True)
        if len (sprites_list) > 0:
            health -= 1

        sprites_list = sprite.groupcollide(monster, bullets, True, True)
        for i in sprites_list:
            ufo = Enemy('ufo.png', randint(80,400), -40, 80, 50, randint(1,2))
            monster.add(ufo)
            score += 1
            
        if missed > 3 or health <= 0:
            finish = True
            font3 = font.Font(None, 100)
            text_lose = font3.render("You lose!",10, (255, 0, 0 ))
            window.blit(text_lose, (150, 150))
        



    display.update ()
    clock.tick(FPS)