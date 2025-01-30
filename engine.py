import random
from tabnanny import check


class Ship:
    def __init__(self, size):
        self.row = random.randrange(0,9)
        self.col = random.randrange(0,9)
        self.size = size
        self.orientation = random.choice(["h","v"])
        self.indexes = self.compute_indexes()

    def compute_indexes(self):
        start_index = self.row * 10 + self.col
        if self.orientation == "h":
            return [start_index + i for i in range(self.size)]
        elif self.orientation == "v":
            return [start_index + i*10 for i in range(self.size)]

class Player:
    def __init__ (self):
        self.ships = []
        self.search = ["U" for i in range (100)] # "U" for "unknown"
        self.place_ships(sizes = [5,4,3,3,2])
        list_of_lists = [ship.indexes for ship in self.ships]
        self.indexes = [index for sublist in list_of_lists for index in sublist]

    def place_ships(self, sizes):
        for size in sizes:
            placed = False
            while not placed:
                ship = Ship(size)
                possible = True
                for i in ship.indexes:
                    if i >= 100:
                        possible = False
                        break
                    new_row = i // 10
                    new_col = i % 10
                    if new_row != ship.row and new_col != ship.col:
                        possible = False
                        break
                    for other_ship in self.ships:
                        if i in other_ship.indexes:
                            possible=False
                            break
                if possible:
                    self.ships.append(ship)
                    placed = True

    def show_ships(self):
        indexes = ["-" if i not in self.indexes else "X" for i in range(100)]
        for row in range(10):
            print(" ".join(indexes[(row - 1) * 10: row * 10]))

