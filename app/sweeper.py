import random, time, copy
import json

def mine_sweeper(bombs, num_rows, num_cols):
    field = [[0 for i in range(num_cols)] for j in range(num_rows)]
    
    for bomb_location in bombs:
        (bomb_row, bomb_col) = bomb_location
        field[bomb_row][bomb_col] = -1

        row_range = range(bomb_row - 1, bomb_row + 2) #El +2 es xque range, x ej, en (0,0), va a ir de (-1,2), pero la 2 no cuenta, osea que agarra -1,0,1 
        col_range = range(bomb_col - 1, bomb_col + 2)

        for i in row_range:
            for j in col_range:
                if (0 <= i < num_rows and 0 <= j < num_cols and field[i][j] != -1):
                    field[i][j] += 1
    return field
    

print(mine_sweeper([[0,0], [1,2]], 3, 4))

print(range(3,3))

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

    def as_dict(self):
        field = []
        for row in self._field:
            cols = []
            for square in row:
                cols.append(square.as_dict())
            field.append(cols)
        
        return {
            "id": self.id,
            "num_rows": self.num_rows,
            "num_cols": self.num_cols,
            "num_mines": self.num_mines,
            "field": field,
            "is_over": self.is_over,
            "time": self.time
        }

    def init_board(self):
        self._field = [[Square(j, i) for i in range(self.num_cols)] for j in range(self.num_rows)]
        
    #Cambiar nombre, esto convierte una fila de squares a una fila de valores
    def map_listas(self, sqr_list):
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
        print(list(map(self.map_listas, self._field)))
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if (i < self.num_rows and j < self.num_cols and self._field[i][j]._value == -1):
                    row_range = range(i - 1, i + 2) #El +2 es xque range, x ej, en (0,0), va a ir de (-1,2), pero la 2 no cuenta, osea que agarra -1,0,1 
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
                square.flagged = True
            elif action == 'QUESTION':
                square.question = True
            elif action == 'CLICK':
                square.flagged = False
                square.open = True
                if square.is_mine:
                    self.end_game()
                elif square.is_empty:
                    self.click_empty_square(square)
            else:
                square.flagged = False
                square.question = False

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
    
    #Chequear
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
        # value -1 to 8. the number of sorrounding mines. -1 is the mine. 0 means
        # "empty cell"
        self._value = 0
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



"""
ss = Square(3,4)

gg = Game("sarasa", 3, 7, 5)

gg.init_board()

gg.place_mines()

gg.place_proximities()

def map_listas(sqr_list):
    return list(map(lambda x: x._value, sqr_list))

a = list(map(map_listas, gg._field))

print(a)

print(json.dumps(gg.as_dict()))
#print(ss)
#print(ss.as_dict())
#print(json.dumps(ss.as_dict()))

sa = [Square(1,2), Square(2,3), Square(3,4)] 

def map_listas(sqr_list):
    return map(lambda x: x._value, sqr_list)

print(map_listas(sa))
"""