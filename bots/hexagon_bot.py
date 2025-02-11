import random
from src.player import *
from src.structure import *
from src.game_constants import GameConstants as GC

class MyPlayer(Player):
    def __init__(self):
        self.map_rows = 0
        self.map_cols = 0
        pass

    def play_turn(self, turn_num, map, player_info):
        self.map_rows = len(map)
        self.map_cols = len(map[0])

        my_structs, valid_moves = self.parse_map(map, player_info)   
        my_structs = list(set(my_structs))
        valid_moves = list(set(valid_moves))

        self.evaluate(map, my_structs, valid_moves, player_info)
        # randomly bid 1 or 2
        self.set_bid(random.randint(1, 2))
        return


    def evaluate(self, map, my_structs, valid_moves, player_info):
        scores = []
        
        for move in valid_moves:
            new_map = self.updated_map(map, move, player_info.team)
            scores.append(self.calculate_score(new_map, my_structs))

        max_score = max(scores)
        arg = scores.index(max_score)

        if max_score == 0:
            arg = random.randint(0, len(valid_moves) - 1)

        tx = valid_moves[arg][0].x
        ty = valid_moves[arg][0].y
        build_type = valid_moves[arg][1]
        self.build(build_type, tx, ty)
        return 

    def updated_map(self, map, move, player_team):
        x = move[0].x
        y = move[0].y

        new_map = map.copy()
        
        new_map[x][y].type = move[1]
        new_map[x][y].team = player_team 

        return new_map

    def parse_map(self, map, player_info):
        my_structs = []
        valid_moves = []
        for x in range(self.map_rows):
            for y in range(self.map_cols):
                st = map[x][y].structure
                if st is not None and st.team == player_info.team:
                    my_structs.append(map[x][y])
                    self.build_valid_moves(map, player_info, st, valid_moves)
        return my_structs, valid_moves

    def build_valid_moves(self, map, player_info, tile, valid_moves):
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            (nx, ny) = (tile.x + dx, tile.y + dy)
            # check if adjacent tile is valid (on the map and empty)
            if 0 <= nx < self.map_rows and 0 <= ny < self.map_cols and map[nx][ny].structure is None:
                cost = StructureType.TOWER.get_base_cost() * map[nx][ny].passability
                # check if my team can afford this structure
                if player_info.money >= cost:
                    # attempt to build
                    valid_moves.append((map[nx][ny], StructureType.TOWER))

                cost = StructureType.ROAD.get_base_cost() * map[nx][ny].passability
                # check if my team can afford this structure
                if player_info.money >= cost:
                    # attempt to build
                    valid_moves.append((map[nx][ny], StructureType.ROAD))          
        return

    ''' Find the "score" at this map state '''
    def calculate_score(self, map, my_structs):
        pop_served = 0
        # Iterate over all of our structures
        for st in my_structs:
            # If structure is a tower
            if st.structure.type == StructureType.TOWER:
                # Move in a radius of 2
                coverage = [(1, 0), (-1, 0), (0, 1), (0, -1),(2, 0), (-2, 0), 
                        (0, 2), (0, -2),(1, 1), (1, -1), (-1, 1), (-1, -1)]

                for dx, dy in coverage:
                    (nx, ny) = (st.x + dx, st.y + dy)
                    if nx >= self.map_rows or ny >= self.map_cols:
                        continue
                    pop_served += map[nx][ny].population

        return pop_served


