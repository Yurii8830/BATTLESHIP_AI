import random
import pygame

# Constants for game
SCREEN_SIZE = 800
GRID_SIZE = 10
CELL_SIZE = SCREEN_SIZE // (2 * GRID_SIZE)
FPS = 30

COLORS = {
    "water": (173, 216, 230),
    "ship": (0, 0, 128),
    "hit": (255, 0, 0),
    "miss": (255, 255, 255),
    "text": (0, 0, 0),
    "grid": (0, 0, 0),
}

FONT_SIZE = 24

class Ship:
    def __init__(self, size, orientation, row, col):
        self.size = size
        self.orientation = orientation
        self.row = row
        self.col = col
        self.indexes = self.compute_indexes()

    def compute_indexes(self):
        indexes = []
        for i in range(self.size):
            if self.orientation == "h":
                indexes.append(self.row * GRID_SIZE + self.col + i)
            else:
                indexes.append((self.row + i) * GRID_SIZE + self.col)
        return indexes

    def is_sunk(self, board):
        return all(board[i] == "H" for i in self.indexes)

class Player:
    def __init__(self):
        self.ships = []
        self.board = ["U"] * (GRID_SIZE * GRID_SIZE)  # U = Unknown

    def place_ship(self, size):
        placed = False
        while not placed:
            orientation = random.choice(["h", "v"])
            row = random.randint(0, GRID_SIZE - (size if orientation == "v" else 1))
            col = random.randint(0, GRID_SIZE - (size if orientation == "h" else 1))
            new_ship = Ship(size, orientation, row, col)

            if all(self.board[i] == "U" for i in new_ship.indexes):
                self.ships.append(new_ship)
                for i in new_ship.indexes:
                    self.board[i] = "S"  # S = Ship
                placed = True

    def all_sunk(self):
        return all(ship.is_sunk(self.board) for ship in self.ships)

class Game:
    def __init__(self):
        self.player1 = Player()
        self.player2 = Player()
        self.player1_turn = True
        self.running = True
        self.difficulty = "medium"  # Default difficulty

        self.player1.place_ship(5)
        self.player2.place_ship(5)
        self.place_additional_ships(self.player1)
        self.place_additional_ships(self.player2)

        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption("Battleship")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, FONT_SIZE)

    def place_additional_ships(self, player):
        for size in [4, 3, 3, 2, 2, 2]:
            player.place_ship(size)

    def draw_grid(self, offset_x=0):
        for x in range(0, GRID_SIZE * CELL_SIZE, CELL_SIZE):
            pygame.draw.line(self.screen, COLORS["grid"], (x + offset_x, 0), (x + offset_x, GRID_SIZE * CELL_SIZE))
            pygame.draw.line(self.screen, COLORS["grid"], (offset_x, x), (offset_x + GRID_SIZE * CELL_SIZE, x))

    def draw_board(self, player, offset_x=0, show_ships=False):
        for i in range(GRID_SIZE * GRID_SIZE):
            row, col = divmod(i, GRID_SIZE)
            x, y = col * CELL_SIZE + offset_x, row * CELL_SIZE

            if player.board[i] == "S" and show_ships:
                color = COLORS["ship"]
            elif player.board[i] == "H":
                color = COLORS["hit"]
            elif player.board[i] == "M":
                color = COLORS["miss"]
            else:
                color = COLORS["water"]

            pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(self.screen, COLORS["grid"], (x, y, CELL_SIZE, CELL_SIZE), 1)

    def make_move(self, index, player):
        if player.board[index] == "S":
            player.board[index] = "H"
            return True
        elif player.board[index] == "U":
            player.board[index] = "M"
            return False

    def ai_move(self, player):
        valid_moves = [i for i, square in enumerate(player.board) if square == "U"]

        if self.difficulty == "easy":
            move = random.choice(valid_moves)
        elif self.difficulty == "medium":
            move = valid_moves[len(valid_moves) // 2]
        else:  # Hard difficulty
            move = random.choice(valid_moves[:len(valid_moves) // 2])

        return self.make_move(move, player)

    def display_message(self, text, y_offset):
        text_surface = self.font.render(text, True, COLORS["text"])
        text_rect = text_surface.get_rect(center=(SCREEN_SIZE // 2, y_offset))
        self.screen.blit(text_surface, text_rect)

    def play(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(COLORS["water"])
            self.draw_board(self.player1, offset_x=0, show_ships=True)
            self.draw_board(self.player2, offset_x=SCREEN_SIZE // 2)
            self.draw_grid()

            self.display_message("Player 1", SCREEN_SIZE // 2 - 50)
            self.display_message("Player 2", SCREEN_SIZE - 50)

            if self.player1_turn:
                self.ai_move(self.player2)
            else:
                self.ai_move(self.player1)

            self.player1_turn = not self.player1_turn

            if self.player1.all_sunk() or self.player2.all_sunk():
                self.running = False
                winner = "Player 1" if self.player2.all_sunk() else "Player 2"
                self.display_message(f"{winner} wins!", SCREEN_SIZE // 2)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.play()
