import pygame
from pygame import mixer
import os

# Задаємо кольори
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
NEON = (244, 20, 170)

# Налаштування папки ассетів
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(os.path.dirname(__file__), 'pictures')
platform_img = pygame.image.load(os.path.join(img_folder, 'platform.png'))
fon_img = pygame.image.load(os.path.join(img_folder, 'game_fon.jpg'))
block_img = pygame.image.load(os.path.join(img_folder, 'block.png'))
ball_img = pygame.image.load(os.path.join(img_folder, 'ball.png'))

mixer.init()
mixer.music.load("sounds/soundtrack.mp3")
mixer.music.play(-1)

#Класс платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self):        
        pygame.sprite.Sprite.__init__(self)
        self.image = platform_img
        self.rect = self.image.get_rect()
        self.rect.center = (1200 / 2, 800 - 40)    
    
    def update(self):  
        keys = pygame.key.get_pressed()        
        if keys[pygame.K_RIGHT] and self.rect.x < 1200-138:            
            self.rect.x += 15        
        if keys[pygame.K_LEFT] and self.rect.x > 5:            
            self.rect.x -= 15

#Класс шарика
class Ball(pygame.sprite.Sprite):    
    def __init__(self):        
        pygame.sprite.Sprite.__init__(self)        
        self.image = ball_img        
        self.rect = self.image.get_rect()        
        self.rect.center = (1200 / 2, 800 - 80)        
        self.dx = 1        
        self.dy = -1    
    
    #Определение стороны столкновения и изменение направления движения шарика соответственно    
    def detect_collision(self, dx, dy, sq):        
        if dx > 0:            
            delta_x = self.rect.right - sq.rect.left        
        else:            
            delta_x = sq.rect.right - self.rect.left        
        if dy > 0:            
            delta_y = self.rect.bottom - sq.rect.top        
        else:            
            delta_y = sq.rect.bottom - self.rect.top        
        if abs(delta_x - delta_y) < 10:            
            dx, dy = -dx, -dy        
        elif delta_x > delta_y:            
            dy = -dy        
        elif delta_y > delta_x:            
            dx = -dx        
        return dx, dy    
    
    def update(self):    
        #Направление движения        
        self.rect.x += (15/2) * self.dx        
        self.rect.y += (15/2) * self.dy    
        
        #Столкновение с боками игрового поля        
        if self.rect.centerx < 20 or self.rect.centerx > 1200 - 20:            
            self.dx = -self.dx    
        #Столкновение с верхом игрового поля        
        if self.rect.centery < 20:            
            self.dy = -self.dy    
        #Столкновение с платформой        
        if self.rect.colliderect(platform) and self.dy > 0:            
            #self.dy = -self.dy            
            self.dx, self.dy = self.detect_collision(self.dx, self.dy, platform)    
        #Столкновение с блоками        
        hit_index = self.rect.collidelist(blocks)        
        if hit_index != -1:            
            blocks[hit_index].rect.inflate_ip(self.rect.width * 50, self.rect.height * 50)            
            self.dx, self.dy = self.detect_collision(self.dx, self.dy, blocks[hit_index])            
            blocks.pop(hit_index)    
        #Победа/Поражение        
        if self.rect.bottom > 800 + 40:            
            mixer.music.stop()            
            global running            
            running = False        
        elif not len(blocks):            
            mixer.music.stop()            
            running = False

#Класс блоков
class Block(pygame.sprite.Sprite):    
    def __init__(self, x, y):        
        pygame.sprite.Sprite.__init__(self)        
        self.image = block_img        
        self.rect = self.image.get_rect()        
        self.rect.center = (x, y)   

# Створюємо гру та вікно
pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
platform = Platform()
all_sprites.add(platform)
ball = Ball()
all_sprites.add(ball)
blocks = []
for i in range(4):    
    for j in range(15):        
        blocks.append(Block((j*78)+55, (i*60)+35))
all_sprites.add(blocks)

# Цикл гри
running = True
while running:    
    # Тримаємо цикл на правильній швидкості    
    clock.tick(60)   
    # Введення процесу (події)    
    for event in pygame.event.get():        
        # Проверка на закрытие окна        
        if event.type == pygame.QUIT:            
            running = False   

    # Оновлення    
    all_sprites.update()    
    
    # Рендеринг    
    screen.blit(fon_img, (0, 0))    
    all_sprites.draw(screen)    
    
    # Після відображення всього, перевертаємо екран    
    pygame.display.flip()
pygame.quit()
