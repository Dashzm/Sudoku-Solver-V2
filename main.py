from itertools import product
from testBoards import testBoardEasy as easyTest
from testBoards import testBoardMedium as medTest
from testBoards import testBoardHard as hardTest
from testBoards import testBoardExpert as expTest
from testBoards import testBoardEvil as evilTest
from testBoards import testBoardInvalid as invalTest


class Sudoku:
    def __init__(self, board_text):
        self.board = []
        if board_text is not None:
            self.parse(board_text)
        else:
            self.parse(".........\n.........\n.........\n.........\n.........\n.........\n.........\n.........\n.........\n")

    def __repr__(self):
        out_string = ""
        for j in range(0, 9):
            for i in range(0, 9):
                cell = self.board[j][i]
                if cell is None:
                    if len(self.poss(i, j)) == 2:
                        out_string += '.'
                    else:
                        out_string += '.'
                else:
                    out_string += str(cell)
            out_string += "\n"
        return out_string

    def parse(self, board):
        def process_char(c):
            try:
                if int(c) in {1, 2, 3, 4, 5, 6, 7, 8, 9}:
                    return int(c)
                else:
                    return None
            except ValueError:
                return None

        board = board.split('\n')

        self.board = []
        for line in board:
            self.board.append([process_char(c) for c in line])

    def poss(self, i, j):
        values = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        
        currentValRow = self.currentValRow(j)
        currentValCol = self.currentValCol(i)
        currentValBox = self.currentValBox(i, j)

        posVals = values - currentValRow - currentValCol - currentValBox
        return posVals

    def currentValRow(self, j):
        return set(self.board[j])

    def currentValCol(self, i):
        colVals = []
        for j in range(9):
            colVals.append(self.board[j][i])
        return set(colVals)

    def currentValBox(self, i, j):
        tlI = ((i // 3) * 3)
        tlJ = ((j // 3) * 3)
        items = set()
        for row in range(tlJ, tlJ + 3):
            for col in range(tlI, tlI + 3):
                items.add(self.board[row][col])
        return items

    def empty_finder(self):
      empty_cells = []
      for row in range(9):
          for col in range(9):
              cellVal = self.board[row][col]
              if cellVal is None:
                  possVals = self.poss(col, row)
                  empty_cells.append((row, col, possVals))
      return empty_cells
                  
    def naive_solve(self):
      prev_board_state = None
      while True:
          empty_cells = self.empty_finder()
          if not empty_cells:
              break
          prev_board_state = [row[:] for row in self.board]
          for empty_cell in empty_cells:
              if len(empty_cell) == 3:
                  row, col, possVals = empty_cell
                  if len(possVals) == 1:
                      self.board[row][col] = list(possVals)[0]
              elif len(empty_cell) == 2:
                  row, col = empty_cell
                  possVals = self.poss(col, row)
                  if len(possVals) == 1:
                      self.board[row][col] = list(possVals)[0]
          if prev_board_state == self.board:
              break

    def solve(self):
      empty_cells = self.empty_finder()
      
      if not empty_cells:
          return True
      row, col, possVals = min(empty_cells, key=lambda x: len(x[2]))
      
      for val in possVals:
          self.board[row][col] = val
          if self.solve():
              return True
          self.board[row][col] = None
      return False

    
def main():
    sudoku = Sudoku(evilTest)
    print("Original Sudoku:")
    print(sudoku)
    
    sudoku.naive_solve()
    print("After Naive Solve:")
    print(sudoku)

    if any(None in row for row in sudoku.board):
        if sudoku.solve():
            print("Solved Sudoku:")
            print(sudoku)
        else:
            print("No solution found.")
    else:
        print("Sudoku already solved with naive_solve.")
    
if __name__ == "__main__":
    main()