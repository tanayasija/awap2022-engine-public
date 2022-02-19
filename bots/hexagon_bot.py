import random
from src.player import *
from src.structure import *
from src.game_constants import GameConstants as GC

class MyPlayer(Player):
    def __init__(self):
        self.map_rows = None
        self.map_cols = None
        self.cell_metric = None
        pass

    def play_turn(self, turn_num, map, player_info):
        self.map_rows = len(map)
        self.map_cols = len(map[0])

        my_structs = list(set(self.parse_map(map, player_info)))
        if self.cell_metric is None:
            self.calculate_metric(map, player_info)
        # randomly bid 1 or 2
        self.set_bid(random.randint(1, 2))
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

                    for dx, dy in coverage:
                        (nx, ny) = (x + dx, y + dy)
                        if nx < self.map_rows and ny < self.map_cols:
                            self.cell_metric.append(map[nx][ny])

