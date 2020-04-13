import random, time
import json

class Game:

    def __init__(self, uid, rows, cols, mines):
        
        self.id = uid
        self.num_rows = rows
        self.num_cols = cols
        
        self.num_mines = mines

        self._field = None
        self.is_over = False
        self.time = 0

        #Board setup
        self.init_board()
        self.place_mines()
        self.place_proximities()

    def field_as_dict(self):
        field = []
        for row in self._field:
            cols = []
            for square in row:
                cols.append(square.as_dict())
            field.append(cols)
        return field

    def as_dict(self):
        return {
            "id": self.id,
            "num_rows": self.num_rows,
            "num_cols": self.num_cols,
            "num_mines": self.num_mines,
            "field": self.field_as_dict(),
            "is_over": self.is_over,
            "time": self.time
        }

    def init_board(self):
        self._field = [[Square(j, i) for i in range(self.num_cols)] for j in range(self.num_rows)]
        
    def from_squares_to_values(self, sqr_list):
        return list(map(lambda x: x._value, sqr_list))

    def place_mines(self):
        for _ in range(self.num_mines):
            self.place_mine()

    #Modifico el valor de un cuadrado elegido al azar
    def place_mine(self):
        row = random.randint(0, self.num_rows - 1)
        col = random.randint(0, self.num_cols - 1)

        currentRow = self._field[row]
        if currentRow[col]._value != -1:
            self._field[row][col]._value = -1
        else:
            self.place_mine()
        
        print("random row and col %d x %d" % (row, col))
        return (row, col)

    def place_proximities(self):
        print(list(map(self.from_squares_to_values, self._field)))
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if (i < self.num_rows and j < self.num_cols and self._field[i][j]._value == -1):
                    row_range = range(i - 1, i + 2)
                    col_range = range(j - 1, j + 2)
                
                    for i2 in row_range:
                        for j2 in col_range:
                            if (0 <= i2 < self.num_rows and 0 <= j2 < self.num_cols and self._field[i2][j2]._value != -1):
                                self._field[i2][j2]._value += 1
        
        return self._field

    def get_square_by_coordinate(self, row, col):
        return self._field[row][col]

    def click_square(self, row, col, action):
        square = self._field[row][col]

        if not square.open:
            if action == 'FLAG':
                if square.flagged: #Turn flag to question mark
                    square.flagged = False
                    square.question = True
                elif square.question: #Remove question mark (already unflagged)
                    square.question = False
                else: #Placing flag
                    square.flagged = True
            elif action == 'CLICK' and not square.flagged and not square.question:
                square.open = True
                if square.is_mine:
                    self.end_game()
                elif square.is_empty:
                    self.click_empty_square(square)

            self.check_end_game()

    def end_game(self):
        self.is_over = True

    def click_empty_square(self, square):
        adjacent_squares = self.get_adjacent_squares(square)
        for adjacent_square in adjacent_squares:
            self.click_square(adjacent_square.row, adjacent_square.col, 'CLICK')
    
    def get_adjacent_squares(self, square):
        adjacent_squares = []

        row_range = range(square.row - 1, square.row + 2) 
        col_range = range(square.col - 1, square.col + 2)

        for i in row_range:
            for j in col_range:
                if (0 <= i < self.num_rows and 0 <= j < self.num_cols and not (square.row == i and square.col == j)):
                    adjacent_squares.append(self._field[i][j])
        
        return adjacent_squares

    def click_result(self):
        return {
            "id": self.id,
            "field": self.field_as_dict(),
            "is_over": self.is_over
        }

    def check_end_game(self):
        num_flags = 0
        for row in self._field:
            for square in row:
                if square.flagged and square.is_mine:
                    num_flags += 1
        
        if num_flags == self.num_mines:
            self.end_game()



class Square:
    def __init__(self, row, col):

        self.row = row
        self.col = col
        self._value = 0 # value -1 to 8. the number of sorrounding mines. -1 is the mine. 0 means
        self.flagged = False
        self.question = False
        self.open = False

    def as_dict(self):
        return {
            "row": self.row,
            "col": self.col,
            "value": self._value,
            "flagged": self.flagged,
            "question": self.question,
            "is_mine": self.is_mine,
            "open": self.open
        }

    @property
    def is_mine(self):
        return self._value == -1

    @property
    def is_empty(self):
        return self._value == 0