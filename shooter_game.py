
from time import sleep
from pygame import *
from random import randint
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Enemy(GameSprite):
    def update(self):
        global lost
        if self.rect.y < 500:
            self.rect.y += self.speed
        else:
            lost += 1
            self.rect.y = 0
            self.rect.x = randint(80, 420)
        
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


class Player(GameSprite):
    def update(self):
        keys_pr = key.get_pressed()
        if keys_pr[K_RIGHT] and self.rect.x < 635:
            self.rect.x += self.speed
        if keys_pr[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx - 10, self.rect.top, 20, 40, 4)
        bullets.add(bullet)

lost = 0
score = 0
window = display.set_mode((700, 500))
display.set_caption('Шутер')
clock = time.Clock()

galaxy = transform.scale(image.load('galaxy.jpg'), (700, 500))
flag = True


sprite1 = Player('rocket.png', 130, 400, 70, 90, 3)
monsters = sprite.Group()
for i in range(1, 5):
    monster = Enemy('ufo.png', randint(80, 420), -40, 90, 50, randint(2,3))
    monsters.add(monster)
font.init()
font = font.SysFont('Arial', 40)
win = font.render('YOU WIN!', True, (255, 255, 255))
lose = font.render('YOU LOSE!', True, (255, 255, 255))
bullets = sprite.Group()

print("Скачивайте игру и делайте файл .exe!")

while flag:
    window.blit(galaxy, (0, 0))
    sprite1.update()
    sprite1.reset()
    bullets.update()
    bullets.draw(window)
    monsters.draw(window)
    monsters.update()
    collides = sprite.groupcollide(monsters, bullets, True, True)
    for c in collides:
        score += 1
        monster = Enemy('ufo.png', randint(80, 420), -40, 90, 50, randint(2,3))
        monsters.add(monster)
    if sprite.spritecollide(sprite1, monsters, False) or lost >= 20:
        window.blit(lose, (300, 250))
        sleep(3)
    if score > 20:
        window.blit(win, (300, 250))
        sleep(3)
    text = font.render("Счет: " + str(score), 1, (255, 255, 255))
    window.blit(text, (10, 20))
    text2 = font.render("Пропущено: " + str(lost), 1, (255, 255, 255))
    window.blit(text2, (10, 50))
    for i in event.get():
        if i.type == QUIT:
            flag = False
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                sprite1.fire()
    display.update()
    clock.tick(60)
