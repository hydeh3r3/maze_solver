import unittest
from unittest.mock import Mock
from main import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        mock_window = Mock()  # Create a mock Window object
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, mock_window)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_break_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10
        mock_window = Mock()  # Create a mock Window object
        maze = Maze(0, 0, num_rows, num_cols, 10, 10, mock_window)
        
        # Check if the entrance (top-left cell) has its top wall removed
        self.assertFalse(maze._cells[0][0].has_top_wall)
        
        # Check if the exit (bottom-right cell) has its bottom wall removed
        self.assertFalse(maze._cells[-1][-1].has_bottom_wall)
        
        # Check if other walls are still intact
        self.assertTrue(maze._cells[0][0].has_left_wall)
        self.assertTrue(maze._cells[0][0].has_right_wall)
        self.assertTrue(maze._cells[0][0].has_bottom_wall)
        
        self.assertTrue(maze._cells[-1][-1].has_left_wall)
        self.assertTrue(maze._cells[-1][-1].has_right_wall)
        self.assertTrue(maze._cells[-1][-1].has_top_wall)

if __name__ == "__main__":
    unittest.main()
