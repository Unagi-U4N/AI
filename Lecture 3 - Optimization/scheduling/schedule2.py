import itertools
import termcolor

"""
Advanced backtracking search with inference.
"""

VARIABLES = ["A", "B", "C", "D", "E", "F", "G"]
CONSTRAINTS = [
    ("A", "G"),
    ("A", "B"),
    ("A", "C"),
    ("B", "C"),
    ("B", "D"),
    ("B", "E"),
    ("C", "E"),
    ("C", "F"),
    ("D", "E"),
    ("E", "F"),
    ("E", "G"),
    ("F", "G")
]

count = 0

def backtrack(assignment, log=False):
    """Runs backtracking search to find an assignment."""

    global count

    # Check if assignment is complete
    if len(assignment) == len(VARIABLES):
        termcolor.cprint("\n+-------------------------------+\n      Assignment complete\n+-------------------------------+", "magenta")
        termcolor.cprint("Number of backtracks: " + str(count), "magenta")
        return assignment
    
    if log:
        count += 1
        print("\n+-------------------------------+\n     Number of backtracks:" , count, "\n+-------------------------------+")

    # Try a new variable
    var = select_unassigned_variable(assignment)
    for value in ["Monday", "Tuesday", "Wednesday"]:
        new_assignment = assignment.copy()
        new_assignment[var] = value
        if consistent(new_assignment):
            inference = INFERENCE(new_assignment, var, True)
            if inference is not None:
                new_assignment[inference[0]] = inference[1]
            result = backtrack(new_assignment, True)
            if result is not None:
                return result
    return None


def INFERENCE(assignment, var, log=False):
    """Runs forward checking to find an inference."""
    
    # Initialize known, triangle and domain
    known = []
    triangle = [var]
    termcolor.cprint("Variable to be infered: " + var, "yellow")

    Domain = ["Monday", "Tuesday", "Wednesday"]
    for (x, y) in CONSTRAINTS:

        # Get the other variables that are connected to the current one
        if x == var:
            triangle.append(y)
        elif y == var:
            triangle.append(x)

    print("Triangle: ", triangle)
    
    # Check if any triangle set is complete by iterating through all sets of 3 
    for subset in powerset(triangle):
        if len(subset) == 3:

            # If the subset is complete with values for each variable, add the variable into known and remove them from the triangle
            if subset[0] in assignment and subset[1] in assignment and subset[2] in assignment:
                for x in subset:
                    known.append(x)
                    triangle.remove(x)
        
    print("Triangle after filter: ", triangle)

    # Iterate through the triangle, If there's a value, remove it from the domain, remove the variable from the triangle
    
    new_triangle = triangle.copy()
    for z in triangle:
        if z in assignment and assignment[z] is not None:
            Domain.remove(assignment[z])
            known.append(z)
            new_triangle.remove(z)
            termcolor.cprint("\nremoved: "+ z + " --> " + assignment[z], "red")

    termcolor.cprint("\nRemaining domain: "+ str(Domain), "green")
    termcolor.cprint("Remaining triangle: "+ str(new_triangle), "green")
    termcolor.cprint("Known variables: "+ str(known), "cyan")

    # If there's only one value left in the domain and triangle, return it
    if len(Domain) == 1 and len(new_triangle) == 1:
        if log:
            print("New inference found: ", new_triangle[0], Domain[0])
        return (new_triangle[0], Domain[0])
    
    # Consider possible triangles, if variable in triangle has connections with 2 other variables
    for apex in new_triangle:
        
        termcolor.cprint("\nTesting apex: " + apex, "yellow")
        possible_triangle = []

        # For all the possible constraints, check if the apex has a connection with a known variable
        for (x, y) in CONSTRAINTS:

            if x == apex and y in known:
                possible_triangle.append((x, y))
            elif y == apex and x in known:
                possible_triangle.append((x, y))
            
        print("Possible triangle: ", possible_triangle)

        # If the apex has 2 connections, it fulfills the requirements for a triangle
        if len(possible_triangle) == 2:
            termcolor.cprint("Apex: " + str(apex) + " Connections: " + str(possible_triangle), "green")
            if log:
                print("New inference found: ", apex, Domain[0])
            return (apex, Domain[0])
        
        else:
            print("No connections found for: ", apex)

    return None
    

def powerset(s):
    """
    Return a list of all possible subsets of 3 of set s.
    """
    s = list(s)
    return list(itertools.combinations(s, 3))


def select_unassigned_variable(assignment):
    """Chooses a variable not yet assigned, in order."""
    for variable in VARIABLES:
        if variable not in assignment:
            return variable
    return None


def consistent(assignment):
    """Checks to see if an assignment is consistent."""
    for (x, y) in CONSTRAINTS:

        # Only consider arcs where both are assigned
        if x not in assignment or y not in assignment:
            continue

        # If both have same value, then not consistent
        if assignment[x] == assignment[y]:
            return False

    # If nothing inconsistent, then assignment is consistent
    return True


solution = backtrack(dict(), True)
print(solution)