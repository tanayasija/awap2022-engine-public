from src.player import *
from src.structure import *
from src.game_constants import GameConstants as GC

class Hexagon(Player):
    def __init__(self):
        self.map_rows = 0
        self.map_cols = 0
        pass

    def play_turn(self, turn_num, map, player_info):
        self.map_rows = len(map)
        self.map_cols = len(map[0])

        valid_moves = set(self.parse_map(map, player_info))   
        self.evaluate(valid_moves)
    
        return

    def evaluate(self, moves):
        for move in moves:
            new_map = updated_map(move)
            scores.append(calculate_score(new_map))

        arg = scores.index(max(scores))

        tx = moves[arg][0].x
        ty = moves[arg][0].y
        build_type = moves[arg][1]
        self.build(build_type, tx, ty)
        return 

    def parse_map(self, map, player_info):
        valid_moves = []
        for x in range(self.map_rows):
            for y in range(self.MAP_HEIGHT):
                st = map[x][y].structure
                if st is not None and st.team == player_info.team:
                    self.build_valid_moves(map, player_info, st, valid_moves)
        return valid_moves

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
        # Iterate over all of our structures
        for st in my_struct:
            # If structure is a tower
            if st.type == StructureType.TOWER:
                pop_served = 0
                
                # Move in a radius of 2
                coverage = [(1, 0), (-1, 0), (0, 1), (0, -1),(2, 0), (-2, 0), 
                        (0, 2), (0, -2),(1, 1), (1, -1), (-1, 1), (-1, -1)]

                for dx, dy in coverage:
                    (nx, ny) = (st.x + dx, st.y + dy)
                    pop_served += map[nx][ny].population

    return pop_served


