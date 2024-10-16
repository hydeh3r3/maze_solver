# Maze Solver

This project implements a maze generator and solver using Python and Tkinter for visualization.

## Features

- Generates random mazes using a recursive backtracking algorithm
- Visualizes the maze generation process
- Implements a simple GUI using Tkinter

## Classes

### Point
Represents a 2D point with x and y coordinates.

### Line
Represents a line segment between two points. Can draw itself on a canvas.

### Cell
Represents a single cell in the maze. Manages its walls and can draw itself.

### Window
Handles the Tkinter window and canvas for visualization.

### Maze
Generates the maze structure and manages the maze creation process.

## Usage

To run the maze generator:

### Main.py

This will create a window displaying the maze generation process.

## Customization

You can customize the maze size and cell dimensions by modifying the parameters in the `main()` function:

## Dependencies

- Python 3.x
- Tkinter (usually comes pre-installed with Python)

## Note

This project is a work in progress and currently only implements maze generation. Solving functionality may be added in future updates.
