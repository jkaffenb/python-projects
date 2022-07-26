"""
    File:        range.py
    Author:      Jack Kaffenbarger
    Course:      CS 307 - Computational Geometry
    Assignment:  Problem Set 5 - Range Searching
    Description: Methods to construct a kd-tree, perform
    range queries, test and time the range query.
"""
from typing import List, Tuple
import math
import random
import datetime

class Node:
    def __init__(self, point, depth):
        self.point = point
        self.depth = depth
        self.left = None
        self.right = None

    def is_leaf(self):
        return self.left == None and self.right == None


def kdtree_helper(value, points, direction, x_or_y):
    """Given a value and a list of sorted points, return an updated list in linear time"""
    answer = []
    if direction == "left":
        #inclusive
        for point in points:
            if point[x_or_y] <= value[x_or_y]:
                answer.append(point)
    else:
        for point in points:
            if point[x_or_y] > value[x_or_y]:
                answer.append(point)
    return answer

def create_kdtree(points: List[Tuple[int,int]], depth=0):
    """
    Construct a kd-tree from a list of 2D points 
    and return its root. 
        Keyword arguments:
        points -- the list of 2d points
    Return the root of the kd-tree
    """
    
    if len(points) == 1:
        return Node(points[0], depth)

    if (depth % 2) == 0:
        points.sort()
    else:
        points.sort(key = lambda x: x[1])

    median_index = math.ceil(len(points) / 2)
    p_one = points[:median_index]
    p_two = points[median_index:]
    v_left = create_kdtree(p_one, depth + 1)
    v_right = create_kdtree(p_two, depth + 1)

    v = Node(points[median_index - 1], depth % 2)
    v.left = v_left
    v.right = v_right
    return v

def report_subtree(tree):
    """Given a tree, report the leaves"""
    if tree.is_leaf():
        return [tree.point]
    return report_subtree(tree.left) + report_subtree(tree.right)

def in_rectangle(point, rectangle):
    """Return true if point in rectangle"""
    return rectangle[0][0] <= point[0] <= rectangle[0][1] and rectangle[1][0] <= point[1] <= rectangle[1][1]

def type_of_intersection(region, query_range):
    """Returns the type of intersection between two rectangles"""
    if in_rectangle([region[0][0], region[1][0]], query_range) and in_rectangle([region[0][1], region[1][1]], query_range):
        return "contains"
    
    bottom_left_region = [region[0][0], region[1][0]]
    top_right_region = [region[0][1], region[1][1]]
    bottom_left_query_range = [query_range[0][0], query_range[1][0]]
    top_right_query_range = [query_range[0][1], query_range[1][1]]

    #check if one rectangle is above another
    if bottom_left_query_range[1] > top_right_region[1] or bottom_left_region[1] > top_right_query_range[1]:
        return "nointersect"

    #check if one rectangle is to the right of another
    if bottom_left_query_range[0] > top_right_region[0] or bottom_left_region[0] > top_right_query_range[0]:
        return "nointersect"
    return "intersects"

def update_region(kd_tree, region, subtree):
    """update the region"""
    #determine horizontal or vertical line
    if kd_tree.depth % 2 == 0:
        #vertical line, change x region
        if subtree == "left":
            return [[region[0][0], kd_tree.point[0]], [region[1][0], region[1][1]]]

        else:
            return [[kd_tree.point[0], region[0][1]], [region[1][0], region[1][1]]]
    else:
        #horizontal line, change y region
        if subtree == "left":
            return [[region[0][0], region[0][1]], [region[1][0], kd_tree.point[1]]]
        else:
            return [[region[0][0], region[0][1]], [kd_tree.point[1], region[1][1]]]

def range_query(kd_tree, query_range: Tuple[Tuple[int,int],Tuple[int,int]], 
                region=[[-math.inf, math.inf], [-math.inf, math.inf]]) -> List[Tuple[int,int]]:
    """
    Perform a 2D range reporting query using kd_tree and the given query range
    and return the list of points.
        Keyword arguments:
        kd_tree: the root node of the kd-tree to query
        query_range: a rectangular range to query
    Return the points in the query range as a list of tuples.
    """
    if kd_tree.is_leaf():
        if in_rectangle(kd_tree.point, query_range):
            return [kd_tree.point]
    else:
        answer = []
        if type_of_intersection(update_region(kd_tree, region, "left"), query_range) == "contains":
            answer += report_subtree(kd_tree.left)
        else:
            if type_of_intersection(update_region(kd_tree, region, "left"), query_range) == "intersects":
                answer += range_query(kd_tree.left, query_range, update_region(kd_tree, region, "left"))

        if type_of_intersection(update_region(kd_tree, region, "right"), query_range) == "contains":
            answer += report_subtree(kd_tree.right)
        else:
            if type_of_intersection(update_region(kd_tree, region, "right"), query_range) == "intersects":
                answer += range_query(kd_tree.right, query_range, update_region(kd_tree, region, "right"))

        return answer
    return []

