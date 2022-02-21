"""
 *****************************************************************************
    FILE:        hw1.py
    AUTHOR:      Miles Wyner, Jack Kaffenbarger, Carter Steckbeck
    ASSIGNMENT:  Homework 1
    DATE:        February 8, 2021
    DESCRIPTION: Implementation of a vaccumm agent with the goal of cleaning
                 all dirty cells within a grid of cells containing some
                 assortment of dirty cells, clean cells, and obstacle cells.
*****************************************************************************
"""


from vacuum_environment import VacuumEnvironment
import math


class VacuumEnvironment375(VacuumEnvironment):

    def __str__(self):
        """ prints grid of the enviroment showing dirt, obstacles, clean cells,
            and agent, each represented by their first letter capitalized. grid
            surrounded by obstacles to make environment bounds clear """
        string = "O " * (self.cols + 2) + "\n"
        for row in range(self.rows):
            string = string + str(self.grid[row]) + "\n"
        string = string + "O " * (self.cols + 2) + "\n"
        a = string.replace("Obstacle", "O")
        b = a.replace("Empty", "E")
        c = b.replace("Dirt", "D")
        d = c.replace("Agent", "A")
        e = d.replace(",", "")
        f = e.replace("'", "")
        g = f.replace("]", " O")
        return g.replace("[", "O ")

    def __hash__(self):
        return hash(self.__str__())

    def all_clean(self):
        """ output: true if the environment is clean, false otherwise. """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.__getitem__((row, col)) == "Dirt":
                    return False
        return True

    def count_dirty_cells(self):
        """ output: total dirty cells in current environment. """
        count = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if self.__getitem__((row, col)) == "Dirt":
                    count += 1
        return count

    def distance_from_center(self):
        """ output: straight line distance of agent to center. """
        center_col = math.floor(self.cols / 2)
        center_row = math.floor(self.rows / 2)
        agent_row = self.agent_loc[0]
        agent_col = self.agent_loc[1]
        return abs(center_col - agent_col) + abs(center_row - agent_row)

    def heuristic1(self):
        return self.count_dirty_cells()

    def heuristic2(self):
        return self.distance_from_center()

def main():
    pass
if __name__ == "__main__":
    main()
