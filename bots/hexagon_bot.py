import random
import heapq
from src.player import *
from src.structure import *
from src.game_constants import GameConstants as GC

class MyPlayer(Player):
    def __init__(self):
        self.map_rows = None
        self.map_cols = None
        self.cell_metric = None
        self.weight = 0.5
        pass

    def play_turn(self, turn_num, map, player_info):
        self.map_rows = len(map)
        self.map_cols = len(map[0])

        my_structs = list(set(self.parse_map(map, player_info)))
        self.calculate_metric(map, player_info)
        self.shortest_dist(my_structs, map, player_info)
        # randomly bid 1 or 2
        self.set_bid(random.randint(1, 5))
        return

    def find_min(self, node_dict):
        min_dist = list(node_dict.values())[0]
        min_node = list(node_dict.keys())[0]
        for node in node_dict:
            if node_dict[node] < min_dist:
                min_dist = node_dict[node]
                min_node = node
        return min_node

    def shortest_dist(self, my_structs, map, player_info):
        dist_min = self.map_cols**2 + self.map_rows**2 + 1
        cell_min = None
        struct_min = None
        for struct in my_structs:
            for cell in self.cell_metric:
                distance = (struct.x - cell.x)**2 + (struct.y - cell.y)**2
                if distance < dist_min:
                    dist_min = distance
                    cell_min = cell
                    struct_min = struct
        start_node = struct_min
        node_dict = {struct_min: 0}
        parent = {struct_min : None}
        node = None
        node_cost = None
        visited = {}
        while len(node_dict) > 0:
            node = self.find_min(node_dict)
            node_cost = node_dict[node]
            visited[node] = True
            if  (node.x == cell_min.x and node.y == cell_min.y):
                node_cost = node_dict[node]
                break
            for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                nx, ny = (node.x + dx, node.y + dy)
                if nx >= 0 and nx < self.map_rows and ny >= 0 and ny <= self.map_cols:
                    cur_node = map[nx][ny]
                    if cur_node in visited or cur_node in my_structs:
                        continue
                    distance = node_cost + map[nx][ny].passability + ((cell_min.x - cur_node.x)**2 + (cell_min.y - cur_node.y)**2)*self.weight
                    if map[nx][ny] in node_dict and node_dict[cur_node] > distance and parent[cur_node] != node:
                        node_dict[cur_node]= distance
                        parent[cur_node]= node
                    elif map[nx][ny] not in node_dict:
                        node_dict[cur_node] = distance
                        parent[cur_node]= node
            node_dict.pop(node)
        # print("min parent len", len(parent))
        path = []
        par_node = node
        while True:
            path.append(parent[par_node])
            par_node = parent[par_node]
            if(par_node.x == start_node.x and par_node.y == start_node.y):
                break
        path.reverse()
        for p in path:
            # print("Node", p.x, p.y)
            if map[p.x][p.y].passability * StructureType.ROAD.get_base_cost() <= player_info.money: 
                self.build(StructureType.ROAD, p.x, p.y)
            else:
                return
        if map[node.x][node.y].passability * StructureType.TOWER.get_base_cost() <= player_info.money:
            self.build(StructureType.TOWER, p.x, p.y)
        return

    def parse_map(self, map, player_info):
        my_structs = []
        for x in range(self.map_rows):
            for y in range(self.map_cols):
                st = map[x][y].structure
                if st is not None and st.team == player_info.team:
                    my_structs.append(map[x][y])
        return my_structs

    ''' Find the "score" at this map state '''
    def calculate_metric(self, map, player_info):
        self.cell_metric = []
        # Iterate over all of our structures
        for x in range(self.map_rows):
            for y in range(self.map_cols):
                st = map[x][y].structure
                if st is None:
                    # Move in a radius of 2
                    coverage = [(1, 0), (-1, 0), (0, 1), (0, -1),(2, 0), (-2, 0), 
                            (0, 2), (0, -2),(1, 1), (1, -1), (-1, 1), (-1, -1)]

                    pop_served = 0
                    for dx, dy in coverage:
                        (nx, ny) = (x + dx, y + dy)
                        if nx >= 0 and nx < self.map_rows and ny >= 0 and ny < self.map_cols:
                            pop_served += map[nx][ny].population
                    if pop_served > 0:
                        self.cell_metric.append(map[x][y])
