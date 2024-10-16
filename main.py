from tkinter import Tk, BOTH, Canvas

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

def main():
    win = Window(800, 600)
    win.wait_for_close()

if __name__ == "__main__":
    main()
