"""
    File:        sweep.py
    Author:      Jack Kaffenbarger
    Course:      CS 307 - Computational Geometry
    Assignment:  Problem Set 2 - Line Segment Intersection
    Description: Methods to generate horizontal and vertical segments 
    and compute their intersection points.
"""
from typing import List, Tuple
from sortedcontainers import SortedList

def generate_segments(num_segments : int, num_intersections: int) -> List[Tuple[int,int]]:
    """
    Generate a list of num_segments horizontal and vertical line segments.
        Keyword arguments:
        num_segments      -- the number of segments to generate
        num_intersections -- the number of intersections between
                             the generated segments
    Return a list of integer tuples (pairs). Supposing the list 
    is called segments, line segment i is stored as endpoints
    in segment[2i] and segment[2i+1].
    """
    if num_intersections < 0 or num_intersections > (num_segments * num_segments) / 4:
        print("input valid num_intersections")
        return

    #[in - i^2] <- use this formula to determin number of vertical and horizontal 
    #lines
    range_lst = SortedList()
    for i in range((num_segments // 2) + 1):
        range_lst.add((i * num_segments) - (i * i))

    #number of vertical lines needed
    idx = range_lst.bisect(num_intersections)

    #dealing with case where input is the max # of intersections
    if idx == len(range_lst):
        idx -= 1

    points = []
    #compute vertical lines (general position)
    for i in range(idx):
        points.append([i + 1, -i - 1])
        points.append([i + 1, num_segments - idx + i + 1])

    remaining_intersections = num_intersections
    #compute horizontal lines (general position)
    for i in range(num_segments - idx):
        #no more intersections
        if remaining_intersections == 0:
            points.append([-0.5 - i, i])
            points.append([- i, i])
        #full row of intersections
        elif remaining_intersections % idx == 0:
            points.append([-0.5 - i, i])
            points.append([idx + 1 + i, i])
            remaining_intersections -= idx
        #< full row of intersections
        else:
            points.append([-0.5 - i, i])
            points.append([(remaining_intersections % idx) + 0.5, i])
            remaining_intersections -= remaining_intersections % idx

    return points

def compute_intersections(prev_point, point, sweepline_lst):
    """Given two endpoints of a horizontal line, compute the number
    of points that lie in between. Then build a list of the intersections
    points."""
    intersections = []
    new_x_values = sweepline_lst.irange(prev_point[0], point[0], (False, False))
    for value in new_x_values:
        intersections.append([value, point[1]])

    return intersections

def report_intersections(segments: List[Tuple[int,int]]) -> List[Tuple[int,int]]:
    """
    Compute a list of the I intersections between horizontal
    and vertical line segments in time O(n lg n + I).
        Keyword arguments:
        segments -- a list of horizontal and vertical line segments
                    which are stored as tuples of integers (pairs)
                    of their endpoints. Line segment i is stored as 
                    endpoints segments[2i] and segments[2i+1].
    Return a list of integer tuples (pairs), which are the intersection
    points between all line segments in segments.
    """
    #Setting up the data structures
    sweepline_lst = SortedList()
    segments.sort(key = lambda x: -x[1])

    #prev_point needed to know when we are poscessing a horizontal line
    intersections = []
    sweepline_lst.add(segments[0][0])
    prev_point = segments[0]
    for point in segments[1:]:
        if point[1] == prev_point[1]:
            #endpoint of a horizontal line, find number of intersections and remove 
            #prev_point[0] from the event queue
            intersections += compute_intersections(prev_point, point, sweepline_lst)
            sweepline_lst.remove(prev_point[0])
            prev_point = point

        elif point[0] not in sweepline_lst:
            #upper endpoint of a vertical line, add to event queue
            sweepline_lst.add(point[0])
            prev_point = point

        elif point[0] in sweepline_lst:
            #lower endpoint of a vertical line, remove from event queue
            sweepline_lst.remove(point[0])
            prev_point = point

        else:
            print("points are not in general position")
            return
    
    return intersections

def test() -> None:
    """
    C-4: Used loops and checked the results by hand to make sure 
    the answers were correct, as well as making sure the arguments passed
    to generate_segments matched with the output of report_intersections. 
    Tested edge cases such as no intersections, max intersections (for number
    of segments), odd and even inputs, etc...
    """
    print("Segments: ", generate_segments(8, 7))
    print(generate_segments(8, 7))
    print("ANSWER: ", report_intersections(generate_segments(8, 7)))
    for i in range(16):
        report_intersections(generate_segments(8, i))
    return
