"""
 *****************************************************************************
   FILE:        grids.py

   AUTHOR:      Jack Kaffenbarger   

   ASSIGNMENT:  grids.py

   DATE:        9/30/18

   DESCRIPTION: Program that searches a given input for a target, replaces the
   target with 0's, and adds together numbers in a given direction from the 
   target numbers.

 *****************************************************************************
"""

from professors import input_data

# Complete these functions.  Don't change the headers (def line:
# function names and parameters) or the docstrings. The program is
# already designed to use these.

def locate_target(grid, target):
    """ Return a list of the locations (tuples) of target within grid. """
    location_list = []
    
    # Searches the given grid for a target, and if found adds its position as
    # a tuple to a list.
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == target:
                location_list.append((i, j))

    return location_list

def is_in_bounds(grid, loc_tuple):
    """ Return True if loc_tuple is a legal position within grid.
        Return False otherwise. """

    # For convenience, get the grid size (all grids are square), and pull
    # apart the given loc_tuple:
    
    # Simple boolean statement that checks if a given tuple is within the 
    # appropriate range.
    return bool(
        (0 <= loc_tuple[0] < len(grid)) and (0 <= loc_tuple[1] < len(grid)))

def sum_all_neighbors(grid, location_list, direction):
    """ For each location in location_list, determine its neighbor in the 
        given direction, if it exists.  Return the sum of all such 
        neighbors. """
    
    directions = [(-1, 0), (-1, 1), (0, 1), (1, 1),
                  (1, 0), (1, -1), (0, -1), (-1, -1)]
    
    # Converting the inputted direction to a useable tuple to add to the 
    # location list.
    position = directions[direction]
    neighbor_sum = 0
    
    # Loop that runs through the location list, and if the 'neighbor' 
    # exists it adds to a running sum.
    for loc in location_list:
        #CITE: TA Minh.
        #DESC: Helped me pass a tuple and not an int.
        if is_in_bounds(grid, (position[0] + loc[0], position[1] + loc[1])):
            neighbor_sum = neighbor_sum + \
            grid[position[0] + loc[0]][position[1] + loc[1]]

    return neighbor_sum

def print_zero_grid(grid, location_list):
    """ Prints the grid with each entry at the locations in location_list
        replaced by the digit 0. Does not actually modify grid.  
        The output should be in square form, each number in a row followed by
        a space, and each row terminated with a newline. """
    
    # The below loops print out the old list, but when it finds a target it 
    # prints a '0' in it's place.
    new_grid = ''
    for i in range(len(grid)):
        for j in range(len(grid)):
            #CITE: TA Colleen
            #DESC: Helped me make use of the if in loop to search a list of 
            # tuples.
            if (i, j) in location_list:
                new_grid = new_grid + '0' + ' '
            else: 
                new_grid = new_grid + str(grid[i][j]) + ' '
        #CITE: TA Minh
        #DESC: Helped me utilize both the inner and outer loop to print the list
        # in the desired format.
        print(new_grid)
        new_grid = ''
    
    #CITE: TA Roger
    #DESC: Helped me make sense of the error I was getting for the final test of 
    # grids, and find a clever way around it.
    if new_grid == '':
        return None
    return new_grid
       
#######################################
#    DO NOT MODIFY BELOW THIS POINT   #
#######################################    

def main():
    """ The main function. """

    # Do not modify this function
    
    grid, target, direction = input_data()

    # Request a list of all locations of target in the given_grid:
    location_list = locate_target(grid, target)

    # Print the grid with each instance of target replaced by a zero:
    print_zero_grid(grid, location_list)

    # Print the location list
    for entry in location_list:
        print(entry)

    # Request the sum of neighbors of those locations in direction:
    neighbor_sum = sum_all_neighbors(grid, location_list, direction)
    print(neighbor_sum)


        
if __name__ == '__main__':
    main()
