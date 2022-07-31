from datatypes import *;
from objects import *;

import matplotlib.pyplot as plt;

environment = Environment();
environment.add_object(Sphere(Vector3D(0, 0, 0), 2, Color3(50, 50, 50), 1, False));
environment.add_object(Sphere(Vector3D(0, -105, 0), 100, Color3(50, 50, 50), 1, False));
environment.add_object(PointLight(Vector3D(0, 5, -6), 2, Color3(0, 0, 255), 5));
environment.add_object(PointLight(Vector3D(0, 8, 0), 2, Color3(255, 0, 0), 5));

camera = Camera(Vector3D(-10, 0, 0), Angle2D(0, 0), (500, 300), (85, 60));

scene = camera.capture(environment);

plt.imshow(scene);
plt.show();