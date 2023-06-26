import pygame
import random
import os
import numpy
pygame.init()

win = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption("Plane Game")

velocity = 1
tree_depth = 10
cloud_depth = 20
tree_objs = []
projectile_objs = []
cloud_objs = []
cloud_size = 15

x = 1920/2
y = 1080/2
fire_x = x+62
fire_y = y+26
pressed = False
explosion_scale = 60

run = True

explosion_1 = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'explosion1.png')), (explosion_scale, explosion_scale)) 
explosion_2 = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'explosion2.png')), (explosion_scale, explosion_scale))
missile = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'missile.png')), (30, 30)) 
player = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'player.png')), (140, 140)) 

# Types are Blaster 0, Missile 1, Lighting bolt 2 x+62 & y+26
# Inital blaster bolt will be green and transition to red as upgraded
class Projectile():
    def __init__(self, power, type):
        self.power = power
        self.type = type
        self.x = x+62
        self.y = y+26
    
    def update_projectile(self):
        if self.type == 0: # Blaster
            pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, 5, 15))
            self.y -= velocity+10
        elif self.type == 1: # Missile
            pass 
    
    def get_y_ps(self):
        return self.y


class Tree():
    def __init__(self, x_ps, y_ps):
        self.x_ps = x_ps
        self.y_ps = y_ps
 
    def get_y_ps(self):
        return self.y_ps
    
    def regenerate(self):
        self.y_ps = random.randint(920, 1050)
        self.x_ps = random.randint(100, 1800)
    
    def update_trees(self):
        self.y_ps += velocity
        
    def draw_tree(self):
        pygame.draw.rect(win, (150, 75, 0), (self.x_ps, self.y_ps, 10, 30))
        for i in range(0,3):
            if i < 2:
                pygame.draw.rect(win, (0, 122, 24), (((self.x_ps+i*10)-15), (self.y_ps-i*8), 40/(i+1), 8))
            else:
                pygame.draw.rect(win, (0, 122, 24), (((self.x_ps+i+13)-15), (self.y_ps-i*8), 40/(i+2), 8))


class Clouds:
    def __init__(self, x_ps, y_ps, cloud_size):
        self.x_ps = x_ps
        self.y_ps = y_ps
        self.cloud_props = []
        self.cloud_size = cloud_size
        self.noise_a = 0
        self.noise_b = 0
        
    def setup(self):
        noise = [-1,1]
        self.noise_a = (random.choice(noise)*random.randint(2,8))
        self.noise_b = (random.choice(noise)*random.randint(2,8))
        self.y_ps = random.randint(-1800, -50)
        self.x_ps = random.randint(10, 1850)
        self.cloud_props = numpy.random.choice([0,1],size=(self.cloud_size, self.cloud_size))
    
    def draw_clouds(self):
        
        for i in range(cloud_size):
            for j in range(cloud_size):
                if self.cloud_props[i][j] == 1:
                    noise = [-1, 1]
                    pygame.draw.rect(win, (255, 255, 255), (self.x_ps + j*10 + self.noise_a, self.y_ps+i*10 + self.noise_b, 10, 10))
        self.y_ps += 1
    def get_y(self):
        return self.y_ps
       
        


# Cloud Setup
for clouds in range(cloud_depth):
    cloud_objs.append(Clouds(random.randint(10, 1850), random.randint(-1000, -25), cloud_size))
    cloud_objs[clouds].setup()


for tree in range(tree_depth):
    tree_x = random.randint(100, 1800)
    tree_y = random.randint(920, 1050)
    tree_objs.append(Tree(tree_x, tree_y))


# Main Loop
while run:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and not pressed:
                pressed = True
                             
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and x > 0:
        x -= velocity + 3
    if keys[pygame.K_d] and x < 1800:
        x += velocity + 3
    if keys[pygame.K_w] and y > 0:
        y -= velocity + 3
    if keys[pygame.K_s] and y < 980:
        y += velocity + 3

    
    win.fill((0,196,255))

    # Background drawing
    pygame.draw.rect(win, (0, 255, 111), (0, 900, 1920, 180))

    # Trees
    for trees in tree_objs:
        trees.draw_tree()
        trees.update_trees()
        if trees.get_y_ps() - 30 > 1050:
            trees.regenerate()
    


    if pressed:
        projectile_objs.append(Projectile(10, 0))
        pressed = False
                    


    for projectile in projectile_objs:
        projectile.update_projectile()
        if projectile.get_y_ps() < 0:
            projectile_objs.pop(projectile_objs.index(projectile))
    
    # Ship - Shooting pos is x+62 & y+26
    win.blit(player, (x, y))
    
    for clouds in cloud_objs:
        clouds.draw_clouds()
        if clouds.get_y() > 1100:
            clouds.setup()
    
    pygame.display.flip() 
    
pygame.quit()