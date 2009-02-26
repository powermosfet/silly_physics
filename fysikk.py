#! /usr/bin/env python

import time, pygame, os, sys, pickle
from pygame.locals import *
from math import sin, cos, sqrt, log, pi, exp

path = os.path.dirname(os.path.abspath(__file__))

class Engine(object):
    def __init__(self, conf, size=(8, 6)):
        self.x = conf["x"]
        self.x0 = conf["x"]
        self.y = conf["y"]        
        self.y0 = conf["y"]        
        self.m = conf["m"]
        self.v0x = conf["v"] * cos(conf["th"]/360.0*2*pi)
        self.v0y = conf["v"] * sin(conf["th"]/360.0*2*pi)
        self.g = conf["g"]
        self.k = conf["k"]
        self.r = conf["r"]
        self.kb = conf["kb"]
        self.size = size
    def xf(self, t):
        return (self.x0*self.k+self.v0x*self.m)/self.k-self.v0x*self.m*exp(-self.k*t/self.m)/self.k
    def yf(self, t):
        return -self.m*exp(-self.k*t/self.m)*(self.v0y*self.k+self.m*self.g)/self.k**2-self.m*self.g*t/self.k+(self.y0*self.k**2+self.m*self.v0y*self.k+self.m**2*self.g)/self.k**2
    def xdf(self, t):
        return self.v0x*exp(-self.k*t/self.m)
    def ydf(self, t):
        return exp(-self.k*t/self.m)*(self.v0y*self.k+self.m*self.g)/self.k-self.m*self.g/self.k
    def collide(self, x, y):
        tDelta = time.time() - self.t0
        vx = self.xdf(tDelta)
        vy = self.ydf(tDelta)
        self.t0 = time.time()
        self.x0 = self.x
        self.y0 = self.y
        if x < 0:
            xFact = self.kb * -1
        else:
            xFact = (3.0+self.kb)/4
        if y < 0:
            yFact = self.kb * -1
        else:
            yFact = (3.0+self.kb)/4
        self.v0x = vx * xFact
        self.v0y = vy * yFact
    def go(self):
        pygame.display.init()
        self.t0 = time.time()
        self.actualSize = (self.size[0]*100, self.size[1]*100)
        screen = pygame.display.set_mode(self.actualSize, 0)
        ball = pygame.image.load(path + "/ball.png")
        black = ball.copy()
        black.fill((0,0,0))
        rect = ball.get_rect()
        clock = pygame.time.Clock()
        while 1:
            clock.tick(60)
            for e in pygame.event.get():
                if e.type == KEYDOWN or e.type == QUIT:
                    pygame.display.quit()
                    return
            if self.x < 0:
                self.x = 0
                self.collide(-1, 1)
            elif self.size[0] - self.x < self.r*2:
                self.x = self.size[0] - self.r*2
                self.collide(-1, 1)
            elif self.y < 0:
                self.y = 0
                self.collide(1, -1)
            elif self.size[1] - self.y < self.r*2:
                self.y = self.size[1] - self.r*2
                self.collide(1, -1)
            tDelta = time.time() - self.t0
            self.x = self.xf(tDelta)
            self.y = self.yf(tDelta)
            screen.blit(black, rect)
            rect.bottomleft = (int(self.x * 100), self.actualSize[1] - int(self. y * 100))
            screen.blit(ball, rect)
            pygame.display.flip()
    
cmd = ""
conf = {}
print "Welcome to the physics engine test mode. Set options and type go."
while cmd != "quit":
    cmd = raw_input("> ")
    if ":" in cmd:
        opt = cmd.split(":")
        conf[opt[0]] = float(opt[1])
    elif cmd == "go":
        test = Engine(conf, (int(conf["w"]), int(conf["h"])))
        test.go()
    elif cmd == "save":
        pickle.dump(conf, open("saved.dat", 'wb'))
    elif cmd == "load":
        conf = pickle.load(open("saved.dat", 'rb'))
    elif cmd == "print":
        for x in conf.keys():
            print x + ": " + str(conf[x])
    elif cmd != "quit":
        print "Unknown command"
