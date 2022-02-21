"""
FILE:       project3.py
AUTHOR:      Miles Wyner, Jack Kaffenbarger
ASSIGNMENT:  Project 3: Genetic Programming
DATE:        April 16, 2021

Implements nodes for program trees and random initialization. More to come...
"""

import operator, random, math, heapq, copy, csv

MAX_FLOAT = 1e12

def safe_division(numerator, denominator):
    """Divides numerator by denominator. If denominator is close to 0, returns
    MAX_FLOAT as an approximate of infinity."""
    if abs(denominator) <= 1 / MAX_FLOAT:
        return MAX_FLOAT
    return numerator / denominator

def safe_exp(power):
    """Takes e^power. If this results in a math overflow, or is greater
    than MAX_FLOAT, instead returns MAX_FLOAT"""
    try:
        result = math.exp(power)
        if result > MAX_FLOAT:
            return MAX_FLOAT
        return result
    except OverflowError:
        return MAX_FLOAT

# Dictionary mapping function stings to functions that perform them
FUNCTION_DICT = {"+": operator.add,
                 "-": operator.sub,
                 "*": operator.mul,
                 "/": safe_division,
                 "exp": safe_exp,
                 "sin": math.sin,
                 "cos": math.cos}

# Dictionary mapping function strings to their arities (number of arguments)
FUNCTION_ARITIES = {"+": 2,
                    "-": 2,
                    "*": 2,
                    "/": 2,
                    "exp": 1,
                    "sin": 1,
                    "cos": 1}

# Perfectly generated data for training cases for the function
# x1^2 + log(sin(x2) + 2). Variable ranges determined from function graph.
TRAINING_CASES = []

x0vals = [-5, -3, -1, 0, 1, 3, 5]
x1vals = [-3.14, -2, -1, 0, 1, 2, 3.14]
for x0 in x0vals:
    for x1 in x1vals:
        y = (x0 * x0) + (math.log(math.sin(x1) + 2))
        TRAINING_CASES.append((y, x0, x1))


def set_global_training_cases(cases):
    """ easily change training cases. """
    TRAINING_CASES = cases
    return

FUNCTIONS = list(FUNCTION_DICT.keys())

# Strings for each variable
VARIABLES = ["x0", "x1"]


class TerminalNode:
    """Leaf nodes that contain terminals."""

    def __init__(self, value):
        """value might be a literal (i.e. 5.32), or a variable as a string."""
        self.value = value

    def __str__(self):
        return str(self.value)

    def eval(self, variable_assignments):
        """Evaluates node given a dictionary of variable assignments."""

        if self.value in VARIABLES:
            return variable_assignments[self.value]

        return self.value

    def tree_depth(self):
        """Returns the total depth of tree rooted at this node.
        Since this is a terminal node, this is just 0."""

        return 0

    def size_of_subtree(self):
        """Gives the size of the subtree of this node, in number of nodes.
        Since this is a terminal node, this is just 1."""

        return 1


class FunctionNode:
    """Internal nodes that contain functions."""

    def __init__(self, function_symbol, children):
        self.function_symbol = function_symbol
        self.function = FUNCTION_DICT[self.function_symbol]
        self.children = children

        assert len(self.children) == FUNCTION_ARITIES[self.function_symbol]

    def __str__(self):
        """This should make printed programs look like Lisp."""

        result = f"({self.function_symbol}"
        for child in self.children:
            result += " " + str(child)
        result += ")"
        return result

    def eval(self, variable_assignments):
        """Evaluates node given a dictionary of variable assignments."""

        try:
            # Calculate the values of children nodes
            children_results = [child.eval(variable_assignments) for child in self.children]

        except Exception:
            print("hit recursion depth limit, depth of self: ", self.program.tree_depth())
            raise

        # Apply function to children_results.
        return self.function(*children_results)

    def tree_depth(self):
        """Returns the total depth of tree rooted at this node."""

        return 1 + max(child.tree_depth() for child in self.children)

    def size_of_subtree(self):
        """Gives the size of the subtree of this node, in number of nodes."""

        return 1 + sum(child.size_of_subtree() for child in self.children)


