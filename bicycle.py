import pygame
from pygame.math import Vector3, Vector2
import numpy as np

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

#pygame.init()
#screen = pygame.display.set_mode((1000, 1000))
#clock = pygame.time.Clock()



class Bicycle:
    def __init__(self):
        self.position = Vector2(250, 250)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.theta = -45
        self.delta = 0
        self.L = 50
        self.width = 25
        self.height = 10
        self.steering = False
        self.omega = 0
        self.MAX_DELTA = 45
        self.MAX_VELOCITY = 250
        self.accelerating = False
        self.r = 50
        self.last_cte = 0
        self.cte_sum = 0
        self.back_pos = self.position - Vector2(self.L, 0).rotate(-self.theta)


    def update2(self, action, dt): # 0: N 1: F 2: L 3: R 4: FL 5: FR 6: B
        acc = 0
        delta_prime = 0
        brake = False
        if action == 1:
            acc = 100
        elif action == 2:
            delta_prime = 1
        elif action == 3:
            delta_prime = -1
        elif action == 4:
            acc = 100
            delta_prime = 1
        elif action == 5:
            acc = 100
            delta_prime = -1
        elif action == 6:
            brake = True
        else:
            pass

        self.update(acc, delta_prime, dt, brake, 0, 0)

    def update(self, acc, delta_prime, dt, brake, delta, vel):
        if abs(delta) > 0:
            self.delta = delta
        else:
            self.delta += delta_prime
        if abs(self.delta) > 0:
            self.steering = True
        if self.delta > self.MAX_DELTA: self.delta = self.MAX_DELTA
        elif self.delta < -self.MAX_DELTA: self.delta = -self.MAX_DELTA
        self.acceleration = Vector2(acc, 0)
        if self.acceleration.magnitude() > 0: self.accelerating = True
        #self.velocity = Vector2(vel, 0)
        if brake:
            self.velocity *= .94
        elif self.acceleration:
            self.velocity += self.acceleration*.0045
        else:
            self.velocity *= .98

        if self.velocity.x > self.MAX_VELOCITY: self.velocity = Vector2(self.MAX_VELOCITY, 0)
        elif self.velocity.x < -self.MAX_VELOCITY: self.velocity = Vector2(-self.MAX_VELOCITY, 0)
        self.position += self.velocity.rotate(-self.theta)*dt
        if self.steering:
            R = 1/np.sin(np.radians(self.delta))
            self.omega = self.velocity.x/R
        else:
            self.omega = 0
        self.theta += self.omega*.0045
        self.theta %= 360
        self.back_pos = self.position - Vector2(self.L, 0).rotate(-self.theta)
        #print(self.velocity)

    def pd(self, cte, Kp, Ki, Kd):
        P = Kp*cte
        I = Ki*self.cte_sum
        D = Kd*(cte-self.last_cte)
        O = P + D
        self.last_cte = cte
        self.cte_sum += cte

        #if O > 1: O = 1
        #elif O < -1: O = -1
        return O




    def render(self, surf):
        front = [
            Vector2(-self.width / 2.0, -self.height / 2.0).rotate(-self.theta-self.delta) + self.position,
            Vector2(self.width / 2.0, -self.height / 2.0).rotate(-self.theta-self.delta) + self.position,
            Vector2(self.width / 2.0, self.height / 2.0).rotate(-self.theta-self.delta) + self.position,
            Vector2(-self.width / 2.0, self.height / 2.0).rotate(-self.theta-self.delta) + self.position
        ]



        back = [
            Vector2(-self.width / 2.0, -self.height / 2.0).rotate(-self.theta) + self.back_pos,
            Vector2(self.width / 2.0, -self.height / 2.0).rotate(-self.theta) + self.back_pos,
            Vector2(self.width / 2.0, self.height / 2.0).rotate(-self.theta) + self.back_pos,
            Vector2(-self.width / 2.0, self.height / 2.0).rotate(-self.theta) + self.back_pos
        ]

        pygame.draw.polygon(surf, BLACK, front, 2) # front_wheel
        pygame.draw.polygon(surf, BLACK, back, 2) #back_wheel

        pygame.draw.line(surf, BLACK, self.back_pos, self.position, 2) #body






test = '''
b = Bicycle()
done = False
dt = 0
delta_prime = 0
acc = 0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: done = True
    screen.fill(WHITE)
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_RIGHT]: delta_prime = -3
    elif pressed[pygame.K_LEFT]: delta_prime = 3
    else: delta_prime = 0

    if pressed[pygame.K_UP]: acc = 100
    elif pressed[pygame.K_DOWN]: acc = -100
    else:
        acc = 0
        #b.velocity = Vector2(0, 0)
    b.update(acc, delta_prime, dt, pressed[pygame.K_SPACE])
    b.render(screen)
    pygame.display.update()
    dt = clock.tick(60) /1000
pygame.quit()'''