def test():
    """
    Test range_query.
    For testing I copied one of the sets of points from the book, and made sure that my KD-tree was
    built correctly, and then tested edge cases such as all inside query range, none, edges, and other 
    subsets of points
    """
    points = [[0, 0], [1, 2], [1.5, -2], [0, 5], [3, 4], [7, -3], [4, .5], [10, -.5], [5, 5], [5.5, 3]]
    tree = create_kdtree(points)
    print(range_query(tree, [[.5, 11], [-5, 6]]))
    print(range_query(tree, [[.5, 11], [-1, 6]]))
    print(range_query(tree, [[.5, 3], [-1, 6]]))
    print(range_query(tree, [[.5, 3], [-2, 6]]))
    print(range_query(tree, [[.5, 3], [5, 6]]))
    # region = [[0, 10], [-3, 5]]
    # print(update_region(tree.left, region, "left"))
    # print(update_region(tree.left, region, "right"))
    # print(tree.point)
    # print(update_region(tree.left, [[0, 10], [-3, 5]], "left"))
    # print(update_region(tree, [[0, 10], [-3, 5]], "right"))

    print(report_subtree(tree))
    # print(in_rectangle([1, 1], [[-1, 1], [-1, 1]]))
    # print(tree.left.left.left.left.point)
    # print(tree.left.left.left.right.point)
    # print(tree.left.left.right.point)
    # print(tree.left.right.left.point)
    print(tree.point) #(3, 4)
    print(tree.left.point) #(1, 2)
    print(tree.right.point) #(4, .5)
    print(tree.left.left.point) #(1, 2)
    print(tree.left.right.point) #(0, 5)
    # print(tree.right.left.point) #(7, -3)
    # print(tree.right.right.point) #(5, 5)
    # print(tree.left.left.left.point) #(0, 0)
    # print(tree.left.left.right.point) #(1.5, -2)
    # print(tree.left.right.left.point) #(0, 5)
    # print(tree.left.right.right.point) #(3, 4)
    # print(tree.left.left.left.left.point) #(0, 0)
    # print(tree.left.left.left.right.point) #(1, 2)
    # print(tree.right.left.left.point) #(7, 3)
    # print(tree.right.left.right.point) #(10, -.5)
    # print(tree.right.right.left.point) #(5, 5)
    # print(tree.right.right.right.point) #(5.5, 3)
    # print(tree.right.left.left.left.point) #(7, 3)
    # print(tree.right.left.left.right.point) #(4, .5)

    return

def generate_points(num_points):
    """Given a number of points, randomly generate that number of points. Given the type, put appropriate num of
    points in a random query range"""
    points = []
    for i in range(num_points):
        x_value = random.randrange(num_points) 
        y_value = random.randrange(num_points)
        points.append([x_value, y_value])
    return points

def n_experiment():
    """Run experiment and change n"""
    time_diff = None
    n = 4
    while True:
        time_diff = None
        for i in range(3):
            points = generate_points(n)
            query = [[-random.randrange(n), random.randrange(n)], [-random.randrange(n), random.randrange(n)]]
            tree = create_kdtree(points)
            start = datetime.datetime.now()
            range_query(tree, query)
            end = datetime.datetime.now()
            if time_diff == None:
                time_diff = end - start
            else:
                time_diff = time_diff + end - start
        time_ms = time_diff.microseconds // 1000
        time_ms = time_ms + time_diff.seconds * 1000
        time_ms = time_ms + time_diff.days * 24 * 60 * 60 * 1000
        print("SIZE OF N, TIME: ", n, time_ms)
        n *= 2
    return

def time_experiment():
    """
    Custom experiment to show that kd-tree has query time O(sqrt(n) + k).
    I tried to seperate n growing and k growing but it was difficult to choose
    a productive query range. As n doubles the time should roughly 1.5x
    """
    print("Welcome to Range Timer! Press Ctrl+C at any time to end...")
    option = input("Type n to start! ")
    while option not in ["n"]:
        print("Unrecognized option '", option, "'")
        option = input("Type n to start! ")

    if option == "n":
        n_experiment()
        return
    return

if __name__ == "__main__":

    #test() # use for testing, comment when done
    time_experiment()
