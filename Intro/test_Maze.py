import unittest
from Maze import Maze

class TestMaze(unittest.TestCase):
    def setUp(self):
        self.maze = Maze(5, 5)
        self.maze.start = (0, 0)
        self.maze.goal = (4, 4)
        self.maze.solution = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4)]
        self.maze.explored = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4)]

    def test_output_image_show_solution(self):
        self.maze.output_image("maze_solution.png", show_solution=True)
        # Add assertions to check if the image was created correctly

    def test_output_image_hide_solution(self):
        self.maze.output_image("maze_no_solution.png", show_solution=False)
        # Add assertions to check if the image was created correctly

    def test_output_image_show_explored(self):
        self.maze.output_image("maze_explored.png", show_explored=True)
        # Add assertions to check if the image was created correctly

    def test_output_image_hide_explored(self):
        self.maze.output_image("maze_no_explored.png", show_explored=False)
        # Add assertions to check if the image was created correctly

if __name__ == "__main__":
    unittest.main()
    import unittest
from Maze import Maze
from PIL import Image

class TestMaze(unittest.TestCase):
    def setUp(self):
        self.maze = Maze(5, 5)
        self.maze.start = (0, 0)
        self.maze.goal = (4, 4)
        self.maze.solution = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4)]
        self.maze.explored = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4)]

    def test_output_image_show_solution(self):
        self.maze.output_image("maze_solution.png", show_solution=True)
        image = Image.open("maze_solution.png")
        self.assertIsNotNone(image)
        # Add more assertions to check if the image was created correctly

    def test_output_image_hide_solution(self):
        self.maze.output_image("maze_no_solution.png", show_solution=False)
        image = Image.open("maze_no_solution.png")
        self.assertIsNotNone(image)
        # Add more assertions to check if the image was created correctly

    def test_output_image_show_explored(self):
        self.maze.output_image("maze_explored.png", show_explored=True)
        image = Image.open("maze_explored.png")
        self.assertIsNotNone(image)
        # Add more assertions to check if the image was created correctly

    def test_output_image_hide_explored(self):
        self.maze.output_image("maze_no_explored.png", show_explored=False)
        image = Image.open("maze_no_explored.png")
        self.assertIsNotNone(image)
        # Add more assertions to check if the image was created correctly

if __name__ == "__main__":
    unittest.main()