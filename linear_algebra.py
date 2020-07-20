import numpy as np
import pygame
from pygame.math import Vector2
import pygame

def get_line_mat(center, length):
    return np.array([[center[0]-length/2, center[1]],
                     [center[0]+length/2, center[1]]])

def get_rect_mat(rect):
    return np.array([[rect.x, rect.y],
              [rect.x + rect.width, rect.y],
              [rect.x + rect.width, rect.y + rect.height],
              [rect.x, rect.y + rect.height]])

def get_rot_mat(a):
    return np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]], dtype=np.float16)

def rotate_mat(mat, angle):
    rot_mat = get_rot_mat(np.radians(angle))
    mat = np.array(mat, dtype=np.int64)
    return ((mat-mat.mean()).dot(rot_mat)) + mat.mean()

def line_circle_intersection(E, L, C, r):
    d = L - E
    f = E - C
    a = d.dot(d)
    b = 2*f.dot(d)
    c = f.dot(f) - r**2

    disc = b**2-4*a*c
    if disc < 0:
        return None
    else:
        disc = np.sqrt(disc)
        t1 = (-b - disc)/(2*a)
        t2 = (-b + disc)/(2*a)
        vals = []
        if t1 >= 0 and t1 <= 1:
            vals.append((t1, Vector2(E+d*t1)))
        if t2 >= 0 and t2 <= 1:
            vals.append((t2, Vector2(E+d*t2)))
        return vals

def get_final_line_circle_intersection(C, r, path, last_lookahead_triple):
    points = []
    ts = []
    indexs = []
    for i in range(len(path)-1):
        E = path[i]
        L = path[i+1]
        vals = line_circle_intersection(E, L, C, r)
        if vals != None and len(vals) > 0:
            for item in vals:
                ts.append(item[0])
                points.append(item[1])
                indexs.append(i)
    intersects = list(zip(ts, points, indexs))
    if len(intersects) == 0: return last_lookahead_triple
    else:
        greatest_frac_index_index = np.argmax([t+i for t, p, i in intersects])
        best_intersect = intersects[greatest_frac_index_index]
        if best_intersect[0]+best_intersect[2] > last_lookahead_triple[0]+last_lookahead_triple[2]:
            return best_intersect
        else: return last_lookahead_triple
        #return best_intersect

def get_side(line1, line2, point):
    m = (line2.y - line1.y)/(line2.x - line1.x)
    val = m*point.x + (line1.y - m*line1.x)
    return np.sign(point.y - val)

def get_cte(theta, robot_pos, lookahead_pos, path_pos):
    a = -np.tan(theta)
    c = np.tan(theta)*robot_pos.x - robot_pos.y
    L = lookahead_pos-robot_pos
    B = robot_pos+Vector2(np.cos(theta), np.sin(theta))
    #s = -np.sign((lookahead_pos.x-path_pos.x)*(robot_pos.y-path_pos.y) - (lookahead_pos.y-path_pos.y)*(robot_pos.x-path_pos.x))
    s = get_side(path_pos, lookahead_pos, robot_pos)
    #m = (lookahead_pos.y-path_pos.y)/(lookahead_pos.x-path_pos.x)
    #b = (path_pos.y-m*path_pos.x)
    N = Vector2(a, 1)
    d = L.dot(N)/N.magnitude()
    #angle = np.arccos(L.dot(N)/(L.magnitude()*N.magnitude()))
    angle = np.arccos(L.dot(B)/(L.magnitude()*B.magnitude()))
    #print(np.abs(a*lookahead_pos.x + lookahead_pos.y + c)/np.sqrt(np.square(a)+1), np.abs(d), np.degrees(angle))
    return s*np.abs(a*lookahead_pos.x + lookahead_pos.y + c)/np.sqrt(np.square(a)+1)
    #return s*L.magnitude()

def get_alpha(theta, robot_pos, lookahead_pos, path_pos):
    a = -np.tan(theta)
    L = lookahead_pos - robot_pos
    B = robot_pos + Vector2(np.cos(theta), np.sin(theta))
    #N = Vector2(a, 1)
    #d = L.dot(N) / N.magnitude()
    angle = np.arccos(L.dot(B) / (L.magnitude() * B.magnitude()))
    #s = -np.sign((lookahead_pos.x - path_pos.x) * (robot_pos.y - path_pos.y) - (lookahead_pos.y - path_pos.y) * (
                #robot_pos.x - path_pos.x))
    s = get_side(path_pos, lookahead_pos, robot_pos)
    #print(s*np.degrees(angle), B.angle_to(L))
    return s*np.degrees(angle)

def get_xte_by_wp_localization(wp1, wp2, robot_pos):
    D = wp2 - wp1
    l1 = robot_pos - wp1
    theta1 = np.radians(D.angle_to(l1))
    return l1.magnitude()*np.sin(theta1), np.degrees(theta1)





















