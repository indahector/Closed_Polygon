import math
from shapely import geometry
from shapely.geometry import Polygon, mapping
import re
from shapely import wkt

def calculate_distance(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

def calculate_angle(p, centroid):
    return math.atan2(p[1] - centroid[1], p[0] - centroid[0])

def sort_points_to_polygon(points):
    # Calculate centroid
    centroid = [sum(p[0] for p in points) / len(points), sum(p[1] for p in points) / len(points)]
    
    # Find starting point (closest to centroid)
    starting_point = min(points, key=lambda p: calculate_distance(p, centroid))
    
    # Calculate angles for the remaining points
    angles = [(p, calculate_angle(p, centroid)) for p in points if p != starting_point]
    
    # Sort points based on angles
    sorted_points = [p for p, _ in sorted(angles, key=lambda x: x[1])]
    
    # Create the closed polygon
    sorted_polygon = [starting_point] + sorted_points + [starting_point]
    
    return sorted_polygon

def closed_polygon(X,Y):
    points = [(x,y) for x,y in zip(X,Y)]
    sorted_points = sort_points_to_polygon(points)
    poly = "POLYGON (("
    for (x,y) in sorted_points:
        poly += "{} {}, ".format(x,y)
    poly = poly[:-2] + "))"
    poly_wkt = add_closing_coordinates(poly)
    polygon = wkt.loads(poly_wkt)
    return polygon