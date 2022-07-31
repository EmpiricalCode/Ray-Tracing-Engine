class Object:
    
    def __init__(self, position, reflectivity, transparent):
        self.reflectivity = reflectivity;
        self.position = position;
        self.transparent = transparent;
        self.type = "object";

class Light:

    def __init__(self, position, intensity, color):
        self.position = position;
        self.intensity = intensity;
        self.color = color;
        self.transparent = True;
        self.type = "light";