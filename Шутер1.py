from pygame import *
from random import randint
win_width = 700
win_height = 500
window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load('NASO.jpg'),(700,500))
class GameSprite(sprite.Sprite):
    def __init__(self, player_image,player_x,player_y,size_x,size_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x,size_y))#распределяем,загружаем и задаём размеры спрайту
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):#метод выстрела
        bullet = Bullet('bullet.png', self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)
lost = 0
score = 0
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(100,win_width - 100)
            lost += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <  0:
            self.kill()
bullets = sprite.Group()
monsters = sprite.Group()
for i in range(5):
    monster = Enemy('UFO.png',randint(80,win_width - 80), -40, 77,77,randint(1,5))
    monsters.add(monster)
'''
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
'''
rocket = Player('rocket.png',350,400,95,95,10)
font.init()#подключили все шрифты
font1 = font.SysFont('Arial',36)
font2 = font.SysFont('Arial',72)
win = font2.render('YOU WIN!',True,(255,255,255))
lose = font2.render('YOU LOSE!',True,(255,255,255))
game = True
finish = False
while game:
    
    for e in event.get():#проходимся по получиным событиям
        if e.type == QUIT:#проверяем равно ли событие событию QUIT
            game = False#игра завершается
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()
    if not finish:
        window.blit(background,(0,0))#отображаем фон 
        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255,255,255))
        window.blit(text_lose,(10,50))
        text_win = font1.render('Убито: ' + str(score), 1, (255,255,255))
        window.blit(text_win,(15,25))  
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)  
        rocket.update() 
        rocket.reset()

        sprites_list = sprite.groupcollide(monsters,bullets,True,True)#список столкновений мобов и пуль
        sprites_list2 = sprite.spritecollide(rocket,monsters,False)
        for i in sprites_list:
            score += 1
            monster = Enemy('UFO.png',randint(80,win_width - 80), -40, 77,77,randint(1,5))
            monsters.add(monster)
        if score >= 7:#условие выйгрыша
            finish = True
            window.blit(win,(245,225))
        if lost > 7 or len(sprites_list2) == 3:
            finish = True
            window.blit(lose,(245,225))
    display.update()#обновление кадров возникающих на экране
    time.delay(60)
