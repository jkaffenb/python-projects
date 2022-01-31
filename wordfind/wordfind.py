"""
 *****************************************************************************
   FILE:        wordfind.py

   AUTHOR:      Jack Kaffenbarger 

   ASSIGNMENT:  wordfind.py

   DATE:        10/2/18

   DESCRIPTION: Program that takes a grid and a list of words, and searches 
   the grid for instances of each word, and capitalizes them if found.

 *****************************************************************************
"""


def printGrid(grid):
    """ Display the grid in a nice way """
    for row in grid:
        print(row)


def wordcap(grid, locations):
    """ Capitalize found list of locations """
    
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if (row, col) in locations:
                grid[row][col] = grid[row][col].upper()
            
    return grid


def wordcaplocations(starting_position, dr, dc, word):
    """ Finds all the locations of letters that need to be capitalized """
    
    #Set list and starting stop
    cap_lst = [starting_position]
    shifted_row = starting_position[0] 
    shifted_col = starting_position[1] 

    for _ in range(len(word[1:])):
        # Loops down the desired direction for all letters excluding the 
        # starting one
        shifted_row = shifted_row + dr
        shifted_col = shifted_col + dc
        cap_lst.append((shifted_row, shifted_col))
    return cap_lst


def is_in_bounds(grid, loc_tuple):
    """ Return True if loc_tuple is a legal position within grid.
        Return False otherwise. """

    # Boolean statement that checks if a given tuple is within the 
    # appropriate range.
    return bool(
        (0 <= loc_tuple[0] < len(grid)) and (0 <= loc_tuple[1] < len(grid[0])))


def firstletterloc(grid, word):
    """ Find location of first letters """
    lst = []

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if word[0] == grid[row][col]:
                lst.append((row, col))
    return lst
        

def pattern_search_at_in(grid, word, start_row, start_col, dr, dc):
    """ Searches the entire length of a word in a given direction """
    #CITE: Class connect four example

    current_row = start_row
    current_col = start_col
    # For each position of the word, 
    for i in range(len(word)):
        # verify we are still on the board,
        if current_row < 0 or current_row >= len(grid) or \
           current_col < 0 or current_col >= len(grid[0]):
            return None
        # and that the board element matches the pattern element
        if grid[current_row][current_col] != word[i]:
            return None
        # move on to the next position on the board
        current_row = current_row + dr
        current_col = current_col + dc
    return wordcaplocations((start_row, start_col), dr, dc, word)
    #return ((start_row, start_col), (dr, dc))

def pattern_search_at(grid, word, start_row, start_col):
    """ Search for word in every direction (dr, dc) beginning at a given 
        starting position.  If found, return (start_row, start_col, dr, dc).
        Otherwise, return None """
    #CITE: Class connect four example
    
    # for each possible direction,
    for direction in [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
        # extract the dr and dc components, and
        dr = direction[0]
        dc = direction[1]
        # try to search for the pattern at the given start position 
        # and moving in that direction.
        result = pattern_search_at_in(grid, word, start_row, start_col, dr, dc)
        # if that search is successful, return its result
        if result is not None:
            return result
    # if no direction search was successful, return None.
    return None


def pattern_search(grid, word):
    """ Search every starting location for word. If we find it, 
        return information about where it is found: 
        (start_row, start_col, dr, dc).  Otherwise, return None."""
    #CITE: Class connect four example

    # get the possible starting positions by using the firstletterloc
    # function written for the grids project.  This will yield a list
    # of tuples representing grid positions, where the first item in the
    # word can be found.
    starting_positions = firstletterloc(grid, word)

    # for each of these tuples,
    for start_pos in starting_positions:
        # extract its row and column components, and
        start_row = start_pos[0]
        start_col = start_pos[1]
        # try to search for the pattern at the given start position.
        result = pattern_search_at(grid, word, start_row, start_col)
        # if that search is successful, return its result
        if result is not None:
            return result
    # if no starting position search was successful, return None
    return None
    

def wordfind(grid, words):
    """ For each word in words, if possible, find it once in the grid, case 
        insensitive.  Convert those found letters in the grid 
        to upper-case."""
    
    # appending all the locations of words that need to be capitalized
    answer = []
    for word in words:
        answer.append(pattern_search(grid, word))
    
    lst = []
    count = 0
    
    # turning the list of list of tuples form in answer to a list of tuples
    for word in answer:
        if word is None:
            lst = lst
        else:
            #CITE: Professor Campbell
            #DESC: Suggested the count += operation to return the correct count
            count += 1
            for loc in word:
                lst.append(loc)
    
    wordcap(grid, lst)
    return count



def main():
    """ The main program is just for your own testing purposes.
        Modify this in any way you wish.  It will not be graded. """
    
    myGrid = [['j', 'm', 'w', 'e'],
              ['e', 'e', 'p', 'p'],
              ['q', 'o', 'x', 'u'],
              ['w', 'w', 'e', 'd'],
              ['w', 'g', 'j', 'o']]
    lst = ['meow', 'wed', 'do', 'justice']
    
    # printGrid(myGrid)
    # print('-------------------')
    print(wordfind(myGrid, lst))
    # print('-------------------')
    #print(firstletterloc(myGrid, 'meow')[0])
    #print(wordcaplocations((0, 1), 1, 0, 'meow'))
    
   



if __name__ == "__main__":
    main()