class Individual:
    def __init__(self, program, error_vector, total_error, individual_probability):
        self.program = program
        self.error_vector = error_vector
        self.total_error = total_error
        self.individual_probability = individual_probability

    def find_error_vector(self):
        """ Updates error_vector to be a list of tuples containing
                1. case values in the form (y, x0, x1)
            and
                2. the error of the prog. on that case.'

            ex. ((25.692350536865362, 5, -3.14), 34.26096877503003) """

        for case in TRAINING_CASES:

            # assignments
            correct_error = case[0]
            assignments = {"x0": case[1], "x1": case[2]}

            # evaluation
            y = self.program.eval(assignments)
            error = abs(y - correct_error)

            # update vector
            self.error_vector.append((case, error))

        return

    def print_error_vector(self):
        """ Prints the error vector. """

        print("start error_vector")
        for case in self.error_vector:
            print(case)
        print("end error_vector")

    def find_total_error(self):
        """ Updates self.total_error to be total error of the program when run
        on all test cases. """

        for case in TRAINING_CASES:

            # assignments
            correct_error = case[0]
            assignments = {"x0": case[1], "x1": case[2]}

            # evaluation
            y = self.program.eval(assignments)
            self.total_error += abs(y - correct_error)

        return

    def print_total_error(self):
        """ Prints the total error. """

        print("total_error = ", self.total_error)
        return

    def __lt__(self, other):
        return self.individual_probability < other.individual_probability


def random_terminal():
    """Returns a random TerminalNode
    Half the time pick a random variable, and half the time a random float in
    the range [-10.0, 10.0]"""

    if random.random() < 0.5:
        terminal_value = random.choice(VARIABLES)
    else:
        terminal_value = random.uniform(-10.0, 10.0)

    return TerminalNode(terminal_value)


def generate_tree_full(max_depth):
    """Generates and returns a new tree using the Full method for tree
    generation and a given max_depth."""

    if max_depth <= 0:
        return random_terminal()

    function_symbol = random.choice(FUNCTIONS)
    arity = FUNCTION_ARITIES[function_symbol]
    children = [generate_tree_full(max_depth - 1) for _ in range(arity)]

    return FunctionNode(function_symbol, children)


def generate_tree_grow(max_depth):
    """Generates and returns a new tree using the Grow method for tree
    generation and a given max_depth."""

    ## What percent of the time do we want to select a terminal?
    percent_terminal = 0.25

    if max_depth <= 0 or random.random() < percent_terminal:
        return random_terminal()

    function_symbol = random.choice(FUNCTIONS)
    arity = FUNCTION_ARITIES[function_symbol]
    children = [generate_tree_grow(max_depth - 1) for _ in range(arity)]

    return FunctionNode(function_symbol, children)


def generate_random_program():
    """Creates a random program as a syntax tree.
    This uses Ramped Half-and-Half.
    max-depth taken from the range [2, 5] inclusive."""

    depth = random.randint(2, 5)
    if random.random() < 0.5:
        return generate_tree_full(depth)
    else:
        return generate_tree_grow(depth)


def read_data(filename, delimiter=",", has_header=True):
    """Reads classification data from a file.
    Returns a list of the header labels and a list containing each datapoint."""
    data = []
    header = []
    with open(filename) as f:
        reader = csv.reader(f, delimiter=delimiter)
        if has_header:
            header = next(reader, None)
        for line in reader:
            example = [float(x) for x in line]
            data.append(example)

        return header, data


def make_csv_training_cases():
    """Makes a list of training cases. Each training case is a dictionary
    mapping x_i and y to their values. x_i starts at x0.

    Example case: (hash value key, (y, x0, x1)}

    Right now, this is hard-coded to solve this problem:
    https://github.com/EpistasisLab/pmlb/tree/master/datasets/192_vineyard
    but it should be easy to adopt to other CSVs.
    """
    header, data = read_data("192_vineyard.tsv", "\t")
    cases = []

    for row in data:
        x0 = row[0]
        x1 = row[1]
        y = row[2]
        cases.append((y, x0, x1))

    return cases


def subtree_at_index(node, index):
    """Returns subtree at particular index in this tree. Traverses tree in
    depth-first order."""
    if index == 0:
        return node
    # Subtract 1 for the current node
    index -= 1
    # Go through each child of the node, and find the one that contains this index
    for child in node.children:
        child_size = child.size_of_subtree()
        if index < child_size:
            return subtree_at_index(child, index)
        index -= child_size
    return "INDEX {} OUT OF BOUNDS".format(index)


