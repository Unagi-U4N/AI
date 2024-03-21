import sys
import copy
from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword

        # Create dicionary with keys: variable, values: all the values in the vocabulary
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        self.new_domains = copy.deepcopy(self.domains)

        # Compare the length of the variables with the words in domain
        for var in self.crossword.variables:
            length = var.length
            
            # Iterate through all the words in the variable
            for words in self.domains[var]:
                if len(words) != length:
                    self.new_domains[var].remove(words)

        self.domains = self.new_domains
        # print(self.domains)

        # raise NotImplementedError


    def revise(self, x, y, log=False):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        
        revision = False

        # Check if there is a intersection between both variables (Only one intersection for each set of variables)
        intersection = None
        if (x, y) in self.crossword.overlaps:
            if self.crossword.overlaps[x, y] is not None:
                intersection = self.crossword.overlaps[x, y]
        elif (y, x) in self.crossword.overlaps:
            if self.crossword.overlaps[y, x] is not None:
                intersection = self.crossword.overlaps[y, x]
        
        if log:
            if intersection is not None:
                print("\nInspecting intersection:", intersection, "between", x, "and", y)

        self.new_domains = copy.deepcopy(self.domains)
        # Loop over all the overlaps, for all the words in x and y
        if intersection is not None:
            
            # Convert the intersection to a list
            intersection = list(intersection)

            # Get the values of i, j
            i = intersection[0]
            j = intersection[1]

            for wordsx in self.domains[x]:
                    
                # For words in x, if any words in y satisfy the condition, continue
                if any(wordsx[i] == wordsy[j] for wordsy in self.domains[y]):
                    continue
                else:
                    self.new_domains[x].remove(wordsx)
                    revision = True
                    print("Removed:", wordsx, "from", x, "because (", wordsx[i], ") does not match any words in", self.domains[y])
                    continue

            self.domains = self.new_domains
            print(self.domains)

        return revision
    
        raise NotImplementedError


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        print("Going through ac3 algorithm...")

        # If arcs is None, begin with initial list of all arcs in the problem
        if arcs is None:
            arcs = []
            print("Nothing in arcs, creating new arcs\n\n+----------------------------------+\n")
            for x in self.crossword.variables:
                for y in self.crossword.variables:

                    # If x and y are not the same
                    if x != y:
                        arcs.append((x, y))

        # Loop over all the arcs
        # queue = arcs
        print("Arcs in queue:", len(arcs))
        index = 0

        while len(arcs) != 0:
            index += 1
            x, y = arcs.pop(0)
            print("Arcs pair" , index , "-->" , "Arcx" , x , "Arcy" , y)
            # If revise is True, append the new arcs to the queue
            if self.revise(x, y, log=True):
                if len(self.domains[x]) == 0:
                    return False
                
                # Get the neighbor arcs of var z
                count = 0
                for z in self.crossword.neighbors(x):    
                    count = 0
                    arcs.append((z, x))
                    count += 1
                    
                if count != 0:
                    print("Revision occured, adding" , count , "to the queue")
        
        return True
    
        raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        for var in assignment:
            if assignment[var] is not None:
                return True
        
        return False
            

        raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        for var in assignment:
            if len(assignment[var]) == var.length:
                for othervar in assignment:
                    if assignment[var] == assignment[othervar]:
                        return False
                
                return True
        
        return False
        
        raise NotImplementedError

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        degree = []

        # Get a list of overlapping variables
        self.overlaps = self.crossword.neighbors(var)

        # Get all the pairs of variable that overlaps
        for (x, y) in self.overlaps:

            # If overlap pairs exits, and they are in the main overlap group, reorder the pairs
            if [x, y] or [y, x] in self.crossword.overlaps:
                if [y, x] in self.crossword.overlaps:
                    x, y = y, x
                
                # For all the overlap (i, j) in the pairs
                for overlaps in self.crossword.overlaps[x, y]:
                    overlaps = list(overlaps)
                    i = overlaps[0]
                    j = overlaps[1]

                    for wordsx in assignment[x]:
                        n = 0
                        
                        # Check how many times a character in var y at index "j" is not equal to a character in var x at index "i" 
                        for wordsy in assignment[y]:
                            if wordsy[j] != wordsx[i]:
                                n += 1
                    
                        degree.append((wordsx, n))

        sorted(degree, key=lambda word: word[1])
        return degree           
                        
        raise NotImplementedError
    

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        
        remain = []
        degree = []

        # For all the variables not in assignment, append remaining values in domain and the degree
        print("Variables not in assignment:")
        for var in self.crossword.variables:
            if var not in assignment:
                print(var)
                num_of_words = len(self.domains[var])
                remain.append([var, num_of_words])
                degree.append([var, len(self.crossword.neighbors(var))])

        # Set the lowest value and highest degree, Get a list of minimum value or maximum degree if more than 1
        lowest = min(remain, key=lambda words: words[1])[1]
        highest = max(degree, key=lambda words: words[1])[1]
        min_remain = [[k, v] for k, v in remain if v==lowest]
        max_degree = [[k, v] for k, v in degree if v==highest]
        print("Minimum of remains:", min_remain)
        print("Maximum of degrees:", max_degree)

        # If there is more than 1 minimum value, check for the maximum degree, else return the first value(only value)
        if len(min_remain) > 1:

            # If there is more than 1 maximum degree, return a random one(first value in maximum degree), else return the first value(only value)
            if len(max_degree) > 1:
                choice =  max_degree[0][0]
            choice =  max_degree[0][0]
        choice = min_remain[0][0]

        print("Choice:", choice)
        return choice
    
        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        # If the assignment is complete, return the assignment
        if self.assignment_complete(assignment):
            return assignment
        
        # Select an unassigned variable
        var = self.select_unassigned_variable(assignment)

        # For the selected variable, order the domain values
        for value in self.domains[var]:
            print("Testing value:" , value)
            new_assignment = copy.deepcopy(assignment)
            new_assignment[var] = value
            print("New assignment:", new_assignment)

            # If the assignment is consistent, continue with the assignment
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
        return None
    
        raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
