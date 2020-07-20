import pygame
from pygame.math import Vector3, Vector2
import numpy as np
from bicycle import Bicycle, BLACK, RED, WHITE
from path_manager import Path
import time
from linear_algebra import get_final_line_circle_intersection, get_cte, get_alpha, get_xte_by_wp_localization



class Environment:
    def __init__(self, render_game=False, human_input=False):
        self.render_game = render_game
        self.human_input = human_input
        if self.render_game:
            pygame.init()
            self.screen = pygame.display.set_mode((1000, 1000))
            self.clock = pygame.time.Clock()
        self.bike = Bicycle()
        self.curr_time = 0
        self.path = []


    def render(self):
        if self.render_game:
            self.screen.fill(WHITE)
            Path.visualize_path_pygame(self.screen, self.path, RED)
            self.bike.render(self.screen)
            pygame.display.update()

    def update2(self, action):
        new_time = time.time()
        dt = new_time - self.curr_time
        #print(dt)
        self.curr_time = new_time
        if self.render_game and self.human_input:
            action = 0
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_SPACE]:
                action = 6
                print("BRAKE")
            elif pressed[pygame.K_UP]:
                if pressed[pygame.K_LEFT]:
                    action = 4
                    print("UP | LEFT")
                elif pressed[pygame.K_RIGHT]:
                    action = 5
                    print("UP | RIGHT")
                else:
                    action = 1
                    print("UP")
            elif pressed[pygame.K_LEFT]:
                action = 2
                print("LEFT")
            elif pressed[pygame.K_RIGHT]:
                action = 3
                print("RIGHT")

        self.bike.update2(action, dt)


    def update(self):
        delta_prime = 0
        acc = 0
        brake = False
        new_time = time.time()
        dt = new_time - self.curr_time
        print(dt)
        self.curr_time = new_time
        if self.render_game and self.human_input:
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_RIGHT]:
                delta_prime = -1
            elif pressed[pygame.K_LEFT]:
                delta_prime = 1


            if pressed[pygame.K_UP]:
                acc = 100
            elif pressed[pygame.K_DOWN]:
                acc = -100
            brake = pressed[pygame.K_SPACE]
        #self.bike.update(acc, delta_prime, dt, brake, 0, 0)
        self.bike.update2(0, dt)
        #print(cte, new_delta, self.bike.delta)



    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def end(self):
        pygame.quit()

















































test = '''class Environment:
    def __init__(self, render_game=False):
        self.render_game = render_game
        if self.render_game:
            pygame.init()
            self.screen = pygame.display.set_mode((1000, 1000))
            self.clock = pygame.time.Clock()
        self.bike = Bicycle()
        self.curr_time = 0
        self.path = []
        #self.path = Path.insert_robot_waypoint(self.bike.position, self.path)
        #print(self.path)
        for x, y in list(zip(list(range(int(self.bike.position.x), 400, 50)), list(range(int(self.bike.position.y), 400, 50)))):
            self.path.append(Vector2(x, y))

        for x, y in list(zip(list(range(400, 800, 50)), list(range(400, 200, -50)))):
            self.path.append(Vector2(x, y))
        print(self.path)
        new_path = Path.inject_points(self.path, 20)
        #new_path = self.path
        smooth_path = Path.smooth_path(new_path, .25, .75, .001)
        self.path = smooth_path
        # Path.visualize_path(self.path)
        self.last_lookahead_triple = (0, Vector2(self.path[0]), 0)

    def render(self):
        if self.render_game:
            self.screen.fill(WHITE)
            Path.visualize_path_pygame(self.screen, self.path, RED)
            self.bike.render(self.screen)
            #index = np.argmin([(self.bike.position - i).magnitude() for i in self.path])
            #closest_point = self.path[index]
            #pygame.draw.line(self.screen, (0, 255, 0), self.bike.position, closest_point, 2)
            #pygame.draw.circle(self.screen, BLACK, (int(self.bike.position.x), int(self.bike.position.y)), self.bike.r, 2)
            #pygame.draw.line(self.screen, (0, 0, 255), self.bike.position, self.last_lookahead_triple[1], 2)
            pygame.display.update()

    def update(self):
        self.last_lookahead_triple = get_final_line_circle_intersection(self.bike.position, self.bike.r, self.path,
                                                                        self.last_lookahead_triple)
        #alpha = get_alpha(self.bike.theta, self.bike.position, self.last_lookahead_triple[1], self.path[self.last_lookahead_triple[2]])
        #new_delta = np.degrees(np.arctan(2*self.bike.L*np.sin(np.radians(alpha))/self.bike.r))
        #cte = get_cte(self.bike.theta, self.bike.position, self.last_lookahead_triple[1], self.path[self.last_lookahead_triple[2]])
        #print(cte, alpha)
        #new_delta = self.bike.pd(cte, 10, 1)
        #xte, alpha = get_xte_by_wp_localization(self.path[self.last_lookahead_triple[2]], self.path[self.last_lookahead_triple[2]+1], self.bike.position)
        #new_delta = np.degrees(np.arctan(np.sin(np.radians(alpha)) / self.bike.r))
        #new_delta = self.bike.pd(xte, .01, .001, .001)
        #print(xte)
        delta_prime = 0
        acc = 0
        brake = False
        #vel = 0
        #dt = self.clock.tick(80) / 1000
        new_time = time.time()
        dt = new_time - self.curr_time
        print(dt)
        # print(new_time - self.curr_time, dt)
        self.curr_time = new_time
        if self.render_game:
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_RIGHT]:
                delta_prime = -1
            elif pressed[pygame.K_LEFT]:
                delta_prime = 1
            #if new_delta - self.bike.delta > 3:
                #delta_prime = 1
            #elif self.bike.delta - new_delta > 3:
                #delta_prime = -1

            if pressed[pygame.K_UP]:
                acc = 100
            elif pressed[pygame.K_DOWN]:
                acc = -100
        self.bike.update(acc, delta_prime, dt, brake, 0, 0)
        #print(cte, new_delta, self.bike.delta)



    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def end(self):
        pygame.quit()'''