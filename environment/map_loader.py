from .walls import Wall
from .mesh_loader import generate
from entities import Player, Enemy
import pygame
import os
import math
import pickle

DENSITY = 25

class MapLoader():
    def __init__(self, current_map):
        self.name = current_map
        self.walls = []
        self.background = pygame.image.load(f'maps/{current_map}/background.png')
        self.size = self.background.get_size()
        self.parse_walls()
        self.nav_mesh = self.generate_nav_mesh()
        self.nav_mesh_walls = self.generate_nav_mesh_walls()
 
    def parse_walls(self):
        with open(f"maps/{self.name}/walls.txt") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                try:
                    x, y, height, width = map(int, line.split(','))
                    self.walls.append(Wall(x, y, height, width))
                except ValueError:
                    print(f"Error parsing line : {line}")
                    continue
  
    def generate_nav_mesh(self):
        path = f"maps/{self.name}/navmesh.pkl"
        #commented for debugging, caches mesh calculation
        # if os.path.exists(path):
        #     with open(path, 'rb') as file:
        #         return pickle.load(file)
            
        # else:
        #     mesh = generate(self.size, self.walls, DENSITY)
        #     with open(path, 'wb') as f:
        #         pickle.dump(mesh, f)
        #     return mesh # density = distance in px between two nodes
        mesh = generate(self.size, self.walls, DENSITY)
        with open(path, 'wb') as f:
            pickle.dump(mesh, f)
        return mesh 
        
    def generate_nav_mesh_walls(self):
        walls = []
        mesh_width, mesh_height = self.nav_mesh.width, self.nav_mesh.height
        density = self.nav_mesh.density
        for i in range(mesh_width):
            for j in range(mesh_height):
                eps = self.nav_mesh.edge_tolerance
                r = pygame.Rect(i * density, j * density, density, density)
                r_inf = pygame.Rect(i * density-eps, j * density-eps, density+2*eps, density+2*eps)
                if r_inf.collidelist(self.walls) != -1:
                    walls.append(Wall(i*density, j*density, density, density))
        return walls

    
    def resolve_collision_x(self, entity, dx):
        if isinstance(entity, Enemy):
            walls = self.walls

        if isinstance(entity, Player):
            walls = self.walls

        for wall in walls:
            if wall.rect.colliderect(entity.rect):
                if dx < 0 and entity.rect.left < wall.rect.right:
                    entity.rect.left = wall.rect.right
                if dx > 0 and entity.rect.right > wall.rect.left:
                    entity.rect.right = wall.rect.left
                    
                entity.x_pos, entity.y_pos = entity.rect.center

    def resolve_collision_y(self, entity, dy):
        if isinstance(entity, Enemy):
            walls = self.walls

        if isinstance(entity, Player):
            walls = self.walls

        for wall in walls:
            if wall.rect.colliderect(entity.rect):
                if dy < 0 and entity.rect.top < wall.rect.bottom:
                    entity.rect.top = wall.rect.bottom
                    
                if dy > 0 and entity.rect.bottom > wall.rect.top:
                    entity.rect.bottom = wall.rect.top

                entity.x_pos, entity.y_pos = entity.rect.center

