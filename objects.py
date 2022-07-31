from datatypes import *;
from structures import *;
from math import *;

import numpy as np;

class Environment:

    def __init__(self):
        self.objects = [];
        self.light_sources = [];

    def add_object(self, obj):
        if (obj.type == "object"):
            self.objects.append(obj);
        elif (obj.type == "light"):
            self.light_sources.append(obj);

class Camera:

    def __init__(self, position, orientation, screen_dim, fov):

        self.hfov = fov[0];
        self.vfov = fov[1];

        self.sx = screen_dim[0];
        self.sy = screen_dim[1];

        self.position = position;
        self.orientation = orientation;
        self.screen_distance = 5;

    def get_shading(self, environment, object, point):

        light_sources = environment.light_sources;
        current_color = [0, 0, 0];

        # Checking if point is in a shadow
        for light in light_sources:
           # print(light.position.unpack());
            light_ray = Ray(light.position, Vector3D.from_iter(np.subtract(light.position.unpack(), point.unpack())));
            light_reaches_object = True;

            for obstruction in environment.objects:

                intersection = obstruction.get_closest_intersection(light_ray);

                if (not obstruction.transparent):
                    if (obstruction != object):
                        if (intersection and intersection.get_distance(light.position) < point.get_distance(light.position)):
                            light_reaches_object = False;

            # If the light source reaches the object, calculate the angle between the normal and light-ray to determine the color added by that light
            if (light_reaches_object):
                normal_vector = object.get_normal(point);
                normal_magnitude = normal_vector.magnitude();

                light_ray_vector = light_ray.direction;
                light_ray_magnitude = light_ray_vector.magnitude();

                t = np.dot(normal_vector.unpack(), light_ray_vector.unpack()) / (normal_magnitude * light_ray_magnitude) * object.reflectivity * light.intensity;

                # Inverse Square Law
                t = np.multiply(t, (light.distance ** 2) / (point.get_distance(light.position) ** 2))

                color = Color3.from_iter(np.multiply(object.color.unpack(), t).astype(int));
                color.clamp();

                current_color = np.add(current_color, color.unpack());
                current_color = np.add(current_color, np.multiply(light.color.unpack(), t).astype(int));

        return current_color;

    def capture(self, environment):

        # (30, 30, 30) RGB is the ambient environment color
        screen = [[[30, 30, 30] for i in range(self.sx)] for v in range(self.sy)];

        pos = self.position;

        # Calculating the dimensions of the real-world screen
        world_screen_width = 2 * self.screen_distance * tan(radians(self.hfov / 2));
        world_screen_height = 2 * self.screen_distance * tan(radians(self.vfov / 2));

        # Calculating the direction vectors of the camera
        forward_vector = self.orientation.to_vector();
        left_vector = Angle2D(self.orientation.x - 90, 0).to_vector();
        right_vector = Angle2D(self.orientation.x + 90, 0).to_vector();
        top_vector = Angle2D(self.orientation.x, self.orientation.y - 90).to_vector();
        bottom_vector = Angle2D(self.orientation.x, self.orientation.y + 90).to_vector();

        # Getting the midpoint and the top left point on the real-world screen
        mid_pos = np.add(np.multiply(forward_vector.unpack(), self.screen_distance), pos.unpack());
        top_left_pos = np.add(np.add(mid_pos, np.multiply(left_vector.unpack(), world_screen_width / 2)), np.multiply(top_vector.unpack(), world_screen_height / 2));

        # Getting increments for traversing the world-screen vertically and horizontally
        increment_vertical = np.multiply(bottom_vector.unpack(), world_screen_height / self.sy);
        increment_horizontal = np.multiply(right_vector.unpack(), world_screen_width / self.sx);

        pixel_width = world_screen_width / self.sx;
        pixel_height = world_screen_height / self.sy;
        pixel_offset = np.add(np.multiply(bottom_vector.unpack(), pixel_height / 2), np.multiply(right_vector.unpack(), pixel_width / 2));

        # Shooting a ray through each pixel in the screen
        for i in range(self.sy):
            for v in range(self.sx):
                current_pixel_pos = np.add(np.add(np.add(top_left_pos, np.multiply(increment_vertical, i)), np.multiply(increment_horizontal, v)), pixel_offset);

                ray = Ray(pos, Vector3D.from_iter(np.subtract(current_pixel_pos, pos.unpack())));

                closest_intersected_object = None;
                closest_intersection = None;
                closest_intersection_distance = -1;

                # Getting the nearest object hit by the ray and displaying its color
                for object in environment.objects:

                    if (not object.transparent):
                        intersection = object.get_closest_intersection(ray);

                        if (intersection):
                            intersection_distance = intersection.get_distance(pos);

                            if (closest_intersection_distance < 0 or intersection_distance < closest_intersection_distance):
                                closest_intersected_object = object;
                                closest_intersection = intersection;
                                closest_intersection_distance = intersection_distance;

                if (closest_intersection):

                    # To avoid rendering objects behind us (which still interact with the ray since it is bi-directional)
                    # We need to check if the vector pointing towards the intersection point matches up with the vector going  
                    # out from the camera's position
                    vector_to_intersection = Vector3D.from_iter(np.subtract(closest_intersection.unpack(), current_pixel_pos));
                    angle_diff = acos(np.dot(self.orientation.to_vector().unpack(), vector_to_intersection.unpack()) / (self.orientation.to_vector().magnitude() * vector_to_intersection.magnitude()));
                            
                    # Epsilon value of 1 to account for error
                    if (angle_diff < 1):
                        screen[i][v] = self.get_shading(environment, closest_intersected_object, closest_intersection);

        return screen;

class Sphere(Object):
      
    def __init__(self, position, radius, color, reflectivity, transparent):
        
        super().__init__(position, reflectivity, transparent);
        
        self.radius = radius;
        self.color = color;

    def get_closest_intersection(self, ray): 
        
        x0, y0, z0 = ray.start.unpack();
        dx, dy, dz = ray.direction.unpack();
        cx, cy, cz = self.position.unpack();

        r = self.radius;

        a = dx * dx + dy * dy + dz * dz;
        b = 2 * dx * (x0 - cx) + 2 * dy * (y0 - cy) + 2 * dz * (z0 - cz);
        c = cx * cx + cy * cy + cz * cz + x0 * x0 + y0 * y0 + z0 * z0 - 2 * (cx * x0 + cy * y0 + cz * z0) - r ** 2;

        disc = b ** 2 - 4 * a * c;

        if (disc < 0):
            return None;
        else:
            t = (-b - sqrt(b ** 2 - 4 * a * c)) / (2 * a);

            return Vector3D(x0 + t * dx, y0 + t * dy, z0 + t * dz); 

    def get_normal(self, pos):
        return Vector3D.from_iter(np.subtract(pos.unpack(), self.position.unpack()));

class PointLight(Light):

    def __init__(self, position, intensity, color, distance):

        super().__init__(position, intensity, color, distance);