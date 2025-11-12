import pygame
from math import sqrt
from utilities.mesh import Mesh

EDGE_TOLERANCE = 10 # reduces tolerance to approaching walls

def rect(i, j, density):
    i = max(0, i*density - EDGE_TOLERANCE)
    j = max(0, j*density - EDGE_TOLERANCE)
    return pygame.Rect(i, j, density + 2*EDGE_TOLERANCE, density+ 2*EDGE_TOLERANCE)


def generate(size, walls, density):
    map_width, map_height = size

    mesh_width = map_width//density
    mesh_height = map_height//density

    mesh_size = mesh_width*mesh_height

    mesh = Mesh(mesh_size, mesh_width, mesh_height, density, EDGE_TOLERANCE)
    mesh.adjacency_map = {(i, j): [] for i in range(mesh_width) for j in range(mesh_height)}

    for i in range(mesh_width):
        for j in range(mesh_height):
            current_rect = rect(i, j, density)

            if current_rect.collidelist(walls) != -1:
                continue
            
            # Cardinal directions (weight = 1)
            
            if i > 0 and rect(i-1, j, density).collidelist(walls) == -1:
                mesh.adjacency_map[(i, j)].append(((i-1, j), 1))
            if i < mesh_width-1 and rect(i+1, j, density).collidelist(walls) == -1:
                mesh.adjacency_map[(i, j)].append(((i+1, j), 1))
            if j > 0 and rect(i, j-1, density).collidelist(walls) == -1:
                mesh.adjacency_map[(i, j)].append(((i, j-1), 1))
            if j < mesh_height-1 and rect(i, j+1, density).collidelist(walls) == -1:
                mesh.adjacency_map[(i, j)].append(((i, j+1), 1))
            
            # Diagonals (weight = sqrt(2))
            # 1. UP-LEFT
            if (i > 0 and j > 0 and 
                rect(i-1, j-1, density).collidelist(walls) == -1 and  # Destination clear
                rect(i-1, j, density).collidelist(walls) == -1 and   # Corner 1 (Left) clear
                rect(i, j-1, density).collidelist(walls) == -1):     # Corner 2 (Up) clear
                    
                mesh.adjacency_map[(i, j)].append(((i-1, j-1), sqrt(2)))
            # 2. UP-RIGHT
            if (i < mesh_width-1 and j > 0 and 
                rect(i+1, j-1, density).collidelist(walls) == -1 and  # Destination clear
                rect(i+1, j, density).collidelist(walls) == -1 and   # Corner 1 (Right) clear
                rect(i, j-1, density).collidelist(walls) == -1):     # Corner 2 (Up) clear
                    
                mesh.adjacency_map[(i, j)].append(((i+1, j-1), sqrt(2)))
            # 3. DOWN-LEFT
            if (i > 0 and j < mesh_height-1 and 
                rect(i-1, j+1, density).collidelist(walls) == -1 and  # Destination clear
                rect(i-1, j, density).collidelist(walls) == -1 and   # Corner 1 (Left) clear
                rect(i, j+1, density).collidelist(walls) == -1):     # Corner 2 (Down) clear
                    
                mesh.adjacency_map[(i, j)].append(((i-1, j+1), sqrt(2)))
            # 4. DOWN-RIGHT
            if (i < mesh_width-1 and j < mesh_height-1 and 
                rect(i+1, j+1, density).collidelist(walls) == -1 and  # Destination clear
                rect(i+1, j, density).collidelist(walls) == -1 and   # Corner 1 (Right) clear
                rect(i, j+1, density).collidelist(walls) == -1):     # Corner 2 (Down) clear
                    
                mesh.adjacency_map[(i, j)].append(((i+1, j+1), sqrt(2)))
    
    return mesh

""" def generate(size, walls, density):
    map_width, map_height = size

    mesh_width = map_width//density
    mesh_height = map_height//density

    mesh_size = mesh_width*mesh_height

    mesh = Mesh(mesh_size, mesh_width, mesh_height, density)
    mesh.adjacency_map = {(i, j): [] for i in range(mesh_width) for j in range(mesh_height)}

    for i in range(mesh_width):
        for j in range(mesh_height):
            current_rect = rect(i, j, density)

            # DEBUG: Temporarily disabled collision check
            # if current_rect.collidelist(walls):
            #     continue
            
            # Cardinal directions (weight = 1)
            if i > 0:  # not rect(i-1, j, density).collidelist(walls):
                mesh.adjacency_map[(i, j)].append(((i-1, j), 1))
            if i < mesh_width-1:  # and not rect(i+1, j, density).collidelist(walls):
                mesh.adjacency_map[(i, j)].append(((i+1, j), 1))
            if j > 0:  # and not rect(i, j-1, density).collidelist(walls):
                mesh.adjacency_map[(i, j)].append(((i, j-1), 1))
            if j < mesh_height-1:  # and not rect(i, j+1, density).collidelist(walls):
                mesh.adjacency_map[(i, j)].append(((i, j+1), 1))
            
            # Diagonals (weight = sqrt(2))
            if i > 0 and j > 0:
                mesh.adjacency_map[(i, j)].append(((i-1, j-1), sqrt(2)))
            if i < mesh_width-1 and j > 0:
                mesh.adjacency_map[(i, j)].append(((i+1, j-1), sqrt(2)))
            if i > 0 and j < mesh_height-1:
                mesh.adjacency_map[(i, j)].append(((i-1, j+1), sqrt(2)))
            if i < mesh_width-1 and j < mesh_height-1:
                mesh.adjacency_map[(i, j)].append(((i+1, j+1), sqrt(2)))
    
    return mesh
 """