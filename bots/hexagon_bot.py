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

        valid_moves = []
        for x in range(self.map_rows):
            for y in range(self.MAP_HEIGHT):
                st = map[x][y].structure
                if st is not None and st.team == player_info.team:
                    self.build_valid_moves(map, player_info, st, valid_moves)     

        return

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