def replace_subtree_at_index(node, index, new_subtree):
    """Replaces subtree at particular index in this tree. Traverses tree in
    depth-first order."""
    # Return the subtree if we've found index == 0
    if index == 0:
        return new_subtree
    # Subtract 1 for the current node
    index -= 1
    # Go through each child of the node, and find the one that contains this index
    for child_index in range(len(node.children)):
        child_size = node.children[child_index].size_of_subtree()
        if index < child_size:
            new_child = replace_subtree_at_index(node.children[child_index], index, new_subtree)
            node.children[child_index] = new_child
            return node
        index -= child_size
    return "INDEX {} OUT OF BOUNDS".format(index)


def random_subtree(program):
    """Returns a random subtree from given program, selected uniformly."""
    nodes = program.size_of_subtree()
    node_index = random.randint(0, nodes - 1)
    return subtree_at_index(program, node_index)


def replace_random_subtree(program, new_subtree):
    """Replaces a random subtree with new_subtree in program, with node to
    be replaced selected uniformly."""
    nodes = program.size_of_subtree()
    node_index = random.randint(0, nodes - 1)
    new_program = copy.deepcopy(program)
    return replace_subtree_at_index(new_program, node_index, new_subtree)


def find_selection_probability(subpopulation):
    """ Takes a subset of individuals in a population, updates their
    probabilities of being selected for parent selection within the
    given subset of the population. """

    # find total fitness plus needed for finding probability of selection
    total_fitness_plus = 0
    for individual in subpopulation:
        total_fitness_plus += 1 / individual.total_error

    for individual in subpopulation:
        fitness_plus = 1 / individual.total_error
        individual.individual_probability = fitness_plus / total_fitness_plus

    return


def bloat_controlled_selection_probability(subpopulation):
    """ Takes a subset of individuals in a population, updates their
    probabilities of being selected for parent selection within the
    given subset of the population. Takes into account both error and size of
    program, where both are calculated in the same way fitness+ works; we now
    use size+ and fitness+ combined. """

    total_fitness_plus = 0
    total_program_size = 0

    for individual in subpopulation:
        total_program_size += individual.program.size_of_subtree()
        total_fitness_plus += 1 / individual.total_error

    for individual in subpopulation:
        fitness_plus = 1 / individual.total_error / total_fitness_plus
        size_plus = 1 / individual.program.size_of_subtree() / total_program_size
        individual.individual_probability = fitness_plus + (1 * size_plus)

    return


def tournament_selection(population, pop_size):
    """ Takes a population of individuals and returns the most fit parent
    out of a random subset of that population. """

    # Select a subset of population for parent selection
    parent_subset_size = pop_size // 25
    parent_subset = random.sample(population, parent_subset_size)

    # CHOOSE ONE:
    # find_selection_probability(parent_subset)
    bloat_controlled_selection_probability(parent_subset)

    parent = max(parent_subset)
    parent = copy.deepcopy(parent)

    return parent

def check_different_parents(parent1, parent2):
    """ returns bool, true if parents equal """
    return parent1 == parent2

def crossover(population, pop_size):
    """ Takes two parents, replaces a random subtree from one at a random node
    in the other. returns the new child created. """

    # initialize parents
    parent1 = tournament_selection(population, pop_size)
    parent2 = tournament_selection(population, pop_size)

    # replace random subtree from one parent at a random node in the other
    subtree = random_subtree(parent2.program)
    new_program = replace_random_subtree(parent1.program, subtree)

    # generate a next generation individual
    child = Individual(new_program, error_vector = [], total_error = 0, individual_probability = 0)
    return child


def size_fair_crossover(population, pop_size):
    """ Takes two parents, replaces a random subtree with size S from one parent
    with a random subtree from the other parent with a similar size. Returns
    the new child created. """

    # initialize parents
    parent1 = tournament_selection(population, pop_size)
    parent2 = tournament_selection(population, pop_size)

    # prevent incest
    while check_different_parents(parent1, parent2):
        parent2 = tournament_selection(population, pop_size)

    # generate a random index
    index_to_replace = random.randint(0, parent1.program.size_of_subtree() - 1)

    # find the size of the subtree at that index in parent1
    subtree_size = subtree_at_index(parent1.program, index_to_replace).size_of_subtree()
    lower_bound = subtree_size // 2
    upper_bound = 3 * subtree_size // 2

    # find a random subtree from parent2 where the size falls inbounds
    new_subtree = None
    if parent2.program.size_of_subtree() < lower_bound:
        new_subtree = parent2.program

    while new_subtree == None:
        temp_subtree = random_subtree(parent2.program)
        if lower_bound <= temp_subtree.size_of_subtree() <= upper_bound:
            new_subtree = temp_subtree

    # replace the subtree found in parent2 at the index generated for in parent1
    new_program = replace_subtree_at_index(parent1.program, index_to_replace, new_subtree)
    child = Individual(new_program, error_vector = [], total_error = 0, individual_probability = 0)

    return child


