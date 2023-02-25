# copyright Tomasz Zgrys (Digital-Apprentice) - 2022 - MIT license 
# vectors - a class that implements vector operations and functions


import math
import random

class Vector:
    def __init__(self, x, y, z = None):
        self.x = x
        self.y = y
        self.z = z
            
    def dimensions(self):
        if self.z is None:
            return 2
        else:
            return 3
        
    def __add__(self,_vector):
        if isinstance(_vector, Vector):
            if self.dimensions() == _vector.dimensions():
                if self.dimensions() == 2:
                    return Vector(self.x + _vector.x, self.y + _vector.y)
                elif self.dimensions() == 3:
                    return Vector(self.x + _vector.x, self.y + _vector.y, self.z + _vector.z)
            else:
                raise ValueError("Cannot add vectors of different dimensions")                
        else:
            raise TypeError("Cannot add non-vector object to a vector")         
    
    def __sub__(self, _vector):
        if isinstance(_vector, Vector):
            if self.dimensions() == _vector.dimensions():
                if self.dimensions() == 2:
                    return Vector(self.x - _vector.x, self.y - _vector.y)
                elif self.dimensions() == 3:
                    return Vector(self.x - _vector.x, self.y - _vector.y, self.z - _vector.z)
            else:
                raise ValueError("Cannot subtract vectors of different dimensions")
        else:
            raise TypeError("Cannot subtract non-vector object from a vector")
    
    def __mul__(self, _vector):
        if isinstance(_vector, (int, float)):  # if the _vector ist a number (scalar)
            if self.dimensions() == 2:
                return Vector(self.x * _vector, self.y * _vector)
            elif self.dimensions() == 3:
                return Vector(self.x * _vector, self.y * _vector, self.z * _vector)
        elif isinstance(_vector,Vector):  # if the _vector is a vector
            if self.dimensions() == _vector.dimensions():
                if self.dimensions() == 2:
                    return self.x * _vector.x + self.y * _vector.y
                elif self.dimensions() == 3:
                    return self.x * _vector.x + self.y * _vector.y + self.z * _vector.z
            else:
                raise ValueError("Cannot calculate dot product of vectors with different dimensions")
    
    def __truediv__(self, scalar):
        if isinstance(scalar, (int, float)):  # if the scalar is a number
            if self.dimensions() == 2:
                return Vector(self.x / scalar, self.y / scalar)
            elif self.dimensions() == 3:
                return Vector(self.x / scalar, self.y / scalar, self.z / scalar)
        else:
            raise TypeError("Cannot multiply vector by non-numeric object")
    
    def __floordiv__(self, scalar):
        if isinstance(variable, (int, float)):  # if the variable is a number
            return Vector(self.x // scalar, self.y // scalar)
        else:
            raise TypeError("variable must be a scalar")
    
    def __repr__(self):
        if self.z is not None:
            return f"Vector3D({self.x}, {self.y}, {self.z})"
        else:
            return f"Vector2D({self.x}, {self.y})"
    
    def polar2cartesian(self, r, theta, phi=None):
        # the magnitude (length = r) and direction (angle = theta) of a vector
        if phi is None:
            self.x = r * math.sin(theta)
            self.y = r * math.cos(theta)
        else:
            self.x = r * math.sin(theta) * math.cos(phi)
            self.y = r * math.sin(theta) * math.sin(phi)
            self.z = r * math.cos(theta)           
    
    def cartesian2polar(self):
        if self.dimensions() == 2:
            r = math.sqrt(self.x ** 2 + self.y ** 2)
            theta = self.angle_xy()
            return (r,theta)
        elif self.dimensions() == 3:
            r = math.sqrt(self.x**2 + self.y**2 + self.z**2)
            phi = self.angle_xy()
            theta = math.acos(self.z / r)
            return (r, phi, theta)
            
    def rotate_2d(self, angle, point=(0,0)):   
        if isinstance(point,Vector):
            xc = point.x
            yc = point.y
        else:     
            xc = point[0]
            yc = point[1]
        
        # Store the original coordinates in temporary variables
        x_original, y_original = self.x, self.y

        # Perform the rotation around the point
        self.x = xc + (x_original - xc) * math.cos(angle) - (y_original - yc) * math.sin(angle)
        self.y = yc + (x_original - xc) * math.sin(angle) + (y_original - yc) * math.cos(angle)
            
    def rotate_3d(self, angle, point=(0,0), axis='x'):       
        if isinstance(point,Vector):
            xc = point.x
            yc = point.y
            zc = point.z 
        else:
            xc = point[0]
            yc = point[1]
            zc = point[2]
    
        # Store the original coordinates in temporary variables
        x_original, y_original, z_original = self.x, self.y, self.z

        # Perform the rotation around the point
        if axis == 'x':
            self.y = yc + (y_original - yc) * math.cos(angle) - (z_original - zc) * math.sin(angle)
            self.z = zc + (y_original - yc) * math.sin(angle) + (z_original - zc) * math.cos(angle)
        elif axis == 'y':
            self.x = xc + (x_original - xc) * math.cos(angle) - (z_original - zc) * math.sin(angle)
            self.z = zc + (x_original - xc) * math.sin(angle) + (z_original - zc) * math.cos(angle)
        elif axis == 'z':
            self.x = xc + (x_original - xc) * math.cos(angle) - (y_original - yc) * math.sin(angle)
            self.y = yc + (x_original - xc) * math.sin(angle) + (y_original - yc) * math.cos(angle)       
        
    def angle_xy(self):
        return math.atan2(self.y, self.x)  # calculate the angle of inclination of the vector in the xy plane
    
    def angle_xz(self):        
        return math.atan2(self.z, self.x)  # calculate the angle of inclination of the vector in the xz plane
    
    def angle_yz(self):
        return math.atan2(self.z, self.y)  # calculate the angle of inclination of the vector in the yz plane
    
    def get_magnitude(self):
        if self.z is not None:
            return math.sqrt(self.x**2 + self.y**2 + self.z**2)  # oblicz długość wektora 3D
        else:
            return math.sqrt(self.x**2 + self.y**2)  # oblicz długość wektora 2D
    
    def set_magnitude(self, magnitude):		# set desired vector lenght
        self.normalize()
        self.x *= magnitude
        self.y *= magnitude
        if self.dimensions() == 3:
                self.z *= magnitude       
    
    def limit(self, max_magnitude):		# set desired maximum vector lenght
        if self.magnitude() > max_magnitude:
            self.set_magnitude(max_magnitude)
    
    def normalize(self):		# normalizuja wektor, czyli ustaw jego długość na 1
        magnitude = self.get_magnitude()
        if magnitude > 0:
            self.x /= magnitude
            self.y /= magnitude
            if self.dimensions() == 3:
                self.z /= magnitude
                return Vector(self.x, self.y, self.z)
            return Vector(self.x, self.y)
        else:
            if self.dimensions() == 2:
                return Vector(0,0)
            elif self.dimensions() == 3:
                return Vector(0,0,0)
    
    def distributive(self, _vector):
        if self.dimensions() == _vector.dimensions():
            if self.dimensions() == 2:
                return Vector(self.x * _vector.x, self.y * _vector.y)
            elif self.dimensions() == 3:
                return Vector(self.x * _vector.x, self.y * _vector.y, self.z * _vector.z)
        else:
            raise ValueError("Cannot calculate distributive product of vectors with different dimensions")
        
    def cross(self, _vector):
        if self.dimensions() == 3 and _vector.dimensions() == 3:
            x = self.y * _vector.z - self.z * _vector.y
            y = self.z * _vector.x - self.x * _vector.z
            z = self.x + _vector.y - self.y * _vector.x
            return Vector (x, y, z)
        else:
            raise ValueError("Cannot calculate cross product of vectors that are not both 3D") 
    
    def distance(self, _vector):
        if isinstance(_vector, Vector):
            if self.dimensions() == _vector.dimensions():
                if self.dimensions() == 2:
                    return math.sqrt((self.x - _vector.x)**2 + (self.y - _vector.y)**2)
                elif self.dimensions() == 3:
                    return math.sqrt((self.x - _vector.x)**2 + (self.y - _vector.y)**2 + (self.z - _vector.z)**2)
            else:
                raise ValueError("Cannot calculate distance between vectors of different dimensions")
        else:
            raise TypeError("Cannot calculate distance between non-vector object and vector")
      
    def random2D(self):
        angle = random.uniform(0,2 * math.pi)
        return Vector(math.cos(angle), math.sin(angle))
    
    def new_point(min_x=5,max_x=27,min_y=3,max_y=5):
        # given values were defined for small adressable led matrix (8x32), may be other
        return Vector(random.randint(min_x,max_x),random.randint(min_y,max_y))