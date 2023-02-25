# copyright Tomasz Zgrys (Digital-Apprentice) - 2023 - MIT license 
# Classes of physical interactions

import math

class Spring:
    def __init__(self, anchor, length, damping = 0.98, k=0.2):
        self.anchor = anchor  # coordinates of anchor as Vector representation 
        self.length = length  # arm legth
        self.damping = damping  # damping force simulating friction
        self.k = k # elasticity coefficient
        
    def connect(self, mover):
        self.mover = mover  # mover object connected to spring
        self.force = self.get_direction(self.mover)
        distance = self.force.get_magnitude()
        stretch = distance - self.length
        self.force.normalize()
        self.force *= (-1 * self.k * stretch)
        self.mover.damping = self.damping
        self.mover.apply_force(self.force)
    
    def get_direction(self, mover):
        direction = self.mover.position-self.anchor
        return direction
        
    def constrain_length(self, min_length=1, max_length=10):
        direction = self.get_direction(self.mover)
        distance = direction.get_magnitude()
        if distance < min_length:
            direction.normalize()
            direction *= min_length
            self.mover.position = self.anchor + direction
            self.mover.velocity *= 0
        elif distance > max_length:
            direction.normalize()
            direction *= max_length
            self.mover.position = self.anchor + direction
            self.mover.velocity *= 0

class Pendulum:
    def __init__(self, r, angle, angular_velocity, angular_acceleration, origin, position, friction = 0.995, G = 0.4):      
        self.r = r
        self.angle = angle
        self.angular_velocity = angular_velocity
        self.angular_acceleration = angular_acceleration
        self.origin = origin
        self.position = position
        self.friction = friction
        self.G = G
    
    def update(self):
        self.angular_acceleration = (-1 * self.G /self.r)* math.sin(self.angle)
        self.angular_velocity += self.angular_acceleration
        self.angle += self.angular_velocity
        self.angular_velocity *= self.friction
        
    def get_position(self):
        self.position.x = self.r * math.sin(self.angle)
        self.position.y = self.r * math.cos(self.angle)
        self.position += self.origin
        return self.position


class Oscillator:
    def __init__(self, angle, velocity, amplitude, angular_velocity):
        self.angle = angle
        self.velocity = velocity
        self.amplitude = amplitude
        self.angular_velocity = angular_velocity
        
    def oscillate(self):
        self.angle += self.velocity


class Attractor:
    def __init__(self, mass, position, G = 0.4, min_dist=5, max_dist=25):
        self.mass = mass
        self.G = G
        self.position = position
        self.min_dist = min_dist
        self.max_dist = max_dist
    
    def attraction(self, mover):
        force = self.position - mover.position
        distance = force.get_magnitude()
        distance = min(max(distance, self.min_dist), self.max_dist)
        force.normalize()
        strength = (self.G * self.mass * mover.mass) / (distance * distance)
        force *= strength
        return force
    
    def repulsion(self, mover):
        return self.attraction(mover)*(-1)

class Environment:	# enviroment coefficient of drag (ce)
    def __init__(self, xe,ye,we,he,ce=0):
        self.xe = xe
        self.ye = ye
        self.we = we
        self.he = he
        self.ce = ce  # współczynnik oporu (coefficient of drag)
        

class Mover:
    def __init__(self, position, velocity, acceleration, gravity, G=0.4,  mass=1, cf = None, ce = None, damping = None, topspeed = None):
        self.position = position # wektor położenia
        self.velocity = velocity # wektor prędkości
        self.acceleration = acceleration # wektor przyspieszenia liniowego
        self.gravity = gravity # wektor grawitacji
        self.G = G # stała grawitacji
        self.mass = mass # masa (skalar)
        self.angle = 0 # kąt obrotu (skalar) 
        self.angular_velocity = 0 # prędkość kątowa (angular velocity) - (skalar)
        self.angular_acceleration = 0 # przyspieszenie kątowe (angular acceleration) - (skalar)        self.G = G # stała grawitacji
        self.cf = cf	# współczynnik tarcia (coefficient of friction) - (skalar)
        self.ce = ce	# współczynnik oporu środowiska (coefficient of drag) - (skalar)
        self.damping = damping
        self.topspeed = topspeed # prędkość maksymalna - (skalar)
       
    def pointer(self, point):
        self.point = point
    
    def clear_acceleration(self):
        self.acceleration *= 0
        
    def update(self, type_of_movement='l'): # l = linear motion, a = angular motion
        #self.acceleration = self.acceleration.random2D()
        if self.cf != None and self.cf != 0:
            self.friction(cf)
        self.velocity += self.acceleration
        if self.damping:
            self.velocity *= self.damping
        if self.topspeed != None and self.topspeed != 0:
            self.velocity.limit(self.topspeed)               
        self.position += self.velocity
        if type_of_movement == 'a':
           self.angular_velocity += self.angular_acceleration
           self.angle += self.angular_velocity
        self.clear_acceleration()       
    
    def heading(self, angle='xy'):
        if angle == 'xy':
            return self.velocity.angle_xy()
        elif angle == 'xz':
            return self.velocity.angle_xz()
        elif angle == 'yz':
            return self.velocity.angle_yz()
        
    def get_velocity(self):
        return self.velocity
    
    def get_angular_velocity(self):
        return self.angular_velocity
    
    def set_angular_velocity(self, angular_velocity):
        self.angular_velocity = angular_velocity
    
    def get_angular_acceleration(self):
        return self.angular_acceleration
    
    def set_angular_acceleration(self, angular_acceleration):
        self.angular_acceleration = angular_acceleration
        
    def get_acceleration(self):
        return self.acceleration
    
    def get_position(self):
        return self.position
    
    def get_position_x(self):
        return self.position.x
    
    def get_position_y(self):
        return self.position.y
    
    def get_position_z(self):
        return self.position.z
                 
    def set_damping(self, damping):
        self.damping = damping
    
    def get_damping(self):
        return self.damping
    
    def friction_force(self, cf = 0.01):
        self.cf = cf                 
        if self.cf != 0:
            self.friction = self.get_velocity()
            self.friction *= -1
            self.friction.normalize()
            self.friction *= cf
            self.apply_force(self.friction)        
    
    def drag_force(self,environment):
        if self.is_inside(environment):            
            speed = self.velocity.magnitude()
            drag_magnitude = environment.ce * speed * speed
            self.drag = self.get_velocity()
            self.drag *= -1
            self.drag.normalize()
            self.drag *= drag_magnitude
            self.apply_force(self.drag)
        
    def gravity_force(self, g=None):
        if g is None:
            g = self.G
        m = g * self.mass
        self.gravity.x = 0
        self.gravity.y = m
        self.apply_force(self.gravity)
    
    def attraction_force(self, attractor, G=0.4,min_dist=5,max_dist=25):
        force = self.position - attractor.position
        distance = force.magnitude()
        distance = min(max(distance, min_dist), max_dist)
        force.normalize()
        strength = (G * self.mass * attractor.mass) / (distance * distance)
        force *= strength
        self.apply_force(force)
        
    def apply_force(self, force):
        self.acceleration += force / self.mass
     
    def is_inside(self, enviroment):
        if self.position.x > enviroment.xe and self.position.x < enviroment.xe + enviroment.we and self.position.y > enviroment.ye and self.position.y < enviroment.ye + enviroment.he:
            return True
        else:
            return False
     
    def constrain(self, value, min_val, max_val):
        return min(max(value, min_val), max_val)



        
        