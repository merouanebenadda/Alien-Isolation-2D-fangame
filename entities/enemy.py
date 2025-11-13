from .entity import Entity
from .player import Player
from utilities.mesh import Mesh
from utilities import geometry
import pygame
import math

class Enemy(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.ENEMY_SIZE = (32, 32)
        enemy_surface = pygame.image.load('textures/enemy/red_dot.png').convert_alpha()
        self.texture = pygame.transform.scale(enemy_surface, self.ENEMY_SIZE)
        self.rect = self.texture.get_rect()
        self.rect.center = (x, y)
        self.sprint_speed = 2
        self.state = 'RUSH' # 'RUSH', 'FIND'
        self.current_path = None
        self.next_position = None
        self.current_objective = None
        self.last_path_computation_time = 0
        self.path_computation_refresh = 1000 # in ms
        self.is_on_unaccessible_tile = None
        self.rush_threshold = 64


    def rush(self, player:Player, current_map):
        old_x = self.x_pos
        old_y = self.y_pos

        self.current_speed = self.sprint_speed

        if player.x_pos == self.x_pos and player.y_pos == self.y_pos:
            return None

        movement_vector_x = player.x_pos - self.x_pos
        movement_vector_y = player.y_pos - self.y_pos

        norm = math.sqrt(movement_vector_x**2 + movement_vector_y**2)
        
        if norm != 0:
            super().move(movement_vector_x, movement_vector_y, norm, old_x, old_y, current_map)

    def update_path(self, player, current_map):
        self.is_on_unaccessible_tile, path = current_map.nav_mesh.compute_path(self, player)
        if path != None: 
            self.current_path = path
            self.next_position = self.current_path.pop()
            self.current_objective = (player.x_pos, player.y_pos)
        else:
            return None

    def follow_path(self, current_map):
        if not self.current_path and geometry.euclidian_distance((self.x_pos, self.y_pos), self.next_position) < self.ENEMY_SIZE[0]//2:
            self.current_state = 'FINDING'
            return None
        
        if self.is_on_unaccessible_tile:
            while self.current_path and (self.can_see_point(self.current_path[-1], current_map) 
                                        and geometry.euclidian_distance((self.x_pos, self.y_pos), self.current_path[-1]) < current_map.nav_mesh.density*3):
                self.next_position = self.current_path.pop()
        else:
            while self.current_path and ((self.can_see_point(self.current_path[-1], current_map) 
                                          and geometry.euclidian_distance((self.x_pos, self.y_pos), self.current_path[-1]) < current_map.nav_mesh.density*3) 
                                         or (self.can_go_to_point(self.current_path[-1], current_map) 
                                    and geometry.euclidian_distance((self.x_pos, self.y_pos), self.current_path[-1]) < 100)):
                self.next_position = self.current_path.pop()
        
        if self.current_path and geometry.euclidian_distance((self.x_pos, self.y_pos), self.next_position) < self.ENEMY_SIZE[0]//2:
            self.next_position = self.current_path.pop()

        super().go_to(self.next_position, current_map)

    
    def update(self, player, current_map):
        self.current_speed = self.base_speed

        if self.can_see_entity(player, current_map) and geometry.euclidian_distance_entities(self, player) < self.rush_threshold:
            self.state = 'RUSH'
            self.rush(player, current_map)

        elif self.state == 'RUSH':
            self.state = 'FINDING'
            
        elif (self.state == 'FINDING'
              or pygame.time.get_ticks() - self.last_path_computation_time > self.path_computation_refresh):
            self.update_path(player, current_map)
            self.last_path_computation_time = pygame.time.get_ticks()
            self.state = 'FIND'

        elif self.state == 'FIND':
            try:
                self.follow_path(current_map)
            except ValueError:
                self.state = 'FINDING'