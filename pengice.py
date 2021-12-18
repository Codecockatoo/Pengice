from os import terminal_size, urandom
import pygame, sys
 
clock = pygame.time.Clock()
 
from pygame.locals import *
pygame.init() 
 
pygame.display.set_caption('Pengice')
#sprites
display = pygame.Surface((300,200))
player_image = pygame.image.load('Player.png')
player_image.set_colorkey((255,255,255))
snow_image = pygame.image.load('snow.png')
spikes_image = pygame.image.load('iceicles.png')
spikes_image.set_colorkey((255,255,255))
present_image = pygame.image.load("present.png")
present_image.set_colorkey((255,255,255))
snowball_image = pygame.image.load("snowball.png")
snowball_image.set_colorkey((255,255,255))
jumps = 100


game_map =[['1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
            ['1','1','1','0','0','0','0','0','0','0','1','0','0','0','0','0','0','1','1'],
            ['1','1','1','0','0','0','0','0','0','0','1','0','0','0','0','0','0','0','1'],
            ['1','1','1','2','1','1','1','2','1','2','1','2','2','2','1','1','2','2','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]
 
WINDOW_SIZE = (600,400)
def collision_test(rect, tiles):
     hit_list = [] # incase of overlap
     for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)             
     return hit_list
def move(rect, movement, tiles):
    collision_types = {"top":False, "bottom":False, "right":False, "left":False} #Dictionary k, v
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0: #seems weird as y increases check bottom for collision however y is inverted in pygame
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) 
moving_right = False
moving_left = False
flight = False
air_timer = 0

player_y_momentum = 0 # gravity
# coords weird y is negative coords not for self
player_rect = pygame.Rect(40,50,player_image.get_width(),player_image.get_height())


while True: 
    display.fill((7, 190, 227))
    
    #non loop variables

    #tile size 16 16
    Tile_Size = 16
    #rows and collums
    r = 0
    tile_rects = [] #all non air
    for row in game_map:
        c = 0
        for tile in row:
            if tile == '1':
                display.blit(snow_image,(c*Tile_Size,r*Tile_Size))
            if tile == '2':
                display.blit(spikes_image, (c*Tile_Size,r*Tile_Size))
            if tile != '0':
               tile_rects.append(pygame.Rect(c*Tile_Size,r*Tile_Size,Tile_Size,Tile_Size)) 
            c += 1
        r += 1
    #collisions
    #movement
    player_movement = [0,0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3: # prevents going too fast
        player_y_momentum = 3
    player_rect, collisions = move(player_rect, player_movement ,tile_rects)
    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1

    display.blit(player_image, (player_rect.x, player_rect.y))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                jumps -= 1
                if jumps > 0 and air_timer < 6:
                        player_y_momentum = -4.5 
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
    tiles = pygame.transform.scale(display,WINDOW_SIZE)
    screen.blit(tiles, (0,0))
    pygame.display.update()
    clock.tick(60)