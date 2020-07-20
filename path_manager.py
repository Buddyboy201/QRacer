from copy import deepcopy
from pygame import Vector2
import pygame
import seaborn as seaborn
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class Path:
    def insert_robot_waypoint(robot_pos, path):
        return [robot_pos] + path

    def inject_points(path, spacing):
        new_path = []
        for i in range(len(path)-1):
            new_path.append(path[i])
            diff = path[i+1]-path[i]
            n = int(diff.magnitude() / float(spacing))-1
            diff = diff.normalize()*spacing
            #print(diff)
            for j in range(n):
                new_path.append(new_path[len(new_path)-1]+diff)
        new_path.append(path[len(path)-1])
        return new_path

    def smooth_path(path, alpha, beta, tolerance):
        smooth = deepcopy(path)
        change = tolerance
        while change >= tolerance:
            change = 0
            for i in range(1, len(smooth)-1):
                for j in range(2):
                    x_i = path[i]
                    y_i, y_prev, y_next = smooth[i], smooth[i - 1], smooth[i + 1]

                    y_i_saved = y_i
                    y_i += alpha * (x_i - y_i) + beta * (y_next + y_prev - (2 * y_i))
                    smooth[i] = y_i

                    change += abs(y_i.x - y_i_saved.x) + abs(y_i.y - y_i_saved.y)
        return smooth

    def visualize_path(path):
        xs = [coord[0] for coord in path]
        ys = [coord[1] for coord in path]
        df = pd.DataFrame({"x": xs, "y": ys})
        sns.scatterplot(x="x", y="y", data=df)
        plt.show()

    def visualize_path_pygame(surf, path, color):
        for i in range(len(path)-1):
            pygame.draw.line(surf, color, path[i], path[i+1], 2)



test= '''path = [Vector2([0, 0]), Vector2([0, 1]), Vector2([0, 2]), Vector2([1, 2]), Vector2([2, 2]), Vector2([3, 2]),
                Vector2([4, 2]), Vector2([4, 3]), Vector2([4, 4])]
Path.visualize_path(path)
new_path = Path.inject_points(path, .5)
Path.visualize_path(new_path)
smooth_path = Path.smooth_path(new_path, .25, .75, .001)
Path.visualize_path(smooth_path)'''