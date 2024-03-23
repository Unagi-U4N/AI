import sys
import copy
from crossword import *

class CrosswordCreator():

    def __init__(self, crossword, log):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.log = log

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
        self.ac3(log=self.log)
        if self.log:
            print("\n\nProceeding with backtracking...")
        self.test = 0
        return self.backtrack(dict(), log=self.log)

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
        xindex = self.getvarname(x, self.arcname)
        yindex = self.getvarname(y, self.arcname)

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
                print("\n+-------------------------------------------------------+")
                print("\nIntersection", intersection, "found between", xindex, "and", yindex)

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
                    if log:
                       print("No revision needed")
                    continue
                else:
                    self.new_domains[x].remove(wordsx)
                    revision = True
                    if log:
                        print("Removed:", wordsx, "from", xindex, "because (", wordsx[i], ") does not match any words in", self.domains[y])
                    continue

            self.domains = self.new_domains
            if revision:
                if log:
                    print("\nRevision occured:")
                    for var in self.domains:
                        print(self.getvarname(var, self.arcname), self.domains[var])
                
        return revision
    
        raise NotImplementedError

    
    def getvarname(self, var, arcname):
        """
        Get the name of the variable from the arcname list
        """
        for arc in arcname:
            if arc[1] == var:
                return arc[0]
        return None
    
        
    def ac3(self, arcs=None, log=False):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if log:
            print("Going through ac3 algorithm...")
        index = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

        # If arcs is None, begin with initial list of all arcs in the problem
        if arcs is None:

            # Keep track of all the arcs and its index
            arcs = []
            self.arcname = []
            count = 0

            if log:
                print("Nothing in arcs, creating new arcs\n\n+----------------------------------+\n\nVariables to be considered:")
            for x in self.crossword.variables:
                if log:
                    print(index[count], x)
                self.arcname.append([index[count], x])
                count += 1
                for y in self.crossword.variables:

                    # If x and y are not the same
                    if x != y:
                        arcs.append((x, y))

        # Loop over all the arcs
        # queue = arcs
        if log:
            print("\n+----------------------------------+\n")
            print("Arcs in queue:", len(arcs))
        index = 0

        while len(arcs) != 0:
            index += 1
            x, y = arcs.pop(0)

            # # Get the index of x and y in the arcname list
            # xindex = self.getvarname(x, self.arcname)
            # yindex = self.getvarname(y, self.arcname)
            
            # print("Arcs pair" , index , "-->" , "Arc" + xindex , "Arc" + yindex)

            # If revise is True, append the new arcs to the queue
            if self.revise(x, y, log=self.log):
                if len(self.domains[x]) == 0:
                    return False
                
                # Get the neighbor arcs of var z
                count = 0
                for z in self.crossword.neighbors(x):    
                    count = 0
                    arcs.append((z, x))
                    count += 1
                    
                if count != 0:
                    if log:
                        print("\nAdding" , count , "to the queue")
        
        return True
    
        raise NotImplementedError

    def assignment_complete(self, assignment, log=False):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """ 
        if log:
            print("\nChecking if assignment is complete...")

        # If any value in the assignment is None, or the length of the assignment is not equal to the length of the variables, return False
        if any(val is None for val in assignment.values()) or len(assignment) != len(self.crossword.variables):
            if log:
                print("Assignment is not complete")
            return False
        
        if log:
            print("Assignment is complete")
        return True
            

        raise NotImplementedError

    def consistent(self, assignment, log=False):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        if log:
            print("\nChecking consistency...")

        for var in assignment:

            # Get the length of the variable
            if var in self.crossword.variables:
                length = var.length
            
            # If the length of the variable is equal to the length of the word
            if len(assignment[var]) == length:
                if log:
                    print("Valid case --> Length of", assignment[var], "is equal to", length)

                # If the number of variables in the assignment is more than 1, can compare the words
                if len(assignment) > 1:
                    for othervar in assignment:
                        if othervar != var:
                            word0 = assignment[var]
                            word1 = assignment[othervar]
                            # Check if the words are equal
                            if word0 == word1:
                                if log:
                                    print("Invalid case --> Words", word0, "are repeated")
                                    print("Assignment is not consistent")
                                return False
                            
                            # Check if the characters match at the intersection
                            if (var, othervar) in self.crossword.overlaps:
                                if self.crossword.overlaps[var, othervar] is not None:
                                    intersection = self.crossword.overlaps[var, othervar]
                                    i = intersection[0]
                                    j = intersection[1]

                                    if word0[i] != word1[j]:
                                        if log:
                                            print("Invalid case --> Words", word0, "and", word1, "do not match at intersection", i, j)
                                            print("Assignment is not consistent")
                                        return False
                                
                            elif (othervar, var) in self.crossword.overlaps:
                                if self.crossword.overlaps[othervar, var] is not None:
                                    intersection = self.crossword.overlaps[othervar, var]
                                    i = intersection[0]
                                    j = intersection[1]

                                    if word0[i] != word1[j]:
                                        if log:
                                            print("Invalid case --> Words", word0, "and", word1, "do not match at intersection", i, j)
                                            print("Assignment is not consistent")
                                        return False
                
                continue

            if log:
                print("Invalid vase --> Length of", assignment[var], "is not equal to", length)
            return False

        if log:
            print("Assignment is consistent")
        return True
        
        raise NotImplementedError

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        degree = {
            word: 0
            for word in self.domains[var]
        }

        # Get a list of overlapping variables
        self.overlaps = self.crossword.neighbors(var)

        # Get all the pairs of variable that overlaps
        for y in self.overlaps:

            # If overlap pairs exits
            if (var, y) in self.crossword.overlaps:
                if self.crossword.overlaps[var, y] is not None:
                    intersection = self.crossword.overlaps[var, y]
            elif (y, var) in self.crossword.overlaps:
                if self.crossword.overlaps[y, var] is not None:
                    intersection = self.crossword.overlaps[y, var]

            # Get the values of i, j
            i = intersection[0]
            j = intersection[1]

            # Get the number of words that can be ruled out
            for word in self.domains[var]:
                for word1 in self.domains[y]:
                    if word == word1 or (word in assignment.values() or word1 in assignment.values()):
                        continue
                    if word[i] != word1[j]:
                        degree[word] += 1


        degreeofval = [[word, degree[word]] for word in self.domains[var]]
        sorted(degreeofval, key=lambda word: word[1])
        return [word[0] for word in degreeofval]       
                        
        raise NotImplementedError
    

    def select_unassigned_variable(self, assignment, log=False):
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
        if log:
            print("\nVariables not in assignment:")
        for var in self.crossword.variables:
            if var not in assignment:
                varname = self.getvarname(var, self.arcname)
                if log:
                    print(varname, var, self.domains[var])
                num_of_words = len(self.domains[var])
                remain.append([var, num_of_words])
                degree.append([var, len(self.crossword.neighbors(var))])

        # Set the lowest value and highest degree, Get a list of minimum value or maximum degree if more than 1
        lowest = min(remain, key=lambda words: words[1])[1]
        highest = max(degree, key=lambda words: words[1])[1]
        min_remain = [[k, v] for k, v in remain if v==lowest]
        max_degree = [[k, v] for k, v in degree if v==highest]
        if log:
            print("\n") 
        # print("Minimum of remains:", min_remain)
        # print("Maximum of degrees:", max_degree)

        # If there is more than 1 minimum value, check for the maximum degree, else return the first value(only value)
        if len(min_remain) > 1:

            # If there is more than 1 maximum degree, return a random one(first value in maximum degree), else return the first value(only value)
            if len(max_degree) > 1:
                if log:
                    print("Returning choice:", self.getvarname(max_degree[0][0], self.arcname))
                return max_degree[0][0]
            if log:
                print("Returning choice:", self.getvarname(max_degree[0][0], self.arcname))
            return max_degree[0][0]
        if log:
            print("Returning choice:", self.getvarname(min_remain[0][0], self.arcname))
        return min_remain[0][0]
    
        raise NotImplementedError

    def backtrack(self, assignment, log=False):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        if log:
            print("Backtracking...")

        # If the assignment is complete, return the assignment
        if self.assignment_complete(assignment, log=self.log):
            if log:
                print("Complete assignment: ")
                for var in assignment:
                    print(var, "-->", assignment[var])
            print("Number of tests:", self.test)
            return assignment
        
        # Select an unassigned variable
        var = self.select_unassigned_variable(assignment, log=self.log)

        # For the selected variable, order the domain values
        for value in self.order_domain_values(var, assignment):
            if log:
                print("Testing value:" , value)
            self.test += 1
            new_assignment = copy.deepcopy(assignment)
            new_assignment[var] = value
            if log:
                print("New assignment:", new_assignment)

            # If the assignment is consistent, continue with the assignment
            if self.consistent(new_assignment, log=self.log):
                result = self.backtrack(new_assignment, log=self.log)
                if result is not None:
                    return result
        return None
    
        raise NotImplementedError


def main(): 

    # Check usage
    if len(sys.argv) not in [5, 6]:
        sys.exit("Length not satisfied\nUsage: python generate1.py structure words [number of times] [log(T/F)] [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    times = int(sys.argv[3])
    log = sys.argv[4]
    output = sys.argv[5] if len(sys.argv) == 6 else None

    # Generate crossword
    assignmentlist = []

    # Solve the crossword, if a solution is found, if the solution is not already in the list, append it to the list
    print("Solving...")
    for x in range(times):
        crossword = Crossword(structure, words)

        if log == "T":
            creator = CrosswordCreator(crossword, log=True)
        elif log == "F":
            creator = CrosswordCreator(crossword, log=False)
        else:
            sys.exit("Usage: python generate1.py structure words [number of times] [log(T/F)] [output]")
        
        assignment = creator.solve()
        if assignment is not None:
            if assignment not in assignmentlist:
                print("New solution found")
                assignmentlist.append(assignment)
            else:
                print("Solution already found")
        else:
            print("No solution found")

    # Print result
    if assignmentlist is None:
        print("No solution.")
    else:
        print("Solutions found:", len(assignmentlist))
        for x in assignmentlist:
            creator.print(x)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
