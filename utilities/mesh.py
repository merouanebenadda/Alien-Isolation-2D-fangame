from .a_star import A_star

class Mesh():
    def __init__(self, size, width, height, density, edge_tolerance):
        self.size = size
        self.width = width
        self.height = height
        self.density = density
        self.edge_tolerance = edge_tolerance
        self.adjacency_map = {}

    def nearest_node(self, entity):
        """
        Converts the entity's continuous pixel position (x_pos, y_pos) 
        into discrete grid coordinates (i, j).
        """
        # Calculate the grid column (i) and row (j) using integer division
        # This gives the floor of the division, which is the correct tile index.
        i = int(entity.rect.centerx // self.density)
        j = int(entity.rect.centery // self.density)

        # Critical Safety: Clamp the indices to the mesh boundaries (0 to width/height - 1)
        # This prevents crashes if an entity somehow moves slightly off the map edge.
        i = max(0, min(i, self.width - 1))
        j = max(0, min(j, self.height - 1))
        
        return (i, j)
    
    def position(self, i, j):
        density = self.density
        return (density*i, density*j)

    def compute_path(self, entity1, entity2):
        path = A_star(self.nearest_node(entity1), self.nearest_node(entity2), self)
        if path != None: 
            return list(map(lambda node: self.position(node[0], node[1]), path))
        else:
            return None