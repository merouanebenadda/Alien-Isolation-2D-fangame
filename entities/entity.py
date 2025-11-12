import pygame
import math
from utilities.geometry import intersects

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x_pos = x
        self.y_pos = y
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.rect.center = (x, y)
        self.base_speed = 1
        self.sprint_speed = 2
        self.current_speed = self.base_speed

    def go_to(self, position, current_map):
        x, y = position
        old_x = self.x_pos
        old_y = self.y_pos

        self.current_speed = self.base_speed


        if x == self.x_pos and y == self.y_pos:
            return None

        movement_vector_x = x - self.x_pos
        movement_vector_y = y - self.y_pos

        norm = math.sqrt(movement_vector_x**2 + movement_vector_y**2)
        
        if norm != 0:
            self.move(movement_vector_x, movement_vector_y, norm, old_x, old_y, current_map)

    def move(self, movement_vector_x, movement_vector_y, norm, old_x, old_y, current_map):
        self.x_pos += movement_vector_x/norm * self.current_speed
        self.rect.center = (self.x_pos, self.y_pos)
        dx = self.x_pos - old_x
        current_map.resolve_collision_x(self, dx)
        
        self.y_pos += movement_vector_y/norm * self.current_speed
        self.rect.center = (self.x_pos, self.y_pos)
        dy = self.y_pos - old_y
        current_map.resolve_collision_y(self, dy)

    def can_see(self, entity, current_map):
        ray = (self.rect.center, entity.rect.center)

        for wall in current_map.walls:
            A = (wall.rect.left, wall.rect.top)
            B = (wall.rect.right, wall.rect.top)
            C = (wall.rect.right, wall.rect.bottom)
            D = (wall.rect.left, wall.rect.bottom)

            wall_edges = [(A, B), (B, C), (C, D), (D, A)]

            for edge in wall_edges:
                if intersects(ray, edge):
                    return False
                
        return True