class Game:
    def __init__(self, human1, human2):
        self.human1 = human1
        self.human2 = human2
        self.player1 = Player ()
        self.player2 = Player ()
        self.player1_turn = True
        self.computer_turn = True if not self.human1 else False
        self.over = False
        self.result = None
        self.n_shots = 0

    def make_move (self, i):
        player = self.player1 if self.player1_turn else self.player2
        opponent = self.player2 if self.player1_turn else self.player1
        hit = False

        # set miss "M" or hit "H"
        if i in opponent.indexes:
            player.search[i] = "H"
            hit = True

            # check if ship is sunk ("S")
            for ship in opponent.ships:
                sunk = True
                for i in ship.indexes:
                    if player.search[i] == "U":
                        sunk = False
                        break
                if sunk:
                    for i in ship.indexes:
                        player.search[i] = "S"
        else:
            player.search[i] = "M"

         # check if game over
        game_over = True
        for i in opponent.indexes:
            if player.search[i] == "U":
                    game_over = False
        self.over = game_over
        self.result = 1 if self.player1_turn else 2

        if not hit:
            self.player1_turn = not self.player1_turn

            # switch between human and computer turns
            if (self.human1 and not self.human2) or (not self.human1 and self.human2):
                self.computer_turn = not self.computer_turn

        self.n_shots += 1

    def random_ai(self):
        search = self.player1.search if self.player1_turn else self.player2.search
        unknown = [i for i, square in enumerate(search) if square == "U"]
        if len(unknown) > 0:
            random_index = random.choice(unknown)
            self.make_move(random_index)

    def basic_ai(self):
        # setup
        search = self.player1.search if self.player1_turn else self.player2.search
        unknown = [i for i, square in enumerate(search) if square == "U"]
        hits = [i for i, square in enumerate(search) if square == "H"]

        # search in neighborhood of hits
        unknown_with_neighboring_hits1 = []
        unknown_with_neighboring_hits2 = []
        for u in unknown:
            if u + 1 in hits or u - 1 in hits or u - 10 in hits or u + 10 in hits:
                unknown_with_neighboring_hits1.append(u)
            if u + 2 in hits or u - 2 in hits or u - 20 in hits or u + 20 in hits:
                unknown_with_neighboring_hits2.append(u)

        for u in unknown:
            if u in unknown_with_neighboring_hits1 and u in unknown_with_neighboring_hits2:
                self.make_move(u)
                return

        # pick "u" square that has a neighbor marked as "H"
        if len(unknown_with_neighboring_hits1) > 0:
            self.make_move(random.choice(unknown_with_neighboring_hits1))
            return

        # checker board pattern
        checker_board = []
        for u in unknown:
            row = u // 10
            col = u % 10
            if (row+col) % 2 == 0:
                checker_board.append(u)
        if len(checker_board) > 0:
            self.make_move(random.choice(checker_board))
            return


        # random move
        self.random_ai()

    def probability_ai(self):
        search = self.player1.search if self.player1_turn else self.player2.search
        unknown = [i for i, square in enumerate(search) if square == "U"]
        hits = [i for i, square in enumerate(search) if square == "H"]

        # Ініціалізація карти ймовірностей з нулями
        probability_map = [0] * 100

        # Крок 1: Якщо є попадання, спробуємо знайти решту частини корабля
        for hit in hits:
            row = hit // 10
            col = hit % 10

            # Перевірка горизонтальних (ліво/право) та вертикальних (вгору/вниз) напрямків від попадання
            # Горизонтальні перевірки (ліво та право)
            for direction in [-1, 1]:
                # Йдемо вліво чи вправо
                length = 1
                while 0 <= col + direction * length < 10 and search[hit + direction * length] == "U":
                    probability_map[hit + direction * length] += 1
                    length += 1

            # Вертикальні перевірки (вгору та вниз)
            for direction in [-10, 10]:
                # Йдемо вгору чи вниз
                length = 1
                while 0 <= hit + direction * length < 100 and search[hit + direction * length] == "U":
                    probability_map[hit + direction * length] += 1
                    length += 1

        # Крок 2: Покарання за клітинки, що вже пропущені
        for i in range(100):
            if search[i] == "M":
                probability_map[i] -= 3  # Тяжче покарання за пропущені клітинки

        # Крок 3: Уточнення ймовірностей з урахуванням розмірів кораблів та їх розташування
        ship_sizes = [5, 4, 3, 3, 2]  # Розміри кораблів, які використовуються в грі
        for ship_size in ship_sizes:
            for i in range(100):
                if search[i] == "U":
                    row = i // 10
                    col = i % 10
                    # Горизонтальне розташування корабля
                    if col + ship_size <= 9:
                        for j in range(ship_size):
                            if search[i + j] == "U":  # Коригуємо тільки для "U" клітинок
                                probability_map[i + j] += 1
                    # Вертикальне розташування корабля
                    if row + ship_size <= 9:
                        for j in range(ship_size):
                            if search[i + j * 10] == "U":  # Коригуємо тільки для "U" клітинок
                                probability_map[i + j * 10] += 1

        # Крок 4: Вибір найкращого ходу, з урахуванням вищої ймовірності для залишкових невідомих клітинок
        best_move = max(range(100), key=lambda x: probability_map[x] if search[x] == "U" else -1)
        self.make_move(best_move)

    def hunting_targeting_ai(self):
        search = self.player1.search if self.player1_turn else self.player2.search
        unknown = [i for i, square in enumerate(search) if square == "U"]
        hits = [i for i, square in enumerate(search) if square == "H"]

        if len(hits) == 0:
            # Start hunting (if no hits yet)
            self.random_ai()
            return

        # Try to target nearby squares after a hit
        target_squares = []
        for hit in hits:
            row = hit // 10
            col = hit % 10
            # Check neighboring squares (up, down, left, right)
            for r, c in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_row = row + r
                new_col = col + c
                if 0 <= new_row < 10 and 0 <= new_col < 10:
                    target_square = new_row * 10 + new_col
                    if search[target_square] == "U":
                        target_squares.append(target_square)

        if target_squares:
            # Make a move targeting the nearest square around a hit
            self.make_move(random.choice(target_squares))
        else:
            # If no neighboring squares found, revert to a random move
            self.random_ai()
