import sys, pygame
from entities import Player, Enemy
from environment import MapLoader
from utilities import debug

pygame.init()
screen = pygame.display.set_mode((1085, 716))
pygame.display.set_caption("Stalker")
clock = pygame.time.Clock()
running = True

current_map_name = "map0"
current_map = MapLoader(current_map_name)

player = Player(500, 300)

enemy = Enemy(900, 200)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        

    is_pressed = pygame.key.get_pressed()
    player.move(is_pressed, current_map)
    enemy.update(player, current_map)

    screen.blit(current_map.background, (0, 0))
    debug.draw_mesh(screen, current_map, enemy)

    screen.blit(player.texture, player.rect.topleft)
    screen.blit(enemy.texture, enemy.rect.topleft)

    
    
    pygame.display.flip()

    clock.tick(60)