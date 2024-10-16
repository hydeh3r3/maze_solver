from tkinter import Tk, BOTH, Canvas
import time
import random

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2
    
    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(
            self.point1.x, self.point1.y, self.point2.x, self.point2.y, 
            fill=fill_color, width=2
        )

class Cell:
    def __init__(self, win: 'Window', x1: int, y1: int, x2: int, y2: int):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = win

    def draw(self):
        bg_color = "#d9d9d9"  # Background color for non-existent walls
        if self.has_left_wall:
            line = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            self._win.draw_line(line, "black")
        else:
            line = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            self._win.draw_line(line, bg_color)
        if self.has_right_wall:
            line = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
            self._win.draw_line(line, "black")
        else:
            line = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
            self._win.draw_line(line, bg_color)
        if self.has_top_wall:
            line = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            self._win.draw_line(line, "black")
        else:
            line = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            self._win.draw_line(line, bg_color)
        if self.has_bottom_wall:
            line = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            self._win.draw_line(line, "black")
        else:
            line = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            self._win.draw_line(line, bg_color)

    def draw_move(self, to_cell, undo=False):
        """
        Draw a line from the center of this cell to the center of another cell.

        Args:
            to_cell (Cell): The cell to draw the line to.
            undo (bool): If True, draw the line in gray (for backtracking). If False, draw in red.
        """
        # Calculate the center coordinates of both cells
        x1 = (self._x1 + self._x2) // 2
        y1 = (self._y1 + self._y2) // 2
        x2 = (to_cell._x1 + to_cell._x2) // 2
        y2 = (to_cell._y1 + to_cell._y2) // 2

        # Create a line between the centers
        line = Line(Point(x1, y1), Point(x2, y2))

        # Draw the line with the appropriate color
        color = "gray" if undo else "red"
        self._win.draw_line(line, color)

class Window:
    def __init__(self, width: int, height: int) -> None:
        """
        Initialize a new Window object.

        Args:
            width (int): The width of the window in pixels.
            height (int): The height of the window in pixels.
        """
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=True)
        self.__running = False

    def redraw(self) -> None:
        """
        Redraw all the graphics in the window.
        """
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self) -> None:
        """
        Enter the main event loop and wait for the window to be closed.
        """
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self) -> None:
        """
        Close the window and stop the main event loop.
        """
        self.__running = False

    def draw_line(self, line: Line, fill_color: str) -> None:
        """
        Draw a line on the canvas.

        Args:
            line (Line): The line to draw.
            fill_color (str): The color to use for drawing the line.
        """
        line.draw(self.__canvas, fill_color)

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []

        if seed is not None:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)  # Start breaking walls from the top-left cell
        self._reset_cells_visited()  # Reset visited status after maze generation

    def _break_entrance_and_exit(self):
        # Break the entrance (top wall of the top-left cell)
        self._cells[0][0].has_top_wall = False
        self._cells[0][0].draw()

        # Break the exit (bottom wall of the bottom-right cell)
        self._cells[-1][-1].has_bottom_wall = False
        self._cells[-1][-1].draw()

    def _create_cells(self):
        for i in range(self._num_cols):
            col = []
            for j in range(self._num_rows):
                x1 = self._x1 + i * self._cell_size_x
                y1 = self._y1 + j * self._cell_size_y
                x2 = x1 + self._cell_size_x
                y2 = y1 + self._cell_size_y
                cell = Cell(self._win, x1, y1, x2, y2)
                col.append(cell)
            self._cells.append(col)
        
        # Draw cells after they've all been created
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)
        
        # Break entrance and exit
        self._break_entrance_and_exit()

    def _draw_cell(self, i: int, j: int):
        if self._win is None:
            return
        try:
            cell = self._cells[i][j]
            cell.draw()
            self._animate()
        except IndexError:
            print(f"Error: Cell at position ({i}, {j}) does not exist.")

    def _animate(self):
        self._win.redraw()
        time.sleep(0.05)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        
        directions = [('N', -1, 0), ('S', 1, 0), ('W', 0, -1), ('E', 0, 1)]
        random.shuffle(directions)
        
        for direction, di, dj in directions:
            next_i, next_j = i + di, j + dj
            
            # Check if the next cell is within the maze bounds
            if (0 <= next_i < self._num_rows and 
                0 <= next_j < self._num_cols and 
                not self._cells[next_i][next_j].visited):
                
                if direction == 'N':
                    self._cells[i][j].has_top_wall = False
                    self._cells[next_i][next_j].has_bottom_wall = False
                elif direction == 'S':
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[next_i][next_j].has_top_wall = False
                elif direction == 'W':
                    self._cells[i][j].has_left_wall = False
                    self._cells[next_i][next_j].has_right_wall = False
                elif direction == 'E':
                    self._cells[i][j].has_right_wall = False
                    self._cells[next_i][next_j].has_left_wall = False
                
                self._cells[i][j].draw()
                self._cells[next_i][next_j].draw()
                self._animate()
                self._break_walls_r(next_i, next_j)
        
        self._draw_cell(i, j)

    def _reset_cells_visited(self):
        """Reset the visited property of all cells to False."""
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        """
        Solve the maze using depth-first search.
        Returns True if the maze was solved, False otherwise.
        """
        # Reset all cells to unvisited before solving
        self._reset_cells_visited()
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        """
        Recursive helper method to solve the maze.
        Returns True if the current cell leads to the solution, False otherwise.
        """
        self._animate()
        self._cells[i][j].visited = True

        # Check if we've reached the end cell (bottom-right corner)
        if i == self._num_rows - 1 and j == self._num_cols - 1:
            return True

        # Define possible directions: right, down, left, up
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for di, dj in directions:
            next_i, next_j = i + di, j + dj

            # Check if the next cell is within the maze and not visited
            if (0 <= next_i < self._num_rows and 
                0 <= next_j < self._num_cols and 
                not self._cells[next_i][next_j].visited):

                # Check if there's no wall blocking the path
                if ((di, dj) == (0, 1) and not self._cells[i][j].has_right_wall) or \
                   ((di, dj) == (1, 0) and not self._cells[i][j].has_bottom_wall) or \
                   ((di, dj) == (0, -1) and not self._cells[i][j].has_left_wall) or \
                   ((di, dj) == (-1, 0) and not self._cells[i][j].has_top_wall):

                    # Draw the move
                    self._cells[i][j].draw_move(self._cells[next_i][next_j])

                    # Recursively solve from the next cell
                    if self._solve_r(next_i, next_j):
                        return True

                    # If the path didn't lead to a solution, undo the move
                    self._cells[i][j].draw_move(self._cells[next_i][next_j], undo=True)

        return False

def main():
    win = Window(800, 600)
    
    # Create a maze
    maze = Maze(50, 50, 10, 10, 50, 50, win, seed=0)
    
    # Break entrance and exit
    maze._break_entrance_and_exit()
    
    # Solve the maze
    solved = maze.solve()
    if solved:
        print("Maze solved!")
    else:
        print("Maze could not be solved.")
    
    win.wait_for_close()

if __name__ == "__main__":
    main()