def mutation(population, pop_size):
    """ Takes random program, generates a new random subtree within that has
    depth not exceeding max depth of original program. """

    # initialize parent
    parent = tournament_selection(population, pop_size)

    subtree = generate_tree_grow(random.randint(1, 3))
    new_program = replace_random_subtree(parent.program, subtree)
    child = Individual(new_program, error_vector = [], total_error = 0, individual_probability = 0)

    return child


def run_GP(population, population_size):
    """ Main algorithm for GP. Iterate over generations, mutating and crossing
    some of the best programs at each generation. """
    gen_count = 30
    best_individuals = []
    find_selection_probability(population)
    curr_best = copy.deepcopy(max(population))
    improvement_count = 0

    while gen_count > 0:

        next_gen = []
        max_depth = 0
        max_depth_individual = None
        best_total_error_programs = []
        best_bloat_controlled_programs = []
        max_depth_individuals = []

        for _ in range(population_size):

            # choose mutation or crossover
            choice = random.randint(1, 10)
            if choice < 3:
                next_gen_ind = mutation(population, population_size)
            elif choice == 9:
                next_gen_ind = size_fair_crossover(population, population_size)
            else:
                next_gen_ind = crossover(population, population_size)

            # initialize error values for new individual
            next_gen_ind.find_error_vector()
            next_gen_ind.find_total_error()

            # keep track of max_depth individual
            if next_gen_ind.program.tree_depth() > max_depth:
                max_depth = next_gen_ind.program.tree_depth()
                max_depth_individual = next_gen_ind

            # add new individual to new population
            next_gen.append(next_gen_ind)

        # Track best program in every generation relative to only fitness+
        find_selection_probability(next_gen)
        best_total_error = max(next_gen)
        best_total_error_programs.append(best_total_error)


        # Track the number of generations where best prog improves (total error)
        if best_total_error.total_error < curr_best.total_error:
            improvement_count += 1
            curr_best.total_error = best_total_error.total_error

        # Track best program in every generation relative to fitness+ + size+
        bloat_controlled_selection_probability(next_gen)
        best_error_and_size = max(next_gen)
        best_bloat_controlled_programs.append(best_error_and_size)

        max_depth_individuals.append(max_depth_individual)

        # Print out information about each generation
        print("Generation ", gen_count)
        print("Lowest total error of any program: ", best_total_error.total_error,
              ", which has program size ", best_total_error.program.size_of_subtree())
        print("Greatest max depth of any ind in generation: ", max_depth)

        # If size+ influences most fit program, show the other program that is
        # best by its fitness+ and size+
        if best_total_error.program.size_of_subtree() != best_error_and_size.program.size_of_subtree():
            print("ATTENTION: interesting program found.")
            print("Lowest total error with size considered of any program: ",
                   best_error_and_size.total_error,
                  ", which has program size ", best_error_and_size.program.size_of_subtree())

        # update our population and generation count
        population = next_gen
        gen_count -= 1


    # Show the best programs in the of all genetics created
    print("Best overall program error: ", max(best_total_error_programs).total_error)
    print("Best overall program size: ", max(best_total_error_programs).program.size_of_subtree())
    # print("Best program based on total_error and size: ", max(best_bloat_controlled_programs).program)
    print("Number of generations seeing improvement: ", improvement_count, "/ 30")

    return best_individuals


def main():
    """ Call GP here."""
    # Initializes a population
    population = []
    population_size = 750
    for _ in range(population_size):
        random_program = generate_random_program()
        new_ind = Individual(random_program, error_vector = [], total_error = 0, individual_probability = 0)
        new_ind.find_error_vector()
        new_ind.find_total_error()
        population.append(new_ind)

    # determine training cases to be used for GP. If set_global_training_cases
    # not called, training cases are defined at the top for global manipulation
    TRAINING_CASES = make_csv_training_cases()

    run_GP(population, population_size)

    find_selection_probability(population)
    print("Best inital program error: ", max(population).total_error)
    print("Best inital program size: ", max(population).program.size_of_subtree())




if __name__ == "__main__":
    main()
