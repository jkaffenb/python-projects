"""
    File:        triangulate.py
    Author:      Jack Kaffenbarger
    Course:      CS 307 - Computational Geometry
    Assignment:  Problem Set 4 - Polygon Triangulation
    Description: Methods to generate y-monotone polygons,
    triangulate them, and verify the triangulation.
"""
from typing import List, Tuple

from numpy import diagonal, poly

import random

import matplotlib.pyplot as plt

def generate_monotone_polygon(num_vertices: int) -> List[Tuple[int,int]]:
    """
    Generate a y-monotone polygon on num_vertices vertices, returned
    as a list of points in clockwise order around its boundary.
        Keyword arguments:
        num_vertices -- the number of vertices the generated polygon
                        should have
    Return a list of integer tuples (pairs), its length should
    be num_vertices.
    """
    if num_vertices < 3:
        return
    last_point = [(-num_vertices // 2, -num_vertices // 2)]
    left_chain = []
    right_chain = [(1, num_vertices), (1.5, num_vertices - 1)]
    num_vertices -= 3
    reflex_chain = 2
    while num_vertices > 0:
        num = random.randint(-3, 3)
        if num <= 1:
            #case 1
            right_chain += [(reflex_chain * reflex_chain, num_vertices)]
            reflex_chain += 1
        if num == 2:
            #case 2
            right_chain += [(reflex_chain + 1, num_vertices)]
            reflex_chain = 0
        if num == 3:
            #case 3
            left_chain = [(-reflex_chain - 1, num_vertices)] + left_chain
            reflex_chain = 0
        num_vertices -= 1

    polygon = right_chain + last_point + left_chain
    #half the time flip the image
    mirror = random.randint(0, 1)
    if mirror == 1:
        polygon = list(map(lambda a: (a[0] * -1, a[1]), polygon))
    return polygon

def orient(p, q, r):
    """Given a line segment pq, determine whether the point r
    lies to the left, right, or directly on pq. Returns either
    positive, negative, or 0 respectively"""
    px, py = p
    qx, qy = q
    rx, ry = r
    return (qx * ry) + (px * qy) + (rx * py) - (qx * py) - (rx * qy) - (ry * px)

def leftmost(polygon):
    """find the index of the leftmost point in a polygon"""
    leftmost_index = 0
    for i in range(len(polygon)):
        if polygon[i][0] < polygon[leftmost_index][0]:
            leftmost_index = i
    return leftmost_index

def inside_triangle(v, u, w, z):
    """return true if z inside triangle vuw"""
    if orient(v, u, z) >= 0 and orient(u, w, z) >= 0 and orient(w, v, z) >= 0:
        return True
    return False

def furthest_from_line(w, u, z_indexes, points):
    """given two points that make up a line, find the point that lies 
    farthest from it"""
    z = points[z_indexes[0]]
    slope = (w[0] - u[0], w[1] - u[1]) 
    for index in z_indexes[1:]:
        if orient((z[0] - slope[0], z[1] - slope[1]), z, points[index]) > 0:
            z = points[index]

    return points.index(z)

def brute_force_triangulate(polygon: List[Tuple[int,int]]) -> List[Tuple[int,int]]:
    """
    Compute a triangulation of a polygon (given as a list of 
    integer pairs (tuples), which is a clockwise ordering 
    of the coordinates of the vertices) in time O(n^2). Return 
    the diagonals as a list of points.
        Keyword arguments:
        polygon -- a list of integer tuples (pairs) representing
                   a clockwise ordering of points around a polygon
    Return a list of integer tuples (pairs). Supposing the list is
    called diagonals, diagonal i is stored as endpoints in 
    diagonal[2i] and diagonal[2i+1].
    """
    if len(polygon) <= 3:
        return []

    v = leftmost(polygon)
    u = (v - 1) % len(polygon)
    w = (v + 1) % len(polygon)

    potential_z_indexes = []
    for i in range(len(polygon)):
        if i == v or i == u or i == w:
            continue
        if inside_triangle(polygon[v], polygon[u], polygon[w], polygon[i]):
            potential_z_indexes.append(i)
    
    if len(potential_z_indexes) == 0:
        answer = [polygon[u], polygon[w]]
        polygon.remove(polygon[v])
        return brute_force_triangulate(polygon) + answer 

    #find the correct z
    z_index = furthest_from_line(polygon[w], polygon[u], potential_z_indexes, polygon)
    if z_index > v:
        if z_index + 1 > len(polygon):
             return brute_force_triangulate(polygon[v:] + [polygon[0]]) + brute_force_triangulate(polygon[z_index:] + polygon[:v + 1]) + [polygon[v]] + [polygon[z_index]]
        else:
            return brute_force_triangulate(polygon[v:z_index + 1]) + brute_force_triangulate(polygon[z_index:] + polygon[:v + 1]) + [polygon[v]] + [polygon[z_index]]
    
    if v + 1 > len(polygon):
        return brute_force_triangulate(polygon[z_index:] + [polygon[0]]) + brute_force_triangulate(polygon[v:] + polygon[:z_index + 1]) + [polygon[v]] + [polygon[z_index]]
    return brute_force_triangulate(polygon[z_index:(v + 1)]) + brute_force_triangulate(polygon[v:] + polygon[:z_index + 1]) + [polygon[v]] + [polygon[z_index]]
  
def order_polygon(polygon):
    """Given a polygon, order vertices from top to bottom, and create a direction lst"""
    highest_vertex = max(polygon, key=lambda vertex:vertex[1])
    lowest_vertex = min(polygon, key=lambda vertex:vertex[1])
    ordered_polygon = [highest_vertex]
    new_polygon = polygon[polygon.index(highest_vertex):] + polygon[:polygon.index(highest_vertex)]
    right_pointer = 1
    left_pointer = len(polygon) - 1
    direction_lst = ['both']

    while right_pointer != new_polygon.index(lowest_vertex) or left_pointer != new_polygon.index(lowest_vertex):
        if new_polygon[right_pointer][1] > new_polygon[left_pointer][1]:
            ordered_polygon.append(new_polygon[right_pointer])
            direction_lst.append('right')
            right_pointer += 1
        else:
            ordered_polygon.append(new_polygon[left_pointer])
            direction_lst.append('left')
            left_pointer -= 1
    ordered_polygon.append(lowest_vertex)
    direction_lst.append('both')
    return ordered_polygon, direction_lst

def reflex_point(stack, current_direction, point):
    """determine if point extends the reflex chain"""
    if current_direction == 'right':
        return orient(stack[-2], stack[-1], point) > 0
    return orient(stack[-2], stack[-1], point) < 0 

def monotone_triangulate(polygon: List[Tuple[int,int]]) -> List[Tuple[int,int]]:
    """
    Compute a triangulation of a polygon (given as a list of 
    integer pairs (tuples), which is a clockwise ordering 
    of the coordinates of the vertices) in time O(n), assuming
    that the polygon is y-monotone. Return the diagonals as a
    list of points.
        Keyword arguments:
        polygon -- a list of integer tuples (pairs) representing
                   a clockwise ordering of points around a polygon
    Return a list of integer tuples (pairs). Supposing the list is
    called diagonals, diagonal i is stored as endpoints in 
    diagonal[2i] and diagonal[2i+1].
    """
    ordered_polygon, direction_lst = order_polygon(polygon)
    diagonals = []
    stack = []
    stack.append(ordered_polygon[0])
    stack.append(ordered_polygon[1])
    current_direction = direction_lst[1]
    for j in range(2, len(polygon) - 1):
        if direction_lst[j] == current_direction:
            #either case 1 or case 2
            if reflex_point(stack, current_direction, ordered_polygon[j]):
                #case 1
                stack.append(ordered_polygon[j])
            else:
                #case 2
                while len(stack) > 1 and not reflex_point(stack, current_direction, ordered_polygon[j]):
                    diagonals.append(ordered_polygon[j])
                    diagonals.append(stack[-2])
                    stack.pop()
                stack.append(ordered_polygon[j])
        else:
            current_direction = direction_lst[j]
            #case 3
            r_k = stack[-1]
            while len(stack) != 1:
                diagonals.append(ordered_polygon[j])
                diagonals.append(stack[-1])
                stack.pop()
            stack.pop()
            stack.append(r_k)
            stack.append(ordered_polygon[j])

    #handle final vertex
    v_n = min(ordered_polygon, key=lambda vertex:vertex[1])
    stack.pop()
    while len(stack) != 1:
        diagonals.append(stack[-1])
        diagonals.append(v_n)
        stack.pop()
    
    return diagonals

def intersect_helper(segmentA, segmentB):
    """determine if one orientation of two segments overlap (ignoring endpoints)"""
    if orient(segmentA[0], segmentA[1], segmentB[0]) < 0:
        if orient(segmentA[0], segmentA[1], segmentB[1]) > 0:
            return True
    if orient(segmentA[0], segmentA[1], segmentB[0]) > 0:
        if orient(segmentA[0], segmentA[1], segmentB[1]) < 0:
            return True

def intersect(segmentA, segmentB):
    """Return True if the two segments intersect (intersection at endpoints is not counted), otherwise return False"""
    if intersect_helper(segmentA, segmentB) and intersect_helper(segmentB, segmentA):
        return True
    return False

def test_intersection_and_duplication(segments):
    """Return True if any of the segments intersect, or if there are any duplications, else False"""
    for i in range(len(segments) // 2):
        i_idx = i * 2
        for j in range(len(segments) // 2):
            j_idx = j * 2
            if i_idx == j_idx:
                continue
            if intersect((segments[i_idx], segments[i_idx + 1]), (segments[j_idx], segments[j_idx + 1])):
                return True
            if segments[i_idx] == segments[j_idx] and segments[i_idx + 1] == segments[j_idx + 1]:
                return True
            if segments[i_idx + 1] == segments[j_idx] and segments[i_idx] == segments[j_idx + 1]:
                return True

    return False

def is_triangulation(polygon: List[Tuple[int,int]], diagonals: List[Tuple[int,int]]) -> bool:
    """
    Return True if and only if diagonals is a triangulation
    of polygon. Must be done efficiently.
        Keyword arguments:
        polygon   -- a list of integer tuples (pairs) representing
                     a clockwise ordering of points around a polygon
        diagonals -- a list of integer tuples (pairs) representing
                     line segments between vertices of the polygon
                     Diagonal i is stored as endpoints in 
                     diagonal[2i] and diagonal[2i+1].
    Return True if diagonals is a trianglulation of polygon, False
    otherwise.
    """
    if len(polygon) - 3 != (len(diagonals) // 2):
        return False

    if test_intersection_and_duplication(diagonals):
        return False
    
    return True

def test() -> None:
    """ Test your triangulation routines. """
    # print(is_triangulation([(-2, 0), (-1, 1), (1, 1), (2, 0), (1, -1), (-1, -1)], [(-2, 0), (2, 0), (-2, 0), (1, 1), (-2, 0), (1, -1)]))
    # print(is_triangulation([(-2, 0), (-1, 1), (1, 1), (2, 0), (1, -1), (-1, -1)], [(-2, 0), (2, 0), (2, 0), (-2, 0), (2, 0), (-1, -1)]))
    # print(is_triangulation([(-1, 1), (1, 1), (1, -1), (-1, -1)], [(-1, -1), (1, 1)]))
    # print(brute_force_triangulate([(-2, 0), (-1, 1), (1, 1), (2, 0), (1, -1), (-1, -1)]))
    # print(brute_force_triangulate([(-1, 1), (1, 1), (1, -1), (-1, -1)]))
    #print("ANSWER: ", brute_force_triangulate([(6, -2), (4, -4), (3, -3), (0, 0), (2, 2), (1, 0)]))
    #print("ANSWER: ", brute_force_triangulate([(0, 0), (5, 5), (4, 2), (2, 1), (6, -2), (4, -4), (3, -2)]))
    # coord = generate_monotone_polygon(10)
    # polygon = coord.copy()
    # print(coord)
    # coord = [(1, 10), (1.5, 9), (3, 7), (0, 6), (1, 5), (3, 4), (0, 2), (2, 1), (-5, -5), (-1, 3)]
    # # #print("GIVEN TRIANGULATION: ", brute_force_triangulate(coord))
    
    # # #print(brute_force_triangulate(coord))
    # # print("passed coord: ", coord)
    # # print(is_triangulation(polygon, brute_force_triangulate(coord)))
    
    # coord.append(coord[0]) #repeat the first point to create a 'closed loop'

    # xs, ys = zip(*coord) #create lists of x and y values

    # plt.figure()
    # plt.plot(xs,ys) 
    # plt.show()
    # # polygon = [(1, 13), (1.5, 12), (4, 11), (3, 10), (6, 9), (7, 8.6), (5, 7), (6.5, 6), (0, 5), (-.5, 5.5), (-3, 6.5), (-2, 8.5), (-1.5, 8.75)]
    # # answer = monotone_triangulate(polygon)
    # # #print(answer)
    # # #print(len(answer) / 2)
    # # print(is_triangulation([(1, 13), (1.5, 12), (4, 11), (3, 10), (6, 9), (7, 8.6), (5, 7), (6.5, 6), (0, 5), (-.5, 5.5), (-3, 6.5), (-2, 8.5), (-1.5, 8.75)], answer))
    # polygon = [(1, 10), (1.5, 9), (3, 7), (0, 6), (1, 5), (3, 4), (0, 2), (2, 1), (-5, -5), (-1, 3)]
    
    # print(is_triangulation([(1, 10), (1.5, 9), (3, 7), (0, 6), (1, 5), (3, 4), (0, 2), (2, 1), (-5, -5), (-1, 3)], brute_force_triangulate(polygon)))
    # print(is_triangulation(polygon, monotone_triangulate(polygon)))
    # print(generate_monotone_polygon(10))    

if __name__ == '__main__':
    test()
