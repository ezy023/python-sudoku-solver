import itertools
import copy
from collections import OrderedDict

def grouper(iterable, n, fillvalue=None):
  args = [iter(iterable)] * n
  return itertools.izip_longest(fillvalue=fillvalue, *args)

def flatten(listOfLists):
  "Flatten one level of nesting"
  return itertools.chain.from_iterable(listOfLists)

def triples(row):
  return list(grouper(row, 3))

def get_boxes(box_rows):
  return zip(*box_rows)

class Sudoku:

  def __init__(self, board):
    self.board = list(board)
    self.indices_board = list(range(0,81))

  def print_board(self):
    print self.board

  def find_row_values(self, row):
    return list(list(grouper(self.board, 9))[row])

  def find_row_for_index(self, index):
    for i in list(range(0,9)):
      if index in list(grouper(self.indices_board, 9))[i]:
        return i

  def find_column_values(self, column):
    return self.slice_columns(self.board)[column]

  def find_column_for_index(self, index):
    for i in list(range(0,9)):
      if index in self.slice_columns(self.indices_board)[i]:
        return i

  def slice_columns(self, board_to_slice):
    transposed_matrix = []
    for i in range(0,9):
      transposed_matrix.append(board_to_slice[i::9])
    return transposed_matrix

  def slice_boxes(self, board_to_slice):
    indices = board_to_slice
    rows = map(list, grouper(indices, 9))
    sets = map(triples, rows)
    cool = map(list, list(grouper(sets, 3)))
    awes = map(list, flatten(map(get_boxes, cool)))
    return awes

  def find_box_values(self, box_number):
    return map(list, map(flatten, self.slice_boxes(self.board)))[box_number]

  def find_box_for_index(self, index):
    for i in list(range(0,9)):
      if index in map(list, map(flatten, self.slice_boxes(self.indices_board)))[i]:
        return i

  def get_coords(self, index):
    coords = []
    coords.append(self.find_row_for_index(index))
    coords.append(self.find_column_for_index(index))
    coords.append(self.find_box_for_index(index))
    return coords

  def all_values(self, row, col, box):
    options =  self.find_row_values(row) + \
               self.find_column_values(col) + \
               self.find_box_values(box)
    return OrderedDict.fromkeys(options).keys()

  def get_index_of_next_empty(self):
    return self.board.index('0')

  def solve(self):
    if '0' not in self.board:
      return "".join(self.board)

    zero_index = self.board.index('0')
    potential_values = map(str, list(range(1,10)))
    unavailable_values = self.all_values(*self.get_coords(zero_index))
    possible_values = [i for i in potential_values if i not in unavailable_values]
    for i in possible_values:
      new_board = copy.copy(self.board)
      new_board[zero_index] = i
      next_board = "".join(new_board)
      new_sudoku = Sudoku("".join(new_board))
      result = new_sudoku.solve()
      if result:
        return result





f = open('puzzles.txt', 'r')
puzzles = f.readlines()
for board in puzzles:
  sudoku = Sudoku(board.rstrip())
  print sudoku.solve()

