class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier():

    '''StackFrontier class to store the nodes in the frontier
       first in last out'''
    
    def __init__(self):
        self.frontier = []
    
    def add(self, node):
        self.frontier.append(node)
    
    def contains_state(self, state):
        # check if the state given from the parameter is equal to the state of the node ("node.state") from the frontier list
        return any(node.state == state for node in self.frontier)
    
    def empty(self):
        return len(self.frontier) == 0
    
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1] # get the last node from the list
            self.frontier = self.frontier[:-1] # update the list by removing the last node
            return node
        
class queueFrontier(StackFrontier):
    
    '''QueueFrontier class to store the nodes in the frontier
       first in first out'''
    
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0] # get the first node from the list
            self.frontier = self.frontier[1:] # update the list by removing the first node
            return node


class maze():
    def __init__(self, filename):

        # Read the maze from a file and set the height and width
        with open(filename) as f:
            contents = f.read()

        # Validate start and goal 
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")
        
        # Determine height and width of maze
        contents = contents.splitlines() # split the contents into lines
        self.height = len(contents)
        self.width = max(len(line) for line in contents) # get the maximum length (char) of the lines

        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    # (i, j) is (x, y) coordinate
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        '''example of the maze translated to a list of lists

        #####B#              [[False, False, False, False, False, False, False],
        ##### #               [False, False, False, False, False, True, False],
        ####  #               [False, False, False, False, True, True, False],
        #### ##      -->      [False, False, False, False, True, False, False],
             ##               [True, True, True, True, True, False, False],
        A######               [False, False, False, False, False, False, False]]
        
        '''
        self.solution = None
        
    def print(self):
        # if the self.solution is not None, then the solution is the second element of the tuple "only the coords", if the self.solution is None, then the solution is None
        solution = self.solution[1] if self.solution is not None else None # self.solution[1] = (i,j)
        print()
        for x in range(len(solution)):
            print("Step", x+1, end=": ")
            print("Go", self.solution[0][x])
            print()
            for i, row in enumerate(self.walls):
                for j, col in enumerate(row):
                    if col: # if the col is True, then print a wall
                        print("█", end="")
                    elif (i, j) == self.start:
                        print("A", end="")
                    elif (i, j) == self.goal and x != len(solution) - 1:
                        print("B", end="")
                    elif solution is not None and (i, j) in solution and solution.index((i, j)) == x:
                        print("*", end="")
                    else:
                        print(" ", end="")
                print()
            print()

        # iterate through the maze (every row and col) and print the maze
        print("Solution: \n")
        for i, row in enumerate(self.walls): # i is the index of the row, row is the list of the row
            for j, col in enumerate(row): # j is the index of the col, col is the boolean value of the col
                if col: # if the col is True, then print a wall
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()
        print(self.num_explored, "steps")

    def neighbors(self, state):
        row, col = state

        # All possible actions
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        # Ensure the actions are valid
        result = []
        for action, (r, c) in candidates: # iterate through the candidates
            try:
                if not self.walls[r][c]: # if the candidate is not a wall "True"
                    result.append((action, (r, c))) # append the action and the coordinates to the result list
            except IndexError:
                continue
        return result
    
    def solve(self):
        """Finds a solution to maze, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start) # add the start node to the frontier

        # Initialize an empty explored set
        self.explored = set()

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            # If node is the goal, then we have a solution
            if node.state == self.goal:
                actions = []
                cells = []

                # Follow parent nodes to find the solution
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:

                    # create a new node named child with the state as correct state after neigbour checking, parent as the current node, and action from the neighbour checking
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)
                    draw.rectangle(
                        ([(j * cell_size, i * cell_size), ((j + 1) * cell_size, (i + 1) * cell_size)]),
                        fill=fill
                    )

                # Start
                if (i, j) == self.start:
                    fill = (255, 0, 0)
                    draw.rectangle(
                        ([(j * cell_size + cell_border, i * cell_size + cell_border), ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                        fill=fill
                    )

                # Goal
                if (i, j) == self.goal:
                    fill = (0, 171, 28)
                    draw.rectangle(
                        ([(j * cell_size + cell_border, i * cell_size + cell_border), ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                        fill=fill
                    )

                # Solution
                if solution is not None and (i, j) in solution:
                    fill = (220, 235, 113)
                    draw.rectangle(
                        ([(j * cell_size + cell_border, i * cell_size + cell_border), ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                        fill=fill
                    )

                # Explored
                if show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)
                    draw.rectangle(
                        ([(j * cell_size + cell_border, i * cell_size + cell_border), ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                        fill=fill
                    )

game = maze("maze1.txt")
game.solve()
game.print()
game.output_image("maze1.png", show_explored=True)

