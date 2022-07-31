from math import *;

import numpy as np;

class Color3:

    def __init__(self, r, g, b):
        self.r = r;
        self.b = b;
        self.g = g;

    def unpack(self):
        return self.r, self.g, self.b;

    def from_iter(iter):
        return Color3(iter[0], iter[1], iter[2]);

    def clamp(self):
        self.r = min(max(0, self.r), 255);
        self.g = min(max(0, self.g), 255);
        self.b = min(max(0, self.b), 255);

class Angle2D:

    def __init__(self, x, y):

        self.x = x;
        self.y = y;

        self.clamp();

    def clamp(self):
        if (self.x > 360):
            self.x %= 360;
        elif (self.x < -360):
            self.x %= -360;

        if (self.x < 0):
            self.x += 360;
        
        if (self.y > 360):
            self.y %= 360;
        elif (self.y < -360):
            self.y %= -360;

        if (self.y < 0):
            self.y += 360;

    def rotate(self, x, y):
        self.x += x;
        self.y += y;

    def to_vector(self):
    
        x, y, z = (0, 0, 0);

        y = -sin(radians(self.y));
        hyp = sqrt(1 - y ** 2);

        z = hyp * sin(radians(self.x));
        x = hyp * cos(radians(self.x));

        if (270 > self.y > 90):
            x *= -1;
            z *= -1;
    
        return Vector3D(x, y, z);

class Vector3D:

    def __init__(self, x, y, z):
        self.x = x;
        self.y = y;
        self.z = z;

    def unpack(self):
        return self.x, self.y, self.z;

    def magnitude(self):
        return Vector3D(0, 0, 0).get_distance(self);

    def get_distance(self, vec):
        return sqrt((self.x - vec.x) ** 2 + (self.y - vec.y) ** 2 + (self.z - vec.z) ** 2);

    def from_iter(iterable):
        return Vector3D(iterable[0], iterable[1], iterable[2]);

class Ray:
    
    def __init__(self, start, direction):
        self.start = start;
        self.direction = direction;