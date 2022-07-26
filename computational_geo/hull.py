"""
    File:        hull.py
    Author:      Jack Kaffenbarger
    Course:      CS 307 - Computational Geometry
    Semester:    Spring 2022
    Assignment:  Problem Set 1 - Convex Hulls
    Description: Methods to generate points and compute convex hulls 
    with different algorithms.
"""
import random

def generate_points(num_points, points_on_hull):
    """Generate a set of num_points points with points_on_hull points
       on its convex hull. Generate hull points on y = x^2, other points on
       y=2x^2"""
    if num_points < points_on_hull:
        print("Input num_points <= points_on_hull")
        return 
    if points_on_hull < 3:
        print("Input at least 3 points on the convex hull")
        return 
    bounds = num_points // 2 
    points = [(0, 0), (bounds, bounds * bounds), (-bounds, bounds * bounds)]
    num_points -= 3
    points_on_hull -= 3
    counter = 1
    while points_on_hull > 0:
        points.append((counter, counter * counter))
        counter *= -1
        points_on_hull -= 1
        num_points -= 1
        if points_on_hull > 0:
            points.append((counter, counter * counter))
            counter *= -1
            points_on_hull -= 1
            num_points -= 1
            counter += 1

    counter = 1
    while num_points > 0:
        points.append((counter, 2 * counter * counter))
        counter *= -1
        num_points -= 1
        if num_points > 0:
            points.append((counter, 2 * counter * counter))
            counter *= -1
            num_points -= 1
            counter += 1

    return points

def orient(p, q, r):
    """Given a line segment pq, determine whether the point r
    lies to the left, right, or directly on pq. Returns either
    positive, negative, or 0 respectively"""
    px, py = p
    qx, qy = q
    rx, ry = r
    return (qx * ry) + (px * qy) + (rx * py) - (qx * py) - (rx * qy) - (ry * px)

def convex_hull_edge(p, q, points):
    """Given two points, and a set of points, return true if every
    other point lies to the right of pq, otherwise return false"""
    for point in points:
        if point == p or point == q:
            continue
        if orient(p, q, point) >= 0:
            return False
    return True

def edges_to_points(edges):
    """Convert a list of directed edges into a list of points in
    clockwise order"""
    edges.sort(key=lambda x: x[0][0])
    points = [edges[0][0], edges[0][1]]
    while True:
        print(points)
        if points[0] == points[-1]:
            return points[:-1]
        #find the edge that starts with the last vertex added to points
        next_point = [edge for edge in edges if edge[0] == points[-1]] 
        points.append(next_point[0][1])

def slow_convex_hull(points):
    """compute the convex hull of points in O(n^3) time"""
    convex_hull = []
    for p in points:
        for q in points:
            if p == q:
                continue
            if convex_hull_edge(p, q, points):
                convex_hull.append((p, q))

    return edges_to_points(convex_hull)

def compute_hull(points):
    """Given a sorted list of points, compute the upper/lower hull"""
    hull = points[:2]
    i = 2
    while i < len(points):
        if len(hull) == 1 or orient(hull[-2], hull[-1], points[i]) < 0:
            hull.append(points[i])
            i += 1
        else:
            #left turn, need to backtrack!
            hull.pop()
    return hull

def graham_scan(points):
    """Run Graham Scan on points in O(n log n) time"""
    points.sort(key=lambda x: x[0])
    upper_hull = compute_hull(points)
    points.reverse()
    lower_hull = compute_hull(points)
    upper_hull.extend(lower_hull[1:-1])
    return upper_hull

def find_leftmost_point(anchor, points):
    """Given an achor point and a list of points, find the leftmost point
    in relation to the anchor point"""
    if points[0] != anchor:
        leftmost = points[0]
    else:
        leftmost = points[1]
        
    for point in points:
        if point == leftmost or point == anchor:
            continue
        if orient(anchor, leftmost, point) > 0:
            leftmost = point
    return leftmost

def jarvis_march(points):
    """Run Jarvis March on points in O(nh) time"""
    convex_hull = [min(points)] #get leftmost startpoint
    while True:
        new_point = find_leftmost_point(convex_hull[-1], points)
        if new_point == convex_hull[0]:
            return convex_hull
        convex_hull.append(new_point)

def test():
    """Get user input and run appropriate timing experiment."""
    #my_hull = [(-1, 0), (0, -1), (1, 0), (0, 1), (0, 0)]
    my_hull = generate_points(10, 10)
    random.shuffle(my_hull)
    print("MY HULL    : ", slow_convex_hull(my_hull))
    # print(convex_hull_edge((10, 100), (3, 18), my_hull))
    # print(orient((10, 100), (3, 18), (1, 1)))
    #print("GRAHAM'S SCAN: ", graham_scan([(0, 0), (1, 1), (2, 4), (3, 9), (4, 16), (5, 25)]))
    # print("GRAHAM'S SCAN: ", graham_scan(my_hull))
    # print("JARVIS MARCH: ", jarvis_march(my_hull))
    return 
